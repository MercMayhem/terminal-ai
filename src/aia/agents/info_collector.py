from autogen import ConversableAgent
from tools.shell import check_command_tool
from tools.filesystem import read_file_tool, get_current_directory_tool, list_directory_tool, file_search_tool

# Subtyping for abstracting over tool registration and llm_config
class InfoCollectorAgent(ConversableAgent):
    def __init__(self, key: str) -> None:
        llm_config = {
            "config_list": [
                {
                    
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": key
                }
            ]
        }

        super().__init__(
            name="InfoCollectorAgent",
            llm_config=llm_config,
            system_message="""
                You are an intelligent information-gathering agent for a terminal AI system.
                Your primary role is to accurately understand user queries, gather all relevant
                information about the execution context (e.g., system state, environment variables,
                resource availability, user intent), and provide this information to the plan
                creator agent. Be thorough and investigate all possible angles and edge cases
                related to the query. Do not assume anything—always verify the information from
                reliable sources or system state before passing it to the plan creator agent.
                Collect both high-level and low-level details to ensure the plan creator agent
                has a complete picture. Prioritize accuracy and relevance—filter out noise and
                ambiguity while ensuring the information covers the full execution context.
                Your goal is to enable the plan creator agent to generate a flawless execution
                plan by providing complete and reliable information.
            """
        )

        read_file_tool.register_tool(self)
        list_directory_tool.register_tool(self)
        file_search_tool.register_tool(self)
        get_current_directory_tool.register_tool(self)
        check_command_tool.register_tool(self)

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

