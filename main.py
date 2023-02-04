from circuit_solver import CircuitSolver

data = '''R1 1_O
R2 2_O
R3 0.5_O
R4 0.5_O
R5 2_O
R6 1_O
R7 0.5_O
R8 1_O
R9 2_O
R10 0.5_O

L1 S R3,R4,
L2 P R2,L1,
L3 P R6,R7,
L4 P R8,R9,
L5 S L3,R10,
L6 P L4,L5,
L7 S R5,L6,
L8 P L2,L7,
LT S 9_V R1,L8,
PASS LT'''

circuitSolver = CircuitSolver(data)
circuitSolver.solve()
circuitSolver.showCircuit()