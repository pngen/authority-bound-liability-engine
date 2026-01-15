# Authority-Bound Liability Engine (ABLE)

## One-sentence value proposition
ABLE provides deterministic enforcement of autonomous actions through consumable authority units, ensuring accountability and traceability.

## Overview
ABLE is a system that binds autonomous execution to consumable authority and priced accountability. It prevents unauthorized actions by construction through mandatory interception points, atomic execution, and immutable tracing.

## Architecture diagram

<pre>
┌─────────────┐    ┌────────────────┐    ┌───────────────┐
│  Action     │───▶│ Execution      │───▶│ Authority     │
│  Request    │    │ Gate           │    │ Manager       │
└─────────────┘    │                │    │               │
                   │                │    │               │
                   │  ┌──────────┐  │    │  ┌─────────┐  │
                   │  │ Validate │  │    │  │ Issue   │  │
                   │  │ Authority│  │    │  │ AU      │  │
                   │  └──────────┘  │    │  └─────────┘  │
                   │                │    │               │
                   │  ┌─────────┐   │    │  ┌─────────┐  │
                   │  │ Consume │   │    │  │ Validate│  │
                   │  │ AU      │   │    │  │ AU      │  │
                   │  └─────────┘   │    │  └─────────┘  │
                   │                │    │               │
                   │  ┌─────────┐   │    │  ┌─────────┐  │
                   │  │ Execute │   │    │  │ Get     │  │
                   │  │ Action  │   │    │  │ AU      │  │
                   │  └─────────┘   │    │  └─────────┘  │
                   │                │    └───────────────┘
                   │  ┌─────────┐   │    
                   │  │ Emit    │   │    
                   │  │ Trace   │   │    
                   │  └─────────┘   │    
                   │                │    
                   │  ┌──────────┐  │    
                   │  │ Emit     │  │    
                   │  │ Liability│  │    
                   │  └──────────┘  │    
                   └────────────────┘    
</pre>

## Core Components

1. **AuthorityUnit (AU)**: A consumable, immutable unit encoding scope, delegation chain, and price.
2. **ExecutionGate (EG)**: The mandatory interception point for any autonomous action.
3. **DecisionTrace (DT)**: An append-only record emitted at execution.
4. **LiabilityRecord (LR)**: A deterministic mapping from DT to accountable parties and price.
5. **AuthorityManager**: Manages authority units and provides validation logic.

## Usage

```python
from able.core.manager import AuthorityManager
from able.core.gate import ExecutionGate
from able.core.authority import AuthorityUnit

# Create manager and gate
manager = AuthorityManager()
gate = ExecutionGate(manager.validate_authority)

# Issue an authority unit
au = AuthorityUnit(
    id="read-123",
    scope="read",
    delegation_chain=["root", "user"],
    price=10,
    timestamp=1640995200.0
)
manager.issue_authority(au)

# Execute an action with authority
def read_data():
    return "sensitive data"

trace, liability = gate.execute_with_authority(
    au=au,
    action_fn=read_data,
    action_name="read_data"
)
```

## Design Principles
- **Deterministic Enforcement**: Given identical inputs and authority state, outcomes are identical.
- **Traceability**: Every action yields an immutable trace bound to the authority consumed.
- **Atomicity**: Authority validation, execution, and trace emission occur as a single atomic operation.
- **Exhaustion**: Consumed authority cannot be reused, replayed, or partially applied.
- **No Bypass**: All autonomous actions must go through the Execution Gate.

## Requirements
- Python 3.7+
- No external dependencies beyond standard library
- All components are immutable where appropriate
- All operations are deterministic and idempotent where possible
- Comprehensive unit tests covering all failure modes

## Limitations
The following characteristics are intentional and correct at this abstraction level:
- In-memory tracking of consumed authority units is sufficient for enforcing single-use semantics within a deterministic execution boundary.
- A minimal AuthorityManager is appropriate; authority issuance and validation are explicit responsibilities, not an orchestration layer.
- The absence of persistence reflects a scoped enforcement core, not an incomplete system.
- No distributed or consensus semantics are implied, required, or claimed by ABLE.
- These constraints are explicit design boundaries, not omissions.
