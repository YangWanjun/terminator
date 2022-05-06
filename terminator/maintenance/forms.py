from datetime import datetime

from sqlalchemy import not_, or_
from wtforms import validators, Field, ValidationError

from terminator.forms.fields import MyDateTimeField, MyTextAreaField, MySelectField, MyStringField, MyBooleanField
from terminator.models import Service, MaintenanceInfo
from terminator.utils import constant
from terminator.utils.base_form import MyForm


class MaintenanceInfoForm(MyForm):
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

    def validate_start_dt(self, field: Field):
        if self.instance is None and field.data < datetime.now():
            raise ValidationError(constant.ERROR_MAINTENANCE_START)
        # 開始・終了日時は重複しているのか
        qs = MaintenanceInfo.query.filter_by(
            service_id=self.service_id.data
        ).filter(
            MaintenanceInfo.start_dt <= self.end_dt.data, MaintenanceInfo.end_dt >= self.start_dt.data
        )
        if self.instance is None:
            if qs.first():
                raise ValidationError(constant.ERROR_PERIOD_CONFLICT)
        else:
            exists_pk = self.instance.id
            if qs.filter(MaintenanceInfo.id != exists_pk).first():
                raise ValidationError(constant.ERROR_PERIOD_CONFLICT)

    def validate_end_dt(self, field: Field):
        start_date = self.start_dt.data
        end_date = field.data
        if start_date >= end_date:
            raise ValidationError(constant.ERROR_DATETIME_PERIOD)


class ServiceForm(MyForm):
    name = MyStringField('サービス名称', validators=[
        validators.DataRequired(),
        validators.Length(max=50),
    ])
    domain = MyStringField('ドメイン', validators=[
        validators.DataRequired(),
        validators.Length(max=50),
    ])
    is_separate = MyBooleanField('フロントエンドとバックエンド分離')

    def validate_domain(self, field: Field):
        # ドメインは一意であること
        if self.instance is None:
            if Service.query.filter_by(domain=field.data).first():
                raise ValidationError(constant.ERROR_UNIQUE.format(name='ドメイン'))
        elif self.instance:
            exists_pk = self.instance.id
            if Service.query.filter(Service.id != exists_pk).filter_by(domain=field.data).first():
                raise ValidationError(constant.ERROR_UNIQUE.format(name='ドメイン'))
