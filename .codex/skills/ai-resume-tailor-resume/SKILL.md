---
name: ai-resume-tailor-resume
description: Tailor an existing resume user profile to a job posting with the local ai_resume_editor MCP server and generate a professional PDF. Trigger when the user asks to make a resume for a role, create a catered or targeted resume, adapt resume bullets to a job description, save tailored resume JSON, adjust a generated resume to fit pages, or generate a resume PDF.
---

# AI Resume Tailor Resume

## Overview

Create a job-specific `DocModel`, save it with `save_catered_resume_data`, and generate the PDF with `generate_pdf`. When creating a new targeted resume, use the MCP prompt named `Create a new resume` from `core/prompt.py` as the governing resume-writing prompt.

Read `references/tailor-workflow.md` for the exact workflow and `references/mcp-schema.md` for the data shape.

## Workflow

1. Identify the user profile, job/company/title, and job posting requirements.
2. Invoke or follow the MCP prompt `Create a new resume` with `name`, `company_name`, `position`, and `job_posting`.
3. Load the base profile through MCP tools/resources when available, or ask for the profile content if it is not available.
4. Build a complete tailored `DocModel` using only truthful profile facts.
5. Call `save_catered_resume_data`; keep the returned `filename`.
6. Call `generate_pdf` with that `filename` and a descriptive `job_name`.
7. Review metadata, especially `page_count` and `page_fill`, then make targeted page-fit edits if needed.
8. Return the generated PDF path/URI and summarize the tailoring choices.

## Tailoring Rules

Prioritize role-relevant experience, projects, education, certifications, and skills. Rewrite bullets to mirror the job's language only when the underlying fact is present in the profile.

Do not invent capabilities, experience, metrics, software, certifications, security clearances, languages, or employment details. If the job requires something missing from the profile, omit it or mention the gap separately.
