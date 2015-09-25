from flask.ext.wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import Required

class LoginForm(Form):
    """Accepts a name."""
    name = StringField('Name', validators=[Required()])
    submit = SubmitField('Enter Raffle')
