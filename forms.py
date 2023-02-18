from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FieldList, FormField, SelectField, RadioField
from wtforms.fields import EmailField

class UserForm(Form):
    matricula = StringField('Matricula')
    nombre = StringField('Nombre')
    apaterno = StringField('Apaterno')
    email = EmailField('Correo')