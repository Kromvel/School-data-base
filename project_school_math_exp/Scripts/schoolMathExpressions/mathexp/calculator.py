'''
Данные модуль проверяет корректно ли составлено математическое выражение (это функция check_valid()) и, если да, то вычисляет его (это функция eval_math()) 
'''
class checkMathExp:
    def __init__(self, mathExp):
        self.mathExp = mathExp
    def check_valid(value):
        # переменная с перечислением всех подходящих символов, нужна для проверки наличия постороннего символа в примере, например буквы
        checkSymbols = '0123456789+-*/.^()'
        # переменная с наличием открывающей и закрывающей скобок. Нужна для проверки имеют ли скобки пару в примере.
        parenthesis = '()'
        # переменная убирает все пробелы из полученного выражения.
        data = value.replace(" ", "")
        # переменная для проверки на наличие пар скобок в ходе итерации
        parenthesisCount = 0
        try:
            for i in data:
                # проверка на посторонний символ
                if i not in checkSymbols:
                    return "Выражение невалидно: есть некорректный символ, например: {}".format(i)
                elif i in parenthesis:
                    # если найдена скобка, то считаем ее как +1 в parenthesisCount
                    parenthesisCount += 1
            if parenthesisCount % 2 != 0:
                # если количество скобок нечетное, то пример составлен некорректно
                return "Выражение невалидно: Количество скобок нечетное"
        except(ValueError,TypeError):
            # объявление ошибки при любых других случаях
            raise ValueError('Тип некорректен')
            
        return data
    def eval_math(formula):
        # объявление функций для основных вычислений
        OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
                '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}
        # сначала полученный пример обрабатывается в этой функции
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
        # далее из parse полученное значение передается в shunting_yard
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
        # в итоге полученные элементы обрарбатываются в calc
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
        # в этой переменной получаем результат
        respond = calc(shunting_yard(parse(formula)))
        # если ответ целое число, то убираем .0, иначе отправляем как есть 
        if respond.is_integer() == True:
            return int(respond)
        elif respond.is_integer() == False:
            return respond
