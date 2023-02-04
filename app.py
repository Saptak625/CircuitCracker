from flask import Flask, render_template, flash
from flask_assets import Environment
import time

from assets import bundles
from forms import InputForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

assets = Environment(app)
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html', data=None)


@app.route('/form', methods=['GET', 'POST'])
def form():
    inputForm = InputForm()
    data = None
    if inputForm.inputString.data:
        time.sleep(2)
        data = inputForm.inputString.data
    print(data)
    return render_template('form.html', data=data, inputForm=inputForm)


if __name__ == '__main__':
    app.run(debug=True)
