---
name: ai-resume-tailor-resume
description: Tailor an existing resume user profile to a job posting with the local ai_resume_editor MCP server and generate a professional PDF. Trigger when the user asks to make a resume for a role, create a catered or targeted resume, adapt resume bullets to a job description, save tailored resume JSON, adjust a generated resume to fit pages, or generate a resume PDF.
---

# AI Resume Tailor Resume

## Overview

Create a job-specific `DocModel`, save it with `save_catered_resume_data`, and generate the PDF with `generate_pdf`. When creating a new targeted resume, use the MCP prompt named `Create a new resume` from `core/prompt.py` as the governing resume-writing prompt.

Read `references/tailor-workflow.md` for the exact workflow and `references/mcp-schema.md` for the data shape.

## Workflow

1. Identify the job/company/title and job posting requirements.
2. Read the `doc://resume-names` resource to find available saved base profiles. Use the returned `name` value as the source profile identifier for MCP tools/resources; use `display_name` only when asking the user to clarify which profile to use.
3. Invoke or follow the MCP prompt `Create a new resume` with `name`, `company_name`, `position`, and `job_posting`.
4. Load the base profile through MCP tools/resources when available, or ask for the profile content if it is not available.
5. Build a complete tailored `DocModel` using only truthful profile facts.
6. Call `save_catered_resume_data`; keep the returned `filename`.
7. Call `generate_pdf` with that `filename` and a descriptive `job_name`.
8. Review metadata, especially `page_count` and `page_fill`, then make targeted page-fit edits if needed.
9. Return the generated PDF path/URI and summarize the tailoring choices.

## Tailoring Rules

Prioritize role-relevant experience, projects, education, certifications, and skills. Rewrite bullets to mirror the job's language only when the underlying fact is present in the profile.

Do not invent capabilities, experience, metrics, software, certifications, security clearances, languages, or employment details. If the job requires something missing from the profile, omit it or mention the gap separately.
