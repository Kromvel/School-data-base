
class checkMathExp:
    def __init__(self, mathExp):
        self.mathExp = mathExp
    def check_valid(value):
        checkSymbols = '0123456789+-*/.^()'
        parenthesis = '()'
        data = value.replace(" ", "")
        parenthesisCount = 0
        try:
            for i in data:
                if i not in checkSymbols:
                    return "Выражение невалидно: есть некорректный символ, например: {}".format(i)
                elif i in parenthesis:
                    parenthesisCount += 1
            if parenthesisCount % 2 != 0:
                return "Выражение невалидно: Количество скобок нечетное"
        except(ValueError,TypeError):
            raise ValueError('Тип некорректен')
            
        return data
    def eval_math(formula):
        OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
                '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}
        def parse(formula_string):
            number = ''
            for s in formula_string:
                if s in '1234567890.': # если символ - цифра, то собираем число
                    number += s  
                elif number: # если символ не цифра, то выдаём собранное число и начинаем собирать заново
                    yield float(number) 
                    number = ''
                if s in OPERATORS or s in "()": # если символ - оператор или скобка, то выдаём как есть
                    yield s 
            if number:  # если в конце строки есть число, выдаём его
                yield float(number)  

        def shunting_yard(parsed_formula):
            stack = []  # в качестве стэка используем список
            for token in parsed_formula:
                # если элемент - оператор, то отправляем дальше все операторы из стека, 
                # чей приоритет больше или равен пришедшему,
                # до открывающей скобки или опустошения стека.
                # здесь мы пользуемся тем, что все операторы право-ассоциативны
                if token in OPERATORS: 
                    while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                        yield stack.pop()
                    stack.append(token)
                elif token == ")":
                    # если элемент - закрывающая скобка, выдаём все элементы из стека, до открывающей скобки,
                    # а открывающую скобку выкидываем из стека.
                    while stack:
                        x = stack.pop()
                        if x == "(":
                            break
                        yield x
                elif token == "(":
                    # если элемент - открывающая скобка, просто положим её в стек
                    stack.append(token)
                else:
                    # если элемент - число, отправим его сразу на выход
                    yield token
            while stack:
                yield stack.pop()
            

        def calc(polish):
            stack = []
            try:
                for token in polish:
                    if token in OPERATORS: # если приходящий элемент - оператор,
                        y, x = stack.pop(), stack.pop()  # забираем 2 числа из стека
                        
                        stack.append(OPERATORS[token][1](x, y)) # вычисляем оператор, возвращаем в стек
                    else:
                        stack.append(token)
                return stack[0] # результат вычисления - единственный элемент в стеке
            except (IndexError):
                raise IndexError('В выражении присутствуют некорректные символы')
            
        respond = calc(shunting_yard(parse(formula)))
        if respond.is_integer() == True:
            print(int(respond))
            return int(respond)
        elif respond.is_integer() == False:
            return respond
if __name__ == '__main__':
    checkMathExp.eval_math('2+2')