-- Create schema and tables
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(255) PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(50),
    city_province VARCHAR(255),
    links TEXT[],
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Sections table (JSONB approach)
CREATE TABLE IF NOT EXISTS sections (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    section_name VARCHAR(255) NOT NULL,
    content JSONB NOT NULL,
    sort_order INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, section_name, sort_order)
);

-- Additionals table
CREATE TABLE IF NOT EXISTS additionals (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255),
    items JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Catered resumes table (stores full DocModel JSON per user+job)
CREATE TABLE IF NOT EXISTS catered_resumes (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) REFERENCES users(id) ON DELETE CASCADE NOT NULL,
    job_name VARCHAR(255) NOT NULL,
    resume_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, job_name)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_sections_user_id ON sections(user_id);
CREATE INDEX IF NOT EXISTS idx_sections_content ON sections USING GIN(content);
CREATE INDEX IF NOT EXISTS idx_additionals_user_id ON additionals(user_id);
CREATE INDEX IF NOT EXISTS idx_additionals_items ON additionals USING GIN(items);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_catered_resumes_user_id ON catered_resumes(user_id);
CREATE INDEX IF NOT EXISTS idx_catered_resumes_resume_data ON catered_resumes USING GIN(resume_data);

