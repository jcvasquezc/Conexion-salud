# pythonspot.com
from flask import Flask, render_template, flash, request
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from pymongo import MongoClient #Manejos de base de datos


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'

class ReusableForm(Form):
    name = TextField('Nombre:', validators=[validators.required()])
    dpto = TextField('Departamento:', validators=[validators.required()])
    city = TextField('Ciudad:', validators=[validators.required()])
    addr = TextField('Dirección:', validators=[validators.required()])
    tel=IntegerField('Teléfono:', validators=[validators.required(), validators.NumberRange(min=0000, max=9999999999, message="Por favor introduzca un teléfono valido")])
    email = TextField('Email:', validators=[validators.required(), validators.Length(min=6, max=35, message="Por favor introduzca un email valido")])


@app.route("/", methods=['GET', 'POST'])
def datos_ips():
    form = ReusableForm(request.form)

    print (form.errors)
    if request.method == 'POST':

        name=request.form['name']
        dpto=request.form['dpto']
        city=request.form['city']
        addr=request.form['addr']
        tel=request.form['tel']
        email=request.form['email']

        print (name, " ", dpto, " ", city, " ", addr, " ", tel, " ", email)

        if form.validate():
            # Save the comment here.
            flash('Gracias por registrarse ' + name)
        else:
            flash('Error: Todos los campos son requeridos. ')

    return render_template('encuesta.html', form=form)

if __name__ == "__main__":
    app.run()
