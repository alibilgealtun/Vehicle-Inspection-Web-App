from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


class StaffForm(FlaskForm):
    first_name = StringField(
        'First Name',
        validators=[
            DataRequired(message="Bu alan gereklidir."),
            Length(min=2, max=50, message="Ad 2 ile 50 karakter arasında olmalıdır.")
        ]
    )
    last_name = StringField(
        'Last Name',
        validators=[
            DataRequired(message="Bu alan gereklidir."),
            Length(min=2, max=50, message="Soyad 2 ile 50 karakter arasında olmalıdır.")
        ]
    )
    password = PasswordField(
        'Password',
        validators=[
            DataRequired(message="Bu alan gereklidir."),
            Length(min=6, message="Şifre en az 6 karakter olmalıdır.")
        ]
    )
    phone_number = StringField(
        'Phone Number',
        validators=[
            DataRequired(message="Bu alan gereklidir."),
            Length(min=2, max=15, message="Telefon numarası 10 ile 15 karakter arasında olmalıdır.")
        ]
    )
    department = StringField(
        'Department',
        validators=[Optional(), Length(max=50, message="Departman 50 karakterden fazla olamaz.")]
    )
    role = StringField(
        'Role',
        validators=[
            DataRequired(message="Rol alanı gereklidir."),
            Length(max=50, message="Rol 50 karakterden fazla olamaz.")
        ]
    )
    branch_id = IntegerField(
        'Branch ID',
        validators=[
            Optional(),
            NumberRange(min=1, message="Geçerli bir Şube ID girin.")
        ]
    )
    submit = SubmitField('Add Staff')
