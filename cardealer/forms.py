from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from cardealer.models import User, CarData

class RegistrationForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired(), Length(min=2, max=50)])
    Company = StringField('Company', validators=[DataRequired(), Length(min=2, max=50)])
    Phone = StringField('Phone', validators=[DataRequired(), Length(min=8, max=8)])
    CVR = StringField('CVR', validators=[DataRequired(), Length(min=7, max=8)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

    def validate_Name(self, name):
        user = User.query.filter_by(username=name.data).first()
        if user:
            raise ValidationError('Name is already taken, choose a different')

    def validate_Company(self, company):
        user = User.query.filter_by(company=company.data).first()
        if user:
            raise ValidationError('Company is already registered, choose a different')
    
    def validate_Phone(self, phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('Phone number is already taken, choose a different')

    def validate_CVR(self, CVR):
        user = User.query.filter_by(CVR=CVR.data).first()
        if user:
            raise ValidationError('CVR number is already taken, choose a different')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email address is already taken, choose a different')

class LoginForm(FlaskForm):
    CVR = StringField('CVR', validators=[DataRequired(), Length(min=7, max=8)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class UpdateAccountForm(FlaskForm):
    CVR = StringField('CVR', validators=[Length(min=7, max=8)])
    email = StringField('Email', validators=[Email()])
  

    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_CVR(self, CVR):
        if CVR.data != current_user.CVR:
            user = User.query.filter_by(CVR=CVR.data).first()
            if user:
                raise ValidationError('CVR number is already taken, choose a different')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email address is already taken, choose a different')

class CarForm(FlaskForm):
    Brand = StringField('Brand', validators=[DataRequired(), Length(min=2, max=50)])
    Model = StringField('Model', validators=[DataRequired(), Length(min=2, max=50)])
    Engine = StringField('Engine', validators=[DataRequired(), Length(min=2, max=50)])
    Colour = StringField('Colour', validators=[DataRequired(), Length(min=2, max=50)])
    Comment = StringField('Comment', validators=[DataRequired(), Length(min=2, max=50)])
    #image_file2 = FileField('Attach picture', validators=[FileAllowed(['jpg', 'png'])])
    
    submit = SubmitField('Submit car')



#class CarForm(FlaskForm):
    #title = StringField('License Plate', validators=[DataRequired()])

    #def API(self, data):
        #ApiUrl = "http://api.nrpla.de/"
        #url = ApiUrl + title() +"?api_token=iZ3T9knspElwMyglvXbFKaKXK8co5k0LKjLzke6Uirnaw5FuqtE20SXKI4ttrZIM&advanced=1"
        #req = requests.get(url)
        #data = json.loads(req.content)
        
    #content = TextAreaField('Comment', validators=[DataRequired()])
    #picturecar = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    #submit = SubmitField('Post')
    