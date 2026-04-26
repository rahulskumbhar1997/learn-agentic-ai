from .base import Tool

class Calculator(Tool):

    @property
    def name(self):
        return "calculator"

    @property
    def description(self):
        return "Evaluate a mathematical expression. Support +,-,*,/,**"
    
    @property
    def parameters(self):
        return {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The math expression to evaluate, eg. '2 + 3 * 4"
                }
            },
            "required": ["expression"]
        }
    
    def execute(self, expression: str):
        
        allowed_vals = set('0123456789+-/*() ')
        for char in expression:
            if char not in allowed_vals:
                raise Exception(f"Expression has char {char} which is not supported.")
        
        result = eval(expression, {"__builtins__": {}}, {})
        print("Tool called")
        return str(result)