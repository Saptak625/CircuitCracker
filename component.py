import enum
 
class CircuitType(enum.Enum):
    series = 1
    parallel = 2

class Resistor:
  roundingPlace = 5

  def __init__(self, name, writeReasoning, voltage = None, current = None, resistance = None, allowBypass = False):
    self.name = name.upper()
    self.writeReasoning = writeReasoning
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
        self.writeReasoning(f'{self.name} has a voltage of {round(self.voltage, Resistor.roundingPlace)} Volts and a current of {round(self.current, Resistor.roundingPlace)} Amps, so its resistance is {round(self.resistance, Resistor.roundingPlace)} Ohms. (Ohm\'s Law)')
      elif self.voltage and self.resistance:
        self.current = self.voltage / self.resistance
        self.currentReason = "Ohm's Law"
        self.writeReasoning(f'{self.name} has a voltage of {round(self.voltage, Resistor.roundingPlace)} Volts, and a resistance of {round(self.resistance, Resistor.roundingPlace)} Ohms, so its current is {round(self.current, Resistor.roundingPlace)} Amps. (Ohm\'s Law)')
      else:
        self.voltage = self.current * self.resistance
        self.voltageReason = "Ohm's Law"
        self.writeReasoning(f'{self.name} has a current of {round(self.current, Resistor.roundingPlace)} Amps and a resistance of {round(self.resistance, Resistor.roundingPlace)} Ohms, so its voltage is {round(self.voltage, Resistor.roundingPlace)} Volts. (Ohm\'s Law)')
      return True
    return False

  def __repr__(self, pretty = False, showVoltage = True, showCurrent = True, showResistance = True):
    return self.__str__(pretty = pretty, showVoltage = showVoltage, showCurrent = showCurrent, showResistance = showResistance)

  def __str__(self, pretty = True, showVoltage = True, showCurrent = True, showResistance = True):
    if pretty:
      props = [f'Voltage: {round(self.voltage, Resistor.roundingPlace)} Volts ({self.voltageReason})', f'Current: {round(self.current, Resistor.roundingPlace)} Amps ({self.currentReason})', f'Resistance: {round(self.resistance, Resistor.roundingPlace)} Ohms ({self.resistanceReason})']
      props = [p for i, p in enumerate(props) if [showVoltage, showCurrent, showResistance][i]]
      return f'{self.name}:\n' + '\n'.join(props)
    else:
      props = [f'{self.voltage}-{self.voltageReason}', f'{self.current}-{self.currentReason}', f'{self.resistance}-{self.resistanceReason}']
      props = [p for i, p in enumerate(props) if [showVoltage, showCurrent, showResistance][i]]
      if props:
        return f'Resistor({self.name}, {props})'
      else:
        return f'Resistor({self.name})'

class Leg(Resistor):
  def __init__(self, name, writeReasoning, circuitType, subcomponents, voltage = None, current = None, resistance = None):
    super().__init__(name, writeReasoning, voltage = voltage, current = current, resistance = resistance, allowBypass = True)
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
          self.writeReasoning(f'{self.name} has a current of {round(self.current, Leg.roundingPlace)} Amps because all subcomponents have the same current. (Series Current Equality)')
        for s in self.subcomponents:
          if not s.current:
            s.current = equalityCurrent
            s.currentReason = 'Series Current Equality'
            s.writeReasoning(f'{s.name} has a current of {round(s.current, Leg.roundingPlace)} Amps because all subcomponents have the same current. (Series Current Equality)')
        return True
    else:
      testSum = len([True for s in self.subcomponents if s.voltage]) + (1 if self.voltage else 0)
      if testSum > 0 and testSum != len(self.subcomponents) + 1:
        equalityVoltage = ([s.voltage for s in self.subcomponents if s.voltage]+([self.voltage] if self.voltage else []))[0]
        if not self.voltage:
          self.voltage = equalityVoltage
          self.voltageReason = 'Parallel Voltage Equality'
          self.writeReasoning(f'{self.name} has a voltage of {round(self.voltage, Leg.roundingPlace)} Volts because all subcomponents have the same voltage. (Parallel Voltage Equality)')
        for s in self.subcomponents:
          if not s.voltage:
            s.voltage = equalityVoltage
            s.voltageReason = 'Parallel Voltage Equality'
            s.writeReasoning(f'{s.name} has a voltage of {round(s.voltage, Leg.roundingPlace)} Volts because all subcomponents have the same voltage. (Parallel Voltage Equality)')
        return True
    return False

  def sumRules(self):
    if self.circuitType == CircuitType.series:
      testVoltageSum = len([True for s in self.subcomponents if s.voltage]) + (1 if self.voltage else 0)
      if testVoltageSum == len(self.subcomponents):
        if not self.voltage: #Voltage for leg not provided. Add all subvoltages.
          self.voltage = sum([s.voltage for s in self.subcomponents])
          self.voltageReason = 'Series Voltage Sum'
          self.writeReasoning(f'{self.name} has a voltage of {round(self.voltage, Leg.roundingPlace)} Volts because it is equal to the sum of the voltages of all subcomponents {", ".join([s.name+" ("+str(round(s.voltage, Leg.roundingPlace))+" Volts)" for s in self.subcomponents])}. (Series Voltage Sum)')
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
          self.writeReasoning(f'{targetSubcomponent.name} has a voltage of {round(targetSubcomponent.voltage, Leg.roundingPlace)} Volts because it is equal to the difference between the voltage of {self.name} ({round(self.voltage, Leg.roundingPlace)} Volts) and the sum of the voltages of all other subcomponents ({", ".join([s.name for s in self.subcomponents if s != targetSubcomponent])}) ({round(subcomponentVoltageSum, Leg.roundingPlace)} Volts). (Series Voltage Sum)')
        return True
      testResistanceSum = len([True for s in self.subcomponents if s.resistance]) + (1 if self.resistance else 0)
      if testResistanceSum == len(self.subcomponents):
        if not self.resistance: #Resistance for leg not provided. Add all subresistances.
          self.resistance = sum([s.resistance for s in self.subcomponents])
          self.resistanceReason = 'Series Resistance Sum'
          self.writeReasoning(f'{self.name} has a resistance of {round(self.resistance, Leg.roundingPlace)} Ohms because it is equal to the sum of the resistances of all subcomponents {", ".join([s.name+" ("+str(round(s.resistance, Leg.roundingPlace))+" Ohms)" for s in self.subcomponents])}. (Series Resistance Sum)')
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
          self.writeReasoning(f'{targetSubcomponent.name} has a resistance of {round(targetSubcomponent.resistance, Leg.roundingPlace)} Ohms because it is equal to the difference between the resistance of {self.name} ({round(self.resistance, Leg.roundingPlace)} Ohms) and the sum of the resistances of all other subcomponents ({", ".join([s.name for s in self.subcomponents if s != targetSubcomponent])}) ({round(subcomponentResistanceSum, Leg.roundingPlace)} Ohms). (Series Resistance Sum)')
        return True
    else:
      testCurrentSum = len([True for s in self.subcomponents if s.current]) + (1 if self.current else 0)
      if testCurrentSum == len(self.subcomponents):
        if not self.current: #Current for leg not provided. Add all subcurrents.
          self.current = sum([s.current for s in self.subcomponents])
          self.currentReason = 'Parallel Current Sum'
          self.writeReasoning(f'{self.name} has a current of {round(self.current, Leg.roundingPlace)} Amps because it is equal to the sum of the currents of all subcomponents {", ".join([s.name+" ("+str(round(s.current, Leg.roundingPlace))+" Amps)" for s in self.subcomponents])}. (Parallel Current Sum)')
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
          self.writeReasoning(f'{targetSubcomponent.name} has a current of {round(targetSubcomponent.current, Leg.roundingPlace)} Amps because it is equal to the difference between the current of {self.name} ({round(self.current, Leg.roundingPlace)} Amps) and the sum of the currents of all other subcomponents ({", ".join([s.name for s in self.subcomponents if s != targetSubcomponent])}) ({round(subcomponentCurrentSum, Leg.roundingPlace)} Amps). (Parallel Current Sum)')
        return True
      testResistanceSum = len([True for s in self.subcomponents if s.resistance]) + (1 if self.resistance else 0)
      if testResistanceSum == len(self.subcomponents):
        if not self.resistance: #Resistance for leg not provided. Add all subresistances using 1/r formula.
          self.resistance = 1/sum([(1/s.resistance) for s in self.subcomponents])
          self.resistanceReason = 'Parallel Resistance Sum'
          self.writeReasoning(f'{self.name} has a resistance of {round(self.resistance, Leg.roundingPlace)} Ohms because it is equal to the reciprocal of the sum of the reciprocals of the resistances of all subcomponents {", ".join([s.name+" ("+str(round(s.resistance, Leg.roundingPlace))+" Ohms)" for s in self.subcomponents])}. (Parallel Resistance Sum)')
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
          self.writeReasoning(f'{targetSubcomponent.name} has a resistance of {round(targetSubcomponent.resistance, Leg.roundingPlace)} Ohms because it is equal to the reciprocal of the difference between the reciprocal of the resistance of {self.name} ({round(self.resistance, Leg.roundingPlace)} Ohms) and the sum of the reciprocals of the resistances of all other subcomponents ({", ".join([s.name for s in self.subcomponents if s != targetSubcomponent])}) ({round(subcomponentResistanceSum, Leg.roundingPlace)} Ohms). (Parallel Resistance Sum)')
        return True
    return False

  def __str__(self, pretty = True, showVoltage = True, showCurrent = True, showResistance = True):
    if pretty:
      props = [f'Voltage: {round(self.voltage, Leg.roundingPlace)} Volts ({self.voltageReason})', f'Current: {round(self.current, Leg.roundingPlace)} Amps ({self.currentReason})', f'Resistance: {round(self.resistance, Leg.roundingPlace)} Ohms ({self.resistanceReason})']
      props = [p for i, p in enumerate(props) if [showVoltage, showCurrent, showResistance][i]]
      return f'{self.name}:\n' + '\n'.join(props)
    else:
      props = [f'{self.voltage}-{self.voltageReason}', f'{self.current}-{self.currentReason}', f'{self.resistance}-{self.resistanceReason}']
      props = [p for i, p in enumerate(props) if [showVoltage, showCurrent, showResistance][i]]
      if props:
        return f'Leg({self.name}, {self.circuitType}, {[s.name for s in self.subcomponents]}, {props})'
      else:
        return f'Leg({self.name}, {self.circuitType}, {[s.name for s in self.subcomponents]})'