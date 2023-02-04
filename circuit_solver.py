from component import CircuitType, Resistor, Leg

class CircuitSolver:
  def __init__(self, circuitCode):
    self.components = {}
    self.compileCircuit(circuitCode)
    self.stepByStepReasoning = ''

  def compileCircuitFromFile(fileName):
    with open(fileName, 'r') as circuitCode:
      circuitSolver = CircuitSolver(circuitCode.read())
    return circuitSolver

  def compileCircuit(self, circuitCode):
    #Read Line by Line to compile code
    returnComponent = ''
    for raw in circuitCode.replace('\r', '\n').split('\n'):
      c = raw.lower()
      c = c.replace('\n', '')
      parameters = c.split(' ')
      if not c:
        continue
      if c[0] == 'r' or c[0] == 'l':
        voltage = None
        current = None
        resistance = None
        subcomponentString = ''
        for p in parameters:
          if '_' in p:
            measure = p.split('_')
            if 'v' in measure[1]:
              voltage = float(measure[0])
            elif 'a' in measure[1]:
              current = float(measure[0])
            elif 'o' in measure[1]:
              resistance = float(measure[0])
          elif ',' in p:
            subcomponentString = p
        if c[0] == 'r':
          #Create new resistor
          r = Resistor(parameters[0], voltage = voltage, current = current, resistance = resistance)
          self.components[r.name] = r
        else:
          #Create new Leg
          if parameters[1] == 's':
            circuitType = CircuitType.series
          elif parameters[1] == 'p':
            circuitType = CircuitType.parallel
          else:
            raise Exception(f'Must declare whether Leg "{parameters[0].upper()}" is series or parallel.')
          subcomponentNames = subcomponentString.split(',')[:-1]
          subcomponents = [self.components[n.upper()] for n in subcomponentNames]
          l = Leg(parameters[0], circuitType, subcomponents, voltage = voltage, current = current, resistance = resistance)
          self.components[l.name] = l
      else:
        #Return Statement
        print('Parameters', parameters)
        returnComponent = parameters[1].upper()
    if returnComponent not in self.components:
      raise Exception(f"Return Statement must be included.")
    self.circuit = self.components[returnComponent]

  def solve(self):
    #Solving Driver
    while not self.circuit.solved():
      if not self.circuit.solve():
        raise Exception('Either not enough information passed resulting in ambigious case or algorithm missing solving method')

  def showCircuit(self, showLegs = True, showResistors = True):
    componentNames = sorted(list(self.components.keys()))
    self.circuit.printValues()
    for n in componentNames:
      if not ((not showLegs and n[0] == 'L') or (not showResistors and n[0] == 'R') or n == self.circuit.name):
        print()
        self.components[n].printValues()

  def writeReasoning(reasoning):
    self.stepByStepReasoning += reasoning;
