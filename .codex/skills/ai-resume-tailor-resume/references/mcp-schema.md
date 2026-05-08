# ai_resume_editor MCP Schema

Use the same `DocModel` structure for tailored resumes:

Before choosing a saved base profile, read `doc://resume-names`. It returns each profile's tool-safe `name`, user-facing `display_name`, and `filename`; use `name` for MCP tools and `doc://resume/{name}` resource calls.

```json
{
  "user_info": {
    "full_name": "string",
    "email": "string",
    "phone": "string",
    "links": ["string"],
    "city_province": "string"
  },
  "sections": {
    "Section Name": [
      {
        "title": "string",
        "left_subheader": "string",
        "right_subheader": "string",
        "start_date": "YYYY-MM-DD",
        "end_date": "YYYY-MM-DD or null",
        "sub_sections": [
          {
            "description": "string",
            "sub_sections": []
          }
        ]
      }
    ]
  },
  "additionals": {
    "title": "Skills",
    "items": {
      "Group Label": ["string"]
    }
  }
}
```

Key tools:

- Prompt `Create a new resume` in `core/prompt.py`: use when creating a new targeted resume. Inputs are `name`, `company_name`, `position`, and `job_posting`. Follow its guidance for section ordering, preserving business-impact subsections, saving catered resume data, generating the PDF, and page-fit iteration.
- `get_user_sections(name)` and `get_user_additionals(name, title)` load base profile content.
- `save_catered_resume_data(job, data)` saves tailored JSON and returns `filename`.
- `generate_pdf(filename, job_name)` generates the PDF.
- `get_catered_resume_outline(filename)` supports page-fit edits.
- `upsert_catered_resume_subsection`, `delete_catered_resume_subsection`, `upsert_catered_resume_additional_subsection`, and `delete_catered_resume_additional_subsection` make small edits without resending the full resume.
