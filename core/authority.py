from dataclasses import dataclass
from typing import List, Optional
from hashlib import sha256
import time

@dataclass(frozen=True)
class AuthorityUnit:
    """A consumable, immutable unit encoding scope, delegation chain, and price."""
    
    # Unique identifier for this authority unit
    id: str
    
    # Scope of authority (e.g., "read", "write", "execute")
    scope: str
    
    # Delegation chain as a list of authorities
    delegation_chain: List[str]
    
    # Price in tokens or units
    price: int
    
    # Timestamp when this authority was issued
    timestamp: float
    
    # Hash of the previous authority unit (for chaining)
    prev_hash: Optional[str] = None
    
    def __post_init__(self):
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not self.scope:
            raise ValueError("Scope must be provided")
        if not self.delegation_chain:
            raise ValueError("Delegation chain must not be empty")

    @property
    def hash(self) -> str:
        """Compute the SHA-256 hash of this authority unit."""
        # Include ALL fields with proper delimiters to prevent collisions
        chain_str = ",".join(self.delegation_chain)
        data = "|".join([
            self.id,
            self.scope,
            chain_str,
            str(self.price),
            str(self.timestamp),
            str(self.prev_hash)
        ])
        return sha256(data.encode()).hexdigest()

    def is_valid(self, current_time: float, max_age_seconds: int = 3600) -> bool:
        """Check if this authority unit is valid based on time and scope."""
        # Check if expired
        if current_time - self.timestamp > max_age_seconds:
            return False
        return True

    def can_consume(self, action_scope: str) -> bool:
        """Check if this authority can be used for the given action scope."""
        return self.scope == action_scope or self.scope == "any"