
## Project Overview

AI Resume Editor — a Python MCP (Model Context Protocol) server that lets AI systems tailor resumes to job postings and generate professional PDFs via LaTeX. Resume data is stored as JSON, validated with Pydantic models, and rendered through PyLaTeX.

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
