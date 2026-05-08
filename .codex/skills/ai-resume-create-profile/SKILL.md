---
name: ai-resume-create-profile
description: Create or update a base resume user profile through the local ai_resume_editor MCP server. Trigger when the user asks to create a new resume profile, save user resume data, convert raw resume/profile information into the DocModel JSON schema, import a resume profile, or prepare reusable profile data before tailoring resumes.
---

# AI Resume Create Profile

## Overview

Create a validated `DocModel` from the user's source material and save it with `mcp__ai_resume_editor__save_user_data`.

Read `references/profile-workflow.md` for the exact workflow and `references/mcp-schema.md` for the data shape.

## Workflow

1. Extract contact information, sections, dated entries, bullets, and additional grouped lists from the user's profile source.
2. Ask for missing required contact fields or date fields before saving.
3. Normalize into the repository's `DocModel` schema.
4. Call `save_user_data` with the complete profile.
5. Report the saved profile name and any assumptions or omissions.

## Profile Rules

Use base profile language that is factual and reusable across jobs. Prefer broad achievement statements over role-specific keyword stuffing; targeted wording belongs in `$ai-resume-tailor-resume`.

Do not invent credentials, employment history, degrees, metrics, or dates. If a user asks you to infer a field, clearly label the inference before saving.
