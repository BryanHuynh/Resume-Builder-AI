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
                            "description": "Improved SQL-based scheduled jobs by optimizing query logic and execution patterns, increasing throughput without additional compute cost.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Identified, removed, and validated fixes for 20+ critical Java library vulnerabilities, unblocking development and improving security posture across multiple teams.",
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
                        {
                            "description": "Refactored legacy systems and improved test reliability in Java Springboot with full coverage Unit Testing.",
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
                            "description": "Maintained and operated on C# .NET backend to deliver structured data from ArcGIS databases, and SQL databases using Entity Framework to frontend components.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Develop enterprise geohazard management web application using the React framework and Esri ArcGIS",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2022-01-01",
                    "end_date": "2022-08-01",
                },
            ],
            "Personal Projects": [
                {
                    "title": "Resume Builder AI Tool",
                    "left_subheader": "FastMCP, Python, LLM, GenAI, PyLaTeX, PostgreSQL, AWS ECS, Auth0",
                    "right_subheader": "github.com/BryanHuynh/Resume-Builder-AI",
                    "sub_sections": [
                        {
                            "description": "Developed an MCP Server AI-powered tool that generates catered resumes based on user data and job posting.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Implemented a PostgreSQL database to maintain and persist user information across sessions.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Deployed an AWS Lambda server using ECS to handle LaTeX to PDF translation, enabling scalable and serverless document generation.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Integrated Auth0 for user authentication, linking authenticated identities to user records in the PostgreSQL database.",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2026-02-01",
                    "end_date": None,
                },
                {
                    "title": "Elden Ring Chat Bot",
                    "left_subheader": "MCP, RAG, Python, LLM, GenAi",
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
                        {
                            "description": "Developed a GraphQL wrapper enabling LLMs to query GraphQL services directly without requiring model-side code generation.",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2026-01-01",
                    "end_date": None,
                },
                {
                    "title": "Text To Sql GPT",
                    "left_subheader": "Model Finetuning, Pytorch, Data Processing, MVC design",
                    "right_subheader": "github.com/BryanHuynh/Text-To-Sql",
                    "sub_sections": [
                        {
                            "description": "Implemented schema-aware SQL generation using a fine-tuned FLAN-T5 model on the Spider dataset, achieving ~70% execution accuracy on benchmark queries.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Implemented user authentication via Firebase, enforcing Row-Level Security (RLS) within PostgreSQL.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Developed within Java Springboot with full unit test and integration testing coverage.",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2025-01-01",
                    "end_date": None,
                },
                {
                    "title": "Discord Leetcode Notification Bot",
                    "left_subheader": "Typescript React, firebase, postgres, discord.js, cron job",
                    "right_subheader": "github.com/BryanHuynh/LeetCodeDiscordBot",
                    "sub_sections": [
                        {
                            "description": "Developed a Discord bot using TypeScript, discord.js with Postgres DB that enables users within guilds to subscribe and receive real-time notifications when they complete LeetCode problems.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Designed bot features to post solved problem titles and direct submission links to Accepted solutions, fostering accountability, peer motivation and constructive feedback within programming communities.",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2025-01-01",
                    "end_date": None,
                },
                {
                    "title": "Speedrun Charts",
                    "left_subheader": "Typescript React, tailwindcss, MUIxCharts, API's",
                    "right_subheader": "github.com/BryanHuynh/Speedrun-Charts-v2",
                    "sub_sections": [
                        {
                            "description": "Utilized Speedruns.com api to develop a web based visual representation of world record progressions for different games, categories and variables.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Designed to collect 100+ speedrun entries, parse and filter entries to generate an interactive graph within 10 seconds",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2025-01-01",
                    "end_date": None,
                },
                {
                    "title": "Twitch Streamer Network Analysis",
                    "left_subheader": "Python, Pandas, Gephi, Data Visualization, Data Processing and Analysis",
                    "right_subheader": "github.com/BryanHuynh/Twitch-Streamer-Network",
                    "sub_sections": [
                        {
                            "description": "Developed a Python program that generates a directional graph of streamers on Twitch through their mutual followers.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Leveraged the Twitch Developer API to perform data mining of information.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Designed script to output a file structure that can be visually represented on Gephi.",
                            "sub_sections": [],
                        },
                        {
                            "description": "Optimized the resulting network to generate 3,000+ nodes and 10,000+ edges within 10mins.",
                            "sub_sections": [],
                        },
                    ],
                    "start_date": "2024-01-01",
                    "end_date": None,
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
                    "TypeScript",
                    "Python",
                    "Java",
                    "SQL",
                    "C#",
                    "React",
                    "Spring Boot",
                    "PostgreSQL",
                    "NoSQL",
                    "Firebase",
                    "Docker",
                    "Kafka",
                    "AWS ECS",
                    "Auth0",
                ],
                "Skills": [
                    "Technical documentation",
                    "system design",
                    "cross-functional collaboration",
                    "problem solving",
                    "ownership",
                    "adaptability",
                ],
                "Interests": [
                    "Powerlifting",
                    "Piano",
                    "Video Games",
                    "3D Printing",
                    "Miniatures painting",
                    "Drones",
                    "Cooking",
                ],
                "Certifications": [
                    "Anthropic MCP: Advanced topics",
                    "IBM Build RAG Applications",
                    "IBM Develop Generative AI Applications",
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
            "save_user_data",
            arguments={
                "data": sample_data,
            },
        )
        print(f"Auth0 audience: {result}")


if __name__ == "__main__":
    asyncio.run(main())
