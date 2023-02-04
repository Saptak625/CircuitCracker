# ComplexCircuitSolver
Complex Circuit Solver is a Python program to solve Complex Circuits with Resistors with Logical Reasoning. It uses a Component Tree structure with Recursive Solving to determine the voltages, currents, and resistances for any complex circuit.

Demo Link(https://replit.com/@Saptak625/ComplexCircuitSolver#main.py).

## User Guide
In the current version (v1), circuits are represented in .crc circuit code file. These files are compiled line by line by a custom compiler to create a Component Tree structure. The code in main.py will compile the given file when the CiruitSolver class is instantiated.

### Commands

#### R
The "R" command is used to define a new resistor. The resistor requires only 2 parameters, but can take up to 4 parameters. Every resistor needs to have a name/label. This distinguishes each resistor. If 2 resistors are defined with the same name, the latest one will overwrite the previous one. The name directly follows the "R" command. You can make the name as long as you would like as long as it has no newline characters, spaces, underscores, or commas. Usually, however, a simple number will suffice. The other three paramaters are for voltage, current, and resistance. At least one of these parameters must be provided in order for the resistor to not be ambigious. All three parameters can be provided, but if these parameters don't agree, algorithm will not function properly. These three parameters must be provided after the name followed by a space. You must provide the according units for these parameters namely `_V` for voltage, `_A` for current, and `_O` for resistance.

Eg. `R1 250_O`, `RMIDDLE 5_V 200_O`, `R5 10_V 0.01_A 0.1_O`

#### L
The "L" command is used to define legs. Legs are like "abstract" resistors. This is because any complex circuit can be simplified into a single resistor. As a result, legs act as containers for resistors and other legs. Legs accept all the same parameters as a resistor, but also require 2 more parameters. First, a Leg must be defined as Series(S) or Parallel(P). Second, the names of the subcomponents of a leg needed to listed seperated by commas __including an extra comma at the very end.__ A leg must have at least one subcomponent. With only one subcomponent, leg can be either defined as series or parallel. Finally, once again, if overdefining a leg, ensure that it is accurate, otherwise algorithm will not function properly.

Eg. `L1 S 9_V L1,R2,R3,`, `LTOTAL P 3_V 1000_O R1,`

#### PASS
Every circuit code file needs to have a PASS statement. This statement signifies what the root component of the tree is. Root component could be either a single resistor or a leg, which could contain multiple resitors. The PASS statement only requires one parameter, which is simply the name of the root component.

Eg. `PASS LT`

## Future Plans
* Circuit Code may be replaced with interative GUI to design circuits instead. This may result in automatic definitions of legs.
* Expansion to other electrical components such as capacitors and inductors may be added.
