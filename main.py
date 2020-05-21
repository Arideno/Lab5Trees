from abc import ABC, abstractmethod


class Node(ABC):
    left = None
    right = None


class Operator(Node):
    precedence: int
    sign: str

    def __le__(self, other):
        if isinstance(other, Operator):
            return self.precedence <= other.precedence
        else:
            raise ArithmeticError


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


class Number(Node):
    def __init__(self, value: float):
        self.value = value


class Variable(Node):
    def __init__(self, value: str):
        self.value = value


class ListNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    def __init__(self, m):
        self.__m = m
        self.__table = [None] * m

    def __hash(self, key):
        return hash(key) % self.__m

    def __setitem__(self, key, value):
        index = self.__hash(key)
        if self.__table[index] is None:
            self.__table[index] = ListNode(key, value)
        else:
            head = self.__table[index]
            while head.next is not None:
                if head.key == key:
                    head.value = value
                    return
                head = head.next
            if head.key == key:
                head.value = value
                return
            head.next = ListNode(key, value)

    def __getitem__(self, key):
        index = self.__hash(key)
        if self.__table[index] is None:
            return None
        head = self.__table[index]
        while head is not None:
            if head.key == key:
                return head.value
            head = head.next
        return None


class Stack:
    __stack = []

    def __len__(self):
        return len(self.__stack)

    def push(self, value):
        self.__stack.append(value)

    def pop(self):
        assert len(self) > 0
        return self.__stack.pop()

    def top(self):
        assert len(self) > 0
        return self.__stack[-1]

    def empty(self):
        return len(self) == 0


def is_operator(sign):
    return sign in ['+', '-', '*', '/', '(', ')']


def get_operator(sign, binary=True):
    if sign == '+':
        return Plus()
    if sign == '-':
        if binary:
            return Minus()
        else:
            return UnaryMinus()
    if sign == '*':
        return Multiply()
    if sign == '/':
        return Divide()
    raise ArithmeticError


def parse(input_str: str):
    op_stack = Stack()
    tree_stack = Stack()
    i = 0
    while i < len(input_str):
        if not is_operator(input_str[i]):
            j = i + 1
            while j < len(input_str) and not is_operator(input_str[j]):
                j += 1
            value = input_str[i:j]
            if value.isnumeric():
                tree_stack.push(Number(float(value)))
            else:
                tree_stack.push(Variable(value))
