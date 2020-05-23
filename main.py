from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self):
        self.children = []


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


class Assign(BinaryOperator):
    precedence = 1
    sign = "="

    def apply(self, a, b):
        return a, b


class Number(Node):
    def __init__(self, value: float):
        super().__init__()
        self.value = value


class Variable(Node):
    def __init__(self, value: str):
        super().__init__()
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
    def __init__(self):
        self.__stack = []

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


op_stack = Stack()
tree_stack = Stack()


def pop_operator():
    op = op_stack.pop()
    if isinstance(op, UnaryOperator):
        node = tree_stack.pop()
        op.children.append(node)
        tree_stack.push(op)
    elif isinstance(op, BinaryOperator):
        r = tree_stack.pop()
        l = tree_stack.pop()
        if isinstance(l, Number) and l.value == 0:
            if isinstance(op, Divide):
                tree_stack.push(Number(0))
                return
            elif isinstance(op, Plus):
                tree_stack.push(r)
                return
            elif isinstance(op, Multiply):
                tree_stack.push(Number(0))
                return
        elif isinstance(r, Number) and r.value == 0:
            if isinstance(op, Plus) or isinstance(op, Minus):
                tree_stack.push(l)
                return
            elif isinstance(op, Multiply):
                tree_stack.push(Number(0))
                return
        elif isinstance(r, Number) and r.value == 1:
            if isinstance(op, Divide) or isinstance(op, Multiply):
                tree_stack.push(l)
                return
        elif isinstance(l, Number) and l.value == 1:
            if isinstance(op, Multiply):
                tree_stack.push(r)
                return

        op.children.append(l)
        op.children.append(r)
        tree_stack.push(op)


def parse(input_str: str):
    i = 0
    while i < len(input_str):
        if not is_operator(input_str[i]):
            j = i + 1
            while j < len(input_str) and not is_operator(input_str[j]):
                j += 1
            value = input_str[i:j]
            i = j
            if value.isnumeric():
                tree_stack.push(Number(float(value)))
            else:
                tree_stack.push(Variable(value))
        else:
            if input_str[i] == '(':
                op_stack.push('(')
            elif input_str[i] == ')':
                while op_stack.top() != '(':
                    pop_operator()
                op_stack.pop()
            else:
                if input_str[i] == '-' and (i == 0 or input_str[i - 1] == '('):
                    op_stack.push(get_operator('-', False))
                else:
                    op = get_operator(input_str[i])
                    while not op_stack.empty() and op_stack.top() != '(' and op <= op_stack.top():
                        pop_operator()
                    op_stack.push(op)
            i += 1

    while not op_stack.empty():
        pop_operator()

    return tree_stack.pop()


table = HashTable(20)

root = Node()


def calc(node: Node):
    if isinstance(node, Assign):
        a, b = node.apply(*node.children)
        table[a.value] = calc(b)
    elif isinstance(node, Number):
        return node.value
    elif isinstance(node, Variable):
        return table[node.value]
    elif isinstance(node, UnaryOperator):
        return node.apply(calc(node.children[0]))
    elif isinstance(node, BinaryOperator):
        return node.apply(calc(node.children[0]), calc(node.children[1]))
    else:
        for child in node.children:
            if not isinstance(child, Assign):
                return calc(child)
            else:
                calc(child)


with open('input.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if '=' in line:
            k, v = line.split("=")
            node = Assign()
            node.children.append(Variable(k))
            node.children.append(parse(v.rstrip()))
            root.children.append(node)
        elif '>' in line:
            k = line[1:].rstrip()
            v = (input(f"{k} = "))
            node = Assign()
            node.children.append(Variable(k))
            node.children.append(parse(v))
            root.children.append(node)
        else:
            root.children.append(parse(line.rstrip()))


print(calc(root))
