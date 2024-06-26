from wagtail.admin.panels.field_panel import FieldPanel
from wagtail.fields import RichTextField, StreamField

from wagtail.models import Page

from .blocks import PersonChooserBlock
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/people/%i/" % self.id  # just a dummy URL for demonstration purposes.


class HomePage(Page):
    """Demonstrating various field types and the PersonChooser."""
    author = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL)
    blocks = StreamField([
            ("person", PersonChooserBlock())
        ],
        blank=True,
        null=True,
        use_json_field=True,
    )
    text = RichTextField(blank=True, features=["bold", "italic", "link", "person"])

    content_panels = Page.content_panels + [
        FieldPanel("author"),
        FieldPanel("blocks"),
        FieldPanel("text"),
    ]
