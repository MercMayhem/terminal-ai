from .agents.planner import PlannerAgent
from .agents.info_collector import InfoCollectorAgent
from .util import run_bash_script

def start_workflow(key: str) -> None:
    info_collector = InfoCollectorAgent(key)
    planner = PlannerAgent(key)

    query = input("What do you need help with: ")

    info_collection_result = info_collector.run_pipeline(query)
    print(info_collection_result)

    result = planner.run_pipeline(info_collection_result.model_dump_json())
    print(result.script)

    run_bash_script(result.script)
