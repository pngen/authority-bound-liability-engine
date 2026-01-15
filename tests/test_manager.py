import pytest
from able.core.authority import AuthorityUnit
from able.core.manager import AuthorityManager

def test_authority_manager_issue_authority():
    """Test that manager can issue authority units."""
    manager = AuthorityManager()
    
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    manager.issue_authority(au)
    
    # Verify it was stored
    assert manager.get_authority("test-123") == au

def test_authority_manager_duplicate_issue():
    """Test that manager rejects duplicate authority IDs."""
    manager = AuthorityManager()
    
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    manager.issue_authority(au)
    
    # Try to issue the same authority again
    with pytest.raises(ValueError, match="already exists"):
        manager.issue_authority(au)

def test_authority_manager_validate_valid():
    """Test that manager validates valid authorities."""
    manager = AuthorityManager()
    
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    manager.issue_authority(au)
    
    assert manager.validate_authority(au) == True

def test_authority_manager_validate_invalid():
    """Test that manager rejects invalid authorities."""
    manager = AuthorityManager()
    
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # Don't issue it, so validation should fail
    assert manager.validate_authority(au) == False

def test_authority_manager_validate_mismatched():
    """Test that manager rejects mutated authority units."""
    manager = AuthorityManager()
    
    au1 = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    manager.issue_authority(au1)
    
    # Create a copy with different price (mutated)
    au2 = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=20,  # Different price
        timestamp=1640995200.0
    )
    
    # Should not validate because it's a different authority unit
    assert manager.validate_authority(au2) == False

def test_authority_manager_get_nonexistent():
    """Test that manager returns None for nonexistent authority."""
    manager = AuthorityManager()
    
    result = manager.get_authority("nonexistent")
    assert result is None