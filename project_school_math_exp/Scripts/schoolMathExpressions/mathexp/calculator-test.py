from unittest import TestCase, main
from .calculator import checkMathExp

class CalculatorTest(TestCase):
    def test_plus(self):
        self.assertEqual(checkMathExp.eval_math('2+2'), 4)
    
    def test_minus(self):
        self.assertEqual(checkMathExp.eval_math('7-2'), 5)
    
    def test_multi(self):
        self.assertEqual(checkMathExp.eval_math('7*2'), 14)
    def test_divide(self):
        self.assertEqual(checkMathExp.eval_math('7/2'), 3.5)
    def test_no_signs(self):
        with self.assertRaises(IndexError) as e:
            checkMathExp.eval_math('sdfgsfgf')
            self.assertEqual('В выражении присутствуют некорректные символы', e.exception.args[0])
    



if __name__ == '__main__':
    main()