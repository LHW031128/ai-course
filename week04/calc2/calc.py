import ast
import operator

class SafeCalculator(ast.NodeVisitor):
    def __init__(self):
        self.operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = type(node.op)
        if op_type == ast.Div and right == 0:
            raise ZeroDivisionError("0으로 날눌 수 없습니다.")
        if op_type in self.operators:
            return self.operators[op_type](left, right)
        raise ValueError(f"지원하지 않는 연산자입니다: {op_type}")

    def visit_UnaryOp(self, node):
        operand = self.visit(node.operand)
        op_type = type(node.op)
        if op_type in self.operators:
            return self.operators[op_type](operand)
        raise ValueError(f"지원하지 않는 단항 연산자입니다: {op_type}")

    def visit_Constant(self, node):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f"숫자가 아닙니다: {node.value}")

    def generic_visit(self, node):
        raise ValueError(f"지원하지 않는 수식 구조입니다: {type(node).__name__}")

def calculate(expression: str):
    if not expression or not isinstance(expression, str) or not expression.strip():
        raise ValueError("수식이 비어있거나 잘못되었습니다.")
    try:
        tree = ast.parse(expression, mode='eval')
        calc = SafeCalculator()
        return calc.visit(tree.body)
    except ZeroDivisionError as e:
        raise e
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"잘못된 수식입니다: {e}")
    except Exception as e:
        raise ValueError(f"잘못된 수식입니다: {e}")