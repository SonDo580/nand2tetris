from constants import *


class CompilationEngine:
    def __init__(self, tokenizer, output_file):
        self._tokenizer = tokenizer
        self._output_file = output_file
        self._indent = 0  # indentation level

    def compile(self):
        """
        Start compiling the input file
        """
        self._tokenizer.advance()  # Get the first token
        self.__compileClass()

    def __outputXML(self):
        """
        Generate XML for current token
        """
        token = self._tokenizer.current_token()
        token_type = self._tokenizer.token_type()
        indentation = " " * 2 * self._indent
        self._output_file.write(
            f"{indentation}<{token_type}> {token} </{token_type}>\n"
        )

    def __outputTag(self, tagName, isOpen=True):
        """
        Generate XML for opening and closing tags.
        Also update indentation level.
        """
        if isOpen:
            indentation = " " * 2 * self._indent
            self._output_file.write(f"{indentation}<{tagName}>\n")
            self._indent += 1
        else:
            self._indent -= 1
            indentation = " " * 2 * self._indent
            self._output_file.write(f"{indentation}</{tagName}>\n")

    def __process(self, expected_token):
        """
        Handle current token, then advance to next token.
        """
        token = self._tokenizer.current_token()
        token_type = self._tokenizer.token_type()
        if token == expected_token and token_type in [SYMBOL, KEYWORD]:
            self.__outputXML()
        else:
            raise SyntaxError
        self._tokenizer.advance()

    def __compileClass(self):
        """
        Compile a class
        """
        self.__outputTag("class")
        self.__process("class")

        # className
        self.__outputXML()
        self._tokenizer.advance()

        self.__process("{")

        while self._tokenizer.current_token() in ["field", "static"]:
            self.__compileClassVarDec()

        while self._tokenizer.current_token() in ["constructor", "method", "function"]:
            self.__compileSubroutine()

        self.__process("}")
        self.__outputTag("class", False)

    def __compileClassVarDec(self):
        """
        Compile a static variable declaration or a field declaration
        """
        self.__outputTag("classVarDec")
        self.__process(self._tokenizer.current_token())  # field / static

        while self._tokenizer.current_token() != ";":
            self.__outputXML()
            self._tokenizer.advance()

        self.__process(";")
        self.__outputTag("classVarDec", False)

    def __compileSubroutine(self):
        """
        Compile a method, function or constructor
        """
        self.__outputTag("subroutineDec")
        self.__process(
            self._tokenizer.current_token()
        )  # constructor / method / function

        while self._tokenizer.current_token() != "(":
            self.__outputXML()
            self._tokenizer.advance()

        self.__process("(")
        self.__compileParameterList()
        self.__process(")")

        self.__compileSubroutineBody()
        self.__outputTag("subroutineDec", False)

    def __compileParameterList(self):
        """
        Compile a (possibly empty) parameter list. Not handle '(' and ')'
        """
        self.__outputTag("parameterList")

        while self._tokenizer.current_token() != ")":
            self.__outputXML()
            self._tokenizer.advance()

        self.__outputTag("parameterList", False)

    def __compileSubroutineBody(self):
        """
        Compile a subroutine body
        """
        self.__outputTag("subroutineBody")
        self.__process("{")

        while self._tokenizer.current_token() == "var":
            self.__compileVarDec()

        self.__compileStatements()

        self.__process("}")
        self.__outputTag("subroutineBody", False)

    def __compileVarDec(self):
        """
        Compile a var declaration
        """
        self.__outputTag("varDec")
        self.__process("var")

        while self._tokenizer.current_token() != ";":
            self.__outputXML()
            self._tokenizer.advance()

        self.__process(";")
        self.__outputTag("varDec", False)

    def __compileStatements(self):
        """
        Compile a sequence of statements. Not handle '{' and '}'
        """
        self.__outputTag("statements")

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

        self.__outputTag("statements", False)

    def __compileLet(self):
        """
        Compile a 'let' statement
        """
        self.__outputTag("letStatement")
        self.__process("let")

        self.__outputXML()
        self._tokenizer.advance()

        if self._tokenizer.current_token() == "[":
            self.__compileArrayAccess()

        self.__process("=")
        self.__compileExpression()

        self.__process(";")
        self.__outputTag("letStatement", False)

    def __compileIf(self):
        """
        Compile an 'if' statement, possibly with a trailing 'else' clause
        """
        self.__outputTag("ifStatement")

        self.__process("if")
        self.__process("(")
        self.__compileExpression()
        self.__process(")")
        self.__process("{")
        self.__compileStatements()
        self.__process("}")

        if self._tokenizer.current_token() == "else":
            self.__process("else")
            self.__process("{")
            self.__compileStatements()
            self.__process("}")

        self.__outputTag("ifStatement", False)

    def __compileWhile(self):
        """
        Compile a 'while' statement
        """
        self.__outputTag("whileStatement")
        self.__process("while")
        self.__process("(")
        self.__compileExpression()
        self.__process(")")
        self.__process("{")
        self.__compileStatements()
        self.__process("}")
        self.__outputTag("whileStatement", False)

    def __compileDo(self):
        """
        Compile a 'do' statement
        """
        self.__outputTag("doStatement")
        self.__process("do")

        self.__outputXML()
        self._tokenizer.advance()
        self.__compileSubroutineCall()

        self.__process(";")
        self.__outputTag("doStatement", False)

    def __compileSubroutineCall(self):
        """
        Compile a subroutine call: func() / obj.func() / Class.func()
        Handle calling part: .func() / func()
        """
        if self._tokenizer.current_token() == ".":
            self.__process(".")
            self.__outputXML()
            self._tokenizer.advance()

        self.__process("(")
        self.__compileExpressionList()
        self.__process(")")

    def __compileReturn(self):
        """
        Compile a 'return' statement
        """
        self.__outputTag("returnStatement")
        self.__process("return")

        if self._tokenizer.current_token() != ";":
            self.__compileExpression()

        self.__process(";")
        self.__outputTag("returnStatement", False)

    def __compileArrayAccess(self):
        """
        Compile array access: arr[expression]
        Handle indexing part: [expression]
        """
        self.__process("[")
        self.__compileExpression()
        self.__process("]")

    def __compileExpression(self):
        """
        Compile an expression
        """
        self.__outputTag("expression")
        self.__compileTerm()

        while self._tokenizer.current_token() in BINARY_OPS:
            self.__process(self._tokenizer.current_token())
            self.__compileTerm()

        self.__outputTag("expression", False)

    def __compileTerm(self):
        """
        Compile a term
        """
        self.__outputTag("term")
        token = self._tokenizer.current_token()

        # Handle group
        if token == "(":
            self.__process("(")
            self.__compileExpression()
            self.__process(")")

        # Handle unary op
        elif token in UNARY_OPS:
            self.__process(token)
            self.__compileTerm()

        else:
            # Other term types
            self.__outputXML()
            self._tokenizer.advance()

            token = self._tokenizer.current_token()
            if token == "[":
                # Handle array access
                self.__compileArrayAccess()
            elif token in [".", "("]:
                # Handle subroutine call
                self.__compileSubroutineCall()

        self.__outputTag("term", False)

    def __compileExpressionList(self):
        """
        Compile a (possibly empty) comma-separated list of expression.
        Return the number of expressions in the list.
        """
        count_expression = 0
        self.__outputTag("expressionList")

        while self._tokenizer.current_token() != ")":
            self.__compileExpression()
            count_expression += 1

            if self._tokenizer.current_token() == ",":
                self.__process(",")

        self.__outputTag("expressionList", False)
        return count_expression
