import subprocess
from pathlib import Path
from typing import Container
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

    def export(self):
        tex_path = output_dir / self.export_name
        self.doc.generate_tex(str(tex_path))
        subprocess.run(
            [
                "pdflatex",
                "-interaction=batchmode",
                "-halt-on-error",
                f"-output-directory={output_dir}",
                f"{tex_path}.tex",
            ],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=30,
        )
        # Clean aux files
        for ext in [".aux", ".log"]:
            aux = tex_path.with_suffix(ext)
            if aux.exists():
                aux.unlink()
        return Path(f"{tex_path}.pdf")

    def build_header(self, user_info: UserInfo):
        with self.doc.create(MiniPage(align="c")) as header:
            header.append(HugeText(bold(user_info.full_name)))
            header.append(VerticalSpace("0.1cm"))
            header.append(LineBreak())
            header.append(SmallText(user_info.to_string()))
            header.append(VerticalSpace("0.25cm"))
        self.doc.append(LineBreak())

    def build_section(self, section_title: str, section_entries: list[SectionContent]):
        self.doc.append(tools.SectionTitle(section_title, self.doc))
        if self.is_single_entry_section_wrapper(section_title, section_entries):
            with self.doc.create(MiniPage(align="l")) as section:
                self.build_section_entry_content(
                    section_entries[0],
                    section=section,
                    include_leading_linebreak=False,
                )
        else:
            for entry in section_entries:
                with self.doc.create(MiniPage(align="l")) as section:
                    self.build_section_entry(entry, section=section)
                self.doc.append(VerticalSpace("0.25cm"))

    def is_single_entry_section_wrapper(
        self, section_title: str, section_entries: list[SectionContent]
    ) -> bool:
        if len(section_entries) != 1:
            return False

        entry = section_entries[0]
        return (
            entry.title.strip().casefold() == section_title.strip().casefold()
            and entry.left_subheader.strip() == ""
            and entry.right_subheader.strip() == ""
        )

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
        self.build_section_entry_content(entry, section=section)

    def build_section_entry_content(
        self,
        entry: SectionContent,
        section: MiniPage,
        include_leading_linebreak: bool = True,
    ):
        if len(entry.sub_sections) > 0:
            if include_leading_linebreak:
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
