from typing import Optional

from pydantic import BaseModel, field_validator


class Field(BaseModel):
    auto_id: Optional[bool] = False
    name: str
    dtype: str
    description: Optional[str] = ''
    is_primary: Optional[bool] = False
    dim: Optional[int] = 512
    enable_dynamic_field: Optional[bool] = False

    @field_validator('dtype')
    @classmethod
    def name_must_contain_space(cls, var: str) -> str:
        # Aquí puedes agregar validaciones personalizadas para dtype si es necesario
        return var.title()