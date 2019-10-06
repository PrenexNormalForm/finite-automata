#Finite Automata

Simulates deterministic and nondeterministic finite automata.

Use the `NFA` (or `DFA`) class with the (Q,Σ,δ,q0,F) definition of a finite automaton.

If the `finite_automata` module is the main module, then it will look for a file provided as an argument to the program from which to read the definition of an automaton. It can be required that the automaton be a DFA with the optional `--dfa` argument. The program will then indefinitely prompt for user input of strings to test against the automaton.
