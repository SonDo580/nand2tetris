# Token types
KEYWORD = "keyword"
SYMBOL = "symbol"
IDENTIFIER = "identifier"
INT_CONST = "integerConstant"
STR_CONST = "stringConstant"

# Escaped symbols
ESCAPED = {"<": "&lt;", ">": "&gt;", '"': "&quot;", "&": "&amp;"}

# All Jack keywords
KEYWORDS = {
    "class",
    "constructor",
    "function",
    "method",
    "field",
    "static",
    "var",
    "int",
    "char",
    "boolean",
    "void",
    "true",
    "false",
    "null",
    "this",
    "let",
    "do",
    "if",
    "else",
    "while",
    "return",
}

# All Jack symbols
SYMBOLS = {
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    ".",
    ",",
    ";",
    "+",
    "-",
    "*",
    "/",
    "&",
    "|",
    "<",
    ">",
    "=",
    "~",
}

KEYWORD_CONSTANTS = {"true", "false", "null", "this"}

# Unary operators
UNARY_OPS = {"-", "~"}

# Binary operators
BINARY_OPS = {
    "+",
    "-",
    "*",
    "/",
    ESCAPED["&"],
    "|",
    ESCAPED["<"],
    ESCAPED[">"],
    "=",
}

# OS Classes
OS_CLASSES = {
    "Math",
    "Memory",
    "Screen",
    "Output",
    "Keyboard",
    "String",
    "Array",
    "Sys",
}

# Variable kinds
FIELD = "field"
STATIC = "static"
ARG = "argument"
VAR = "local"

# VM virtual segments
CONSTANT = "constant"
ARGUMENT = "argument"
LOCAL = "local"
STATIC = "static"
THIS = "this"
THAT = "that"
POINTER = "pointer"
TEMP = "temp"

# VM commands
ADD = "add"
SUB = "sub"
NEG = "neg"
EQ = "eq"
GT = "gt"
LT = "lt"
AND = "and"
OR = "or"
NOT = "not"

# Unary operator to VM command
UNARY_COMMAND = {"-": NEG, "~": NOT}

# Binary operator to VM command
BINARY_COMMAND = {
    "+": ADD,
    "-": SUB,
    "=": EQ,
    ESCAPED[">"]: GT,
    ESCAPED["<"]: LT,
    ESCAPED["&"]: AND,
    "|": OR,
}
