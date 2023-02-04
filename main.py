from circuit_solver import CircuitSolver

circuitSolver = CircuitSolver.compileCircuitFromFile('circuit.crc')
circuitSolver.setRoundingPlace(5)
circuitSolver.solve()
circuitSolver.showStepByStepReasoning(showVoltageSteps=True, showCurrentSteps=True, showResistanceSteps=True)
print('\n\n')
circuitSolver.showCircuit(showVoltage=True, showCurrent=True, showResistance=True, showLegs=True, showResistors=True)