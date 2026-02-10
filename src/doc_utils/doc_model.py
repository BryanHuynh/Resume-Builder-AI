from typing import Any, Dict, List, Optional
from datetime import date
from pydantic import BaseModel, Field, model_validator


def _inline_recursive_subsections(schema: Dict[str, Any]) -> None:
    base = {
        "type": "object",
        "properties": {"description": {"type": "string"}},
        "required": ["description"],
    }
    d3 = dict(base)
    d2 = {**base, "properties": {**base["properties"], "sub_sections": {
        "anyOf": [{"items": d3, "type": "array"}, {"type": "null"}], "default": [],
    }}}
    d1 = {**base, "properties": {**base["properties"], "sub_sections": {
        "anyOf": [{"items": d2, "type": "array"}, {"type": "null"}], "default": [],
    }}}
    props = schema.get("properties", {})
    if "sub_sections" in props:
        props["sub_sections"] = {
            "anyOf": [{"items": d1, "type": "array"}, {"type": "null"}],
            "default": [],
        }


class UserInfo(BaseModel):
    full_name: str
    email: str
    phone: str
    links: List[str]
    city_province: str

    def to_string(self) -> str:
        return " | ".join(
            [self.email, self.phone, self.city_province, " | ".join(self.links)]
        )


class SectionContentDescriptions(BaseModel):
    model_config = {"json_schema_extra": _inline_recursive_subsections}

    description: str
    sub_sections: Optional[List["SectionContentDescriptions"]] = []

    @model_validator(mode="after")
    def validate_depth(self) -> "SectionContentDescriptions":
        def check_depth(
            node: "SectionContentDescriptions", current_depth: int = 0
        ) -> int:
            if current_depth > 3:  # Maximum allowed depth
                raise ValueError("Maximum depth exceeded")
            if node.sub_sections is None:
                return current_depth
            return max(
                [check_depth(child, current_depth + 1) for child in node.sub_sections],
                default=current_depth,
            )

        check_depth(self)
        return self


SectionContentDescriptions.model_rebuild(force=True)


class SectionContent(BaseModel):
    title: str
    left_subheader: str
    right_subheader: str
    sub_sections: List[SectionContentDescriptions]
    start_date: date
    end_date: Optional[date] = None


class AdditionalsListedSectionContent(BaseModel):
    title: str
    items: Dict[str, List[str]]


class DocModel(BaseModel):
    user_info: UserInfo
    sections: Dict[str, List[SectionContent]]
    additionals: AdditionalsListedSectionContent
