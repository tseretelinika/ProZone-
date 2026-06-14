from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User


class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 30)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(6)])
    confirm = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username already taken. Please choose another.")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email already registered.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign In")


class ReviewForm(FlaskForm):
    content = TextAreaField("Your Review", validators=[DataRequired(), Length(10, 500)])
    rating = SelectField(
        "Rating",
        choices=[(1, "⭐ 1"), (2, "⭐⭐ 2"), (3, "⭐⭐⭐ 3"), (4, "⭐⭐⭐⭐ 4"), (5, "⭐⭐⭐⭐⭐ 5")],
        coerce=int,
    )
    submit = SubmitField("Submit Review")


class ProductForm(FlaskForm):
    name = StringField("Product Name", validators=[DataRequired(), Length(3, 150)])
    brand = SelectField(
        "Brand",
        choices=[
            ("Adidas", "Adidas"),
            ("Nike", "Nike"),
            ("Puma", "Puma"),
            ("Air Jordan", "Air Jordan"),
            ("Under Armour", "Under Armour"),
        ],
    )
    category = StringField("Category", validators=[DataRequired()])
    price = FloatField("Price ($)", validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField("Description", validators=[DataRequired(), Length(10)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Save Product")
