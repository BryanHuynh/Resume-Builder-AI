import base64
from dataclasses import asdict
import json
import re
from pathlib import Path
from fastmcp.server import FastMCP
from mcp import Resource

from doc_utils.doc_builder import DocBuilder
from doc_utils.doc_model import DocModel

from mcp.types import TextContent, BlobResourceContents


docs_dir = Path("documents")
user_dir = docs_dir / "user_data"
catered_resume_dir = docs_dir / "catered_resume_data"

output_dir = Path("output")


def register_tools(mcp: FastMCP):
    @mcp.tool()
    def save_user_data(data: DocModel):
        """Saves the users data as a json file to the user_data directory.
        """
        user_file_path = data.user_info.full_name.replace(" ", "_")
        json_data = data.model_dump_json(indent=2)
        user_dir.mkdir(parents=True, exist_ok=True)
        user_data = user_dir / f"{user_file_path}.json"
        with open(user_data, "w") as f:
            f.write(json_data)
        return {
            "success": True,
            "message": f"Saved user data for {data.user_info.full_name} to {user_data}",
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
        with open(export_path, "rb") as f:
            pdf_bytes = f.read()

        page_count = len(re.findall(rb"/Type\s*/Page(?!s)", pdf_bytes))
        file_size_kb = len(pdf_bytes) / 1024

        def _count_desc_chars(descs):
            return sum(
                len(d.description) + _count_desc_chars(d.sub_sections) for d in descs
            )

        total_chars = sum(
            len(entry.title)
            + len(entry.left_subheader)
            + len(entry.right_subheader)
            + _count_desc_chars(entry.sub_sections)
            for entries in doc_model.sections.values()
            for entry in entries
        )

        metadata = {
            "success": True,
            "message": f"Resume generated successfully for {job_name} position",
            "uri": export_path.resolve().as_uri(),
            "name": export_path.name,
            "page_count": page_count,
            "file_size_kb": file_size_kb,
        }
        return metadata
