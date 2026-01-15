from typing import Dict, List, Optional
from .authority import AuthorityUnit
from .gate import ExecutionGate
import time

class AuthorityManager:
    """
    Manages authority units and provides validation logic.
    
    This class is responsible for maintaining the state of available authorities
    and providing validation functions to the execution gate.
    """
    
    def __init__(self):
        self.authorities: Dict[str, AuthorityUnit] = {}
        
    def issue_authority(self, au: AuthorityUnit) -> None:
        """Issue a new authority unit."""
        if au.id in self.authorities:
            raise ValueError(f"Authority with ID {au.id} already exists")
        self.authorities[au.id] = au
        
    def validate_authority(self, au: AuthorityUnit) -> bool:
        """
        Validate an authority unit.
        
        Returns True if the authority is valid and available for use.
        """
        # Check if it exists
        if au.id not in self.authorities:
            return False
            
        # Get the stored authority to compare
        stored_au = self.authorities[au.id]
        
        # Ensure we're validating the exact same authority unit (not a mutated copy)
        if stored_au != au:
            return False
            
        # Check if it's still valid (not expired)
        current_time = time.time()
        if not au.is_valid(current_time):
            return False
            
        return True
        
    def get_authority(self, au_id: str) -> Optional[AuthorityUnit]:
        """Get an authority unit by ID."""
        return self.authorities.get(au_id)