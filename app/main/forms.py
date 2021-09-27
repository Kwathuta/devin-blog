from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class UpdateProfile(FlaskForm):
    bio = TextAreaField(
        "Let people know a little bit more about you", validators=[DataRequired()]
    )
    submit = SubmitField("Save")


class BlogForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField(
        "Category",
        choices=[
            ("Lifestyle", "Lifestyle"),
            ("Fitness", "Fitness"),
            ("DIY", "DIY"),
        ],
        validators=[DataRequired()],
    )
    post = TextAreaField("Your Blog", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    comment = TextAreaField("Leave a comment", validators=[DataRequired()])
    submit = SubmitField("Comment")
