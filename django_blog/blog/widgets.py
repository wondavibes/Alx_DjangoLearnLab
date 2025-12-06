# blog/widgets.py
from django.forms import TextInput


class TagWidget(TextInput):
    """
    A custom widget for the tags field that adds specific HTML attributes.
    """

    def __init__(self, attrs=None):
        # Add a specific CSS class or placeholder text by default
        default_attrs = {
            "class": "tag-input-field",
            "placeholder": "Enter tags separated by commas",
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)

    # You could add more custom rendering logic here if needed
