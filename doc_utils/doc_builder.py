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
    LineBreak,
    SmallText,
    MiniPage,
    VerticalSpace,
    Itemize,
    NoEscape,
)
from pylatex.utils import bold, escape_latex
import doc_utils.doc_tools as tools

output_dir = Path("output")


class DocBuilder:
    def __init__(self, model: DocModel, export_name: str):
        self.model = model
        self.export_name = export_name
        self.doc = Document(self.export_name, geometry_options=config.geometry_options)
        self.doc.preamble.append(config.enum_item_package)
        self.doc.preamble.append(config.hyperref_package)
        self.doc.preamble.append(config.no_par_indent)
        tools.DocumentFont("ebgaramond").add_to_document(self.doc)
        self.doc.preamble.append(config.get_font_size_preamble())

    def build(self):
        self.build_header(self.model.user_info)
        for section_title, section_entries in self.model.sections.items():
            self.build_section(section_title, section_entries)
            self.doc.append(NoEscape(r"\par"))
        self.build_additionals(self.model.additionals)

    def export(self):
        tex_path = output_dir / self.export_name
        self.doc.generate_tex(str(tex_path))
        result = subprocess.run(
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
        if result.returncode != 0:
            raise RuntimeError(f"pdflatex failed while generating {tex_path}.pdf")
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
            header.append(SmallText(NoEscape(self.format_contact_line(user_info))))
            header.append(VerticalSpace("0.25cm"))
        self.doc.append(NoEscape(r"\par"))

    def format_contact_line(self, user_info: UserInfo) -> str:
        contact_items = [
            self.format_clickable_contact(user_info.email, f"mailto:{user_info.email}"),
            escape_latex(user_info.phone),
            escape_latex(user_info.city_province),
        ]
        contact_items.extend(
            self.format_clickable_contact(link, self.link_target(link))
            for link in user_info.links
        )
        return " | ".join(contact_items)

    def format_clickable_contact(self, display_text: str, target: str) -> str:
        return (
            rf"\href{{{self.escape_href_target(target)}}}"
            rf"{{{escape_latex(display_text)}}}"
        )

    def link_target(self, link: str) -> str:
        if "://" in link or link.startswith("mailto:"):
            return link
        return f"https://{link}"

    def escape_href_target(self, target: str) -> str:
        return (
            target.replace("\\", r"\textbackslash{}")
            .replace("{", r"\{")
            .replace("}", r"\}")
        )

    def build_section(self, section_title: str, section_entries: list[SectionContent]):
        self.doc.append(tools.SectionTitle(section_title, self.doc))
        if self.is_single_entry_section_wrapper(section_title, section_entries):
            with self.doc.create(MiniPage(align="l")) as section:
                self.build_section_entry_content(
                    section_entries[0],
                    section=section,
                    include_leading_linebreak=False,
                )
            self.doc.append(NoEscape(r"\par"))
            self.doc.append(VerticalSpace("0.25cm"))
        else:
            for entry in section_entries:
                with self.doc.create(MiniPage(align="l")) as section:
                    self.build_section_entry(entry, section=section)
                self.doc.append(NoEscape(r"\par"))
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
        date_str = entry.start_date.strftime("%b %Y")
        if entry.end_date:
            date_str += f" - {entry.end_date.strftime('%b %Y')}"
        self.append_bounded_row(
            section,
            entry.title,
            date_str,
            text_command="textbf",
            bottom_space="0.03cm",
        )
        self.append_bounded_row(
            section,
            entry.left_subheader,
            entry.right_subheader,
            text_command="textit",
        )
        self.build_section_entry_content(
            entry,
            section=section,
            include_leading_linebreak=False,
        )

    def append_bounded_row(
        self,
        section: MiniPage,
        left_text: str,
        right_text: str,
        text_command: str,
        bottom_space: str | None = None,
    ):
        left = escape_latex(left_text)
        right = escape_latex(right_text)
        row_spacing = rf"%{chr(10)}\vspace{{{bottom_space}}}" if bottom_space else ""
        section.append(
            NoEscape(
                rf"\noindent"
                rf"\parbox[t]{{0.67\textwidth}}{{\raggedright\large\{text_command}{{{left}}}}}"
                rf"\hfill"
                rf"\parbox[t]{{0.30\textwidth}}{{\raggedleft\large\{text_command}{{{right}}}}}"
                "\n"
                rf"\par{row_spacing}"
            )
        )

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
            additionals_section.append(
                tools.SectionTitle(additionals.title, additionals_section)
            )
            with additionals_section.create(
                Itemize(options=config.additionals_itemize_options)
            ) as itemizer:
                for item_name, item_values in additionals.items.items():
                    itemizer.add_item(SmallText(bold(f"{item_name}: ")))
                    itemizer.append(SmallText(", ".join(item_values)))
