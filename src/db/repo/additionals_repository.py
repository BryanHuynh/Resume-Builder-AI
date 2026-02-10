from doc_utils.doc_model import DocModel, SectionContent
from db.entities.additional import Additional as Additional_db
from doc_utils.doc_model import AdditionalsListedSectionContent
from db.database import get_session
from sqlalchemy import select, delete


def upsert_additionals(
    user_id: str, title: str, content: AdditionalsListedSectionContent
):
    with get_session() as session:
        stmt = select(Additional_db).where(
            content.user_id == user_id, content.title == title
        )
        additional = session.execute(stmt).scalars().first()
        if additional is None:
            additional = Additional_db(
                user_id=user_id,
                title=title,
                items=content.items,
            )
            session.add(additional)
            session.commit()
        else:
            additional.items = content.items
            session.commit()


def get_additionals(user_id: str, title: str) -> AdditionalsListedSectionContent | None:
    with get_session() as session:
        stmt = select(Additional_db).where(
            Additional_db.user_id == user_id, Additional_db.title == title
        )
        additional = session.execute(stmt).scalars().first()
        if additional is None:
            return None
        return AdditionalsListedSectionContent(
            title=additional.title,
            items=additional.items,
        )
