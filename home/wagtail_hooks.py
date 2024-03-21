from wagtail import hooks

from .views import person_chooser_viewset


@hooks.register("register_admin_viewset")
def register_viewset():
    return person_chooser_viewset