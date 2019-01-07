# Satplan_AI
Solving planning problems using SATPLAN, through the creation of an encoder (PDDL) and a solver (DPLL).
Project for the course of Artificial Intelligence and Decision Systems.

SATPLAN is based on the idea of first encoding the planning problem into a SAT problem, and then solving it using a state-of-the-art SAT solver [Kautz, 1992].
So we create a:
1) Encoder - Encode the planning problem (given in an input_domain_data_file), into a SAT problem using PDDL (FOL).
2) Solver - Solve it using a state-of-the-art SAT sover (DPLL).
