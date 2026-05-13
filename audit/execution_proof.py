# audit/execution_proof.py
import time
import hashlib
import json

class ExecutionProof:
    @staticmethod
    def generate(trace, graph_audits, ledger_audit):
        payload = {
            "trace": trace,
            "graph_audits": graph_audits,
            "ledger_audit": ledger_audit,
            "timestamp": time.time()
        }

        fingerprint = hashlib.sha256(
            json.dumps(payload, sort_keys=True).encode()
        ).hexdigest()

        return {
            "type": "EXECUTION_PROOF",
            "status": "VALID"
            if ledger_audit["status"] == "PASS"
            and all(a["status"] == "PASS" for a in graph_audits)
            else "INVALID",
            "fingerprint": fingerprint,
            "payload": payload
        }