-- Arreglar el procedimiento de login para evitar la ambigüedad de username
CREATE OR REPLACE FUNCTION user_login(p_username TEXT, p_password TEXT)
RETURNS TABLE (
    user_id INTEGER,
    username TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    is_valid BOOLEAN,
    role_id INTEGER,
    role_name TEXT,
    role_shortname TEXT
) AS $$
DECLARE
    v_user_record RECORD;
    v_password_valid BOOLEAN := FALSE;
BEGIN
    -- Obtener información del usuario
    SELECT u.id, u.username, u.password, u.firstname, u.lastname, u.email
    INTO v_user_record
    FROM mdl_user u
    WHERE u.username = p_username
    AND u.deleted = FALSE;
    
    -- Verificar si se encontró el usuario
    IF v_user_record.id IS NOT NULL THEN
        -- Validar la contraseña usando una función auxiliar
        SELECT validate_password(p_password, v_user_record.password) INTO v_password_valid;
        
        -- Devolver usuario y roles solo si la contraseña es válida
        IF v_password_valid THEN
            RETURN QUERY
            SELECT 
                v_user_record.id,
                v_user_record.username,
                v_user_record.firstname,
                v_user_record.lastname,
                v_user_record.email,
                TRUE,
                r.id,
                r.name,
                r.shortname
            FROM mdl_role_assignments ra
            JOIN mdl_role r ON ra.roleid = r.id
            WHERE ra.userid = v_user_record.id;
            
            -- Si el usuario no tiene roles, devolver al menos la información del usuario
            IF NOT FOUND THEN
                RETURN QUERY
                SELECT 
                    v_user_record.id,
                    v_user_record.username,
                    v_user_record.firstname,
                    v_user_record.lastname,
                    v_user_record.email,
                    TRUE,
                    NULL::INTEGER,
                    NULL::TEXT,
                    NULL::TEXT;
            END IF;
        ELSE
            -- Contraseña inválida
            RETURN QUERY
            SELECT 
                NULL::INTEGER,
                NULL::TEXT,
                NULL::TEXT,
                NULL::TEXT,
                NULL::TEXT,
                FALSE,
                NULL::INTEGER,
                NULL::TEXT,
                NULL::TEXT;
        END IF;
    ELSE
        -- Usuario no encontrado
        RETURN QUERY
        SELECT 
            NULL::INTEGER,
            NULL::TEXT,
            NULL::TEXT,
            NULL::TEXT,
            NULL::TEXT,
            FALSE,
            NULL::INTEGER,
            NULL::TEXT,
            NULL::TEXT;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Corregir la función para obtener todas las categorías
CREATE OR REPLACE FUNCTION get_all_categories()
RETURNS SETOF mdl_course_categories AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM mdl_course_categories
    ORDER BY sortorder;
END;
$$ LANGUAGE plpgsql;

-- Corregir la función para obtener cursos
CREATE OR REPLACE FUNCTION get_all_courses()
RETURNS SETOF mdl_course AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM mdl_course
    ORDER BY id;
END;
$$ LANGUAGE plpgsql;

-- Corregir la función para obtener un usuario por ID
CREATE OR REPLACE FUNCTION get_user_by_id(p_user_id INTEGER)
RETURNS SETOF mdl_user AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM mdl_user u
    WHERE u.id = p_user_id AND u.deleted = FALSE;
END;
$$ LANGUAGE plpgsql;

-- Corregir la función para obtener secciones de un curso
CREATE OR REPLACE FUNCTION get_course_sections(p_course_id INTEGER)
RETURNS SETOF mdl_course_sections AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM mdl_course_sections
    WHERE course = p_course_id
    ORDER BY section;
END;
$$ LANGUAGE plpgsql;

-- Asegurarse de que la función login por email también funcione
CREATE OR REPLACE FUNCTION login_email(p_email TEXT, p_password TEXT)
RETURNS TABLE (
    user_id INTEGER,
    username TEXT,
    firstname TEXT,
    lastname TEXT,
    email TEXT,
    is_valid BOOLEAN,
    role_id INTEGER,
    role_name TEXT,
    role_shortname TEXT
) AS $$
DECLARE
    v_user_record RECORD;
    v_password_valid BOOLEAN := FALSE;
BEGIN
    -- Obtener información del usuario por email
    SELECT u.id, u.username, u.password, u.firstname, u.lastname, u.email
    INTO v_user_record
    FROM mdl_user u
    WHERE u.email = p_email
    AND u.deleted = FALSE;
    
    -- Verificar si se encontró el usuario
    IF v_user_record.id IS NOT NULL THEN
        -- Validar la contraseña usando una función auxiliar
        SELECT validate_password(p_password, v_user_record.password) INTO v_password_valid;
        
        -- Devolver usuario y roles solo si la contraseña es válida
        IF v_password_valid THEN
            RETURN QUERY
            SELECT 
                v_user_record.id,
                v_user_record.username,
                v_user_record.firstname,
                v_user_record.lastname,
                v_user_record.email,
                TRUE,
                r.id,
                r.name,
                r.shortname
            FROM mdl_role_assignments ra
            JOIN mdl_role r ON ra.roleid = r.id
            WHERE ra.userid = v_user_record.id;
            
            -- Si el usuario no tiene roles, devolver al menos la información del usuario
            IF NOT FOUND THEN
                RETURN QUERY
                SELECT 
                    v_user_record.id,
                    v_user_record.username,
                    v_user_record.firstname,
                    v_user_record.lastname,
                    v_user_record.email,
                    TRUE,
                    NULL::INTEGER,
                    NULL::TEXT,
                    NULL::TEXT;
            END IF;
        ELSE
            -- Contraseña inválida
            RETURN QUERY
            SELECT 
                NULL::INTEGER,
                NULL::TEXT,
                NULL::TEXT,
                NULL::TEXT,
                NULL::TEXT,
                FALSE,
                NULL::INTEGER,
                NULL::TEXT,
                NULL::TEXT;
        END IF;
    ELSE
        -- Usuario no encontrado
        RETURN QUERY
        SELECT 
            NULL::INTEGER,
            NULL::TEXT,
            NULL::TEXT,
            NULL::TEXT,
            NULL::TEXT,
            FALSE,
            NULL::INTEGER,
            NULL::TEXT,
            NULL::TEXT;
    END IF;
END;
$$ LANGUAGE plpgsql;
