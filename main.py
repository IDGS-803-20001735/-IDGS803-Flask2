from flask import Flask, render_template, request
from collections import Counter

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('app.html')
           
@app.route("/Store", methods = ['GET', 'POST'])
def store():
    if request.method == 'POST':
        numberFields = int(request.form.get('txtNumberFields'))
        
        return render_template('process.html', numberFields = numberFields)


@app.route("/Process", methods = ['POST'])
def process():
  numbersString = request.form.getlist('txtNumber')
  numbersInt = list(map(int, numbersString))

  major = max(numbersInt)
  minor = min(numbersInt)

  average = sum(numbersInt) / len(numbersInt)

  counter = Counter(numbersString)
  resultados = counter.most_common()
  results = []
  for r in resultados:
        if r[1] > 1:
            results.append('El numero {0} se repite {1}'.format(r[0], r[1]))

  return render_template('resultado.html', major = major, minor = minor, average = average, results = results)

if __name__ == "__main__":
    app.run(debug = True, port = 8080)