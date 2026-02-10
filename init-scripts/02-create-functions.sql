-- Function to automatically update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sections_updated_at BEFORE UPDATE ON sections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_additionals_updated_at BEFORE UPDATE ON additionals
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_catered_resumes_updated_at BEFORE UPDATE ON catered_resumes
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to get full resume data for a user
CREATE OR REPLACE FUNCTION get_user_resume(p_user_id VARCHAR)
RETURNS JSON AS $$
DECLARE
    result JSON;
BEGIN
	SELECT json_build_object(
		'user_info', row_to_json(u)::jsonb - 'id',
		'sections', (
			SELECT json_object_agg(section_name, section_data)
			FROM (
				SELECT 
					section_name,
					json_agg(content ORDER BY sort_order) as section_data
				FROM sections
				WHERE user_id = u.id
				GROUP BY section_name
			) s
		),
		'additionals', (
		    SELECT row_to_json(t)::jsonb - 'user_id' - 'id'
		    FROM (
		        SELECT * FROM additionals a
		        WHERE a.user_id = u.id
		        LIMIT 1
		    ) t
		)
	)
	INTO result
	FROM users u
	WHERE u.id = p_user_id;
    RETURN result;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION sort_order_next(p_user_id VARCHAR, p_section_name VARCHAR)
RETURNS INTEGER AS $$                                                                                                          
DECLARE
    result INTEGER;
BEGIN
    SELECT COALESCE(MAX(sort_order), 0) + 1 INTO result
    FROM sections
    WHERE sections.user_id = p_user_id AND sections.section_name = p_section_name;
    RETURN result;
END;
$$ LANGUAGE plpgsql; 