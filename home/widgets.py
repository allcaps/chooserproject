"""
Registering a chooser **viewset** will also set up a chooser widget to be used
whenever a ForeignKey field to that model appears in a WagtailAdminModelForm
- see Using forms in admin views. In particular, this means that a panel
definition such as FieldPanel("author"), where author is a foreign key to the
Person model, will automatically use this chooser interface.

The chooser widget class can also be retrieved directly (for use in ordinary Django
forms, for example) as the widget_class property on the viewset. For example,
placing the following code in widgets.py will make the chooser widget
available to be imported with from home.widgets import PersonChooserWidget:
"""


from .views import person_chooser_viewset

PersonChooserWidget = person_chooser_viewset.widget_class
