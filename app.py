from flask import Flask, render_template, flash
from flask_assets import Environment
import time

from assets import bundles
from forms import CircuitForm
from circuit_solver import CircuitSolver

app = Flask(__name__)
app.config['SECRET_KEY'] = '7b7e30111ddc1f8a5b1d80934d336798'

assets = Environment(app)
assets.register(bundles)


@app.route('/')
def index():
    return render_template('index.html', data=None)


@app.route('/solve', methods=['GET', 'POST'])
def form():
    circuitForm = CircuitForm()
    data = None
    if circuitForm.circuitCode.data:
        print(circuitForm.circuitCode.data)
        circuitSolver = CircuitSolver(circuitForm.circuitCode.data)
        circuitSolver.solve()
        circuitSolver.showCircuit()
    return render_template('solve.html', data=data, circuitForm=circuitForm)


if __name__ == '__main__':
    app.run(debug=True)
