#!/usr/bin/python3
#Note: swe = self = this

class NFA:    
    def __init__(
            swe, 
            states: iter, 
            alphabet: iter, 
            transitions: iter, 
            start, 
            accept: iter):
        r'''
        Creates a nondeterministic finite automaton out of the given elements.
        
        states: an iterable of the states of the NFA
        alphabet: an iterable of the symbols over which the NFA is defined. 
            Symbols must be strings of length 1.
        string. To include '\' in your string, escape it with '\\'.
        transitions: this is either 
            1)  a dictionary mapping (state, symbol) pairs to states or 
                iterables of states, or
            2)  an iterable whose elements are themselves iterables of length
                greater than or equal to 2, where the first element is a state,
                the second is a symbol, and the rest are the resulting states
                given by the transition function.
            If 'e' is not in the alphabet of the DFA, then 'e' in a transition 
            will be considered to be the empty string. '\e' will always be 
            considered to be the empty string.
        start: the start state
        accept: an iterable of accepting states
        '''
        swe.states = set(states)
        swe.alphabet = set(alphabet)
        swe.transitions = swe._convert_transitions(transitions)
        swe.start = start
        if start not in swe.states:
            raise ValueError("Start state must be in the set of states")
        swe.accept = set(accept)
    
    def accepts(swe, string: str) -> bool:
        '''
        Determines if the given string is accepted by the NFA.
        
        string: The string to feed to the DFA
        '''
        current_states = swe._traverse_epsilon_transitions({swe.start})
        for symbol in string:
            current_states = swe._transition(current_states, symbol)
            if not current_states:
                return False
            current_states = swe._traverse_epsilon_transitions(current_states)
        return any(state in swe.accept for state in current_states)
    
    def _transition(swe, states:set, symbol: str) -> set:
        '''
        Transitions the NFA from a given set of states to a new set of states
        using the given symbol.
        '''
        new_states = set()
        for state in states:
            if (state, symbol) in swe.transitions.keys():
                new_states |= swe.transitions[(state, symbol)]
        return new_states
    
    def _traverse_epsilon_transitions(swe, states: set) -> set:
        #accumulator of all states in the traversal
        final_states = set(states)
        #the states which have not already been checked for epsilon transitions
        unchecked_states = set(states)
        #the states transitioned to by epsilon edges during the current pass
        new_states = set()
        while unchecked_states:
            for state in unchecked_states:
                if (state, '\e') in swe.transitions.keys():
                    new_states |= swe.transitions[(state, '\e')]
            unchecked_states = new_states - final_states
            final_states |= new_states
            new_states = set()
        return final_states
    
    def _translate_epsilon(swe, symbol: str) -> bool:
        r'''
        Returns '\e' if the given symbol should be considered to be the empty
        string. Otherwise, returns the symbol
        '''
        if symbol == 'e' and 'e' not in swe.alphabet:
            return r'\e'
        return symbol
    
    def _convert_transitions(swe, transitions) -> dict:
        '''
            Converts the given transitions structure into a valid mapping of
            (state, symbol) pairs to sets of states
        '''
        if not transitions:
            return {}
        transition_mapping = {}
        if type(transitions) is dict:
            for key, val in transitions.items():
                #if key is of the form (state, symbol) then continue
                #otherwise, the input is bad
                try:
                    state, symbol = key
                except (TypeError, ValueError):
                    raise ValueError("Transition mapping  must have"
                            "(state, symbol) tuple as keys")
                #if val is iterable, create a set of states out of it
                #otherwise, create a set with it as the only element
                try:
                    resulting_states = set(val)
                except TypeError:
                    resulting_states = {val}
                symbol = swe._translate_epsilon(symbol)
                transition_mapping[(state, symbol)] = resulting_states
        else:
            for it in transitions:
                #if it is an iterable with at least 2 elements, then
                #it's valid as a transition
                try:
                    state, symbol, *result = it
                except (TypeError, ValueError):
                    raise ValueError('Transition mapping must provide a state'
                            'and symbol for each transition')
                symbol = _translate_epsilon(symbol)
                transition_mapping[(state,symbol)] = set(result)
        return transition_mapping


def sadri_nfa(filename: str) -> NFA:
    '''
    Reads in the given Sadri-syntax NFA file and constructs an NFA from it.
    
    filename: the name of the file
    returns: the NFA specified by the file
    '''
    with open(filename, 'r') as f:
        pass


def _test1():
    epsilon = '\e'
    q1, q2, q3, q4, q5 = 'q1', 'q2', 'q3', 'q4', 'q5'
    states = (q1, q2, q3, q4, q5)
    alphabet = [0,1]
    transitions = {
        (q1, epsilon): [q2, q4],
        (q2, 0): q2,
        (q2, 1): q3,
        (q3, 0): (q3),
        (q3, 1): q2,
        (q4, 0): q5,
        (q4, 1): q4,
        (q5, 0): q5,
        (q5, 1): q4,
    }
    start = q1
    accepting = {q3, q5}
    nfa = NFA(states, alphabet, transitions, start, accepting)
    
    tests = {
        '': False,
        '0': True,
        '1': True,
        '11': False,
        '110': True,
        '111': True,
        '101': False,
        '1110': True,
        '1111': False,
        '011': False,
        '01': True,
        '0101': False,
        '010100000000001': True,
        '000000000000011': False,
    }
    
    for test_case, expected in tests.items():
        result = nfa.accepts(test_case)
        print(f'"{test_case}": expected {expected}, got {result}.',
                'passed.' if result == expected else 'failed.')