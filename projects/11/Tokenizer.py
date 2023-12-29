import re

from constants import *


class Tokenizer:
    def __init__(self, file):
        self._file = file  # input file stream
        self._token = None  # current token
        self._token_type = None  # current token type

        self._line = None  # current line of code
        self._num_chars = 0  # Number of characters in 'line'
        self._char_index = 0  # current character index in 'line'

    def __processed_line(self):
        """
        Return a 'pure' line of code
        """
        line = self._file.readline()
        # Check end of the file
        if line == "":
            return None

        # Remove whitespaces at 2 ends and inline comments
        line = line.strip()
        indexComment = line.find("//")
        if indexComment != -1:
            line = line[:indexComment].rstrip()
        return line

    def __next_line(self):
        """
        Set the next line of code
        """
        line = ""
        # Ignore empty lines and comments
        while line == "" or line.startswith("//") or line.startswith("/**"):
            if line.startswith("/**"):
                while not line.endswith("*/"):
                    line = self.__processed_line()
            line = self.__processed_line()
            if line is None:
                break

        # Set current line of code and reset char_index
        self._line = line
        self._num_chars = 0 if self._line is None else len(line)
        self._char_index = 0

    def advance(self):
        """
        Set current token to the next token from the input.
        Assign token type to current token.
        """
        # Read the next line of code when reach end of line
        if self._char_index == self._num_chars:
            self.__next_line()

        # Reached end of file
        if self._line is None:
            self._token = None
            return

        # Get the current character
        char = self._line[self._char_index]

        # Advance to the next non-space character
        while char == " ":
            self._char_index += 1
            char = self._line[self._char_index]

        if char in SYMBOLS:
            # Check if char is a SYMBOL
            self._token = ESCAPED[char] if char in ESCAPED else char
            self._token_type = SYMBOL
            self._char_index += 1

        elif char == '"':
            # Check for string constant. Multi-line strings are not allowed
            token = '"'
            self._char_index += 1
            char = self._line[self._char_index]
            while char != '"':
                token += char
                self._char_index += 1
                char = self._line[self._char_index]

            token += '"'
            self._token = token
            self._token_type = STR_CONST
            self._char_index += 1

        else:
            token = ""
            # Keep adding characters to current token
            while char != " " and char not in SYMBOLS:
                token += char
                self._char_index += 1
                if self._char_index == self._num_chars:
                    # Stop when reach end of line
                    break
                char = self._line[self._char_index]

            self._token = token
            # Assign token type
            if self._token in KEYWORDS:
                self._token_type = KEYWORD
            elif re.match("^[A-Za-z_]\w*$", self._token):
                self._token_type = IDENTIFIER
            elif re.match("^\d+$", self._token):
                self._token_type = INT_CONST

    def current_token(self):
        """
        Return the current token
        """
        if self._token is None:
            return None
        if self._token_type == STR_CONST:
            return self._token[1:-1]  # Remove the quotes
        return self._token

    def token_type(self):
        """
        Return the type of the current token
        """
        return self._token_type
