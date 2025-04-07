from typing import List
from pydantic import BaseModel

class InfoCollectorOutput(BaseModel):
    information: List[str]

class PlannerSteps(BaseModel):
    description: str
    cli_command: str

class PlannerOutputs(BaseModel):
    steps: List[PlannerSteps]

class PlannerScriptmakerOutput(BaseModel):
    script: str
