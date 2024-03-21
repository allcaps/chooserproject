"""
The viewset also makes a StreamField chooser block class available,
through the method get_block_class. Placing the following code in blocks.py
will make a chooser block available for use in StreamField definitions by
importing from home.blocks import PersonChooserBlock:
"""

from .views import person_chooser_viewset


PersonChooserBlock = person_chooser_viewset.get_block_class(
    name="PersonChooserBlock", module_path="home.blocks"
)
