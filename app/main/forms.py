from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, TextAreaField, SubmitField
from wtforms.validators import Required, Length, URL
from wtforms import ValidationError
from ..models import Index, List


class IndexForm(FlaskForm):
    name = StringField('Name', validators=[Length(0, 64)])
    url = StringField('Url', validators=[Required(), Length(1, 255), URL()])
    html = TextAreaField('Html')
    status = RadioField('Status', coerce=int, default='0')
    submit = SubmitField('Submit')

    def __init__(self, index=None, *args, **kwargs):
        super(IndexForm, self).__init__(*args, **kwargs)
        self.status.choices = [(0, 'Initial'), (1, 'Downloaded'), (2, 'Deprecated')]
        self.index = index

    def validate_url(self, field):
        if self.index is None:
            if Index.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')
        else:
            if self.index.url != field.data and \
                    Index.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')


class ListForm(FlaskForm):
    index_id = SelectField('Index id', coerce=int)
    name = StringField('Name', validators=[Length(0, 64)])
    url = StringField('Url', validators=[Required(), Length(1, 255), URL()])
    html = TextAreaField('Html')
    status = RadioField('Status', coerce=int, default=0)
    submit = SubmitField('Submit')

    def __init__(self, item=None, *args, **kwargs):
        super(ListForm, self).__init__(*args, **kwargs)
        self.index_id.choices = [(index.id, index.name) for index in Index.query.filter_by(status=1).all()]
        self.status.choices = [(0, 'Initial'), (1, 'Downloaded'), (2, 'Deprecated')]
        self.item = item

    def validate_url(self, field):
        if self.item is None:
            if List.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')
        else:
            if self.item.url != field.data and \
                    List.query.filter_by(url=field.data).first():
                raise ValidationError('Url already in use.')
