from wtforms import StringField, Label, DateTimeField, TextAreaField, SelectField, BooleanField

from terminator.forms.widgets import MyTextInput, MyDateTimeInput, MyTextArea, MySelect, MyCheckboxInput


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


class ValidateMixin(object):

    def export_js_validations(self):
        js_extra_part = ""
        js_field = """
const _eleField_{0} = document.querySelector("#{0}");
_eleField_{0}.setCustomValidity('error');
_eleField_{0}.addEventListener('change', function (e) {{
    _eleField_{0}.setCustomValidity('');
}});
        """.format(self.id)
        if hasattr(self, 'id_date') and hasattr(self, 'id_time'):
            js_extra_part = """
const _eleFieldDate_{1} = document.querySelector("#{1}");
const _eleFieldTime_{2} = document.querySelector("#{2}");
_eleFieldDate_{1}.addEventListener('change', function (e) {{
    _eleField_{0}.setCustomValidity('');
}});
_eleFieldTime_{2}.addEventListener('change', function (e) {{
    _eleField_{0}.setCustomValidity('');
}});
            """.format(self.id, self.id_date, self.id_time)
        return '<script type="text/javascript">{}{}</script>'.format(js_field, js_extra_part)


class MyLabel(Label):

    def __init__(self, field_id, text, required=False):
        super(MyLabel, self).__init__(field_id, text)
        self.required = required

    def __html__(self):
        attrs = {'class': f'form-label {"required" if self.required else ""}'}
        return self(**attrs)


class MyStringField(LabelMixin, ValidateMixin, StringField):
    widget = MyTextInput()


class MySelectField(LabelMixin, ValidateMixin, SelectField):
    widget = MySelect()


class MyDateTimeField(LabelMixin, ValidateMixin, DateTimeField):
    widget = MyDateTimeInput()

    @property
    def id_date(self):
        return f'{self.id}_date'

    @property
    def id_time(self):
        return f'{self.id}_time'


class MyBooleanField(LabelMixin, ValidateMixin, BooleanField):
    widget = MyCheckboxInput()

    def process_formdata(self, valuelist):
        if not valuelist or valuelist[0] in self.false_values:
            self.data = False
        else:
            self.data = True


class MyTextAreaField(LabelMixin, ValidateMixin, TextAreaField):
    widget = MyTextArea()
