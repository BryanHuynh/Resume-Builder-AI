# Create Profile Workflow

1. Gather source material from the user: existing resume text, LinkedIn/profile notes, education, work history, projects, certifications, and skills.
2. Extract only factual information. Do not invent missing details.
3. Normalize contact details into `user_info`.
4. Group experience into `sections`. Common section names are `Education`, `Work Experience`, `Projects`, `Volunteer Experience`, and `Certifications`.
5. Create each section entry with:
   - `title`: employer, school, project, or certification title.
   - `left_subheader`: role, degree, credential, or short descriptor.
   - `right_subheader`: location or context.
   - `start_date` and `end_date`.
   - `sub_sections`: bullet descriptions.
6. Put skills and other compact grouped lists into `additionals`.
7. Call `mcp__ai_resume_editor__save_user_data`.
8. Confirm the saved full name and mention any fields the user may want to improve later.

Ask before saving if required contact fields, dates, or section details are missing.
