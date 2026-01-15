import pytest
from unittest.mock import Mock
from able.core.authority import AuthorityUnit
from able.core.gate import ExecutionGate, ExecutionGateError
from able.core.trace import DecisionTrace, LiabilityRecord

def test_execution_gate_valid_authority():
    """Test that gate executes action with valid authority."""
    # Setup mock validator that always returns True
    validator = Mock(return_value=True)
    
    gate = ExecutionGate(validator)
    
    def sample_action():
        return "success"
        
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    trace, liability = gate.execute_with_authority(
        au=au,
        action_fn=sample_action,
        action_name="test_action",
        action_scope="read"
    )
    
    # Verify trace and liability were created
    assert isinstance(trace, DecisionTrace)
    assert isinstance(liability, LiabilityRecord)
    assert trace.action_name == "test_action"
    assert trace.authority_id == "test-123"
    assert liability.authority_id == "test-123"
    assert liability.price == 10

def test_execution_gate_invalid_authority():
    """Test that gate rejects invalid authority."""
    # Setup mock validator that always returns False
    validator = Mock(return_value=False)
    
    gate = ExecutionGate(validator)
    
    def sample_action():
        return "success"
        
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    with pytest.raises(ExecutionGateError, match="Invalid authority unit"):
        gate.execute_with_authority(
            au=au,
            action_fn=sample_action,
            action_name="test_action",
            action_scope="read"
        )

def test_execution_gate_already_consumed():
    """Test that gate rejects already consumed authority."""
    # Setup mock validator that always returns True
    validator = Mock(return_value=True)
    
    gate = ExecutionGate(validator)
    
    def sample_action():
        return "success"
        
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # First execution should succeed
    trace, liability = gate.execute_with_authority(
        au=au,
        action_fn=sample_action,
        action_name="test_action",
        action_scope="read"
    )
    
    # Second execution with same authority should fail
    with pytest.raises(ExecutionGateError, match="Authority unit already consumed"):
        gate.execute_with_authority(
            au=au,
            action_fn=sample_action,
            action_name="test_action_2",
            action_scope="read"
        )

def test_execution_gate_action_failure():
    """Test that gate rolls back consumption on action failure."""
    # Setup mock validator that always returns True
    validator = Mock(return_value=True)
    
    gate = ExecutionGate(validator)
    
    def failing_action():
        raise RuntimeError("Action failed")
        
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # Execution should fail and consumption should be rolled back
    with pytest.raises(ExecutionGateError, match="Action execution failed"):
        gate.execute_with_authority(
            au=au,
            action_fn=failing_action,
            action_name="failing_action",
            action_scope="read"
        )
    
    # Verify that the authority was not consumed (since it was rolled back)
    assert au.id not in gate.consumed_au_ids

def test_execution_gate_scope_validation():
    """Test that gate enforces scope validation."""
    # Setup mock validator that always returns True
    validator = Mock(return_value=True)
    
    gate = ExecutionGate(validator)
    
    def sample_action():
        return "success"
        
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # Should succeed - matching scope
    trace, liability = gate.execute_with_authority(
        au=au,
        action_fn=sample_action,
        action_name="fetch_data",
        action_scope="read"
    )
    
    # Should fail - mismatched scope
    with pytest.raises(ExecutionGateError, match="cannot perform"):
        gate.execute_with_authority(
            au=au,
            action_fn=sample_action,
            action_name="write_data",
            action_scope="write"
        )

def test_execution_gate_any_scope():
    """Test that 'any' scope allows all actions."""
    # Setup mock validator that always returns True
    validator = Mock(return_value=True)
    
    gate = ExecutionGate(validator)
    
    def sample_action():
        return "success"
        
    au1 = AuthorityUnit(
        id="test-123",
        scope="any",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    au2 = AuthorityUnit(
        id="test-456",
        scope="any",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # Should succeed for any action scope
    trace1, liability1 = gate.execute_with_authority(
        au=au1,
        action_fn=sample_action,
        action_name="fetch_data",
        action_scope="read"
    )
    
    trace2, liability2 = gate.execute_with_authority(
        au=au2,
        action_fn=sample_action,
        action_name="write_data",
        action_scope="write"
    )