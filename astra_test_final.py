python -c "
from core.pipeline_guard import PipelineGuard
from core.state_machine import StateMachine
from core.pipeline_executor import PipelineExecutor
from core.orchestrator import Orchestrator

guard = PipelineGuard('config/runtime_rules/stage_order.json')
sm = StateMachine(guard)

executor = PipelineExecutor(
    guard=guard,
    stage_handlers={
        'L0_INPUT': lambda x: {'ok': True, 'stage': 'L0_INPUT'},
        'L1_SEMANTIC': lambda x: {'ok': True, 'stage': 'L1_SEMANTIC'}
    }
)

orch = Orchestrator(guard, executor, sm)

print('INIT:', orch.initialize())

sm.transition('L1_SEMANTIC')

result = orch.run_stage({'x': 1}, next_stage='L1_SEMANTIC')

print('RESULT:', result)
print('SNAPSHOT:', orch.snapshot())
"