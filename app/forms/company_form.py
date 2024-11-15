from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, URL, Length


class CompanyForm(FlaskForm):
    name = StringField('Company Name', validators=[DataRequired(), Length(max=100)])
    phone_1 = StringField('Primary Phone', validators=[Optional(), Length(max=15)])
    phone_2 = StringField('Secondary Phone', validators=[Optional(), Length(max=15)])
    fax = StringField('Fax', validators=[Optional(), Length(max=15)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=100)])
    website = StringField('Website', validators=[Optional(), URL(), Length(max=100)])
    address = StringField('Address', validators=[Optional(), Length(max=255)])
    my_business_address_link = StringField('My Business Address Link', validators=[Optional(), URL(), Length(max=255)])
    submit = SubmitField('Save')
