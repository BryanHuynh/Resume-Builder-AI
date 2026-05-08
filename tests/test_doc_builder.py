import unittest
from datetime import date

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


if __name__ == "__main__":
    unittest.main()
