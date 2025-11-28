class VM:
    def __init__(self):
        self.stack = []
        self.variables = {}
        self.functions = {}

    def execute(self, ast):
        for node in ast:
            self.execute_node(node)

    def execute_node(self, node):
        if isinstance(node, Number):
            self.stack.append(node.value)
        elif isinstance(node, String):
            self.stack.append(node.value)
        elif isinstance(node, Variable):
            self.stack.append(self.variables.get(node.name, None))
        elif isinstance(node, Assign):
            value = self.execute_node(node.expr)
            self.variables[node.var] = value
        elif isinstance(node, BinOp):
            left = self.execute_node(node.left)
            right = self.execute_node(node.right)
            if node.op == '+':
                self.stack.append(left + right)
            elif node.op == '-':
                self.stack.append(left - right)
            elif node.op == '*':
                self.stack.append(left * right)
            elif node.op == '/':
                self.stack.append(left / right)
        elif isinstance(node, If):
            condition = self.execute_node(node.condition)
            if condition:
                for stmt in node.then_branch:
                    self.execute_node(stmt)
            elif node.else_branch:
                for stmt in node.else_branch:
                    self.execute_node(stmt)
        elif isinstance(node, While):
            while self.execute_node(node.condition):
                for stmt in node.body:
                    self.execute_node(stmt)
        elif isinstance(node, FunctionDef):
            self.functions[node.name] = node
        elif isinstance(node, FunctionCall):
            func = self.functions.get(node.name, None)
            if func:
                for arg in node.args:
                    self.execute_node(arg)
                args = []
                for _ in range(len(func.args)):
                    args.insert(0, self.stack.pop())
                for i, arg in enumerate(args):
                    self.variables[func.args[i]] = arg
                for stmt in func.body:
                    self.execute_node(stmt)