from autogen import ConversableAgent
from .agents.info_collector import InfoCollectorAgent

def start_workflow(key: str) -> None:
    info_collector = InfoCollectorAgent(key)
    the_human = ConversableAgent(
        name="human",
        human_input_mode="ALWAYS",
    )

    _ = info_collector.initiate_chats(
        chat_queue=[
            {
                "recipient": the_human,
                "message": "what do you need help with?",
                "max_turns": 2,
                "summary_method": "reflection_with_llm"
            },

            {
                "recipient": info_collector.executor,
                "message": "help me execute some tools",
                "max_turns": 3,
                "summary_method": "reflection_with_llm"
            },

            {
                "recipient": info_collector.reviewer,
                "message": "review my work",
                "max_turns": 1,
                "summary_method": "reflection_with_llm"
            },

            {
                "recipient": info_collector.executor,
                "message": "help me execute some tools",
                "max_turns": 3,
                "summary_method": "reflection_with_llm"
            },

            {
                "recipient": info_collector.reviewer,
                "message": "review my work",
                "max_turns": 1,
                "summary_method": "reflection_with_llm"
            },
        ]
    )
