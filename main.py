from abc import ABC, abstractmethod


class Node(ABC):
    left = None
    right = None


class Operator(Node):
    precedence: int
    sign: str


class UnaryOperator(Operator):
    @abstractmethod
    def apply(self, a):
        raise NotImplementedError


class BinaryOperator(Operator):
    @abstractmethod
    def apply(self, a, b):
        raise NotImplementedError


class UnaryMinus(UnaryOperator):
    precedence = 0
    sign = "-"

    def apply(self, a):
        return a * (-1)


class Minus(BinaryOperator):
    precedence = 0
    sign = "-"

    def apply(self, a, b):
        return a - b


class Plus(BinaryOperator):
    precedence = 0
    sign = "+"

    def apply(self, a, b):
        return a + b


class Multiply(BinaryOperator):
    precedence = 1
    sign = "*"

    def apply(self, a, b):
        return a * b


class Divide(BinaryOperator):
    precedence = 1
    sign = "/"

    def apply(self, a, b):
        return a / b





