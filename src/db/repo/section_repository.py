from doc_utils.doc_model import DocModel, SectionContent
from db.entities.section import Section
from db.database import get_session
from sqlalchemy import select, delete


def upsert_section(
    user_id: str, section_name: str, content: SectionContent, order: int = 0
):
    with get_session() as session:
        stmt = select(Section).where(
            Section.user_id == user_id, Section.section_name == section_name
        )
        sections = session.execute(stmt).scalars().all()
        section = next(
            (s for s in sections if s.content["title"] == content.title),
            None,
        )
        if section is None:
            section = Section(
                user_id=user_id,
                section_name=section_name,
                content=content.model_dump(mode="json"),
                sort_order=order,
            )
            session.add(section)
            session.commit()
        else:
            section.content = content.model_dump(mode="json")
            session.commit()


def get_all_sections(user_id: str) -> list[Section]:
    with get_session() as session:
        stmt = select(Section).where(Section.user_id == user_id)
        return session.execute(stmt).scalars().all()
