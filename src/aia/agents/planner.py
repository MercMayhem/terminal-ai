from autogen import ConversableAgent
from ..models import PlannerOutputs, PlannerScriptmakerOutput
import json
from pydantic import parse_obj_as


class PlannerAgent(ConversableAgent):

    def __init__(self, key: str) -> None:
        self.key = key

        llm_config = {
            "config_list": [
                {
                    
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": key,
                    "response_format": PlannerOutputs
                }
            ]
        }

        super().__init__(
            name="PlannerAgent",
            llm_config=llm_config,
            system_message="""
                You are the Planner Agent, responsible for analyzing the system state collected by the Info Collector Agent and generating an efficient, step-by-step execution plan.

                Responsibilities:
                1. Interpret System State – Process the collected information and determine necessary actions to achieve the user’s goal.
                2. Generate Optimized Plans – Create a structured, logical sequence of actions that balances efficiency, reliability, and minimal disruption.
                3. Generate CLI Commands - generate CLI commands which will execute the plans which have been created
            """
        )

        llm_config = {
            "config_list": [
                {
                    "api_type": "openai",
                    "model": "gpt-4o-mini",
                    "api_key": key,
                    "response_format": PlannerScriptmakerOutput
                }
            ]
        }

        self.scriptmaker = ConversableAgent(
            name="PlannerScriptmaker",
            description="Takes the output of the planner and incorporates commands and its plans to a bash script",
            llm_config=llm_config,
            system_message="""
                You are responsible for taking in the output of the planner
                and integrating its steps into a bash script
            """
        )

    def run_pipeline(self, information: str) -> PlannerScriptmakerOutput:
        # result = self.run(f"Info collected: {information}", summary_method="last_msg")
        the_human = ConversableAgent(
            name="human",
            human_input_mode="ALWAYS",
        )

        result = the_human.initiate_chats(
            chat_queue = [
                {
                    "recipient": self,
                    "message": f"Info collected: {information}",
                    "summary_method": "last_msg"
                },

                {
                    "recipient": self.scriptmaker,
                    "message": "create the script",
                    "summary_method": "last_msg"
                },
            ]
        )

        summary_data = json.loads(result[-1].summary)
        return parse_obj_as(PlannerScriptmakerOutput, summary_data)

