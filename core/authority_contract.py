from enum import Enum


class AuthorityLevel(str, Enum):
    STATE = "STATE"
    GRAPH = "GRAPH"
    EXECUTION = "EXECUTION"
    FLOW = "FLOW"


class AuthorityContract:
    """
    ASTRA v1.1 — Constitutional Authority Layer

    PURPOSE:
    - Define ownership boundaries
    - NOT enforce runtime behavior
    - NOT replace Guard / StateMachine logic
    """

    # =========================
    # STATE AUTHORITY (StateMachine)
    # =========================
    STATE_MACHINE = {
        "owns": ["current_stage", "history", "execution_context"],
        "can": ["commit_state", "record_trace"],
        "cannot": ["execute_logic", "decide_flow", "validate_graph"]
    }

    # =========================
    # GRAPH AUTHORITY (PipelineGuard)
    # =========================
    PIPELINE_GUARD = {
        "owns": ["graph_rules", "transition_validation"],
        "can": ["validate_edge", "reject_transition"],
        "cannot": ["commit_state", "execute_logic", "own_runtime_state"]
    }

    # =========================
    # EXECUTION AUTHORITY (Executor)
    # =========================
    EXECUTOR = {
        "owns": ["handler_execution", "io_transform"],
        "can": ["run_handler"],
        "cannot": ["commit_state", "decide_flow", "validate_graph"]
    }

    # =========================
    # FLOW AUTHORITY (Orchestrator)
    # =========================
    ORCHESTRATOR = {
        "owns": ["execution_flow"],
        "can": ["call_executor", "pass_payload", "select_next_stage"],
        "cannot": ["commit_state", "own_state", "validate_graph"]
    }

    # =========================
    # PURE CHECK (OPTIONAL DEBUG ONLY)
    # =========================
    @staticmethod
    def check_violation(component: str, action: str) -> bool:
        """
        DEBUG ONLY (NOT ENFORCEMENT)

        Used only for diagnostics, not runtime control.
        """

        rules = {
            "STATE_MACHINE": AuthorityContract.STATE_MACHINE,
            "PIPELINE_GUARD": AuthorityContract.PIPELINE_GUARD,
            "EXECUTOR": AuthorityContract.EXECUTOR,
            "ORCHESTRATOR": AuthorityContract.ORCHESTRATOR
        }

        if component not in rules:
            return False

        return action in rules[component]["cannot"]