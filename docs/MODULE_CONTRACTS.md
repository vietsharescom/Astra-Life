MODULE_CONTRACTS.md
Astra Life v1.0 — Module Authority & Responsibility Contracts
(Binding Governance Specification — Frozen)
________________________________________
0. ROLE OF THIS DOCUMENT (SYSTEM-CRITICAL)
This document is:
• The binding authority contract for every system module
• The enforcement reference for:
•	Orchestrator 
•	Pipeline execution engine 
•	Schema enforcer 
•	Test harness 
•	Audit & replay engine 
This document defines:
• What each module MUST do
• What each module MAY do
• What each module is STRICTLY FORBIDDEN to do
This document is NOT:
• Code
• Pseudo-code
• A design suggestion
If any implementation violates this document → IMPLEMENTATION IS INVALID
________________________________________
1. SYSTEM CONTRACT PRINCIPLES (IMMUTABLE)
1.	Every module has exactly one authority domain 
2.	No module may:
• expand its authority
• compensate for another module
• silently correct upstream output 
3.	All modules except Agents are stateless 
4.	All authority boundaries are hard-fail, not best-effort 
5.	Contracts override prompts, heuristics, and model behavior 
________________________________________
2. MODULE CONTRACTS (CANONICAL)
________________________________________
2.1 Orchestrator
Role: Execution Authority (Coordinator Only)
MUST
• Initialize execution context
• Assign trace_id, correlation_id
• Invoke pipeline stages in exact order defined in PIPELINE_SPEC.md
• Enforce pipeline invariants
• Stop pipeline on hard failure
MUST NOT
• Interpret user input
• Perform semantic reasoning
• Modify payload content
• Make business or policy decisions
• Call tools
• Access memory
State
• Stateless
• Context-passing only
________________________________________
2.2 Semantic Engine
Role: Meaning Extraction & Normalization
MUST
• Accept raw user input only
• Produce Unified Item JSON strictly compliant with schema
• Operate deterministically within model constraints
MUST NOT
• Access memory
• Call tools
• Perform planning
• Apply policy or governance rules
• Infer user traits or intentions
Failure Mode
• Emit semantic_error
• Pipeline must stop immediately
State
• Stateless
________________________________________
2.3 Enforcer
Role: Governance Gate (Validation Only)
MUST
• Validate schema compliance
• Validate contract compliance
• Validate governance constraints
MUST NOT
• Modify payload
• Repair invalid structures
• Infer missing fields
• Apply business logic
Hard Rules
• INVALID → REJECT
• No soft-fail allowed
State
• Stateless
________________________________________
2.4 Router
Role: Routing Selector (No Reasoning)
MUST
• Select domain pack
• Select agent pipeline identifier
MUST NOT
• Perform semantic reasoning
• Access memory
• Modify payload
• Apply policy
• Execute tools
State
• Stateless
________________________________________
2.5 Decision Authority Layer
Role: Permission & Risk Authority
SINGLE QUESTION
Does the system have permission to execute this action?
Output (EXACTLY ONE)
• allow
• require_human_approval
• reject
• escalate
MUST NOT
• Evaluate business logic
• Apply policies
• Call tools
• Modify intent
State
• Stateless
________________________________________
2.6 Policy Engine
Role: Policy & Compliance Authority (Independent)
MUST
• Evaluate policy rules
• Check compliance constraints
• Resolve policy conflicts
MUST NOT
• Call tools
• Write to memory
• Modify intent or payload
• Perform execution logic
Properties
• Versioned
• Human-editable
• Testable
• Hot-reloadable
State
• Stateless
________________________________________
2.7 Agent (Domain Executor)
Role: Controlled Execution Unit
Preconditions (MANDATORY)
• Decision Authority = allow
• Policy Engine = pass
MAY
• Access memory
• Call approved tools
• Execute workflows within domain scope
MUST NOT
• Bypass policy
• Expand scope autonomously
• Create new tools
• Modify schema
• Override decisions
State
• Stateful (contract-bound)
________________________________________
2.8 Memory Layer
Role: State Persistence (Passive)
MUST
• Serve read/write requests only from Agent
• Maintain auditability
MUST NOT
• Trigger actions
• Modify intent
• Call tools
Types
• Structured memory
• Semantic memory
• Session memory
________________________________________
2.9 Tool Layer
Role: Capability Execution (Passive)
MUST
• Enforce input/output schema
• Enforce permission scope
• Emit audit logs
MUST NOT
• Be called directly by non-Agent modules
• Perform autonomous decisions
________________________________________
2.10 Recovery Layer
Role: Execution Failure Handler (Conditional)
Triggered Only On
• Runtime error
• Timeout
• Tool failure
MAY
• Retry
• Fallback
• Route to dead-letter queue
MUST NOT
• Change semantic intent
• Override approved decisions
________________________________________
2.11 Response Generator
Role: Human-Facing Output Formatter
MUST
• Convert structured results into user-facing response
MUST NOT
• Fabricate information
• Infer unsupported meaning
• Alter business results
State
• Stateless
________________________________________
2.12 Observability & Audit
Role: System Truth Recorder (Always-On)
MUST
Log at every stage:
• Input
• Output
• Timestamp
• Trace ID
• Decision state
MUST NOT
• Affect execution flow
________________________________________
3. CROSS-MODULE VIOLATION RULE
If any module:
• Assumes another module’s responsibility
• Compensates for upstream errors
• Expands its authority
→ This is a CRITICAL SYSTEM BUG
→ Pipeline execution must be halted
________________________________________
4. RELATIONSHIP TO OTHER DOCUMENTS
Document	Role
ASTRA_MASTER_CONTEXT.md	System constitution
PIPELINE_SPEC.md	Execution law
MODULE_CONTRACTS.md	Authority boundaries
SCHEMA_REFERENCE.md	Data structure
ORCHESTRATOR_SPEC.md	Coordination logic
________________________________________
5. FINAL DECLARATION (SYSTEM LOCK)
Module authority is law.
No module may be smarter than its contract.
No prompt may override contracts.
No implementation may reinterpret responsibility.
________________________________________
STATUS
✅ Pipeline-aligned
✅ Governance-locked
✅ Buildable
✅ Auditable
✅ Enterprise-grade

