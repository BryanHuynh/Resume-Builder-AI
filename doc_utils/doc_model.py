from typing import Dict, List, Optional
from datetime import date
from pydantic import BaseModel


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
    description: str
    sub_sections: List["SectionContentDescriptions"]


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
