from typing import Callable, Any
from .authority import AuthorityUnit
from .trace import DecisionTrace, LiabilityRecord
import time

class ExecutionGateError(Exception):
    """Custom exception for execution gate errors."""
    pass

class ExecutionGate:
    """
    The mandatory interception point for any autonomous action.
    
    Invariant: Blocks execution absent a valid AU.
    """
    
    def __init__(self, validator: Callable[[AuthorityUnit], bool]):
        self.validator = validator
        self.consumed_au_ids = set()
        
    def execute_with_authority(
        self,
        au: AuthorityUnit,
        action_fn: Callable[[], Any],
        action_name: str,
        action_scope: str
    ) -> tuple[DecisionTrace, LiabilityRecord]:
        """
        Execute an action with authority validation and atomic commit.
        
        Args:
            au: The authority unit to validate and consume
            action_fn: The function to execute if validation passes
            action_name: Name of the action for trace purposes
            action_scope: Scope required for this action (e.g., "read", "write")
            
        Returns:
            Tuple of (DecisionTrace, LiabilityRecord)
            
        Raises:
            ExecutionGateError: If validation fails or execution cannot proceed
        """
        # Validate authority unit
        if not self.validator(au):
            raise ExecutionGateError(f"Invalid authority unit: {au.id}")
        
        # Check if already consumed
        if au.id in self.consumed_au_ids:
            raise ExecutionGateError(f"Authority unit already consumed: {au.id}")
            
        # Check scope authorization
        if not au.can_consume(action_scope):
            raise ExecutionGateError(
                f"Authority scope '{au.scope}' cannot perform action scope '{action_scope}'"
            )
        
        # Consume the authority unit atomically
        self.consumed_au_ids.add(au.id)
        
        try:
            # Execute the action
            result = action_fn()
            
            # Create decision trace and liability record
            dt = DecisionTrace(
                action_name=action_name,
                authority_id=au.id,
                timestamp=time.time(),
                result=result
            )
            
            lr = LiabilityRecord(
                trace_id=dt.id,
                authority_id=au.id,
                price=au.price,
                scope=au.scope,
                timestamp=dt.timestamp
            )
            
            return dt, lr
            
        except Exception as e:
            # Rollback consumption on failure
            self.consumed_au_ids.discard(au.id)
            raise ExecutionGateError(f"Action execution failed: {str(e)}") from e