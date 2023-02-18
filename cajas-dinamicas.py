from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('cajas-dinamicas.html')
           
@app.route("/Store", methods = ['GET', 'POST'])
def process():
    if request.method == 'POST':
        fields = int(request.form.get('fields'))

        return render_template('result.html', fields = fields)
        
    return render_template('cajas-dinamicas.html')

@app.route("/Calculos", methods = ['POST'])
def calculos():
    if request.method == 'POST':
        numeros = request.form.getlist('txtNumero')
        numeros = [int(num) for num in numeros]

        mayor = max(numeros)
        menor = min(numeros)

        return render_template('result.html', mayor = mayor, menor = menor)
    
    return render_template('result.html')
    

if __name__ == "__main__":
    app.run(debug = True, port = 8080)