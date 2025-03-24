from .agents.info_collector import InfoCollectorAgent

def start_workflow(key: str) -> None:
    info_collector = InfoCollectorAgent(key)
    query = input("What do you need help with: ")
    info_collection_result = info_collector.run_pipeline(query)

    print(info_collection_result)
