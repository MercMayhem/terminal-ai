from autogen import ConversableAgent, GroupChat, GroupChatManager
from .agents.info_collector import InfoCollectorAgent

def start_workflow(key: str) -> None:
    info_collector = InfoCollectorAgent(key)
    the_human = ConversableAgent(
        name="human",
        human_input_mode="ALWAYS",
    )

    groupchat = GroupChat(
        agents=[
            the_human,
            info_collector,
            info_collector.executor,
            info_collector.reviewer,
            info_collector.formatter
        ],
        speaker_selection_method="auto",
        messages=[],
    )

    llm_config = {
        "config_list": [
            {
                
                "api_type": "openai",
                "model": "gpt-4o-mini",
                "api_key": key
            }
        ]
    }

    manager = GroupChatManager(
        name="group_manager",
        groupchat=groupchat,
        llm_config=llm_config,
    )

    query = input()

    result = the_human.initiate_chats(
        chat_queue = [
            {
                "recipient": manager,
                "message": "Collect info for getting this help: {}".format(query),
                "summary_method": "reflection_with_llm"
            },

            {
                "recipient": info_collector.formatter,
                "message": "format the info",
                "max_turn": 1,
                "summary_method": "last_msg"
            }
        ]
    )

    print(result[-1].summary)
