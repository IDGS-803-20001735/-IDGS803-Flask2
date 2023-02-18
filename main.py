from flask import Flask, render_template, request

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

  results = []
  for number in numbersInt:
    appearance = numbersInt.count(number)
    results.append("{} aparece {} veces".format(number, appearance))

  return render_template('resultado.html', major = major, minor = minor, average = average, results = results)

if __name__ == "__main__":
    app.run(debug = True, port = 8080)