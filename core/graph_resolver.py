from typing import Dict, Optional


class GraphResolver:

    def __init__(self, guard):
        self.graph = guard.graph

    def resolve_next_stage(self, current_stage: str, execution_result=None) -> Optional[str]:

        if current_stage not in self.graph:
            return None

        next_nodes = self.graph[current_stage]

        if not next_nodes:
            return None

        return next_nodes[0]