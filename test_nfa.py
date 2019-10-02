from finite_automata import *

def _test_against(nfa, tests):
    failed_tests = []
    for test_case, expected in tests.items():
        try:
            result = nfa.accepts(test_case)
        except (ValueError, TypeError) as e:
            result = e
        if expected != result:
            failed_tests.append((test_case, expected, result))
    if failed_tests:
        pad = max(len(str(s)) for s in tests.keys())
        print(f'Failed {len(failed_tests)} tests.')
        for test_case, expected, result in failed_tests:
            print(str(test_case).ljust(pad), end=': ')
            print(f'expected {expected}, received {result}.')
    else:
        print('All tests passed.')

def _test1():
    print('TEST 1')
    epsilon = r'\e'
    q1, q2, q3, q4, q5 = 'q1', 'q2', 'q3', 'q4', 'q5'
    states = (q1, q2, q3, q4, q5)
    alphabet = ['0','1']
    transitions = {
        (q1, epsilon): [q2, q4],
        (q2, '0'): q2,
        (q2, '1'): q3,
        (q3, '0'): (q3),
        (q3, '1'): q2,
        (q4, '0'): q5,
        (q4, '1'): q4,
        (q5, '0'): q5,
        (q5, '1'): q4,
    }
    start = q1
    accepting = {q3, q5}
    nfa = NFA(states, alphabet, transitions, start, accepting)
    print(str(nfa))
    print('Deterministic?', nfa.is_deterministic())
    
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
        '0000000000000110': True,
    }
    
    _test_against(nfa, tests)

def _test2():
    #this is just test 1 but with the elements replaced with non-string types
    #tests the pythonic-ness of the NFA class. Any immutable object can represent
    #a symbol or state.
    print('TEST 2')
    epsilon = 0
    states = [1,2,3,None,5]
    alphabet = {7, 2.8}
    transitions = {
        (1, epsilon): [2, None],
        (2, 7): 2,
        (2, 2.8): 3,
        (3, 7): 3,
        (3, 2.8): 2,
        (None, 7): 5,
        (None, 2.8): None,
        (5, 7): 5,
        (5, 2.8): None,
    }
    start = 1
    accepting = {3, 5}
    nfa = NFA(states, alphabet, transitions, start, accepting, empty_string=epsilon)
    print(nfa)
    print('Deterministic?', nfa.is_deterministic())
    
    tests = {
        (): False,
        (7,): True,
        (2.8,): True,
        (2.8, 2.8): False,
        (2.8, 2.8, 7): True,
        (2.8, 2.8, 2.8): True,
        (2.8, 7, 2.8): False,
        (2.8, 2.8, 2.8, 7): True,
        (2.8, 2.8, 2.8, 2.8): False,
        (7, 2.8, 2.8): False,
        (7, 2.8): True,
        (7, 2.8, 7, 2.8): False,
        (7, 2.8, 7, 2.8, 7, 7, 7, 7, 7, 7, 7, 2.8): True,
        (7,7,7,7,7,7,7,7,7,7,7,7,2.8,2.8): False,
        (7,7,7,7,7,7,7,7,7,7,7,7,2.8,2.8,7): True,
    }
    
    _test_against(nfa, tests)

def _test3():
    #test the regular expression a(a U bb)*ba
    print('TEST 3')
    states = set(range(1,15))
    alphabet = {'a', 'b'}
    a, b, e = 'a', 'b', 'e'
    mapping = {
        (1, a): 2,
        (2, e): 3,
        (3, e): {4,11},
        (4, e): {5,7},
        (5, a): 6,
        (6, e): {4,11},
        (7, b): 8,
        (8, e): {9},
        (9, b): 10,
        (10, e): {4,11},
        (11, b): 12,
        (12, e): 13,
        (13, a): 14
    }
    nfa = NFA(states, alphabet, mapping, 1, {14})
    print(nfa)
    print('Deterministic?', nfa.is_deterministic())
    
    tests = {
        '': False,
        'a': False,
        'b': False,
        'ab': False,
        'aa': False,
        'bb': False,
        'aaa': False,
        'aab': False,
        'aba': True,
        'abb': False,
        'aaaa': False,
        'aaba': True,
        'aaab': False,
        'aaaba': True,
        'aaaaaaaaaaaaba': True,
        'abbba': True,
        'abba': False,
        'abbbbba': True,
        'abbbba': False,
        'abbaaaaabbabbbbaba': True,
    }
    
    _test_against(nfa, tests)

def _test4():
    #minimal test, accepts empty set
    print('TEST 4')
    nfa = NFA({1}, {'a'}, {}, 1, set())
    print(nfa)
    print('Deterministic?', nfa.is_deterministic())
    tests = {
        '': False, 'a': False, 'asdf': False
    }
    _test_against(nfa, tests)

def _test5():
    #minimal test, accepts empty string
    print('TEST 5')
    nfa = NFA({1}, {'a'}, {}, 1, {1})
    print(nfa)
    print('Deterministic?', nfa.is_deterministic())
    tests = {
        '': True, 'a': False, 'asdf': False
    }
    _test_against(nfa, tests)

def _test6():
    #minimal test, accepts the element a
    print('TEST 6')
    nfa = NFA({1,2}, {'a'}, ((1, 'a', 2),), 1, {2})
    print(nfa)
    print('Deterministic?', nfa.is_deterministic())
    tests = {
        '': False, 
        'a': True, 
        'b': False, 
        'ab': False, 
        'ba': False,
        'aa': False,
        'asdf': False
    }
    _test_against(nfa, tests)

def _test7():
    #test determinism
    print('TEST 7')
    dfa = NFA(
            {1,2}, 
            {'a', 'b'}, 
            {(1, 'a'): 2, (1, 'b'):1, (2, 'a'): 1, (2, 'b'): 2},
            1,
            {2})
    print(dfa)
    print('Deterministic?', dfa.is_deterministic())
    dfa = NFA(
            {1,2}, 
            {'a', 'b'}, 
            {(1, 'a'): 2, (1, 'b'):1, (2, 'a'): 1, (2, 'b'): 2, (1, 'e'): 2},
            1,
            {2})
    print(dfa)
    print('Deterministic?', dfa.is_deterministic())

def _test8():
    #test validation
    print('TEST 8')
    try:
        NFA({1,2}, set(), {}, 3, {2})
        print('failed')
    except:
        print('success')
    try:
        NFA({1,2}, set(), {(1,'a'):1}, 2, {2})
        print('failed')
    except:
        print('success')
    try:
        NFA({1,2}, {'a'}, {(4,'a'):1}, 1, {2})
        print('failed')
    except:
        print('success')
    try:
        NFA({1,2}, {'a'}, {(1,'a'):3}, 1, {2})
        print('failed')
    except:
        print('success')
    try:
        NFA({1,2}, {'a'}, {(1,'a'):2}, 1, {3})
        print('failed')
    except:
        print('success')
    try:
        NFA({1,2}, {'a'}, {(1,'e'):2}, 1, {2})
        print('success')
    except:
        print('failed')
        
    

if __name__ == '__main__':
    _test1()
    print()
    _test2()
    print()
    _test3()
    print()
    _test4()
    print()
    _test5()
    print()
    _test6()
    print()
    _test7()
    print()
    _test8()