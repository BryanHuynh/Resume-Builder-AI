import re
from pathlib import Path
from fastmcp import FastMCP
import pymupdf
from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import (
    AdditionalsListedSectionContent,
    DocModel,
    SectionContent,
)

docs_dir = Path("documents")
user_dir = docs_dir / "user_data"
catered_resume_dir = docs_dir / "catered_resume_data"

output_dir = Path("output")


def _user_path(name: str) -> Path:
    return user_dir / f"{name.replace(' ', '_')}.json"


def _load_user(name: str) -> DocModel | None:
    path = _user_path(name)
    if not path.exists():
        return None
    return DocModel.model_validate_json(path.read_text())


def _save_user(data: DocModel) -> Path:
    user_dir.mkdir(parents=True, exist_ok=True)
    path = _user_path(data.user_info.full_name)
    path.write_text(data.model_dump_json(indent=2))
    return path


def register_tools(mcp: FastMCP):
    @mcp.tool()
    def save_user_data(data: DocModel):
        """Saves the users data as a json file to the user_data directory."""
        path = _save_user(data)
        return {
            "success": True,
            "message": f"Saved user data for {data.user_info.full_name} to {path}",
        }

    @mcp.tool()
    def get_user_sections(name: str):
        """Gets the user's sections details from their saved resume data.

        name: The user's full name (matches the saved file in user_data).
        """
        data = _load_user(name)
        if data is None:
            return {
                "success": False,
                "message": f"User {name} not found. Ask them to upload a sample resume first.",
            }
        return data.sections

    @mcp.tool()
    def upsert_user_section(name: str, section_name: str, content: SectionContent):
        """Updates (or inserts) one entry within a section of the user's saved resume data.

        name: The user's full name (matches the saved file in user_data).
        section_name: The name of the section to update (eg. "Education", "Work Experience").
        content: The SectionContent entry. If an entry with the same title already exists
                 under section_name, it is replaced; otherwise the entry is appended.
        """
        data = _load_user(name)
        if data is None:
            return {
                "success": False,
                "message": f"User {name} not found. Ask them to upload a sample resume first.",
            }
        entries = data.sections.get(section_name, [])
        replaced = False
        for i, existing in enumerate(entries):
            if existing.title == content.title:
                entries[i] = content
                replaced = True
                break
        if not replaced:
            entries.append(content)
        data.sections[section_name] = entries
        _save_user(data)
        return {
            "success": True,
            "message": f"{'Updated' if replaced else 'Added'} entry '{content.title}' in section '{section_name}' for {name}",
        }

    @mcp.tool()
    def get_user_additionals(name: str, title: str):
        """Gets the user's additionals details from their saved resume data.

        name: The user's full name (matches the saved file in user_data).
        title: The title of the additionals to get (eg. "Certifications", "Skills").
        """
        data = _load_user(name)
        if data is None:
            return {
                "success": False,
                "message": f"User {name} not found. Ask them to upload a sample resume first.",
            }
        if data.additionals.title != title:
            return {
                "success": False,
                "message": f"Additionals titled '{title}' not found for {name}.",
            }
        return data.additionals

    @mcp.tool()
    def upsert_user_additionals(
        name: str, title: str, content: AdditionalsListedSectionContent
    ):
        """Updates the user's additionals details in their saved resume data.

        name: The user's full name (matches the saved file in user_data).
        title: The title of the additionals to update (eg. "Certifications", "Skills").
        content: The AdditionalsListedSectionContent to store. Replaces the existing
                 additionals on the user's record.
        """
        data = _load_user(name)
        if data is None:
            return {
                "success": False,
                "message": f"User {name} not found. Ask them to upload a sample resume first.",
            }
        data.additionals = content
        _save_user(data)
        return {
            "success": True,
            "message": f"Updated additionals '{title}' for {name}",
        }
    
    @mcp.tool()
    def save_catered_resume_data(job: str, data: DocModel):
        """Saves the catered resume data as a json file to the catered resumes directory.

        Returns the filename to pass to generate_pdf.
        """
        user_folder = data.user_info.full_name.replace(" ", "_")
        user_job_dir = catered_resume_dir / user_folder
        json_data = data.model_dump_json(indent=2)
        user_job_dir.mkdir(parents=True, exist_ok=True)
        job_data = user_job_dir / f"{job}.json"
        with open(job_data, "w") as f:
            f.write(json_data)
        # Return the relative filename that generate_pdf expects
        generate_pdf_filename = f"{user_folder}/{job}.json"
        return {
            "success": True,
            "message": f"Saved catered resume data for {data.user_info.full_name} to {job_data}",
            "filename": generate_pdf_filename,
        }

    @mcp.tool()
    def get_catered_resume_data(filepath: str):
        """Gets the job posting as json data from the jobs directory"""
        job_data = Path(filepath)
        if not job_data.exists():
            return None
        with open(job_data, "r") as f:
            return f.read()

    @mcp.tool()
    def generate_pdf(filename: str, job_name: str):
        """Generates a PDF from the catered resume data and returns it with metadata.

        Args:
            filename: Relative path from catered_resume_data dir (e.g. "Bryan_Huynh/CNRL.json").
                      Use the "filename" field returned by save_catered_resume_data.
            job_name: Name used for the output PDF file. Use the company name and the job title.

        Returns the PDF as an embedded resource for Claude Desktop to analyze,
        along with metadata including page count, file size, and output path.
        """
        resume_path = catered_resume_dir / Path(filename)
        if not resume_path.exists():
            return "Catered Resume data not found"
        with open(resume_path, "r") as f:
            data = f.read()
        output_dir.mkdir(parents=True, exist_ok=True)
        doc_model = DocModel.model_validate_json(data)
        builder = DocBuilder(doc_model, job_name)
        builder.build()
        export_path = builder.export()
        pdf = pymupdf.open(str(export_path))
        page_count = len(pdf)
        file_size_kb = export_path.stat().st_size / 1024

        last_page = pdf[-1]
        page_height = last_page.rect.height
        content_blocks = last_page.get_text("blocks")
        if content_blocks:
            lowest_y = max(block[3] for block in content_blocks)  # block[3] = y1
        else:
            lowest_y = 0.0
        page_fill = round(lowest_y / page_height, 2)
        pdf.close()

        metadata = {
            "success": True,
            "message": f"Resume generated successfully for {job_name} position",
            "path": export_path.resolve().as_uri(),
            "name": export_path.name,
            "page_count": page_count,
            "file_size_kb": file_size_kb,
            "page_fill": page_fill,
        }
        return metadata
