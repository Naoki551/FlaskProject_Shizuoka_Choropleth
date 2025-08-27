from flask_wtf import FlaskForm
from wtforms import FileField,StringField, SubmitField
from wtforms.validators import DataRequired
# import gunicorn

class UploadCSVForm(FlaskForm):
    file = FileField('CSVかExcelファイル', validators=[DataRequired()])
    municipalities = StringField('自治体名の入ったコラム名', validators=[DataRequired()], default='自治体名')
    values = StringField("データの入ったコラム名",validators=[DataRequired()],default="収入額（千円）")
    title = StringField("タイトルを設定", validators=[DataRequired()],default="SAMPLE")
    submit = SubmitField('Upload')

class ValueForm(FlaskForm):
    pass