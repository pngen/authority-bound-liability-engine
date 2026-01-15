import pytest
from able.core.authority import AuthorityUnit

def test_authority_unit_creation():
    """Test that AuthorityUnit can be created with valid parameters."""
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root", "user"],
        price=10,
        timestamp=1640995200.0
    )
    
    assert au.id == "test-123"
    assert au.scope == "read"
    assert au.price == 10
    assert len(au.delegation_chain) == 2

def test_authority_unit_invalid_price():
    """Test that AuthorityUnit raises error for negative price."""
    with pytest.raises(ValueError, match="Price cannot be negative"):
        AuthorityUnit(
            id="test-123",
            scope="read",
            delegation_chain=["root"],
            price=-5,
            timestamp=1640995200.0
        )

def test_authority_unit_empty_scope():
    """Test that AuthorityUnit raises error for empty scope."""
    with pytest.raises(ValueError, match="Scope must be provided"):
        AuthorityUnit(
            id="test-123",
            scope="",
            delegation_chain=["root"],
            price=10,
            timestamp=1640995200.0
        )

def test_authority_unit_empty_delegation():
    """Test that AuthorityUnit raises error for empty delegation chain."""
    with pytest.raises(ValueError, match="Delegation chain must not be empty"):
        AuthorityUnit(
            id="test-123",
            scope="read",
            delegation_chain=[],
            price=10,
            timestamp=1640995200.0
        )

def test_authority_unit_hash():
    """Test that AuthorityUnit computes hash correctly."""
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    assert isinstance(au.hash, str)
    assert len(au.hash) == 64  # SHA-256 produces 64 hex characters

def test_authority_unit_hash_collision_resistance():
    """Test that hash computation prevents collisions."""
    au1 = AuthorityUnit(
        id="a",
        scope="bc",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    au2 = AuthorityUnit(
        id="ab",
        scope="c",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # These should have different hashes due to proper delimiters
    assert au1.hash != au2.hash

def test_authority_unit_validity():
    """Test that AuthorityUnit validity check works."""
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    # Should be valid at creation time
    assert au.is_valid(1640995200.0 + 1000) == True
    
    # Should be invalid after expiration (default max_age = 3600)
    assert au.is_valid(1640995200.0 + 3700) == False

def test_authority_unit_consumption():
    """Test that AuthorityUnit can check if it can consume an action."""
    au = AuthorityUnit(
        id="test-123",
        scope="read",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    assert au.can_consume("read") == True
    assert au.can_consume("write") == False
    
    # Test "any" scope
    au_any = AuthorityUnit(
        id="test-456",
        scope="any",
        delegation_chain=["root"],
        price=10,
        timestamp=1640995200.0
    )
    
    assert au_any.can_consume("read") == True
    assert au_any.can_consume("write") == True