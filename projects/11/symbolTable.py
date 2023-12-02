from constants import *


class SymbolTable:
    def __init__(self):
        self._class_symbols = {}
        self._subroutine_symbols = {}
        self._index = {FIELD: 0, STATIC: 0, ARG: 0, VAR: 0}

    def reset(self):
        """
        Reset the subroutine symbol table and running indexes.
        Should be called when starting a subroutine.
        """
        self._subroutine_symbols = {}
        self._index[ARG] = 0
        self._index[VAR] = 0

    def define(self, name, type, kind):
        """
        Add a new variable to the symbol table
        """
        symbol = {"type": type, "kind": kind, "index": self._index[kind]}
        if kind in [FIELD, STATIC]:
            self._class_symbols[name] = symbol
        elif kind in [ARG, VAR]:
            self._subroutine_symbols[name] = symbol
        else:
            raise SyntaxError
        self._index[kind] += 1

    def __property(self, name, prop):
        """
        Return a property (kind / type / index) of the identifier.
        Return None if the identifier is not found.
        """
        if name in self._subroutine_symbols:
            return self._subroutine_symbols[name][prop]
        if name in self._class_symbols:
            return self._class_symbols[name][prop]
        return None

    def kind(self, name):
        return self.__property(name, "kind")

    def type(self, name):
        return self.__property(name, "type")

    def index(self, name):
        return self.__property(name, "index")

    def var_count(self, kind):
        """
        Return the number of variables of the given kind
        """
        return self._index[kind] + 1
