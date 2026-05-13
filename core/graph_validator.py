from typing import Dict, List


class GraphValidationError(Exception):
    pass


class GraphValidator:
    """
    ASTRA v1.3 — ACTIVE GRAPH VALIDATOR
    Runs BEFORE runtime execution
    """

    def validate(self, graph: Dict[str, List[str]]) -> None:

        if not isinstance(graph, dict):
            raise GraphValidationError("Graph must be dict")

        all_nodes = set(graph.keys())
        child_nodes = set()

        for src, targets in graph.items():
            for t in targets:
                child_nodes.add(t)

        # detect orphan nodes (not in graph keys but used)
        missing_nodes = child_nodes - all_nodes

        if missing_nodes:
            raise GraphValidationError(
                f"Missing nodes in graph: {missing_nodes}"
            )

        # detect empty graph
        if not graph:
            raise GraphValidationError("Empty graph")

        return True