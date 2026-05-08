# ai_resume_editor MCP Schema

Use `mcp__ai_resume_editor__save_user_data` with this `DocModel` shape:

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
    "Work Experience": [
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
      "Technical": ["Python", "SQL"]
    }
  }
}
```

Required profile fields: `full_name`, `email`, `phone`, `links`, `city_province`, `sections`, and `additionals`.

Use ISO dates. For current roles, use `end_date: null`. For partial dates, ask the user before choosing a placeholder day.
