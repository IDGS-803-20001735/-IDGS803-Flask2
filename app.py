from flask import Flask, render_template, request, make_response, flash
from flask_wtf.csrf import CSRFProtect
from forms import TradForm as trad
from forms import LangForm as lang

import forms

app = Flask(__name__)
app.config['SECRET_KEY'] = "Esta es la clave encriptada"
csrf = CSRFProtect()

@app.errorhandler(404)
def no_encontrada(e):
    return render_template('404.html'), 404

@app.route("/cookies", methods=["GET", "POST"])
def cookies():
    reg_user = forms.LoginForm(request.form)
    datos = ' '
    if request.method == 'POST' and reg_user.validate():
        user = reg_user.username.data
        passw = reg_user.password.data
        datos = user + '@' + passw
        success_message = 'Bienvenido {}'.format(user)
        flash(success_message)

    response = make_response(render_template('cookies.html', form = reg_user))

    if len(datos) > 0:
        response.set_cookie('datos_user', datos)
    return response

@app.route("/saludo")
def saludo():
    valor_cookie = request.cookies.get('datos_user')
    nombres = valor_cookie.split('@')
    return render_template('saludo.html', nombres = nombres[0])

@app.route('/')
def formulario():
    return render_template('formulario.html')
           
@app.route("/Alumnos", methods = ['GET', 'POST'])
def alumnos():
    alum_form = forms.UserForm(request.form)

    if request.method == 'POST' and alum_form.validate():
        print(alum_form.matricula.data)
        print(alum_form.nombre.data)
        
    return render_template('alumnos.html', form = alum_form)

@app.route("/traductor", methods=['POST', 'GET'])
def traductor():
    reg_lang = lang(request.form)
    reg_trad = trad(request.form)

    if request.method == 'POST' and reg_lang.validate():
        with open('traducciones.txt', 'a') as f:
            f.write(f"{reg_lang.espanniol.data.lower()} = {reg_lang.ingles.data.lower()}\n")
        flash('Traducción guradada')
        return render_template('traductor.html', reg_lang = reg_lang, reg_trad = reg_trad)
    else:
        return render_template('traductor.html', reg_lang = reg_lang, reg_trad = reg_trad)

@app.route("/traductor_resultado", methods = ['POST', 'GET'])
def traductor_resultado():
    reg_trad = trad(request.form)
    reg_lang = lang(request.form)

    if request.method == 'POST' and reg_trad.validate():
        idioma = request.form.get('lenguaje')
        if idioma == 'es':
            palabra = request.form.get('inputEspanol')
        else:
            palabra = request.form.get('inputIngles')
        resultado = buscar_traduccion(palabra, idioma)
        if resultado is '':
            if idioma == 'es':
                mensaje = "No se encontró traducción para {} en inglés.".format(palabra)
            elif idioma == 'en':
                mensaje = "No se encontró traducción para {} en español.".format(palabra)
            flash(mensaje)
        if idioma == 'es':
            return render_template('traductor.html', form = reg_lang, formSalida = reg_trad, ingles = resultado, español = palabra)
        else:
            return render_template('traductor.html', form = reg_lang, formSalida = reg_trad, ingles = palabra, español = resultado)
    return render_template('traductor.html', form = reg_lang, formSalida = reg_trad)

def buscar_traduccion(palabra, lenguaje):
    with open('traducciones.txt', 'r') as f:
        lineas = f.readlines()
        for linea in lineas:
            partes = linea.strip().split('=')
            if len(partes) == 2:
                if lenguaje == 'es' and partes[0].lower() == palabra.lower():
                    return partes[1]
                elif lenguaje == 'en' and partes[1].lower() == palabra.lower():
                    return partes[0]
    return ''

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug = True, port = 8080)