from sqlalchemy import select, delete

from db.database import get_session
from db.entities.user import User
from db.entities.section import Section
from db.entities.additional import Additional
from doc_utils.doc_model import DocModel, SectionContent

def upsert_user(user_id: str, doc_model: DocModel):
    """Upsert a user and their full resume data (sections + additionals)."""
    info = doc_model.user_info
    with get_session() as session:
        user = session.get(User, user_id)
        if user is None:
            user = User(
                id=user_id,
                full_name=info.full_name,
                email=info.email,
                phone=info.phone,
                city_province=info.city_province,
                links=info.links,
            )
            session.add(user)
        else:
            user.full_name = info.full_name
            user.email = info.email
            user.phone = info.phone
            user.city_province = info.city_province
            user.links = info.links

        for section_name, entries in doc_model.sections.items():
            for sort_order, entry in enumerate(entries):
                section = Section(
                    user_id=user_id,
                    section_name=section_name,
                    content=entry.model_dump(mode="json"),
                    sort_order=sort_order,
                )
                session.add(section)

        additional = Additional(
            user_id=user_id,
            title=doc_model.additionals.title,
            items=doc_model.additionals.items,
        )
        session.add(additional)


def get_user_resume(user_id: str) -> DocModel | None:
    """Load a full resume from DB and reconstruct a DocModel."""
    with get_session() as db:
        user = db.get(User, user_id)
        if user is None:
            return None

        sections_rows = (
            db.execute(
                select(Section)
                .where(Section.user_id == user_id)
                .order_by(Section.section_name, Section.sort_order)
            )
            .scalars()
            .all()
        )

        additional_row = (
            db.execute(select(Additional).where(Additional.user_id == user_id))
            .scalars()
            .first()
        )

        # Build sections dict
        sections: dict[str, list] = {}
        for row in sections_rows:
            sections.setdefault(row.section_name, []).append(row.content)

        # Build additionals
        additionals = {
            "title": additional_row.title if additional_row else "",
            "items": additional_row.items if additional_row else {},
        }

        resume_data = {
            "user_info": {
                "full_name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "links": user.links or [],
                "city_province": user.city_province or "",
            },
            "sections": sections,
            "additionals": additionals,
        }
        return DocModel.model_validate(resume_data)


def get_user_resume_json(user_id: str) -> str | None:
    """Return the user's resume as a JSON string, or None if not found."""
    doc_model = get_user_resume(user_id)
    if doc_model is None:
        return None
    return doc_model.model_dump_json(indent=2)
