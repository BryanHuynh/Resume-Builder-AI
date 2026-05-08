---
name: ai-resume-editor
description: Use the local ai_resume_editor MCP server to create resume user profiles, tailor resumes to job postings, maintain tailored resume JSON, and generate professional PDF resumes. Trigger when the user asks to build a resume profile, save resume data, tailor a resume for a job posting, create a catered resume, update a tailored resume section, or generate a resume PDF using this repository's MCP tools.
---

# AI Resume Editor

## Overview

Use this as the router for the `ai_resume_editor` MCP server. It has two focused companion skills:

- `$ai-resume-create-profile` for creating or updating base user profiles.
- `$ai-resume-tailor-resume` for tailoring an existing profile to a job posting and generating a PDF.

Read `references/mcp-schema.md` when you need the full data shape, tool sequence, or page-fit adjustment workflow.

## Routing

Use `$ai-resume-create-profile` when the user provides raw resume information, an existing resume, profile details, or asks to create a new user profile.

Use `$ai-resume-tailor-resume` when the user provides a job posting, role description, company name, or asks for a new resume/PDF targeted to a role. That workflow should use the MCP prompt named `Create a new resume` from `core/prompt.py` when creating the targeted resume.

Use this parent skill directly only for mixed tasks that span both workflows.

## MCP Server

Prefer the `mcp__ai_resume_editor__` tools when they are available. If the tools are not loaded, use tool discovery for `ai_resume_editor` before falling back to file edits.

The local server is this repository's `main.py` stdio MCP server. It stores base profiles in `documents/user_data`, tailored JSON in `documents/catered_resume_data`, and generated PDFs/TeX in `output`.

## Quality Bar

Always keep claims grounded in supplied profile data. Do not invent employers, degrees, dates, certifications, metrics, or contact details. If a required field is missing, ask for it or mark it as intentionally blank only when the user approves.
