"""Midea Smart Home Expression Evaluator."""

import logging
import re
import ast
from typing import Union, Any, Optional

_LOGGER = logging.getLogger(__name__)

class ExpressionEvaluator:
    """Evaluates expressions and applies calculations to device data."""

    def __init__(self, calculate_config: Optional[dict] = None):
        self.calculate_config = calculate_config or {}

    def evaluate_expression(self, expression: str, data: dict) -> Union[str, int, float, bool, None]:
        """Evaluate a string expression using data variables."""
        def replace_var(match):
            var_name = match.group(1)
            if var_name in data:
                return str(data[var_name])
            return "0"

        if re.fullmatch(r'\[[a-zA-Z_][a-zA-Z0-9_]*\]', expression):
            var_name = expression[1:-1]
            return data.get(var_name)

        result_expr = re.sub(r'\[([a-zA-Z_][a-zA-Z0-9_]*)\]', replace_var, expression)

        preserve_functions = ['float', 'int', 'str', 'bool']
        result_expr = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b',
                           lambda m: str(data[m.group(1)]) if m.group(1) in data and m.group(1) not in preserve_functions else m.group(1),
                           result_expr)

        dangerous_patterns = ['__', 'import', 'exec', 'eval', 'compile', 'open', 'file', 'input']
        for pattern in dangerous_patterns:
            if pattern in result_expr.lower():
                _LOGGER.warning("Dangerous pattern '%s' detected in expression: %s", pattern, expression)
                return None

        try:
            allowed_names = {"float": float, "int": int, "str": str, "abs": abs, "round": round, "min": min, "max": max}
            node = ast.parse(result_expr, mode='eval')

            for node_type in ast.walk(node):
                if isinstance(node_type, (ast.Call, ast.Attribute, ast.Subscript)):
                    if isinstance(node_type, ast.Attribute):
                        if node_type.attr.startswith('_'):
                            _LOGGER.warning("Access to private attribute '%s' denied", node_type.attr)
                            return None

            return eval(compile(node, '<string>', 'eval'), {"__builtins__": {}}, allowed_names)
        except (SyntaxError, ValueError, TypeError, NameError, AttributeError) as e:
            _LOGGER.warning("Failed to evaluate expression '%s': %s", expression, e)
            return None

    def apply_calculations(self, data: dict) -> dict:
        """Apply configured calculations to the data."""
        if not data:
            return data

        get_calculations = self.calculate_config.get("get", [])
        for calc in get_calculations:
            lvalue = calc.get("lvalue")
            rvalue = calc.get("rvalue")
            if lvalue and rvalue:
                result = self.evaluate_expression(rvalue, data)
                if result is not None:
                    if lvalue.startswith('[') and lvalue.endswith(']'):
                        actual_lvalue = lvalue[1:-1]
                    else:
                        actual_lvalue = lvalue
                    data[actual_lvalue] = result

        return data
