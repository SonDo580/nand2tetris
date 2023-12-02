from constants import *
from tokenizer import Tokenizer
from symbolTable import SymbolTable
from vmWriter import VMWriter


class CompileEngine:
    def __init__(self, input_file, output_file):
        self._tokenizer = Tokenizer(input_file)
        self._writer = VMWriter(output_file)
        self._symbols = SymbolTable()

        self._class_name = None  # current class name
        self._func_name = None  # current subroutine name
        self._label_index = 0  # current label index
        # current subroutine kind: constructor / method/ function
        self._func_kind = None

    def compile(self):
        """
        Start compiling the input file
        """
        self._tokenizer.advance()  # Get the first token
        self.__compileClass()

    def __process(self, expected_token):
        """
        Handle current token, then advance to next token.
        """
        token = self._tokenizer.current_token()
        token_type = self._tokenizer.token_type()
        if token == expected_token and token_type in [SYMBOL, KEYWORD]:
            self._tokenizer.advance()
        else:
            raise SyntaxError

    def __compileClass(self):
        """
        Compile a class
        """
        self.__process("class")
        self._class_name = self._tokenizer.current_token()
        self._tokenizer.advance()
        self.__process("{")

        while self._tokenizer.current_token() in ["field", "static"]:
            self.__compileClassVarDec()

        while self._tokenizer.current_token() in ["constructor", "method", "function"]:
            self.__compileSubroutine()

        self.__process("}")

    def __compileClassVarDec(self):
        """
        Compile a static variable declaration or a field declaration
        """
        var_kind = self._tokenizer.current_token()  # field / static
        self.__process(var_kind)

        var_type = self._tokenizer.current_token()
        self._tokenizer.advance()

        while self._tokenizer.current_token() != ";":
            var_name = self._tokenizer.current_token()
            self._symbols.define(var_name, var_type, var_kind)
            self._tokenizer.advance()

            if self._tokenizer.current_token() == ",":
                self.__process(",")

        self.__process(";")

    def __compileSubroutine(self):
        """
        Compile a method, function or constructor
        """
        # Reset symbol table and label index
        self._symbols.reset()
        self._label_index = 0

        self._func_kind = self._tokenizer.current_token()
        if self._func_kind == "method":
            # Add 'this' as argument 0 to symbol table
            self._symbols.define("this", self._class_name, ARG)

        self.__process(self._func_kind)
        self._tokenizer.advance()  # subroutine return type

        self._func_name = self._tokenizer.current_token()  # subroutine name
        self._tokenizer.advance()

        self.__process("(")
        self.__compileParameterList()
        self.__process(")")

        self.__compileSubroutineBody()

    def __compileParameterList(self):
        """
        Compile a (possibly empty) parameter list. Not handle '(' and ')'
        """
        var_kind = ARG

        while self._tokenizer.current_token() != ")":
            var_type = self._tokenizer.current_token()
            self._tokenizer.advance()

            var_name = self._tokenizer.current_token()
            self._tokenizer.advance()

            self._symbols.define(var_name, var_type, var_kind)

            if self._tokenizer.current_token() == ",":
                self.__process(",")

    def __compileSubroutineBody(self):
        """
        Compile a subroutine body
        """
        self.__process("{")
        while self._tokenizer.current_token() == "var":
            self.__compileVarDec()

        # Write VM function after process all local variable declarations
        func = f"{self._class_name}.{self._func_name}"
        num_vars = self._symbols.var_count(VAR)
        self._writer.writeFunction(func, num_vars)

        if self._func_kind == "constructor":
            # Allocate a block of free memory
            # Then set THIS to the base address
            num_fields = self._symbols.var_count(FIELD)
            self._writer.writePush(CONSTANT, num_fields)
            self._writer.writeCall("Memory.alloc", 1)
            self._writer.writePop(POINTER, 0)

        elif self._func_kind == "method":
            # Set THIS to argument 0
            self._writer.writePush(ARGUMENT, 0)
            self._writer.writePop(POINTER, 0)

        self.__compileStatements()
        self.__process("}")

    def __compileVarDec(self):
        """
        Compile a var declaration
        """
        self.__process("var")
        var_kind = VAR

        var_type = self._tokenizer.current_token()
        self._tokenizer.advance()

        while self._tokenizer.current_token() != ";":
            var_name = self._tokenizer.current_token()
            self._symbols.define(var_name, var_type, var_kind)
            self._tokenizer.advance()

            if self._tokenizer.current_token() == ",":
                self.__process(",")

        self.__process(";")

    def __compileStatements(self):
        """
        Compile a sequence of statements. Not handle '{' and '}'
        """
        while True:
            token = self._tokenizer.current_token()
            if token == "let":
                self.__compileLet()
            elif token == "if":
                self.__compileIf()
            elif token == "while":
                self.__compileWhile()
            elif token == "do":
                self.__compileDo()
            elif token == "return":
                self.__compileReturn()
            else:
                break

    def __get_segment(self, kind):
        if kind == STATIC:
            return STATIC
        if kind == FIELD:
            return THIS
        if kind == ARG:
            return ARGUMENT
        if kind == VAR:
            return LOCAL
        return SyntaxError

    def __compileLet(self):
        """
        Compile a 'let' statement
        """
        self.__process("let")

        var_name = self._tokenizer.current_token()
        var_kind = self._symbols.kind(var_name)
        var_index = self._symbols.index(var_name)
        segment = self.__get_segment(var_kind)

        self._tokenizer.advance()
        if self._tokenizer.current_token() == "[":
            # Handle array access: let arr[expression1] = expression2
            self._writer.writePush(segment, var_index)
            self.__process("[")
            self.__compileExpression()
            self.__process("]")
            self._writer.writeArithmetic(ADD)
            # current top stack: arr[expression1] address

            self.__process("=")
            self.__compileExpression()
            # current top stack: expression2

            self._writer.writePop(TEMP, 0)  # save expression2 to temp0
            self._writer.writePop(POINTER, 1)  # set THAT = arr[expression1] address
            self._writer.writePush(TEMP, 0)
            self._writer.writePop(THAT, 0)  # set arr[expression1] = expression2

        else:
            self.__process("=")
            self.__compileExpression()
            self._writer.writePop(segment, var_index)

        self.__process(";")

    def __get_label(self):
        """
        Generate a label (for compileIf and compileWhile).
        Increment the label index.
        """
        label = f"{self._func_name}{self._label_index}"
        self._label_index += 1
        return label

    def __compileIf(self):
        """
        Compile an 'if' statement, possibly with a trailing 'else' clause
        """
        self.__process("if")
        self.__process("(")
        self.__compileExpression()
        self.__process(")")

        self._writer.writeArithmetic(NOT)
        label1 = self.__get_label()
        self._writer.writeIf(label1)

        self.__process("{")
        self.__compileStatements()
        self.__process("}")

        if self._tokenizer.current_token() == "else":
            label2 = self.__get_label()
            self._writer.writeGoto(label2)

            self._writer.writeLabel(label1)
            self.__process("else")
            self.__process("{")
            self.__compileStatements()
            self.__process("}")

            self._writer.writeLabel(label2)
        else:
            self._writer.writeLabel(label1)

    def __compileWhile(self):
        """
        Compile a 'while' statement
        """
        label1 = self.__get_label()
        label2 = self.__get_label()

        self._writer.writeLabel(label1)

        self.__process("while")
        self.__process("(")
        self.__compileExpression()
        self.__process(")")

        self._writer.writeArithmetic(NOT)
        self._writer.writeIf(label2)

        self.__process("{")
        self.__compileStatements()
        self.__process("}")

        self._writer.writeGoto(label1)
        self._writer.writeLabel(label2)

    def __compileDo(self):
        """
        Compile a 'do' statement
        """
        self.__process("do")
        self.__compileExpression()
        self._writer.writePop(TEMP, 0)  # get rid of the dummy value
        self.__process(";")

    def __compileReturn(self):
        """
        Compile a 'return' statement
        """
        self.__process("return")
        if self._tokenizer.current_token() != ";":
            self.__compileExpression()
        else:
            # push a dummy value, will be tossed away by compileDo
            self._writer.writePush(CONSTANT, 0)
        self._writer.writeReturn()
        self.__process(";")

    def __output_operator(self, operator):
        if operator in BINARY_COMMAND:
            self._writer.writeArithmetic(BINARY_COMMAND[operator])
        elif operator == "*":
            self._writer.writeCall("Math.multiply", 2)
        elif operator == "/":
            self._writer.writeCall("Math.divide", 2)

    def __compileExpression(self):
        """
        Compile an expression
        """
        self.__compileTerm()
        while self._tokenizer.current_token() in BINARY_OPS:
            operator = self._tokenizer.current_token()
            self.__process(operator)
            self.__compileTerm()
            self.__output_operator(operator)

    def __compileTerm(self):
        """
        Compile a term
        """
        token = self._tokenizer.current_token()

        # Handle group
        if token == "(":
            self.__process("(")
            self.__compileExpression()
            self.__process(")")
            return

        # Handle unary op
        if token in UNARY_OPS:
            self.__process(token)
            self.__compileTerm()
            self._writer.writeArithmetic(UNARY_COMMAND[token])
            return

        # Handle integer constant
        token_type = self._tokenizer.token_type()
        if token_type == INT_CONST:
            self._writer.writePush(CONSTANT, token)
            self._tokenizer.advance()
            return

        # Handle keyword constant
        if token_type == KEYWORD and token in KEYWORD_CONSTANTS:
            if token == "true":
                self._writer.writePush(CONSTANT, 1)
                self._writer.writeArithmetic(NEG)
            elif token in {"false", "null"}:
                self._writer.writePush(CONSTANT, 0)
            elif token == "this":
                self._writer.writePush(POINTER, 0)
            self._tokenizer.advance()
            return

        # Handle string constant
        if token_type == STR_CONST:
            str_len = len(token)
            self._writer.writePush(CONSTANT, str_len)
            self._writer.writeCall("String.new", 1)

            # Keep adding characters to the string
            for c in token:
                self._writer.writePush(CONSTANT, ord(c))
                self._writer.writeCall("String.appendChar", 2)

            self._tokenizer.advance()
            return

        var_kind = self._symbols.kind(token)
        if var_kind is not None:
            # If token is a variable
            var_index = self._symbols.index(token)
            segment = self.__get_segment(var_kind)
            self._writer.writePush(segment, var_index)

            # var_type will be a ClassName for object variable.
            # used for method call: obj.func()
            var_type = self._symbols.type(token)

            # Advance to the next token
            self._tokenizer.advance()
            token = self._tokenizer.current_token()

            # Handle array access
            if token == "[":
                self.__process("[")
                self.__compileExpression()
                self.__process("]")

                self._writer.writeArithmetic(ADD)
                self._writer.writePop(POINTER, 1)
                self._writer.writePush(THAT, 0)
                return

            # Handle method call: obj.func()
            elif token == ".":
                self.__process(".")
                func = f"{var_type}.{self._tokenizer.current_token()}"
                self._tokenizer.advance()

                self.__process("(")
                # argument 0 is obj
                num_vars = 1 + self.__compileExpressionList()
                self.__process(")")
                self._writer.writeCall(func, num_vars)

        else:
            # Variable not found =>
            # 1) method call in the same class: func()
            # 2) constructor / function call: Class.func()
            prev_token = token
            num_vars = 0

            # Examine the next token
            self._tokenizer.advance()
            token = self._tokenizer.current_token()

            if token == ".":
                # constructor / function call: Class.func()
                self.__process(".")
                func = f"{prev_token}.{self._tokenizer.current_token()}"
                self._tokenizer.advance()

            elif token == "(":
                # method call in the same class: func()
                func = f"{self._class_name}.{prev_token}"
                # push current THIS as argument 0
                self._writer.writePush(POINTER, 0)
                num_vars += 1

            self.__process("(")
            num_vars += self.__compileExpressionList()
            self.__process(")")
            self._writer.writeCall(func, num_vars)

    def __compileExpressionList(self):
        """
        Compile a (possibly empty) comma-separated list of expression.
        Return the number of expressions in the list.
        """
        count_expression = 0

        while self._tokenizer.current_token() != ")":
            self.__compileExpression()
            count_expression += 1

            if self._tokenizer.current_token() == ",":
                self.__process(",")

        return count_expression
