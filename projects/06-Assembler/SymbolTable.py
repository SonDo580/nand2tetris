class SymbolTable:
    """Handle symbols."""

    def __init__(self):
        # Add predefined symbols
        self._table: dict[str, int] = {
            "SCREEN": 16384,
            "KBD": 24576,
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
        }
        for i in range(16):
            self._table[f"R{str(i)}"] = i

    def addEntry(self, symbol: str, address: int):
        """Add (symbol, address) to the table."""
        self._table[symbol] = address

    def contains(self, symbol: str) -> bool:
        """Return true if symbol exists in table."""
        return symbol in self._table

    def getAddress(self, symbol: str) -> int:
        """Return the address associated with symbol."""
        return self._table[symbol]
