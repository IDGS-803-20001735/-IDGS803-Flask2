from flask import Flask, render_template, request, make_response, flash
from flask_wtf.csrf import CSRFProtect

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

@app.route("/Diccionario", methods = ['GET', 'POST'])
def diccionario():
    reg_palabras = forms.TradForm(request.form)
    if request.method == 'POST':
        with open('diccionario.txt', 'a') as f:
            f.write(f"{reg_palabras.inputEspanol.data.lower()}:{reg_palabras.inputIngles.data.lower()}\n")
        flash("Las palabras se almacenaron de forma correcta!!!", "success")
        return render_template('diccionario.html', form = reg_palabras)
        
    return render_template('diccionario.html', form = reg_palabras)

@app.route("/Traductor", methods=['GET', 'POST'])
def traductor():
    reg_palabras = forms.TradForm(request.form)
    if request.method == 'POST':
        idioma = request.form.get('lenguaje')
        palabra = request.form.get('text')

        traduccion = buscar_traduccion(palabra, idioma)

        traduccion = traduccion.capitalize()

        if not traduccion:
            flash(f"No se encontró traducción para {palabra} en {'español' if idioma == 'es' else 'ingles'}.", "error")
        
        return render_template('diccionario.html', form = reg_palabras, traduccion = traduccion)

    return render_template('diccionario.html', form = reg_palabras)

def buscar_traduccion(palabra, lenguaje):
    with open('diccionario.txt', 'r') as f:
        palabras = f.read().splitlines()
        for frase in palabras:
            partes = frase.split(':')
            if len(partes) == 2:
                if partes[0 if lenguaje == 'en' else 1].lower() == palabra.lower():
                    return partes[1 if lenguaje == 'en' else 0]
    return ''

@app.route("/Resistencia", methods=['GET', 'POST'])
def calResistencia():
    resistencia_form = forms.ResistenciaForm(request.form)
    if request.method == 'POST' and resistencia_form.validate():
        codigo_colores = {
          'black': 0,
          'maroon': 1,
          'red': 2,
          'orange': 3,
          'yellow': 4,
          'green': 5,
          'blue': 6,
          'violet': 7,
          'gray': 8,
          'white': 9,
          'gold': 0.05,
          'silver': 0.1
        }

        color1 = resistencia_form.bandaUno.data
        color2 = resistencia_form.bandaDos.data
        color3 = resistencia_form.bandaTres.data
        color4 = resistencia_form.tolerancia.data

        bandaUno = codigo_colores[color1]
        bandaDos = codigo_colores[color2]
        bandaTres = codigo_colores[color3]
        tolerancia = codigo_colores[color4]

        valorNominal = (bandaUno * 10 + bandaDos) * 10 ** bandaTres

        minimo = 0
        maximo = 0
        if tolerancia == 0.05:
            maximo = valorNominal + valorNominal*(0.05)
            minimo = valorNominal - valorNominal*(0.05)
        elif tolerancia == 0.1:
            maximo = valorNominal + valorNominal*(0.1)
            minimo = valorNominal - valorNominal*(0.1)

        return render_template('resistencia.html', form = resistencia_form, color1 = color1, color2 = color2, color3 = color3, color4 = color4, 
                               valorNominal = valorNominal, minimo =  minimo, maximo = maximo)
    return render_template('resistencia.html', form = resistencia_form)

if __name__ == "__main__":
    csrf.init_app(app)
    app.run(debug = True, port = 8080)