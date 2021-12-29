# -*- coding: utf-8 -*-

from dataclasses import dataclass, asdict
from typing import List, Optional

class BaseModel:
    def dict(self) -> dict:
        return asdict(self)

@dataclass
class ParameterError(BaseModel):
    field: str
    error: str

@dataclass
class MutationResponse(BaseModel):
    success: bool
    errors: Optional[List[ParameterError]]
