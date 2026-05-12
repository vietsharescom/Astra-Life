PIPELINE_SPEC.md
ASTRA LIFE v1.0 — CANONICAL EXECUTION PIPELINE SPECIFICATION
(Single Source of Truth for Runtime Behavior — FROZEN)
________________________________________
0. DOCUMENT AUTHORITY (SYSTEM LOCK)
This document is:
•	The highest authority on Astra Life execution flow 
•	A mandatory standard for all runtime implementations 
•	The single reference source for: 
o	debugging 
o	auditing 
o	replay 
o	deterministic verification 
o	system expansion 
This document is NOT:
•	A schema definition (see SCHEMA_REFERENCE.md) 
•	A module contract specification (see MODULE_CONTRACTS.md) 
•	Code or pseudo-code 
If implementation code conflicts with this document → THE CODE IS WRONG.
________________________________________
1. PIPELINE OBJECTIVE
The Astra Life pipeline exists to:
•	Process user input through a fully controlled execution sequence 
•	Eliminate: 
o	hidden steps 
o	implicit reasoning 
o	unauthorized behavior 
•	Enforce: 
o	deterministic governance 
o	full audit & replay capability 
o	human interruption and override at critical points 
This pipeline is not an optimization layer.
It is a governance enforcement mechanism.
________________________________________
2. PIPELINE PRINCIPLES (IMMUTABLE)
The pipeline MUST obey the following rules:
1.	Strictly linear — no implicit loops 
2.	Single responsibility per step 
3.	No step may be skipped 
4.	No module may directly invoke another module 
5.	Orchestrator is the sole coordination authority 
Violation of any principle constitutes a critical system defect.
________________________________________
3. STANDARD PIPELINE FLOW v1.0 (CANONICAL)
User Input
   ↓
Orchestrator (Entry Authority)
   ↓
Semantic Engine
   ↓
Enforcer
   ↓
Router
   ↓
Decision Authority Layer
   ↓
Policy Engine
   ↓
Agent (Domain Pack)
   ↓
Memory & Tool Layer
   ↓
Recovery Layer (conditional)
   ↓
Response Generator (Prompt rendering is a presentation concern.
It does not affect pipeline control or authority.)
   ↓
Observability & Audit (always-on)
This order is non-negotiable.
________________________________________
4. DETAILED PIPELINE STAGE SPECIFICATION
4.1 User Input
Sources
•	Text 
•	Voice (already transcribed) 
Rules
•	Raw, unstructured 
•	No semantic meaning 
•	No intent 
•	No preprocessing beyond normalization 
________________________________________
4.2 Orchestrator — ENTRY AUTHORITY
Responsibilities
•	Initialize execution context 
•	Assign trace_id and correlation_id 
•	Invoke pipeline stages in canonical order 
•	Enforce pipeline invariants 
•	Handle stop / abort / rollback 
Orchestrator MUST NOT
•	Interpret user content 
•	Modify payloads 
•	Make business or policy decisions 
________________________________________
4.3 Semantic Engine
Input
•	Raw user input 
Output
•	Unified Item JSON (schema-compliant) 
Guarantees
•	Stateless 
•	Deterministic mapping (within model constraints) 
Failure Mode
•	semantic_error 
•	Pipeline terminates immediately 
________________________________________
4.4 Enforcer
Input
•	Unified Item JSON 
Responsibilities
•	Schema validation 
•	Contract validation 
•	Governance rule validation 
Hard Rules
•	INVALID → reject 
•	No modification 
•	No inference 
•	No recovery 
________________________________________
4.5 Router
Input
•	Validated semantic payload 
Responsibilities
•	Select domain pack 
•	Select agent pipeline 
Router MUST NOT
•	Access memory 
•	Perform semantic reasoning 
•	Modify payload 
________________________________________
4.6 Decision Authority Layer (MANDATORY)
Single Question
Does the system have PERMISSION to execute this action?
Possible Outputs
•	allow 
•	require_human_approval 
•	reject 
•	escalate 
Scope
•	Permission 
•	Risk category 
•	Authority boundary 
Explicitly EXCLUDES
•	Business logic 
•	Policy rule evaluation 
________________________________________
4.7 Policy Engine (INDEPENDENT)
Responsibilities
•	Apply business policies 
•	Evaluate compliance rules 
•	Resolve policy conflicts 
Policy Engine MUST NOT
•	Call tools 
•	Write memory 
•	Modify intent or semantics 
Policies are versioned, testable, and external to prompts.
________________________________________
4.8 Agent Layer (Domain Executor)
Execution Preconditions
•	Decision Authority = allow 
•	Policy Engine = pass 
Agent MAY
•	Access memory 
•	Call tools 
•	Execute workflows 
Agent MUST NOT
•	Bypass policy 
•	Expand scope autonomously 
•	Create new tools 
•	Modify schemas 
________________________________________
4.9 Memory & Tool Layer
Rules
•	Only Agent may invoke 
•	Every call is audited 
•	No hidden execution 
•	Tools must be schema-bound 
________________________________________
4.10 Recovery Layer (CONDITIONAL)
Triggers
•	Runtime errors 
•	Timeouts 
•	Tool failures 
Recovery MAY
•	Retry 
•	Fallback 
•	Escalate 
Recovery MUST NOT
•	Change semantic intent 
•	Override approved decisions 
•	Bypass policy or authority 
________________________________________
4.11 Response Generator
Input
•	Structured execution result 
Output
•	User-facing response 
STRICTLY FORBIDDEN
•	Fabrication 
•	Unsupported inference 
•	Emotional injection not present in data 
________________________________________
4.12 Observability & Audit (ALWAYS-ON)
Every stage MUST log:
•	Input 
•	Output 
•	Timestamp 
•	trace_id 
•	Decision state 
No black-box behavior is permitted.
________________________________________
5. PIPELINE INVARIANTS (SYSTEM LOCK)
The pipeline is valid if and only if:
1.	Semantic Engine does not access memory 
2.	Enforcer does not modify payload 
3.	Router does not reason 
4.	Agent does not exceed domain scope 
5.	Tools are only called by Agent 
6.	Policy is never embedded in prompts 
7.	Orchestrator does not perform business logic 
Any violation → CRITICAL BUG
________________________________________
6. PIPELINE STOP & ESCALATION
The pipeline MUST halt immediately on:
•	Schema invalidation 
•	Governance rejection 
•	Policy conflict 
•	Human approval required 
No auto-continuation is allowed.
________________________________________
7. VERSIONING & CHANGE CONTROL
•	Pipeline is strictly versioned 
•	Every change MUST include: 
o	changelog 
o	tests 
o	replay verification 
Silent behavior changes are forbidden.
________________________________________
8. DOCUMENT RELATIONSHIP MAP
Document	Role
ASTRA_MASTER_CONTEXT.md	System constitution
PIPELINE_SPEC.md	Execution law
MODULE_CONTRACTS.md	Authority boundaries
SCHEMA_REFERENCE.md	Data structure
ORCHESTRATOR_SPEC.md	Coordination logic
________________________________________
9. FINAL DECLARATION (FROZEN)
The pipeline is law.
No module may be more intelligent than the pipeline.
No prompt may override the pipeline.
________________________________________
STATUS
•	Buildable ✅ 
•	Auditable ✅ 
•	Replayable ✅ 
•	Scalable ✅ 
•	Unambiguous ✅
-------------------------------------====


ASTRA LIFE v1.0 — CANONICAL PROJECT TREE
(Final · Frozen · Constitution-Level)
astra-life/
│
├── ASTRA_MASTER_CONTEXT.md        # 🔒 System Constitution (FROZEN)
├── PIPELINE_SPEC.md               # 🔒 Execution Law
├── MODULE_CONTRACTS.md            # 🔒 Module Boundaries
├── SCHEMA_REFERENCE.md            # 🔒 Data Canon
├── ORCHESTRATOR_SPEC.md           # 🔒 Control Logic
│
├── config/                        # 🔴 L4 — SYSTEM CONFIG (ENFORCEMENT CORE)
│   │
│   ├── system_meta.json           # ASTRA_MASTER_CONTEXT → JSON
│   ├── pipeline_flow.json         # PIPELINE_SPEC → JSON
│   ├── module_contracts.json      # MODULE_CONTRACTS → JSON
│   │
│   ├── schemas/                   # 🔒 SCHEMA CANON (READ-ONLY)
│   │   ├── UnifiedItem.schema.json
│   │   ├── RoutingDecision.schema.json
│   │   ├── AgentInput.schema.json
│   │   ├── AgentResult.schema.json
│   │   ├── ToolCall.schema.json
│   │   └── Response.schema.json
│   │
│   └── runtime_rules/             # enforcement-only (NO logic)
│       ├── stage_order.json
│       ├── tool_permissions.json
│       └── safety_constraints.json
│
├── input/                         # 🧊 L0 — SOURCE INPUT (IMMUTABLE)
│   │
│   ├── text/
│   │   └── raw/
│   ├── audio/
│   │   └── raw/
│   ├── image/
│   │   └── raw/
│   ├── document/
│   │   └── raw/
│   │
│   └── manifest/
│       └── sources.json           # source registry (single source of truth)
│
├── preprocess/                    # ⚙️ L1–L3 — PRE-LLM COMPUTE PIPELINE
│   │
│   ├── common/                    # shared utilities (NO business logic)
│   │   ├── io/
│   │   └── __init__.py
│   │
│   ├── p0_ingestion/              # 🟦 L1 — INGESTION (RAW → RECORD)
│   │   ├── text/
│   │   │   ├── adapters/
│   │   │   │   └── raw_text_reader.py
│   │   │   └── pipeline.py
│   │   └── audio/
│   │       ├── adapters/
│   │       └── pipeline.py
│   │
│   ├── p1_processing/             # 🟨 L2 — NORMALIZATION / PARSING
│   │   └── text/
│   │       ├── normalization/
│   │       ├── parsing/
│   │       ├── semantic_event/
│   │       └── pipeline.py
│   │
│   ├── pipeline/                  # 🟧 L3 — PIPELINE ENTRYPOINTS
│   │   ├── p01_text_pipeline.py
│   │   ├── p01_audio_pipeline.py
│   │   └── system_pipeline.py
│   │
│   └── system/                    # 🟧 L3 — EXECUTION ENGINE
│       ├── orchestrator.py
│       ├── dependency_graph.py
│       └── execution_engine.py
│
├── prompts_layer2/                # 🧠 LAYER 2 — LLM RUNTIME ADAPTERS
│   │
│   ├── semantic_prompt.md         # intent understanding adapter
│   ├── router_prompt.md           # routing adapter
│   ├── enforcer_prompt.md         # schema / rule enforcement adapter
│   ├── agent_prompt_base.md       # base agent execution adapter
│   └── response_prompt.md         # response formatting adapter
│
├── runtime/                       # 🚀 L5 — LIVE EXECUTION (CODE)
│   │
│   ├── orchestrator.py
│   ├── semantic_engine.py
│   ├── router.py
│   ├── enforcer.py
│   ├── agent_base.py
│   ├── tool_executor.py
│   ├── response_generator.py
│   └── validator.py
│
├── artifacts/                     # 📦 L6 — IMMUTABLE OUTPUT STORE (FROZEN)
│   │
│   ├── p0/                        # STAGE p0 — INGESTION OUTPUT
│   │   ├── text/
│   │   │   └── P01/
│   │   │       └── runs/
│   │   │           └── run_000001/
│   │   │               └── records_v1.jsonl
│   │   └── audio/
│   │       └── P01/
│   │           └── runs/
│   │               └── run_000001/
│   │                   └── segments_v1.jsonl
│   │
│   ├── p1/                        # STAGE p1 — NORMALIZED
│   ├── p2/                        # STAGE p2 — PARSED
│   ├── p3/                        # STAGE p3 — SEMANTIC
│   │
│   └── trace/                     # execution traces (read-only)
│
├── scripts/                       # 🧪 L7 — OPS / GOVERNANCE
│   ├── validation/
│   ├── replay/
│   ├── audit/
│   └── reports/
│
└── README.md



-----------==
Runtime/schema_enforcer.py

## SYSTEM DIRECTORY CONSTITUTION (CANONICAL — FROZEN)

├── core/                              # ⚙️ L4.5 — ENFORCEMENT RUNTIME (EXECUTOR ONLY)
│   ├── pipeline_executor.py           # Executes pipeline_flow.json verbatim
│   ├── schema_enforcer.py             # Validates all I/O against schemas/*
│   ├── state_machine.py               # Stage transitions + lifecycle
│   ├── context_loader.py              # Loads system_meta.json
│   └── pipeline_guard.py            # Enforces runtime_rules/*changed name (runtime_guard.py)
│
│

LƯU Ý
•	Core không nằm trong pipeline 
•	Core không được phép định nghĩa logic 
•	Core chỉ thực thi những gì JSON nói
-----------==
Đặt trong preprocess/
preprocess/
├── adapters/
│   └── llm/
│       ├── prompt_renderer.py      ✅
│       └── response_formatter.py


________________________________________
QUY ƯỚC ĐẶT TÊN — KHÓA CỨNG (PHẢI TUÂN THEO)
1. STAGE (BẤT BIẾN)
p0 → p1 → p2 → p3
•	p0 = ingestion output 
•	p1 = normalized 
•	p2 = parsed 
•	p3 = semantic 
⛔ Không được đổi tên, không được thêm chữ.
________________________________________
2. PIPELINE ID
P01, P02, P03…
•	In hoa 
•	Không mô tả 
•	Mapping trong pipeline_registry 
________________________________________
3. RUN ID
run_000001
•	Zero-padded 
•	Monotonic 
•	Immutable 
________________________________________
4. FILE OUTPUT
<content>_v<version>.jsonl
Ví dụ:
•	records_v1.jsonl 
•	segments_v2.jsonl 
•	semantic_events_v1.jsonl 
________________________________________
NGUYÊN TẮC SỐNG CÒN (CẤM VI PHẠM)
•	❌ Không đưa preprocess vào artifacts 
•	❌ Không đưa logic vào config 
•	❌ Không đổi tên thư mục hiến pháp 
•	❌ Không ghi đè artifacts 
•	✅ Mỗi stage = một output bất biến 
•	✅ Mọi thứ đều traceable ngược về run_id 
________________________________________




