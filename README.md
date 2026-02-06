
## Project Overview

AI Resume Editor — a Python MCP (Model Context Protocol) server that lets AI systems tailor resumes to job postings and generate professional PDFs via LaTeX. Resume data is stored as JSON, validated with Pydantic models, and rendered through PyLaTeX.

To download PyLaTeX on windows go to: https://ctan.mirror.rafal.ca/systems/win32/miktex/setup/

## Commands

```bash
# Install dependencies
uv sync

# Run MCP server (stdio transport)
python main.py
```

PDF generation requires a system-level LaTeX installation (e.g., TeX Live, MiKTeX).

## Architecture

**Data flow:** User JSON → AI tailors via MCP tools → Tailored JSON → DocBuilder → LaTeX → PDF

### `core/` — MCP Integration Layer
- `tools.py` — MCP tools: save/load resume data, generate PDFs (`save_resume_data`, `save_catered_resume_data`, `get_catered_resume_data`, `generate_pdf`)
- `resources.py` — Exposes resume data as MCP resources (`doc://resume/{name}`)
- `prompt.py` — Structured prompt guiding AI to tailor resumes to job postings

### `doc_utils/` — Document Generation & Data Models
- `doc_model.py` — Pydantic models defining resume schema (`DocModel`, `UserInfo`, `SectionContent`, `SectionContentDescriptions`, `AdditionalsListedSectionContent`)
- `doc_builder.py` — Orchestrates LaTeX document construction; `build()` assembles the full document, `export()` writes PDF+TeX to `output/`
- `doc_config.py` — LaTeX package/font/spacing configuration (EB Garamond serif, tight margins)
- `doc_tools.py` — Custom LaTeX components (`SectionTitle`, `SectionDivider`)

### `documents/` — Resume Data Storage
- `user_data/` — Base resume profiles (full JSON)
- `catered_resume_data/{Name}/` — Job-specific tailored versions

### `output/` — Generated PDF and TeX files

## Key Patterns

- `SectionContentDescriptions` is recursive — supports nested bullet points with arbitrary depth
- End dates are optional in `SectionContent` (supports ongoing/current roles)
- `generate_pdf()` tool returns the PDF base64-encoded via `EmbeddedResource`
- All file paths use `pathlib.Path`
- Uses `uv` for dependency management with lock file

## Claude Desktop Configuration
```json
{
  "mcpServers": {
    "ai_resume_editor": {
      "command": "uv",
      "args": [
        "--directory",
        "<PATH\\TO\\PROJECT\\DIR>",
        "run",
        "main.py"
      ]
    }
  }
}
```

## Claude Desktop Usage
Ideally Claude should be using your workspace to handle retrival and generation of user data, hense why we changed the directory to our project folder.
1. Start by giving Claude your resumes and ask it to generate a new user entry for your name
2. Double check within the documents/user_data/{your_name}.json file to verify that the information within is correct. This is also were you can add new entries if you'd like
3. Back in Claude, add the prompt to 'Create a new resume'.
4. Give it the user_data file without the suffix (eg: documents/user_data/Bryan_Huynh.json -> Bryan_Huynh)
5. Fill out the company name and job position
6. Copy and paste the job posting into the Job position field and hit enter
7. If all goes right, your curated resume should appear within the output folder
