from flask import render_template
from app import app
from .forms import CalculatorForm
from flask import render_template, flash


@app.route('/')
def index():
    user = {'name': 'Homer Simpson'}
    return render_template('index.html', title='Simple template example', user=user)

@app.route('/fruit')
def displayFruit():
    fruits = ["Apple", "Banana", "Orange", "Kiwi"]
    return render_template("fruit_with_inheritance.html", fruits=fruits)

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    form = CalculatorForm()
    if form.validate_on_submit():
        result = form.number1.data + form.number2.data
        flash('Successfully received form data. %s + %s = %s' % (form.number1.data, form.number2.data, result))
    return render_template('calculator.html', title='Calculator', form=form)