from typing import List
from pydantic import BaseModel

class InfoCollectorOutput(BaseModel):
    information: List[str]
