from operator import add, sub, mul, floordiv

OPERATORS = {'+': add, '-': sub, '*': mul, '/': floordiv}


def postfix_evaluator(expr):
    expr_list = expr.split()
    stack = []
    for elem in expr_list:
        if elem in OPERATORS:
            operand2 = stack.pop()
            operand1 = stack.pop()
            stack.append(OPERATORS[elem](operand1, operand2))
        else:
            stack.append(int(elem))
    return stack.pop()
