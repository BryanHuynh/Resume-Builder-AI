# Tailor Resume Workflow

1. Identify the target job: company, title, posting text, must-have skills, preferred skills, responsibilities, and seniority.
2. Read the `doc://resume-names` resource to find available saved base profiles. Use the returned `name` value for MCP tool/resource calls and `display_name` only for user-facing clarification.
3. Invoke or follow the MCP prompt `Create a new resume` from `core/prompt.py` with `name`, `company_name`, `position`, and `job_posting`.
4. Load the candidate's base profile using MCP tools/resources. If the profile is not available, ask the user to provide it or use `$ai-resume-create-profile` first.
5. Select sections and entries that best support the role. Keep the resume concise.
6. Rewrite bullets to emphasize matching responsibilities, tools, outcomes, and domain language while preserving truth.
7. Reorder or group `additionals.items` so the most relevant skills appear first.
8. Call `mcp__ai_resume_editor__save_catered_resume_data` with a short filesystem-safe `job` label.
9. Call `mcp__ai_resume_editor__generate_pdf` using the returned `filename` and a clear `job_name`, such as `Company - Job Title`.
10. If metadata shows the result needs fit work, use outline and upsert/delete tools to make small targeted edits, then regenerate.
11. Return the generated PDF path/URI and a short summary of what changed for the role.

Do not fabricate missing qualifications. If the posting asks for a requirement not found in the profile, omit it from the resume and mention the gap separately.
