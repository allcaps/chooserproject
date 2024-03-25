from wagtail import hooks
from wagtail.rich_text import LinkHandler

from .models import Person
from .views import person_chooser_viewset


from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext

from wagtail.admin.rich_text.editors.draftail import features as draftail_features
from draftjs_exporter.dom import DOM
from wagtail.admin.rich_text.converters.html_to_contentstate import LinkElementHandler



@hooks.register("register_admin_viewset")
def register_viewset():
    return person_chooser_viewset


class PersonLinkHandler(LinkHandler):
    """
    An 'entity' is a placeholder tag within the saved rich text, which needs to be rewritten
    into real HTML at the point of rendering. Typically, (but not necessarily) the entity will
    be a reference to a model to be fetched to have its data output into the rich text content
    (so that we aren't storing potentially changeable data within the saved rich text).

    An EntityHandler defines how this rewriting is performed.

    Currently, Wagtail supports two kinds of entity: links (represented as <a linktype="...">...</a>)
    and embeds (represented as <embed embedtype="..." />).

    The PersonLinkHandler rewrites from:
        <a linktype="person" pk="1">...</a>
    To:
        <a href="/path/to/person">...</a>
    """
    identifier = 'person'

    @staticmethod
    def get_model():
        return Person

    @classmethod
    def get_instance(cls, attrs):
        model = cls.get_model()
        return model.objects.get(id=attrs.get("id"))

    @classmethod
    def expand_db_attributes(cls, attrs: dict) -> str:
        try:
            person = cls.get_instance(attrs)
        except Person.DoesNotExist:
            return "<a>"
        else:
            return f'<a href="{person.get_absolute_url()}">'


def person_link_entity(props):
    """
    Conversion from content state (DraftJS) to database.
    Will create elements like:
        <a id="1" linktype="store">shop link</a>
    """

    # props["children"] defaults to the string representation of the model if it's missing
    selected_text = props["children"]

    elem = DOM.create_element(
        "a",
        {
            "linktype": "person",
            "id": props.get("id"),
            "data-string": props.get("string"),
            "data-edit-link": props.get("edit_link"),
        },
        selected_text,
    )

    return elem

class PersonLinkElementHandler(LinkElementHandler):
    """
    Rule for populating the attributes of a person link when converting
    from database representation to content state (DraftJS).
    """

    def get_attribute_data(self, attrs):
        return {
            "id": attrs.get("id"),
            "string": attrs.get("data-string"),
            "edit_link": attrs.get("data-edit-link"),
        }


ContentstatePersonLinkConversionRule = {
    "from_database_format": {
        'a[linktype="person"]': PersonLinkElementHandler("PERSON")
    },
    "to_database_format": {"entity_decorators": {"PERSON": person_link_entity}},
}


@hooks.register("register_rich_text_features")
def register_person_link_feature(features):
    feature_name = "person"
    type_ = "PERSON"

    features.register_link_type(PersonLinkHandler)

    features.register_editor_plugin(
        "draftail",
        feature_name,
        draftail_features.EntityFeature(
            {"type": type_, "icon": "snippet", "description": gettext("Person Link")},
            js=[
                # Defines `GENERIC_CHOOSER_MODAL_ONLOAD_HANDLERS`
                # and contains all functions to load the modal,
                # search, paginate, and callback when an item is chosen.
                # The code is borrowed from Wagtail Generic Chooser.
                "home/js/chooser-modal.js",

                # ModalWorkflow.
                # On chosen, will add the person to the editor.
                # Button (opening the modal)
                # Tooltip.
                "home/js/person-modal-workflow.js",
            ],
        ),
    )

    features.register_converter_rule(
        "contentstate", feature_name, ContentstatePersonLinkConversionRule
    )


@hooks.register("insert_editor_js")
def editor_js():
    return format_html(f"""
        <script>
            window.chooserUrls.personChooser = '{reverse('person_chooser:choose')}';
        </script>
    """)
