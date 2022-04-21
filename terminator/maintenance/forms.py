from wtforms import Form, validators

from terminator.forms.fields import MyDateTimeField, MyTextAreaField, MySelectField, MyStringField


class MaintenanceInfoForm(Form):
    service_id = MySelectField('サービス', validators=[
        validators.DataRequired(message='必須です'),
    ])
    start_dt = MyDateTimeField('開始日時', validators=[
        validators.DataRequired(message='必須です'),
    ])
    end_dt = MyDateTimeField('終了日時', validators=[
        validators.DataRequired(message='必須です'),
    ])
    content = MyTextAreaField('詳細内容', validators=[
        validators.Length(max=2000),
    ])


class ServiceForm(Form):
    name = MyStringField('サービス名称', validators=[
        validators.DataRequired(),
        validators.Length(max=50),
    ])
    domain = MyStringField('ドメイン', validators=[
        validators.DataRequired(),
        validators.Length(max=50),
    ])
    upgrade_file = MyStringField('更新ファイルパス', validators=[
        validators.DataRequired(),
        validators.Length(max=200),
    ])
