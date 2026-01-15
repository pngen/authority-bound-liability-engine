from dataclasses import dataclass, field
from typing import Any, Optional
import time
import uuid

@dataclass(frozen=True)
class DecisionTrace:
    """An append-only record emitted at execution."""
    
    # Name of the action that was executed
    action_name: str
    
    # ID of the authority unit used
    authority_id: str
    
    # Timestamp when the action was executed
    timestamp: float
    
    # Result of the action (can be any serializable type)
    result: Any
    
    # Unique identifier for this trace
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        if not self.action_name:
            raise ValueError("Action name must be provided")
        if not self.authority_id:
            raise ValueError("Authority ID must be provided")

@dataclass(frozen=True)
class LiabilityRecord:
    """A deterministic mapping from DT to accountable parties and price."""
    
    # ID of the decision trace that generated this liability
    trace_id: str
    
    # ID of the authority unit used
    authority_id: str
    
    # Price paid for this action
    price: int
    
    # Scope of the authority used
    scope: str
    
    # Timestamp when the action was executed
    timestamp: float
    
    # Unique identifier for this liability record
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.trace_id:
            raise ValueError("Trace ID must be provided")
        if not self.authority_id:
            raise ValueError("Authority ID must be provided")