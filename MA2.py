"""
Solutions to module 2 - A calculator
Student: Sepehr Mohammadi
Mail:sepehr.mohammadi.1613@student.uu.se
Reviewed by: Maximilian Meyer-Moelleringhof
Reviewed date: 19th Sept 2022
"""

"""
Note:
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class SyntaxError is complete as well as handling in main
of SyntaxError and TokenError.
"""

from cmath import cos, exp, log, sin
import math
from statistics import mean
from tokenize import TokenError  
from MA2tokenizer import TokenizeWrapper


class EvaluationError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)

def fib(n, computed = {0: 0, 1: 1}):
    if n<0 or int(n) != n:
        raise EvaluationError('Fib argument must be a non negative integer')
    elif n not in computed:
        computed[n] = fib(n-1, computed) + fib(n-2, computed)
    return computed[n]
        
    
def log(n):
    if n>0:
        return math.log(n)
    else:
        raise EvaluationError("Log argument must be positive")

def fac(n):
    if int(n) != n  or n < 0:
        raise EvaluationError("Fac argument must be non negative integer")
    if n==0:
        return 1
    else:
        return n * fac(n-1)

functions_1 = {'sin':math.sin, 'cos': math.cos, 'exp': math.exp, 'log':log, 'fib':fib, 'fac': fac}

function_n = {'max':max, 'min':min, 'sum':sum, 'mean':mean}


class SyntaxError(Exception):
    def __init__(self, arg):
        self.arg = arg
        super().__init__(self.arg)


def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    if wtok.is_at_end():
        pass
    else:
        raise SyntaxError('Expected to be ended')
    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)
    while wtok.get_current() == '=':
        wtok.next()
        if wtok.is_name():
            variables[wtok.get_current()] = result
            wtok.next()
        else:
            raise SyntaxError("Expected a name")
        
    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)
    while wtok.get_current() == '+' or wtok.get_current() == '-':
        if wtok.get_current() == '+':
            wtok.next()
            result = result + term(wtok, variables)
            
        if wtok.get_current() == '-':
            wtok.next()
            result = result - term(wtok, variables)
           
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)
    while wtok.get_current() == '*' or wtok.get_current() == '/':
        if wtok.get_current() == '*':
            wtok.next()
            result = result * factor(wtok, variables)
            
        if wtok.get_current() == '/':
            wtok.next()
            a = factor(wtok, variables)
            if a != 0:
                result = result / a 
            else:
                raise EvaluationError('Cant devide by 0')
    
        
    return result


def factor(wtok, variables):
    """ See syntax chart for factor"""
    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise SyntaxError("Expected ')'")
        else:
            wtok.next()    
            
    elif wtok.get_current() in functions_1:
        func1 = wtok.get_current()
        wtok.next()
        if wtok.get_current() == '(':
            wtok.next()
            result = assignment(wtok, variables)
            #print(result, wtok.get_current())
            if wtok.get_current() != ')':
                raise SyntaxError("Expected ')'")
            else:
                result = functions_1[func1](result)
                wtok.next()
        else:
             raise SyntaxError("Expected '('")  
         
    elif wtok.get_current() in function_n:
        funcn = wtok.get_current()
        wtok.next()
        result = function_n[funcn](arglist(wtok, variables))
         
    elif wtok.is_number():
        result = float(wtok.get_current())
        wtok.next()
        
    elif wtok.is_name():
        varr = wtok.get_current()
        if varr in variables:
            result = variables[wtok.get_current()]
        else:
            raise EvaluationError ('Variable name is not defined')
        wtok.next() 
        
    elif wtok.get_current() == '-':
        wtok.next()
        result = (-1) * factor(wtok, variables)
        #wtok.next()
        
    else:
        raise SyntaxError(
            "Expected number or '('")  
    return result


def arglist(wtok, variables):
    args = []
    if wtok.get_current() == '(':
        wtok.next()

        while True:
            result = assignment(wtok, variables)
            args.append(result)
            if wtok.get_current() == ')':
                wtok.next()
                break
            
            if wtok.get_current() != ',':
                raise SyntaxError("Expected ','")
            wtok.next()
            
    else:
        raise SyntaxError("Expected '('")
    return args
    
def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """
    
    print("Numerical calculator")
    variables = {"ans": 0.0, "E": math.e, "PI": math.pi}
    
    
    
    # Note: The unit test file initiate variables in this way. If your implementation 
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA2init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0]=='#':
            continue
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye')
            exit()
        else:
            try:
                result = statement(wtok, variables)
                variables['ans'] = result
                print('Result:', result)

            except SyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')
 
            except EvaluationError as se:
                print("*** Evaluation error: ", se)
                print(
                f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

if __name__ == "__main__":
    main()



    
def fac(n):
    if n==0:
        return 1
    else:
        return n * fac(n-1)
    
    functions_1 = {'sin':math.sin, 'cos': math.cos, 'exp': math.exp, 'log':math.log, 'fib':fib, 'fac': math.factorial}
    