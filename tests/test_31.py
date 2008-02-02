# -*- coding: UTF-8 -*-

# Checking if pymacs.el works (pymacs-services unused).

import re
import setup
from Pymacs import lisp, pymacs

def setup_module(module):
    setup.start_emacs()

def teardown_module(module):
    setup.stop_emacs()

def test_1():

    def validate(input, expected):
        output = re.sub(r'\(pymacs-(defun|python) [0-9]*\)',
                        r'(pymacs-\1 0)',
                        setup.ask_emacs(input))
        assert output == expected, (output, expected)

    for quotable, input, output in (
            (False, None, 'nil'),
            (False, 3, '3'),
            (False, 0, '0'),
            (False, -3, '-3'),
            (False, 3., '3.0'),
            (False, 0., '0.0'),
            (False, -3., '-3.0'),
            (False, '', '""'),
            (False, 'a', '"a"'),
            (False, 'byz', '"byz"'),
            (False, 'c\'bz', '"c\'bz"'),
            (False, 'd"z', r'"d\"z"'),
            (False, 'e\\bz', r'"e\\bz"'),
            (False, 'f\bz', '"f\bz"'),
            (False, 'g\fz', '"g\fz"'),
            (False, 'h\nz', '"h\nz"'),
            (False, 'i\tz', '"i\tz"'),
            (False, 'j\x1bz', '"j\x1bz"'),
            (False, (), '[]'),
            (False, (0,), '[0]'),
            (False, (0.0,), '[0.0]'),
            (False, ('a',), '["a"]'),
            (False, (0, 0.0, "a"), '[0 0.0 "a"]'),
            (True, [], 'nil'),
            (True, [0], '(0)'),
            (True, [0.0], '(0.0)'),
            (True, ['a'], '("a")'),
            (True, [0, 0.0, "a"], '(0 0.0 "a")'),
            (False, lisp['nil'], 'nil'),
            (True, lisp['t'], 't'),
            (True, lisp['ab_cd'], 'ab_cd'),
            (True, lisp['ab-cd'], 'ab-cd'),
            (False, lisp.nil, 'nil'),
            (True, lisp.t, 't'),
            (True, lisp.ab_cd, 'ab-cd'),
            # TODO: Lisp and derivatives
            ):
        fragments = []
        pymacs.print_lisp(input, fragments.append, quotable)
        yield validate, '(prin1 %s)' % ''.join(fragments), output
    for input, output in (
            (ord, '(pymacs-defun 0)'),
            (object(), '(pymacs-python 0)'),
            ):
        fragments = []
        pymacs.print_lisp(input, fragments.append, True)
        yield validate, '(prin1 \'%s)' % ''.join(fragments), output

def notest_2():

    def validate(input, expected):
        import re
        output = re.sub(r'\(pymacs-(defun|python) [0-9]*\)',
                        r'(pymacs-\1 0)',
                        setup.ask_emacs(input))
        assert output == expected, (output, expected)

    for quotable, input, ouptut in (
            (False, None, 'nil'),
            (False, 3, '3'),
            (False, 0, '0'),
            (False, -3, '-3'),
            (False, 3., '3.0'),
            (False, 0., '0.0'),
            (False, -3., '-3.0'),
            (False, '', '""'),
            (False, 'a', '"a"'),
            (False, 'byz', '"byz"'),
            (False, 'c\'bz', '"c\'bz"'),
            (False, 'd"z', r'"d\"z"'),
            (False, 'e\\bz', r'"e\\bz"'),
            (False, 'f\bz', '"f\bz"'),
            (False, 'g\fz', '"g\fz"'),
            (False, 'h\nz', '"h\nz"'),
            (False, 'i\tz', '"i\tz"'),
            (False, 'j\x1bz', '"j\x1bz"'),
            (False, (), '[]'),
            (False, (0,), '[0]'),
            (False, (0.0,), '[0.0]'),
            (False, ('a',), '["a"]'),
            (False, (0, 0.0, "a"), '[0 0.0 "a"]'),
            (True, [], 'nil'),
            (True, [0], '(0)'),
            (True, [0.0], '(0.0)'),
            (True, ['a'], '("a")'),
            (True, [0, 0.0, "a"], '(0 0.0 "a")'),
            (False, lisp['nil'], 'nil'),
            (True, lisp['t'], 't'),
            (True, lisp['ab_cd'], 'ab_cd'),
            (True, lisp['ab-cd'], 'ab-cd'),
            (False, lisp.nil, 'nil'),
            (True, lisp.t, 't'),
            (True, lisp.ab_cd, 'ab-cd'),
            # TODO: Lisp and derivatives
            ):
        fragments = []
        pymacs.print_lisp(input, fragments.append, quotable)
        yield (validate,
               '(pymacs-print-for-eval %s)' % ''.join(fragments),
               output)
    #('(let ((pymacs-forget-mutability t)\n'
    # '   (pymacs-print-for-eval %s)))\n'
    # % output),
    for input, output in (
            (ord, '(pymacs-defun 0)'),
            (object(), '(pymacs-python 0)'),
            ):
        fragments = []
        pymacs.print_lisp(input, fragments.append, True)
        yield (validate,
               '(pymacs-print-for-eval \'%s)' % ''.join(fragments),
               output)

def notest_3():
    value = setup.ask_emacs('nil\n')
    assert value == '8', repr(value)

#def test_pymacs_print_for_eval():
#    yield output, '3 + 5', '3 + 5'
#
#def test_pymacs_eval():
#    yield output_eval, '3 + 5', 8
#    yield output_eval, '`3 + 5`', '8'
