#!/usr/bin/python3
#Note: swe means self

class NFA:    
    def __init__(
            swe, 
            states, 
            alphabet, 
            transitions, 
            start, 
            accept,
            empty_string=r'\e'):
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
        empty_string: the immutable object to consider the empty string on
            transition edges
        '''
        swe.empty_string = empty_string
        swe.states = set(states)
        swe.alphabet = set(alphabet)
        swe.transitions = swe._convert_transitions(transitions)
        swe.start = start
        swe.accept = set(accept)
        swe._validate()
    
    def is_deterministic(swe) -> bool:
        #ensure that no epsilon transitions exist, that no transition points to
        #more than one state
        for (state, symbol), states in swe.transitions.items():
            if symbol == swe.empty_string:
                return False
            if len(states) != 1:
                return False
        #ensure that all elements of the alphabet are
        #accounted for in the transitions for every state
        for state in swe.states:
            for symbol in swe.alphabet:
                if (state, symbol) not in swe.transitions.keys():
                    return False
        return True
    
    def accepts(swe, string: str) -> bool:
        '''
        Determines if the given string is accepted by the NFA.
        
        string: The string to feed to the DFA
        '''
        current_states = swe._traverse_epsilon_transitions({swe.start})
        for symbol in string:
            current_states = swe._transition(current_states, symbol)
            #return False if the set of current states is the empty set
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
        '''
        Calculates the set of all states reachable by epsilon transitions from
        the given set of states
        '''
        #accumulator of all states in the traversal
        final_states = set(states)
        #the states which have not already been checked for epsilon transitions
        unchecked_states = set(states)
        #the states transitioned to by epsilon edges during the current pass
        new_states = set()
        while unchecked_states:
            for state in unchecked_states:
                if (state, swe.empty_string) in swe.transitions.keys():
                    new_states |= swe.transitions[(state, swe.empty_string)]
            unchecked_states = new_states - final_states
            final_states |= new_states
            new_states = set()
        return final_states
    
    def _translate_epsilon(swe, symbol: str) -> bool:
        r'''
        Returns empty string if the given symbol should be considered to be the 
        empty string. Otherwise, returns the symbol
        '''
        if symbol == 'e' and 'e' not in swe.alphabet:
            return swe.empty_string
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
                #if val is iterable (not str), create a set of states out of it
                #otherwise, create a set with it as the only element
                try:
                    if type(val) is str:
                        resulting_states = {val}
                    else:
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
                symbol = swe._translate_epsilon(symbol)
                transition_mapping[(state,symbol)] = set(result)
        return transition_mapping
    
    def _validate(swe):
        if swe.start not in swe.states:
            raise ValueError("Start state must be in the set of states")
        if not swe.accept <= swe.states:
            raise ValueError("Accepting states must be a subset of states")
        for (state, symbol), states in swe.transitions.items():
            if state not in swe.states:
                raise ValueError(f"Transition function contains invalid state {state}")
            if symbol not in swe.alphabet and symbol != swe.empty_string:
                raise ValueError(f'Transition function contains invalid symbol {symbol}')
            if not states <= swe.states:
                raise ValueError(f'Transition function contains invalid states {states}')
        
    def __str__(swe):
        from pprint import pformat
        string = '(Q,\u03A3,\u03B4,q\u2080,F), where:\n'
        string += f'Q = {swe.states}\n'
        string += f'\u03A3 = {swe.alphabet}\n'
        string += f'\u03B4 is a function defined by the map\n'
        string += ''.join(f'  {line}\n' for line in 
                pformat(swe.transitions).splitlines())
        string += f'q\u2080 = {swe.start}\n'
        string += f'F = {swe.accept}\n'
        string += f'and {swe.empty_string} is considered to be the empty string.'
        return string


class DFA(NFA):
    def __init__(swe, *args):
        super().__init__(*args)
        if not swe.is_deterministic():
            raise ValueError('DFA must be deterministic')


def sadri_nfa(filename: str) -> NFA:
    '''
    Reads in the given Sadri-syntax NFA file and constructs an NFA from it.
    
    filename: the name of the file
    returns: the NFA specified by the file
    '''
    with open(filename, 'r') as f:
        reading_transitions = False
        transitions = []
        states = {}
        for line in f:
            line = line.lower().strip()
            if line.startswith('number of states:'):
                num_states = int(line.split()[-1])
            elif line.startswith('alphabet:'):
                alphabet = set(line.split()[1:])
            elif line.startswith('start state:'):
                start_state = line.split()[-1]
            elif line.startswith('accept states:'):
                accept = set(line.split()[1:])
            elif reading_transitions:
                if line == 'transitions end':
                    reading_transitions = False
                else:
                    transitions.append(line.split())
                    states.add(transitions[-1][0])
            elif line == 'transitions begin':
                reading_transitions = True
    return NFA(states, alphabet, transitions, start_state, accept)
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        try:
            nfa = sadri_nfa(sys.argv[1])
            while True:
                print('Enter string: ', end='')
                string = input()
                accepted = nfa.accepts(string)
                not_str = 'not ' if not accepted else ''
                print(f'The string {string} is {not_str} accepted.')
        except FileNotFoundError:
            print('File not found.')
        except KeyboardInterrupt:
            pass
    else:
        print('Usage: python finite_automata.py <filename>')
