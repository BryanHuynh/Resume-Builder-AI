import json
import uuid
import httpx
from pathlib import Path
from typing import Container
from config import AWS_PDF_FUNCTION_URL
from doc_utils.doc_model import (
    AdditionalsListedSectionContent,
    DocModel,
    SectionContentDescriptions,
    SectionContent,
    UserInfo,
)
import doc_utils.doc_config as config
from pylatex import (
    Document,
    HugeText,
    LargeText,
    LineBreak,
    MediumText,
    SmallText,
    MiniPage,
    VerticalSpace,
    Itemize,
    Command,
    HFill,
    NoEscape,
)
from pylatex.utils import bold, italic
import doc_utils.doc_tools as tools

output_dir = Path("output")


class DocBuilder:
    def __init__(self, model: DocModel, export_name: str):
        self.model = model
        self.export_name = export_name
        self.doc = Document(self.export_name, geometry_options=config.geometry_options)
        self.doc.preamble.append(config.enum_item_package)
        tools.DocumentFont("ebgaramond").add_to_document(self.doc)
        self.doc.preamble.append(config.get_font_size_preamble())

    def build(self):
        self.build_header(self.model.user_info)
        for section_title, section_entries in self.model.sections.items():
            self.build_section(section_title, section_entries)
            self.doc.append(LineBreak())
        self.build_additionals(self.model.additionals)
        return self

    async def export(self) -> dict:
        latex_str = self.doc.dumps()
        filename = str(uuid.uuid4())
        async with httpx.AsyncClient() as client:
            response = await client.post(
                AWS_PDF_FUNCTION_URL,
                json={"latex": latex_str, "filename": filename}
            )
            result = response.json()
            return result
        
    def build_header(self, user_info: UserInfo):
        with self.doc.create(MiniPage(align="c")) as header:
            header.append(HugeText(bold(user_info.full_name)))
            header.append(VerticalSpace("0.1cm"))
            header.append(LineBreak())
            header.append(SmallText(user_info.to_string()))
            header.append(VerticalSpace("0.25cm"))
        self.doc.append(LineBreak())

    def build_section(self, section_title: str, section_entries: list[SectionContent]):
        with self.doc.create(MiniPage(align="l")) as section:
            section.append(tools.SectionTitle(section_title, section))
            for entry in section_entries:
                self.build_section_entry(entry, section=section)
                section.append(VerticalSpace("0.25cm"))

    def build_section_entry(self, entry: SectionContent, section: MiniPage):
        section.append(LargeText(bold(entry.title)))
        section.append(HFill())
        date_str = entry.start_date.strftime("%b %Y")
        if entry.end_date:
            date_str += f" - {entry.end_date.strftime('%b %Y')}"
        section.append(MediumText(bold(date_str)))
        section.append(LineBreak())
        section.append(MediumText(italic(entry.left_subheader)))
        section.append(HFill())
        section.append(MediumText(italic(entry.right_subheader)))
        if len(entry.sub_sections) > 0:
            section.append(LineBreak())
            with section.create(
                Itemize(options=config.itemize_options)
            ) as itemizer:
                section.append(Command("vspace", NoEscape("-10pt")))
                for description in entry.sub_sections:
                    self.build_section_content(itemizer, description)

                


    def build_section_content(
        self, itemizer: Itemize, section_content: SectionContentDescriptions
    ):
        itemizer.add_item(section_content.description)
        if len(section_content.sub_sections) > 0:
            with itemizer.create(
                Itemize(options=config.sub_itemize_options)
            ) as sub_itemizer:
                for sub_section in section_content.sub_sections:
                    self.build_section_content(sub_itemizer, sub_section)

    def build_additionals(self, additionals: AdditionalsListedSectionContent):
        with self.doc.create(MiniPage(align="l")) as additionals_section:
            self.doc.append(tools.SectionTitle(additionals.title, additionals_section))
            with self.doc.create(Itemize(options=config.itemize_options)) as itemizer:
                self.doc.append(Command("vspace", NoEscape("-15pt")))
                for item_name, item_values in additionals.items.items():
                    itemizer.add_item(SmallText(bold(f"{item_name}: ")))
                    itemizer.append(SmallText(", ".join(item_values)))
