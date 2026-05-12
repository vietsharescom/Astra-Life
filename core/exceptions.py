# core/exceptions.py

class ContractViolationError(RuntimeError):
    """Raised when a module execution violates its declared contract."""
    pass