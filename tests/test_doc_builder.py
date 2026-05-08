import unittest
from datetime import date
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import (
    AdditionalsListedSectionContent,
    DocModel,
    SectionContent,
    SectionContentDescriptions,
    UserInfo,
)


def make_model(section_title: str, entries: list[SectionContent]) -> DocModel:
    return DocModel(
        user_info=UserInfo(
            full_name="Test User",
            email="test@example.com",
            phone="555-555-5555",
            links=["example.com"],
            city_province="Calgary, AB",
        ),
        sections={section_title: entries},
        additionals=AdditionalsListedSectionContent(title="Skills", items={}),
    )


class DocBuilderTests(unittest.TestCase):
    def test_single_entry_section_wrapper_renders_section_title_once(self):
        model = make_model(
            "Summary",
            [
                SectionContent(
                    title="Summary",
                    left_subheader="",
                    right_subheader="",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Focused front-end developer.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2025, 6, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        self.assertEqual(tex.count(r"\textbf{Summary}"), 1)
        self.assertNotIn(r"\textbf{Jun 2025}", tex)
        self.assertNotIn(r"\textit{}%", tex)
        self.assertNotIn(
            "\n\\newline%\n\\linebreak%\n\\begin{itemize}",
            tex,
        )
        self.assertIn("Focused front{-}end developer.", tex)

    def test_user_contact_email_and_links_are_clickable(self):
        model = make_model("Experience", [])
        model.user_info = UserInfo(
            full_name="Test User",
            email="test@example.com",
            phone="555-555-5555",
            links=[
                "github.com/quyanna_resume",
                "https://www.linkedin.com/in/test-user",
            ],
            city_province="Calgary, AB",
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        self.assertIn(r"\usepackage[hidelinks]{hyperref}", tex)
        self.assertIn(
            r"\href{mailto:test@example.com}{test@example.com}",
            tex,
        )
        self.assertIn(
            r"\href{https://github.com/quyanna_resume}{github.com/quyanna\_resume}",
            tex,
        )
        self.assertIn(
            r"\href{https://www.linkedin.com/in/test-user}"
            r"{https://www.linkedin.com/in/test{-}user}",
            tex,
        )

    def test_single_entry_section_wrapper_adds_gap_before_next_section(self):
        model = DocModel(
            user_info=UserInfo(
                full_name="Test User",
                email="test@example.com",
                phone="555-555-5555",
                links=["example.com"],
                city_province="Calgary, AB",
            ),
            sections={
                "Summary": [
                    SectionContent(
                        title="Summary",
                        left_subheader="",
                        right_subheader="",
                        sub_sections=[
                            SectionContentDescriptions(
                                description="Focused front-end developer.",
                                sub_sections=[],
                            )
                        ],
                        start_date=date(2025, 6, 1),
                    )
                ],
                "Projects": [
                    SectionContent(
                        title="Portfolio Website",
                        left_subheader="React, TypeScript",
                        right_subheader="github.com/quyanna/portfolio",
                        sub_sections=[
                            SectionContentDescriptions(
                                description="Built a responsive project portfolio.",
                                sub_sections=[],
                            )
                        ],
                        start_date=date(2026, 1, 1),
                    )
                ],
            },
            additionals=AdditionalsListedSectionContent(title="Skills", items={}),
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        summary_start = tex.index(r"\textbf{Summary}")
        summary_end = tex.index(r"\end{minipage}", summary_start)
        projects_start = tex.index(r"\textbf{Projects}")

        self.assertIn(r"\vspace*{0.25cm}", tex[summary_end:projects_start])

    def test_regular_single_entry_section_keeps_entry_header(self):
        model = make_model(
            "Education",
            [
                SectionContent(
                    title="University of Calgary",
                    left_subheader="Bachelor of Science",
                    right_subheader="Calgary, AB",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Graduated June 2025",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2020, 9, 1),
                    end_date=date(2025, 6, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        self.assertIn(r"\textbf{Education}", tex)
        self.assertIn(r"\textbf{University of Calgary}", tex)
        self.assertIn(r"\textit{Bachelor of Science}", tex)
        self.assertIn(r"\textit{Calgary, AB}", tex)

    def test_multi_entry_section_does_not_wrap_all_entries_in_one_minipage(self):
        model = make_model(
            "Experience",
            [
                SectionContent(
                    title="First Company",
                    left_subheader="Developer",
                    right_subheader="Calgary, AB",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Built internal tooling.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2024, 1, 1),
                ),
                SectionContent(
                    title="Second Company",
                    left_subheader="Developer",
                    right_subheader="Calgary, AB",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Improved operational workflows.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2025, 1, 1),
                ),
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        first_entry = tex.index(r"\textbf{First Company}")
        second_entry = tex.index(r"\textbf{Second Company}")
        minipage_end_between_entries = tex.find(r"\end{minipage}", first_entry, second_entry)

        self.assertNotEqual(-1, minipage_end_between_entries)
        self.assertIn(
            "\\end{minipage}%\n\\par%",
            tex[minipage_end_between_entries : minipage_end_between_entries + 40],
        )

    def test_entry_header_rows_use_bounded_columns_for_long_right_text(self):
        model = make_model(
            "Projects",
            [
                SectionContent(
                    title="Long URL Project",
                    left_subheader="JavaScript, HTML/CSS, Webpack",
                    right_subheader=(
                        "very-long-subdomain.example.com/quyanna/project-with-a-long-path"
                        " | github.com/quyanna/project-with-a-long-path"
                    ),
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Built a project with a long public URL.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2026, 1, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        self.assertIn(r"\parbox[t]{0.67\textwidth}", tex)
        self.assertIn(r"\parbox[t]{0.30\textwidth}", tex)
        self.assertIn(r"\raggedleft", tex)

    def test_entry_header_adds_small_gap_between_title_and_subheaders(self):
        model = make_model(
            "Projects",
            [
                SectionContent(
                    title="Portfolio Website",
                    left_subheader="React, TypeScript",
                    right_subheader="github.com/quyanna/portfolio",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Built a responsive project portfolio.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2026, 1, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        title_row = tex.index(r"\textbf{Portfolio Website}")
        subheader_row = tex.index(r"\textit{React, TypeScript}")

        self.assertIn("\\par%\n\\vspace{0.03cm}", tex[title_row:subheader_row])

    def test_section_title_rule_spacing_is_balanced(self):
        model = make_model(
            "Summary",
            [
                SectionContent(
                    title="Summary",
                    left_subheader="",
                    right_subheader="",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Focused front-end developer.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2025, 6, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        self.assertIn(
            "\\noindent{\\Large\\textbf{Summary}}\\\\[-0.19cm]%\n"
            "\\noindent\\rule{\\textwidth}{0.5pt}%\n"
            "\\par%\n\\vspace{0.03cm}",
            tex,
        )
        self.assertNotIn("\\par%\n\\vspace{-0.08cm}%\n\\noindent\\rule", tex)
        self.assertNotIn("\\end{Large}%\n\\par%\n\\vspace{0.03cm}", tex)
        self.assertNotIn("\\vspace{0.02cm}%\n\\newline%", tex)

    def test_additionals_list_is_created_inside_its_section_without_extra_newline_gap(self):
        model = make_model("Experience", [])
        model.additionals = AdditionalsListedSectionContent(
            title="Technical Skills",
            items={"Front-End": ["React", "TypeScript"]},
        )

        builder = DocBuilder(model, "test")
        builder.build()
        tex = builder.doc.dumps()

        skills_start = tex.index(r"\textbf{Technical Skills}")
        skills_tex = tex[skills_start:]

        self.assertIn(
            "\\vspace{0.03cm}%\n%\n\\begin{itemize}"
            "[nosep, topsep=0pt, partopsep=0pt, leftmargin=*, itemsep=1.5pt, parsep=0pt]",
            skills_tex,
        )
        self.assertNotIn("\\newline%\n\\begin{itemize}", skills_tex)

    def test_export_raises_when_latex_fails(self):
        model = make_model(
            "Summary",
            [
                SectionContent(
                    title="Summary",
                    left_subheader="",
                    right_subheader="",
                    sub_sections=[
                        SectionContentDescriptions(
                            description="Focused front-end developer.",
                            sub_sections=[],
                        )
                    ],
                    start_date=date(2025, 6, 1),
                )
            ],
        )

        builder = DocBuilder(model, "test_compile_failure")
        builder.build()

        try:
            with patch(
                "doc_utils.doc_builder.subprocess.run",
                return_value=SimpleNamespace(returncode=1),
            ):
                with self.assertRaises(RuntimeError):
                    builder.export()
        finally:
            Path("output/test_compile_failure.tex").unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
