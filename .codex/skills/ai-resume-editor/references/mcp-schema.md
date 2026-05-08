# ai_resume_editor MCP Reference

## Server

Use the `mcp__ai_resume_editor__` tools when available. The local MCP server is the `ai_resume_editor` repository's `main.py` stdio server.

Core storage:

- Base profiles: `documents/user_data/{Full_Name_With_Underscores}.json`
- Tailored resumes: `documents/catered_resume_data/{Full_Name_With_Underscores}/{job}.json`
- Generated outputs: `output/`

## DocModel Shape

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
    "title": "string",
    "items": {
      "Group Label": ["string"]
    }
  }
}
```

`SectionContentDescriptions.sub_sections` is recursive to a maximum depth of 3. Keep most resume bullets at one level unless the user explicitly wants nested bullets.

## Main Tools

- Prompt `Create a new resume` in `core/prompt.py` creates the job-targeted resume-writing instructions. Use it when creating a new targeted resume from a saved user profile. Its inputs are `name`, `company_name`, `position`, and `job_posting`.
- `save_user_data(data)` saves a base profile.
- `get_user_sections(name)` reads saved base profile sections.
- `get_user_additionals(name, title)` reads saved base profile additionals.
- `upsert_user_section(name, section_name, content)` updates one base profile entry.
- `upsert_user_additionals(name, title, content)` replaces base profile additionals.
- `save_catered_resume_data(job, data)` saves tailored JSON and returns `filename`.
- `generate_pdf(filename, job_name)` generates the PDF and returns metadata including `path`, `page_count`, and `page_fill`.
- `get_catered_resume_outline(filename)` returns section/subsection names for small PDF fit edits.
- `get_catered_resume_section`, `upsert_catered_resume_section`, `delete_catered_resume_section` operate on full tailored sections.
- `get_catered_resume_subsection`, `upsert_catered_resume_subsection`, `delete_catered_resume_subsection` operate on one tailored section entry.
- `get_catered_resume_additionals`, `upsert_catered_resume_additionals`, `get_catered_resume_additional_subsection`, `upsert_catered_resume_additional_subsection`, and `delete_catered_resume_additional_subsection` operate on tailored additional lists.

## Dates

Use ISO dates. If only month/year is known, use the first day of the month. If only year is known, ask for more detail unless the user approves using `YYYY-01-01`. Use `end_date: null` for current roles.

## PDF Fit Loop

After `generate_pdf`, inspect metadata:

- `page_count`: generated page count.
- `page_fill`: approximate last-page fill ratio.

If the PDF is too long or the final page is sparse, make targeted edits using the catered resume outline and section/subsection upsert/delete tools. Then regenerate with the same filename and job name.
