SCHEMA_REFERENCE.md
ASTRA LIFE v1.0 — Canonical Data Schema Specification
(Single Source of Truth for Data Shape & Validation)
________________________________________
0. ROLE OF THIS DOCUMENT (ABSOLUTE AUTHORITY)
This document defines:
•	All canonical data structures used in Astra Life 
•	Field-level contracts between pipeline stages 
•	Validation boundaries enforced by SchemaEnforcer 
This document is:
•	The only authority on data shape 
•	Mandatory for: 
o	Semantic Engine output 
o	Enforcer validation 
o	Router input 
o	Agent I/O 
o	Tool contracts 
o	Replay & audit 
This document is NOT:
•	Pipeline logic (see PIPELINE_SPEC.md) 
•	Module responsibility (see MODULE_CONTRACTS.md) 
•	Business rules or policies 
•	Prompt instructions 
If runtime data violates this document → PIPELINE MUST STOP
________________________________________
1. SCHEMA GOVERNING PRINCIPLES (SYSTEM LOCK)
1.	Schemas define structure, not behavior 
2.	No schema performs inference 
3.	No schema is optional unless explicitly stated 
4.	No schema mutation allowed at runtime 
5.	Schemas are versioned and immutable once released 
6.	Schema > prompt > model output 
________________________________________
2. GLOBAL SCHEMA CONVENTIONS
2.1 Naming
•	snake_case for all fields 
•	explicit, non-ambiguous naming 
•	no overloaded fields 
2.2 Required Metadata (ALL schemas)
Every schema MUST include:
•	schema_version 
•	trace_id 
•	created_at 
________________________________________
3. CANONICAL PIPELINE SCHEMAS
________________________________________
3.1 UnifiedItem
Produced by: Semantic Engine
Consumed by: Enforcer, Router
Purpose
Canonical semantic representation of user input.
Schema
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "input_type": "text | voice",
  "raw_input_ref": "string",
  "language": "string",
  "intent": {
    "category": "string",
    "confidence": "float"
  },
  "entities": [
    {
      "type": "string",
      "value": "string"
    }
  ],
  "constraints": {
    "sensitive": "boolean",
    "irreversible": "boolean"
  }
}
Hard Rules
•	No memory-derived fields 
•	No inferred personality traits 
•	Confidence is probabilistic, not authoritative 
________________________________________
3.2 RoutingDecision
Produced by: Router
Consumed by: Decision Authority Layer
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "domain_pack": "string",
  "agent_id": "string",
  "routing_reason": "string"
}
Rules:
•	Routing is deterministic 
•	Reason is descriptive, not justificatory 
________________________________________
3.3 AuthorityDecision
Produced by: Decision Authority Layer
Consumed by: Policy Engine
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "decision": "allow | require_human_approval | reject | escalate",
  "risk_level": "low | medium | high",
  "justification": "string"
}
Rules:
•	No business logic evaluation 
•	Risk level ≠ permission 
________________________________________
3.4 PolicyEvaluationResult
Produced by: Policy Engine
Consumed by: Agent
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "policy_version": "string",
  "result": "pass | fail",
  "violations": [
    {
      "policy_id": "string",
      "reason": "string"
    }
  ]
}
Rules:
•	Fail is terminal unless human override 
•	Policy source must be versioned 
________________________________________
3.5 AgentInput
Produced by: Orchestrator
Consumed by: Agent
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "unified_item": {},
  "authority_decision": {},
  "policy_result": {}
}
Rules:
•	AgentInput is a composed object 
•	Agent cannot alter upstream data 
________________________________________
3.6 AgentResult
Produced by: Agent
Consumed by: Response Generator
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "status": "success | failure",
  "output": {},
  "tool_calls": [
    {
      "tool_id": "string",
      "status": "success | failure"
    }
  ]
}
Rules:
•	Tool calls must be auditable 
•	No hidden execution 
________________________________________
3.7 ResponsePayload
Produced by: Response Generator
Consumed by: User / Audit
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "response_text": "string",
  "confidence_notice": "string"
}
Rules:
•	No fabrication 
•	No inference beyond AgentResult 
________________________________________
4. ERROR SCHEMAS (PIPELINE STOP)
4.1 ValidationError
{
  "schema_version": "1.0",
  "trace_id": "string",
  "created_at": "iso8601",
  "error_type": "schema | contract | governance",
  "details": "string"
}
________________________________________
5. SCHEMA VERSIONING
•	Semantic versioning 
•	Backward incompatible changes → new version 
•	Old versions remain replayable 
________________________________________
6. RELATIONSHIP TO OTHER DOCUMENTS
Document	Relationship
ASTRA_MASTER_CONTEXT.md	Philosophical constraints
PIPELINE_SPEC.md	Execution order
MODULE_CONTRACTS.md	Authority boundaries
SCHEMA_REFERENCE.md	Data truth
________________________________________
7. FINAL LOCK
Schemas define reality.
Anything outside schema does not exist to the system.
________________________________________
STATUS
•	Pipeline-aligned: ✅ 
•	Enforcer-ready: ✅ 
•	Replay-safe: ✅ 
•	Production-grade: ✅

