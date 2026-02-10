from fastmcp import Client
import asyncio

sample_data = {
    "user_info": {
        "full_name": "Bryan Huynh",
        "email": "Bryan.huynh42@gmail.com",
        "phone": "(587) 707-8088",
        "links": ["linkedin.com/in/bryan-huynh42", "github.com/BryanHuynh"],
        "city_province": "Calgary, AB",
    },
    "sections": {
        "Work Experience": [
            {
                "title": "Associate Software Engineer II",
                "left_subheader": "Morgan Stanley at Work",
                "right_subheader": "Hybrid, Calgary AB",
                "sub_sections": [
                    {
                        "description": "Identified, removed, and validated fixes for 20+ critical Java library vulnerabilities, unblocking development and improving security posture across multiple teams.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Refactored legacy systems and improved test reliability in Java Spring Boot with full coverage unit testing.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Improved SQL-based scheduled jobs by optimizing query logic and execution patterns, increasing throughput without additional compute cost.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Documented and validated large-scale data migration workflows across 100+ Confluence pages, Java Spring Boot services, Perl scripts, and SQL pipelines supporting legacy system transitions.",
                        "sub_sections": [
                            {
                                "description": "Enabled faster stakeholder discussions by improving traceability, surfacing data conflicts, and identifying optimization opportunities.",
                                "sub_sections": [],
                            }
                        ],
                    },
                    {
                        "description": "Completed Morgan Stanley's Technology Analyst Program (Kafka, AWS ECS, Docker).",
                        "sub_sections": [],
                    },
                    {
                        "description": "Created Bash scripts to streamline and standardize user environment configuration on AWS EC2 instances.",
                        "sub_sections": [],
                    },
                ],
                "start_date": "2023-08-01",
                "end_date": "2025-03-01",
            },
            {
                "title": "Web Developer",
                "left_subheader": "BGC Engineering",
                "right_subheader": "Remote",
                "sub_sections": [
                    {
                        "description": "Led development of a React-based 2D geospatial elevation profiling tool visualizing 10,000+ data points, optimized for low-spec systems through efficient rendering and data handling.",
                        "sub_sections": [
                            {
                                "description": "Resulting in a daily-use tool for field engineers across all sectors from mining, geotechnical analysis, and surveying.",
                                "sub_sections": [],
                            },
                            {
                                "description": "Gained high praise from shareholders for its easy use, application and as an industry leader.",
                                "sub_sections": [],
                            },
                        ],
                    },
                    {
                        "description": "Maintained and operated on C# .NET backend to deliver structured data from ArcGIS databases and SQL databases using Entity Framework to frontend components.",
                        "sub_sections": [],
                    },
                ],
                "start_date": "2022-01-01",
                "end_date": "2022-08-01",
            },
        ],
        "Personal Projects": [
            {
                "title": "Text To SQL GPT",
                "left_subheader": "Model Finetuning, PyTorch, Java Spring Boot, PostgreSQL",
                "right_subheader": "github.com/BryanHuynh/Text-To-Sql",
                "sub_sections": [
                    {
                        "description": "Implemented schema-aware SQL generation using a fine-tuned FLAN-T5 model on the Spider dataset, achieving ~70% execution accuracy on benchmark queries.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Developed within Java Spring Boot with full unit test and integration testing coverage.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Implemented user authentication via Firebase, enforcing Row-Level Security (RLS) within PostgreSQL.",
                        "sub_sections": [],
                    },
                ],
                "start_date": "2025-01-01",
                "end_date": "2025-03-01",
            },
            {
                "title": "Resume Builder AI Tool",
                "left_subheader": "FastMCP, Python, LLM, GenAI, PyLaTeX",
                "right_subheader": "github.com/BryanHuynh/Resume-Builder-AI",
                "sub_sections": [
                    {
                        "description": "Developed an MCP Server AI-powered tool that generates catered resumes based on user data and job posting.",
                        "sub_sections": [],
                    }
                ],
                "start_date": "2026-02-01",
                "end_date": "2026-03-01",
            },
            {
                "title": "Elden Ring Chat Bot",
                "left_subheader": "MCP, RAG, Python, LLM, GenAI",
                "right_subheader": "github.com/BryanHuynh/EldenRingChatBot",
                "sub_sections": [
                    {
                        "description": "Designed and implemented an MCP-based chatbot server to answer Elden Ring gameplay questions using context-aware retrieval from curated online sources.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Processed, cleaned, and chunked wiki data to build a ChromaDB vector store, improving retrieval accuracy by combining BM25 ranking with embedding-based similarity search.",
                        "sub_sections": [],
                    },
                ],
                "start_date": "2026-01-01",
                "end_date": "2026-03-01",
            },
        ],
        "Leadership & Activities": [
            {
                "title": "VP Academic Events",
                "left_subheader": "Computer Science Undergraduate Society (CSUS)",
                "right_subheader": "",
                "sub_sections": [
                    {
                        "description": "Organized academic workshops and annual Cal-Hacks events with 300+ participants, focusing on practical topics beyond coursework.",
                        "sub_sections": [],
                    },
                    {
                        "description": "Led a hands-on Python workshop for 140+ participants on web scraping using BeautifulSoup and Pandas using reusable Jupyter notebooks for live demos and post-event learning.",
                        "sub_sections": [],
                    },
                ],
                "start_date": "2020-01-01",
                "end_date": "2021-12-31",
            }
        ],
        "Education": [
            {
                "title": "Bachelor of Science, Computer Science. 3.3 GPA",
                "left_subheader": "University of Calgary",
                "right_subheader": "Calgary, AB",
                "sub_sections": [],
                "start_date": "2017-01-01",
                "end_date": "2023-12-31",
            }
        ],
    },
    "additionals": {
        "title": "Certifications, Skills & Interests",
        "items": {
            "Technologies": [
                "Java",
                "Spring Boot",
                "SQL",
                "PostgreSQL",
                "Python",
                "TypeScript",
                "React",
                "Docker",
                "Kafka",
                "AWS ECS",
                "Firebase",
            ],
            "Skills": [
                "Technical documentation",
                "system design",
                "cross-functional collaboration",
                "problem solving",
                "ownership",
                "adaptability",
            ],
        },
    },
}

sample_section_data = {
    "title": "Elden Ring Chat Bot",
    "end_date": "2026-03-01",
    "start_date": "2026-01-01",
    "sub_sections": [
        {
            "description": "Designed and implemented an MCP-based chatbot server to answer Elden Ring gameplay questions using context-aware retrieval from curated online sources.",
            "sub_sections": [],
        },
        {
            "description": "Processed, cleaned, and chunked wiki data to build a ChromaDB vector store, improving retrieval accuracy by combining BM25 ranking with embedding-based similarity search.",
            "sub_sections": [],
        },
    ],
    "left_subheader": "MCP, RAG, Python, LLM, GenAI",
    "right_subheader": "github.com/BryanHuynh/EldenRingChatBot",
}


async def main():
    # The client will automatically handle Auth0 OAuth flows
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First-time connection will open Auth0 login in your browser
        print("✓ Authenticated with Auth0!")

        # # Test the protected tool
        # result = await client.call_tool(
        #     "save_catered_resume_data",
        #     arguments={
        #         "job": "test",
        #         "data": sample_data,
        #     },
        # )
        result = await client.call_tool(
            "generate_pdf",
            arguments={
                "job_name": "test",
            },
        )
        print(f"Auth0 audience: {result}")


if __name__ == "__main__":
    asyncio.run(main())
