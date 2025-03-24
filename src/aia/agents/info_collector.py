from copy import deepcopy
from autogen import ConversableAgent, GroupChat, GroupChatManager
from ..models import InfoCollectorOutput
from tools.shell import check_command_tool
from tools.filesystem import read_file_tool, get_current_directory_tool, list_directory_tool, file_search_tool, show_directory_tree_tool

# Subtyping for abstracting over tool registration and llm_config
class InfoCollectorAgent(ConversableAgent):

    def __init__(self, key: str) -> None:
        self.key = key

        self.llm_config = {
            "config_list": [
                {
                    
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": key
                }
            ]
        }

        llm_config = deepcopy(self.llm_config)

        super().__init__(
            name="InfoCollectorAgent",
            llm_config=llm_config,
            system_message="""
                You are an intelligent information-gathering agent for a terminal AI system.
                Your primary role is to accurately understand user queries, gather all relevant
                information about the execution context (e.g., system state, environment variables,
                resource availability, user intent), and provide this information to the plan
                creator agent.

                You run in a loop of Thought, Action, PAUSE, Observation.

                Keep looping this part:
                    Thought: This is you describing your thoughts about the query / question asked by the user and info
                    you have already gathered.

                    Action: This is you making tool calls for gathering info and / or consulting other agents.

                    PAUSE: You will yield here for a response.

                    Observation: Observe the outcomes and provide the info

                Always tag if it is a thought or observation before the thought or observation.
                You can always consult the following:
                    - the user / human (to get info from user. Remember to use this less.),
                    - the reviewer (to get a review on your work so far, remember to use this atleast once),
                    - the executor (to execute your tools)

                Example Session(print this stuff out. things in <> are my comments not how you should actually put in there):
                message: Put all videos in this directory in a seperate folder in this directory

                Thought: I should find videos in this directory.
                Action: <You execute your action here>
                PAUSE

                <Yields to other agent>

                Observation: ... are videos in this directory
            """
        )

        read_file_tool.register_for_llm(self)
        list_directory_tool.register_for_llm(self)
        file_search_tool.register_for_llm(self)
        get_current_directory_tool.register_for_llm(self)
        check_command_tool.register_for_llm(self)
        show_directory_tree_tool.register_for_llm(self)

        self.executor = ConversableAgent(
            name="InfoCollectorExecutorAgent",
            human_input_mode="NEVER"
        )

        read_file_tool.register_for_execution(self.executor)
        list_directory_tool.register_for_execution(self.executor)
        file_search_tool.register_for_execution(self.executor)
        get_current_directory_tool.register_for_execution(self.executor)
        check_command_tool.register_for_execution(self.executor)

        self.reviewer = ConversableAgent(
            name="InfoCollectorReviewerAgent",
            llm_config=llm_config,
            system_message="""
                You are an intelligent review agent for a terminal AI system. Your primary
                role is to critically analyze the information gathered by the info collector
                and identify any gaps, inconsistencies, or overlooked details that could
                cause the execution plan to fail. Carefully examine the extracted information 
                for completeness and accuracy, considering all possible edge cases,
                dependencies, and system constraints. Suggest additional checks or data points
                the info collector should gather to address any potential failure points.
                Anticipate issues that could arise during execution, such as missing environment
                variables, unavailable commands, conflicting dependencies, or incorrect system
                configurations. Encourage the info collector to use all available tools and
                verify critical assumptions. Your goal is to ensure the info collector provides
                a complete and accurate execution context so the plan creator agent can generate
                a flawless plan.

                Remember to ask the info collector which analyses are feasible with the tools
                it possesses and limit additional analysis by the collector to those ones
            """
        )
        
        read_file_tool.register_for_execution(self.reviewer)
        list_directory_tool.register_for_execution(self.reviewer)
        file_search_tool.register_for_execution(self.reviewer)
        get_current_directory_tool.register_for_execution(self.reviewer)
        check_command_tool.register_for_execution(self.reviewer)

        llm_config_structured = {
            "config_list": [
                {
                    
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": key,
                    "response_format": InfoCollectorOutput
                }
            ]
        }

        self.formatter = ConversableAgent(
            name="InfoCollectorFormatter",
            description="The final agent which will run and format all collected info",
            llm_config=llm_config_structured,
            system_message="""
                You are responsible for formatting all information and context
                you have understood from the conversation. You are the final agent
                that will be run
            """
        )


    def run_pipeline(self, query: str) -> InfoCollectorOutput:
        llm_config = {
            "config_list": [
                {
                    
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": self.key
                }
            ]
        }

        the_human = ConversableAgent(
            name="human",
            human_input_mode="ALWAYS",
        )

        groupchat = GroupChat(
            agents=[
                the_human,
                self,
                self.executor,
                self.reviewer,
                self.formatter
            ],
            speaker_selection_method="auto",
            messages=[],
        )

        manager = GroupChatManager(
            name="group_manager",
            groupchat=groupchat,
            llm_config=llm_config,
        )

        result = the_human.initiate_chats(
            chat_queue = [
                {
                    "recipient": manager,
                    "message": "Collect info for getting this help: {}".format(query),
                    "summary_method": "reflection_with_llm"
                },

                {
                    "recipient": self.formatter,
                    "max_turn": 1,
                    "summary_method": "last_msg"
                }
            ]
        )

        return InfoCollectorOutput.model_validate_json(result[-1])
