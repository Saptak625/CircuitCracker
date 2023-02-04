import enum
 
class CircuitType(enum.Enum):
    series = 1
    parallel = 2

class Resistor:
  def __init__(self, name, voltage = None, current = None, resistance = None, allowBypass = False):
    self.name = name.upper()
    if not(voltage or current or resistance) and not allowBypass:
      raise Exception(f"Voltage, current, or resistance needs to be known for Resistor '{self.name}'")
    self.voltage = voltage
    self.current = current
    self.resistance = resistance
    self.voltageReason = 'Given' if voltage else None
    self.currentReason = 'Given' if current else None
    self.resistanceReason = 'Given' if resistance else None

  def solved(self):
    return self.voltage and self.current and self.resistance

  def solve(self):
    return self.ohmsLaw() #If true, ohms law has been applied.
  
  def ohmsLaw(self):
    testSum = (1 if self.voltage else 0) + (1 if self.current else 0) + (1 if self.resistance else 0)
    if testSum == 2: #Only 2 variables
      if self.voltage and self.current:
        self.resistance = self.voltage / self.current
        self.resistanceReason = "Ohm's Law"
      elif self.voltage and self.resistance:
        self.current = self.voltage / self.resistance
        self.currentReason = "Ohm's Law"
      else:
        self.voltage = self.current * self.resistance
        self.voltageReason = "Ohm's Law"
      return True
    return False

  def printValues(self):
    print(f'{self.name}:')
    print(f'Voltage: {round(self.voltage, 5)} Volts ({self.voltageReason})')
    print(f'Current: {round(self.current, 5)} Amps ({self.currentReason})')
    print(f'Resistance: {round(self.resistance, 5)} Ohms ({self.resistanceReason})')

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return f'Resistor({self.name}, [{self.voltage}-{self.voltageReason}, {self.current}-{self.currentReason}, {self.resistance}-{self.resistanceReason}])'

class Leg(Resistor):
  def __init__(self, name, circuitType, subcomponents, voltage = None, current = None, resistance = None):
    super().__init__(name, voltage = voltage, current = current, resistance = resistance, allowBypass = True)
    self.circuitType = circuitType
    if len(subcomponents) == 0:
      raise Exception(f"Leg {self.name} must have at least 1 subresistor.")
    self.subcomponents = subcomponents

  def solved(self):
    subSolved = True
    for s in self.subcomponents:
      subSolved = subSolved and s.solved()
      if not subSolved:
        break
    return self.voltage and self.current and self.resistance and subSolved

  def solve(self):
    if self.ohmsLaw():
      return True
    elif self.equalityRules():
      return True
    elif self.sumRules():
      return True
    else:
      for s in self.subcomponents:
        if s.solve():
          return True
    return False

  #Subcomponent Math
  def equalityRules(self):
    if self.circuitType == CircuitType.series:
      testSum = len([True for s in self.subcomponents if s.current]) + (1 if self.current else 0)
      if testSum > 0 and testSum != len(self.subcomponents) + 1:
        equalityCurrent = ([s.current for s in self.subcomponents if s.current]+([self.current] if self.current else []))[0]
        if not self.current:
          self.current = equalityCurrent
          self.currentReason = 'Series Current Equality'
        for s in self.subcomponents:
          if not s.current:
            s.current = equalityCurrent
            s.currentReason = 'Series Current Equality'
        return True
    else:
      testSum = len([True for s in self.subcomponents if s.voltage]) + (1 if self.voltage else 0)
      if testSum > 0 and testSum != len(self.subcomponents) + 1:
        equalityVoltage = ([s.voltage for s in self.subcomponents if s.voltage]+([self.voltage] if self.voltage else []))[0]
        if not self.voltage:
          self.voltage = equalityVoltage
          self.voltageReason = 'Parallel Voltage Equality'
        for s in self.subcomponents:
          if not s.voltage:
            s.voltage = equalityVoltage
            s.voltageReason = 'Parallel Voltage Equality'
        return True
    return False

  def sumRules(self):
    if self.circuitType == CircuitType.series:
      testVoltageSum = len([True for s in self.subcomponents if s.voltage]) + (1 if self.voltage else 0)
      if testVoltageSum == len(self.subcomponents):
        if not self.voltage: #Voltage for leg not provided. Add all subvoltages.
          self.voltage = sum([s.voltage for s in self.subcomponents])
          self.voltageReason = 'Series Voltage Sum'
        else:
          subcomponentVoltageSum = 0
          targetSubcomponent = None
          for s in self.subcomponents:
            if s.voltage:
              subcomponentVoltageSum += s.voltage
            else:
              targetSubcomponent = s
          targetSubcomponent.voltage = self.voltage - subcomponentVoltageSum
          targetSubcomponent.voltageReason = 'Series Voltage Sum'
        return True
      testResistanceSum = len([True for s in self.subcomponents if s.resistance]) + (1 if self.resistance else 0)
      if testResistanceSum == len(self.subcomponents):
        if not self.resistance: #Resistance for leg not provided. Add all subresistances.
          self.resistance = sum([s.resistance for s in self.subcomponents])
          self.resistanceReason = 'Series Resistance Sum'
        else:
          subcomponentResistanceSum = 0
          targetSubcomponent = None
          for s in self.subcomponents:
            if s.resistance:
              subcomponentResistanceSum += s.resistance
            else:
              targetSubcomponent = s
          targetSubcomponent.resistance = self.resistance - subcomponentResistanceSum
          targetSubcomponent.resistanceReason = 'Series Resistance Sum'
        return True
    else:
      testCurrentSum = len([True for s in self.subcomponents if s.current]) + (1 if self.current else 0)
      if testCurrentSum == len(self.subcomponents):
        if not self.current: #Current for leg not provided. Add all subcurrents.
          self.current = sum([s.current for s in self.subcomponents])
          self.currentReason = 'Parallel Current Sum'
        else:
          subcomponentCurrentSum = 0
          targetSubcomponent = None
          for s in self.subcomponents:
            if s.current:
              subcomponentCurrentSum += s.current
            else:
              targetSubcomponent = s
          targetSubcomponent.current = self.current - subcomponentCurrentSum
          targetSubcomponent.currentReason = 'Parallel Current Sum'
        return True
      testResistanceSum = len([True for s in self.subcomponents if s.resistance]) + (1 if self.resistance else 0)
      if testResistanceSum == len(self.subcomponents):
        if not self.resistance: #Resistance for leg not provided. Add all subresistances using 1/r formula.
          self.resistance = 1/sum([(1/s.resistance) for s in self.subcomponents])
          self.resistanceReason = 'Parallel Resistance Sum'
        else:
          subcomponentResistanceSum = 0
          targetSubcomponent = None
          for s in self.subcomponents:
            if s.resistance:
              subcomponentResistanceSum += (1/s.resistance)
            else:
              targetSubcomponent = s
          targetSubcomponent.resistance = 1/((1/self.resistance) - subcomponentResistanceSum)
          targetSubcomponent.resistanceReason = 'Parallel Resistance Sum'
        return True
    return False

  def __repr__(self):
    return self.__str__()

  def __str__(self):
    return f'Resistor({self.name}, {self.circuitType}, {self.subcomponents}, [{self.voltage}-{self.voltageReason}, {self.current}-{self.currentReason}, {self.resistance}-{self.resistanceReason}])'