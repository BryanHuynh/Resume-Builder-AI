from sqlalchemy import select

from db.database import get_db
from db.entities.catered_resume import CateredResume
from doc_utils.doc_model import DocModel


def save_catered_resume(user_id: str, job_name: str, doc_model: DocModel):
    """Upsert a catered resume for a user+job combination."""
    resume_json = doc_model.model_dump(mode="json")
    with get_db() as db:
        row = db.execute(
            select(CateredResume).where(
                CateredResume.user_id == user_id,
                CateredResume.job_name == job_name,
            )
        ).scalars().first()

        if row is None:
            row = CateredResume(
                user_id=user_id,
                job_name=job_name,
                resume_data=resume_json,
            )
            db.add(row)
        else:
            row.resume_data = resume_json


def get_catered_resume(user_id: str, job_name: str) -> DocModel | None:
    """Retrieve a catered resume by user+job, returning a DocModel."""
    with get_db() as db:
        row = db.execute(
            select(CateredResume).where(
                CateredResume.user_id == user_id,
                CateredResume.job_name == job_name,
            )
        ).scalars().first()

        if row is None:
            return None
        return DocModel.model_validate(row.resume_data)


def get_catered_resume_json(user_id: str, job_name: str) -> str | None:
    """Retrieve a catered resume as JSON string."""
    doc_model = get_catered_resume(user_id, job_name)
    if doc_model is None:
        return None
    return doc_model.model_dump_json(indent=2)
