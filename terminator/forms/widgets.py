from markupsafe import Markup
from wtforms.widgets import TextInput, DateTimeInput, TextArea, Select, CheckboxInput


class MyTextInput(TextInput):

    def __call__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs['class'] = 'form-control'
        return super(MyTextInput, self).__call__(*args, **kwargs)


class MySelect(Select):

    def __call__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs['class'] = 'form-select'
        return super(MySelect, self).__call__(*args, **kwargs)


class MyDateTimeInput(DateTimeInput):

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("type", self.input_type)
        kwargs.setdefault("class", "form-control")
        if "value" not in kwargs:
            kwargs["value"] = field._value()
        flags = getattr(field, "flags", {})
        for k in dir(flags):
            if k in self.validation_attrs and k not in kwargs:
                kwargs[k] = getattr(flags, k)
        html_hidden = "<input %s style='display:none'>" % self.html_params(name=field.name, **kwargs)
        if field.data:
            date_part = field.data.strftime(field.strptime_format[0].split(' ')[0])
            time_part = field.data.strftime(field.strptime_format[0].split(' ')[1])
        else:
            date_part = time_part = None
        html_date = "<input %s>" % self.html_params(
            name=f'{field.name}_date',
            **kwargs | {'id': field.id_date, 'type': 'date', 'value': date_part}
        )
        html_time = "<input %s>" % self.html_params(
            name=f'{field.name}_time',
            **kwargs | {'id': field.id_time, 'type': 'time', 'value': time_part}
        )
        script = '''<script type="text/javascript">
document.querySelector("#{0}").addEventListener("change", () => {{
    let _tmpDate = document.querySelector("#{0}").value;
    let _tmpTime = document.querySelector("#{1}").value;
    if (_tmpDate && _tmpTime) {{
        if (_tmpTime.length < 8) {{
            _tmpTime += ':00';
        }}
        document.querySelector("#{2}").value = `${{_tmpDate}} ${{_tmpTime}}`;
    }}
}});
document.querySelector("#{1}").addEventListener("change", () => {{
    let _tmpDate = document.querySelector("#{0}").value;
    let _tmpTime = document.querySelector("#{1}").value;
    if (_tmpDate && _tmpTime) {{
        if (_tmpTime.length < 8) {{
            _tmpTime += ':00';
        }}
        document.querySelector("#{2}").value = `${{_tmpDate}} ${{_tmpTime}}`;
    }}
}});
</script>'''.format(field.id_date, field.id_time, field.id)
        return Markup('<div class="datetime_wrapper">{}{}</div>{}{}'.format(html_date, html_time, html_hidden, script))


class MyCheckboxInput(CheckboxInput):

    def __call__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs['class'] = 'form-check-input'
        return super(MyCheckboxInput, self).__call__(*args, **kwargs)


class MyTextArea(TextArea):

    def __call__(self, *args, **kwargs):
        kwargs = kwargs or {}
        kwargs['class'] = 'form-control'
        return super(MyTextArea, self).__call__(*args, **kwargs)
