import unittest
from datetime import date

from core.tools import (
    _delete_resume_additional_subsection,
    _delete_resume_section,
    _delete_resume_subsection,
    _get_catered_resume_outline_from_model,
    _upsert_resume_additional_subsection,
    _upsert_resume_additionals,
    _upsert_resume_section,
    _upsert_resume_subsection,
)
from doc_utils.doc_model import (
    AdditionalsListedSectionContent,
    DocModel,
    SectionContent,
    SectionContentDescriptions,
    UserInfo,
)


def _entry(title: str, description: str = "Did useful work") -> SectionContent:
    return SectionContent(
        title=title,
        left_subheader="Company",
        right_subheader="City, AB",
        start_date=date(2023, 1, 1),
        end_date=None,
        sub_sections=[SectionContentDescriptions(description=description)],
    )


def _resume() -> DocModel:
    return DocModel(
        user_info=UserInfo(
            full_name="Test User",
            email="test@example.com",
            phone="555-555-5555",
            links=["https://example.com"],
            city_province="Calgary, AB",
        ),
        sections={
            "Work Experience": [_entry("Developer"), _entry("Analyst")],
            "Projects": [_entry("Resume Editor", "Built a resume editor")],
        },
        additionals=AdditionalsListedSectionContent(
            title="Skills",
            items={"Languages": ["Python"], "Tools": ["Git"]},
        ),
    )


class CateredResumeCrudTest(unittest.TestCase):
    def test_outline_lists_sections_and_subsections_without_bullet_text(self):
        outline = _get_catered_resume_outline_from_model(_resume())

        self.assertEqual(outline["user"], "Test User")
        self.assertEqual(
            outline["sections"][0],
            {
                "name": "Work Experience",
                "subsections": [
                    {"index": 0, "title": "Developer"},
                    {"index": 1, "title": "Analyst"},
                ],
            },
        )
        self.assertEqual(
            outline["additionals"], {"title": "Skills", "keys": ["Languages", "Tools"]}
        )

    def test_upsert_and_delete_section_operate_on_whole_sections(self):
        resume = _resume()
        replacement = [_entry("New Role", "Owned the new role")]

        updated, replaced = _upsert_resume_section(
            resume, "Work Experience", replacement
        )
        self.assertTrue(replaced)
        self.assertEqual(updated.sections["Work Experience"], replacement)
        self.assertEqual(len(resume.sections["Work Experience"]), 2)

        updated, replaced = _upsert_resume_section(updated, "Leadership", [_entry("Lead")])
        self.assertFalse(replaced)
        self.assertIn("Leadership", updated.sections)

        updated, deleted = _delete_resume_section(updated, "Projects")
        self.assertTrue(deleted)
        self.assertNotIn("Projects", updated.sections)

    def test_upsert_and_delete_subsection_operate_on_whole_entries(self):
        resume = _resume()
        replacement = _entry("Developer", "Reduced tokens")

        updated, replaced = _upsert_resume_subsection(
            resume, "Work Experience", replacement
        )
        self.assertTrue(replaced)
        self.assertEqual(
            updated.sections["Work Experience"][0].sub_sections[0].description,
            "Reduced tokens",
        )
        self.assertEqual(
            resume.sections["Work Experience"][0].sub_sections[0].description,
            "Did useful work",
        )

        new_entry = _entry("Manager")
        updated, replaced = _upsert_resume_subsection(updated, "Work Experience", new_entry)
        self.assertFalse(replaced)
        self.assertEqual(updated.sections["Work Experience"][-1].title, "Manager")

        updated, deleted = _delete_resume_subsection(updated, "Work Experience", "Analyst")
        self.assertTrue(deleted)
        self.assertEqual(
            [entry.title for entry in updated.sections["Work Experience"]],
            ["Developer", "Manager"],
        )

    def test_upsert_and_delete_additionals_operate_on_whole_subsections(self):
        resume = _resume()
        replacement = AdditionalsListedSectionContent(
            title="Technical Skills",
            items={"Languages": ["Python", "TypeScript"]},
        )

        updated = _upsert_resume_additionals(resume, replacement)
        self.assertEqual(updated.additionals.title, "Technical Skills")
        self.assertEqual(resume.additionals.title, "Skills")

        updated, replaced = _upsert_resume_additional_subsection(
            updated, "Tools", ["Git", "Docker"]
        )
        self.assertFalse(replaced)
        self.assertEqual(updated.additionals.items["Tools"], ["Git", "Docker"])

        updated, replaced = _upsert_resume_additional_subsection(
            updated, "Tools", ["GitHub Actions"]
        )
        self.assertTrue(replaced)
        self.assertEqual(updated.additionals.items["Tools"], ["GitHub Actions"])

        updated, deleted = _delete_resume_additional_subsection(updated, "Languages")
        self.assertTrue(deleted)
        self.assertNotIn("Languages", updated.additionals.items)


if __name__ == "__main__":
    unittest.main()
