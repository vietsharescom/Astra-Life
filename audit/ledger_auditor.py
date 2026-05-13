from typing import List, Dict, Any


class LedgerAuditor:

    def audit_execution_trace(self, trace: List[Dict[str, Any]]) -> Dict[str, Any]:

        seen_stages = set()
        last_index = -1
        valid = True

        for record in trace:

            stage = record.get("stage")
            index = record.get("index", 0)

            if index is None:
                index = 0

            # order check
            if index < last_index:
                valid = False

            last_index = index
            seen_stages.add(stage)

        # =========================
        # IMPORTANT: CONTRACT FIX
        # =========================
        status = "PASS" if valid else "FAIL"

        return {
            "status": status,          # <<< FIX CRITICAL
            "valid": valid,
            "stages": list(seen_stages),
            "trace_length": len(trace)
        }