from wtforms import StringField, Label, DateTimeField, TextAreaField, SelectField

from terminator.forms.widgets import MyTextInput, MyDateTimeInput, MyTextArea, MySelect


class LabelMixin(object):

    def __init__(self, *args, **kwargs):
        super(LabelMixin, self).__init__(*args, **kwargs)
        label = args[0] if args else kwargs.get('label')
        flags = getattr(self, "flags", {})
        required = getattr(flags, 'required', False)
        self.label = MyLabel(
            self.id,
            label
            if label is not None
            else self.gettext(kwargs.get('name').replace("_", " ").title()),
            required=required
        )


class MyLabel(Label):

    def __init__(self, field_id, text, required=False):
        super(MyLabel, self).__init__(field_id, text)
        self.required = required

    def __html__(self):
        attrs = {'class': f'form-label {"required" if self.required else ""}'}
        return self(**attrs)


class MyStringField(LabelMixin, StringField):
    widget = MyTextInput()


class MySelectField(LabelMixin, SelectField):
    widget = MySelect()


class MyDateTimeField(LabelMixin, DateTimeField):
    widget = MyDateTimeInput()


class MyTextAreaField(LabelMixin, TextAreaField):
    widget = MyTextArea()
