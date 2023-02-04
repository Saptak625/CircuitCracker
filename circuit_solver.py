from component import CircuitType, Resistor, Leg

class CircuitSolver:
  def __init__(self, circuitCode):
    self.components = {}
    self.compileCircuit(circuitCode)
    self.stepByStepReasoning = []

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
          r = Resistor(parameters[0], self.writeReasoning, voltage = voltage, current = current, resistance = resistance)
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
          l = Leg(parameters[0], self.writeReasoning, circuitType, subcomponents, voltage = voltage, current = current, resistance = resistance)
          self.components[l.name] = l
      else:
        #Return Statement
        returnComponent = parameters[1].upper()
    if returnComponent not in self.components:
      raise Exception(f"Return Statement must be included.")
    self.circuit = self.components[returnComponent]

  def setRoundingPlace(self, roundingPlace):
    Resistor.roundingPlace = roundingPlace

  def solve(self):
    #Solving Driver
    while not self.circuit.solved():
      if not self.circuit.solve():
        raise Exception('Either not enough information passed resulting in ambigious case or algorithm missing solving method')

  def writeReasoning(self, reasoning):
    self.stepByStepReasoning.append(reasoning)

  def getStepByStepReasoning(self, showVoltageSteps = True, showCurrentSteps = True, showResistanceSteps = True, asList = False):
    out = []
    i = 1
    for r in self.stepByStepReasoning:
      write = False
      if "Ohm's Law" in r:
        if 'its voltage' in r and showVoltageSteps:
          write = True
        elif 'its current' in r and showCurrentSteps:
          write = True
        elif 'its resistance' in r and showResistanceSteps:
          write = True
      elif 'Voltage' in r and showVoltageSteps:
        write = True
      elif 'Current' in r and showCurrentSteps:
        write = True
      elif 'Resistance' in r and showResistanceSteps:
        write = True
      if write:
        out.append(r if asList else f'{i}. {r}')
        i += 1
    return out if asList else '\n'.join(out)

  def showStepByStepReasoning(self, showVoltageSteps = True, showCurrentSteps = True, showResistanceSteps = True):
    print(self.getStepByStepReasoning(showVoltageSteps=showVoltageSteps, showCurrentSteps=showCurrentSteps, showResistanceSteps=showResistanceSteps))

  def __str__(self, showLegs = True, showResistors = True, showVoltage = True, showCurrent = True, showResistance = True):
    def sortKeys(name):
      return 0 if name[0].upper() == 'L' else 1, sum([ord(i) for i in name[1:]])
    componentNames = sorted(list(self.components.keys()), key = sortKeys)
    out = self.circuit.__str__(showVoltage=showVoltage, showCurrent=showCurrent, showResistance=showResistance)
    for n in componentNames:
      if not ((not showLegs and n[0] == 'L') or (not showResistors and n[0] == 'R') or n == self.circuit.name):
        out += f'\n\n{self.components[n].__str__(showVoltage=showVoltage, showCurrent=showCurrent, showResistance=showResistance)}'
        pass
    return out

  def __repr__(self, showLegs = True, showResistors = True, showVoltage = True, showCurrent = True, showResistance = True):
    return self.__str__(showLegs=showLegs, showResistors=showResistors, showVoltage=showVoltage, showCurrent=showCurrent, showResistance=showResistance)

  def showCircuit(self, showLegs = True, showResistors = True, showVoltage = True, showCurrent = True, showResistance = True):
    print(self.__str__(showLegs=showLegs, showResistors=showResistors, showVoltage=showVoltage, showCurrent=showCurrent, showResistance=showResistance))
