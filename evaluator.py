import os
import re
import sys

#token patterns
pat = re.compile(
 r'(?P<NUM>\d+(?:\.\d+)?)|'
 r'(?P<OP>[+\-*/%^])|'
 r'(?P<LPAREN>\()|'
 r'(?P<RPAREN>\))|'
 r'(?P<SPACE>[ \t]+)'
)

# split the input into pieces
def get_tokens(s):
    tokens = []
    pos = 0

    while pos < len(s):
        match = pat.match(s, pos)
        if match == None:
            raise ValueError("could not understand character near position " + str(pos))

        kind = match.lastgroup
        value = match.group()
        pos = match.end()

        if kind != 'SPACE':
            tokens.append((kind, value))

    tokens.append(('END', ''))
    return tokens


def show(tokens):
    things = []
    for token in tokens:
        if token[0] == 'END':
            things.append('[END]')
        else:
            things.append('[' + token[0] + ':' + token[1] + ']')
    return ' '.join(things)


def num(x):
    if x == int(x):
        return str(int(x))
    else:
        # round it for the output
        return '{:.4f}'.format(round(x, 4))


#parser position
pos = 0


def see(tokens):
    return tokens[pos]


def get(tokens):
    global pos
    value = tokens[pos]
    pos += 1
    return value


# handle addition and subtraction
def add(tokens):
    x = mul(tokens)
    while see(tokens)[0] == 'OP':
        if see(tokens)[1] in ['+', '-']:
            op = get(tokens)[1]
            right = mul(tokens)
            x = ('binop', op, x, right)
        else:
            break
    return x


# handle numbers and parentheses
def atom(tokens):
    token = see(tokens)

    if token[0] == 'NUM':
        get(tokens)
        return ('num', float(token[1]))

    if token[0] == 'LPAREN':
        get(tokens)
        answer = add(tokens)
        if see(tokens)[0] != 'RPAREN':
            raise ValueError("missing closing parenthesis")
        get(tokens)
        return answer

    raise ValueError("expected number or opening parenthesis")


# handle unary minus
def unary(tokens):
    x = see(tokens)

    if x[0] == 'OP' and x[1] == '-':
        get(tokens)
        return ('neg', unary(tokens))

    if x[0] == 'OP' and x[1] == '+':
        raise ValueError("unary plus is not allowed")

    return power(tokens)


# handle powers
def power(tokens):
    x = atom(tokens)

    if see(tokens)[0] == 'OP':
        if see(tokens)[1] == '^':
            get(tokens)
            x = ('binop', '^', x, unary(tokens))

    return x


#handle multiplication and division
def mul(tokens):
    x = unary(tokens)

    while True:
        z = see(tokens)

        if z[0] == 'OP' and z[1] in ['*', '/', '%']:
            op = get(tokens)[1]
            right = unary(tokens)
            x = ('binop', op, x, right)
        elif z[0] == 'LPAREN':
            right = unary(tokens)
            x = ('binop', '*', x, right)
        elif z[0] == 'NUM' and tokens[pos - 1][0] == 'RPAREN':
            right = unary(tokens)
            x = ('binop', '*', x, right)
        else:
            break

    return x

def parse(tokens):
    global pos
    pos = 0
    x = add(tokens)
    if see(tokens)[0] != 'END':
        raise ValueError("extra text after expression")
    return x


def calc(x):
    if x[0] == 'num':
        return x[1]

    if x[0] == 'neg':
        return -calc(x[1])

    first = calc(x[2])
    second = calc(x[3])
    op = x[1]

    if op == '+':
        return first + second
    elif op == '-':
        return first - second
    elif op == '*':
        return first * second
    elif op == '/':
        if second == 0:
            raise ZeroDivisionError("cannot divide by zero")
        return first / second
    elif op == '%':
        if second == 0:
            raise ZeroDivisionError("cannot divide by zero")
        return first % second
    elif op == '^':
        value = first ** second
        if isinstance(value, complex):
            raise ValueError("result is not a real number")
        return value

    raise ValueError("unknown operator")


def tree(x):
    if x[0] == 'num':
        return num(x[1])
    if x[0] == 'neg':
        return '(neg ' + tree(x[1]) + ')'
    return '(' + x[1] + ' ' + tree(x[2]) + ' ' + tree(x[3]) + ')'

#process one expression
def do_line(s):
    # deal with one line
    d = {'input': s, 'tree': None, 'tokens': None, 'result': None, 'error': None}

    try:
        t = get_tokens(s)
        d['tokens'] = show(t)
        x = parse(t)
        d['tree'] = tree(x)
    except ValueError as err:
        d['error'] = str(err)
        if d['tokens'] is None:
            d['tokens'] = 'ERROR'
        d['tree'] = 'ERROR'
        d['result'] = 'ERROR'
        return d
    except Exception as err:
        d['error'] = 'unexpected parsing error: ' + str(err)
        d['tokens'] = d['tokens'] or 'ERROR'
        d['tree'] = 'ERROR'
        d['result'] = 'ERROR'
        return d

    # calculate after parsing
    try:
        d['result'] = float(calc(x))
    except ZeroDivisionError as err:
        d['result'] = 'ERROR'
        d['error'] = str(err)
    except ValueError as err:
        d['result'] = 'ERROR'
        d['error'] = str(err)
    except Exception as err:
        d['result'] = 'ERROR'
        d['error'] = "calculation failed: " + str(err)

    return d
