class Calculator:
    def __init__(self):
        self.operators = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }  # Supported operators
        self.precedence = {
            "+": 1,
            "-": 1,
            "*": 2,
            "/": 2,
        }  # Operator precedence, e.g., * is prioritized than +

    def evaluate(self, expression: str) -> float | None:
        """Evaluate the calculation expression.

        Expression should be separated by any whitespace, i.e., '3+5' will not work.
        """
        if not expression or expression.isspace():
            return None

        tokens = expression.strip().split()
        return self._evaluate_infix(tokens)

    def _evaluate_infix(self, tokens: list[str]) -> float:
        """Main evaluation based on given the "tokenized" expression.

        Works by keeping track of 2 stacks (operands and operators) where order matters.
        """
        values, operators = [], []
        for token in tokens:
            # Process operands by converting everything to float
            if token not in self.operators:
                try:
                    values.append(float(token))
                except ValueError:
                    raise ValueError(f"invalid token: {token}")
            # Process operators with Shunting Yard algorithm (precedence rule)
            else:
                while (
                    operators  # there are any in the stack
                    and operators[-1] in self.operators  # the top is a valid one
                    and self.precedence[operators[-1]]
                    >= self.precedence[token]  # top's precedence is greater than token's
                ):
                    self._apply_operator(operators, values)
                # If the rule above doesn't apply, push to stack
                operators.append(token)
        # Any remaining operator are applied in order
        while operators:
            self._apply_operator(operators, values)

        if len(values) != 1:
            raise ValueError("invalid expression")
        return values[0]

    def _apply_operator(self, operators: list[str], values: list[float]) -> None:
        """Applying calculation based on the mapped lambda function.

        The operator is applied by processing values[-2:] with operators[-1] and
        append its result back to values stack.
        """
        if not operators:
            return

        operator = operators.pop()
        if len(values) < 2:
            raise ValueError(f"not enough operands for operator {operator}")
        b = values.pop()
        a = values.pop()
        values.append(self.operators[operator](a, b))
