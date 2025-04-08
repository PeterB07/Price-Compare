from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Optional

class ProductSearchForm(FlaskForm):
    query = StringField('Search Products', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('', 'All Categories'),
        ('laptops', 'Laptops'),
        ('smartphones', 'Smartphones'),
        ('tablets', 'Tablets'),
        ('tvs', 'TVs'),
        ('cameras', 'Cameras'),
        ('gaming', 'Gaming Consoles'),
        ('audio', 'Audio Devices')
    ], validators=[Optional()])
    submit = SubmitField('Search')

class ProductTrackingForm(FlaskForm):
    target_price = FloatField('Alert me when price drops below:', validators=[Optional()])
    submit = SubmitField('Track Product')

class AddProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    brand = StringField('Brand', validators=[Optional()])
    model = StringField('Model', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('laptops', 'Laptops'),
        ('smartphones', 'Smartphones'),
        ('tablets', 'Tablets'),
        ('tvs', 'TVs'),
        ('cameras', 'Cameras'),
        ('gaming', 'Gaming Consoles'),
        ('audio', 'Audio Devices')
    ], validators=[DataRequired()])
    image_url = StringField('Image URL', validators=[Optional(), URL()])
    submit = SubmitField('Add Product')