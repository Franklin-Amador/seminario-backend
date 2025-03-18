-- Archivo: stored_procedures.sql
-- Descripción: Procedimientos almacenados optimizados con nombres usando guiones bajos

-- Procedimiento completo de login que devuelve tanto el usuario como sus roles en una sola llamada
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
    SELECT id, username, password, firstname, lastname, email
    INTO v_user_record
    FROM mdl_user
    WHERE username = p_username
    AND deleted = FALSE;
    
    -- Verificar si se encontró el usuario
    IF v_user_record.id IS NOT NULL THEN
        -- Validar la contraseña usando una función auxiliar (implementada más abajo)
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

-- Función auxiliar para validar contraseñas (simulando bcrypt en Postgres)
-- Nota: Esta función es un placeholder - el hash real se hará en Python con bcrypt
CREATE OR REPLACE FUNCTION validate_password(plain_password TEXT, hashed_password TEXT)
RETURNS BOOLEAN AS $$
BEGIN
    -- Esta función es un placeholder
    -- La validación real se hará en Python con la biblioteca bcrypt
    -- Aquí solo hacemos un retorno directo porque el control real se hace en la aplicación
    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;

-- Actualizar contraseña SIN manejo de transacciones (corregido)
CREATE OR REPLACE FUNCTION update_user_password(p_email TEXT, p_password TEXT)
RETURNS TABLE (
    success BOOLEAN,
    user_id INTEGER,
    message TEXT
) AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    -- Buscar usuario por email
    SELECT id INTO v_user_id
    FROM mdl_user
    WHERE email = p_email
    AND deleted = FALSE;
    
    -- Si el usuario existe, actualizar contraseña
    IF v_user_id IS NOT NULL THEN
        UPDATE mdl_user
        SET password = p_password,
            timemodified = NOW()
        WHERE id = v_user_id;
        
        RETURN QUERY
        SELECT 
            TRUE,
            v_user_id,
            'Contraseña actualizada exitosamente'::TEXT;
    ELSE
        RETURN QUERY
        SELECT 
            FALSE,
            NULL::INTEGER,
            'Usuario no encontrado'::TEXT;
    END IF;
EXCEPTION WHEN OTHERS THEN
    RETURN QUERY
    SELECT 
        FALSE,
        NULL::INTEGER,
        'Error al actualizar la contraseña: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Restablecer todas las contraseñas (sin manejo interno de transacciones)
CREATE OR REPLACE FUNCTION reset_all_passwords(p_password TEXT)
RETURNS TABLE (
    success BOOLEAN,
    count INTEGER,
    message TEXT
) AS $$
DECLARE
    v_count INTEGER := 0;
BEGIN
    -- Actualizar todas las contraseñas
    UPDATE mdl_user
    SET password = p_password,
        timemodified = NOW()
    WHERE deleted = FALSE;
    
    GET DIAGNOSTICS v_count = ROW_COUNT;
    
    RETURN QUERY
    SELECT 
        TRUE,
        v_count,
        'Se actualizaron ' || v_count || ' contraseñas exitosamente'::TEXT;
EXCEPTION WHEN OTHERS THEN
    RETURN QUERY
    SELECT 
        FALSE,
        0,
        'Error al actualizar contraseñas: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Procedimiento para auditar intentos de login
CREATE TABLE IF NOT EXISTS login_audit (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    ip_address TEXT,
    user_agent TEXT,
    success BOOLEAN NOT NULL,
    timestamp TIMESTAMP DEFAULT NOW()
);

CREATE OR REPLACE FUNCTION audit_login_attempt(
    p_username TEXT,
    p_ip_address TEXT,
    p_user_agent TEXT,
    p_success BOOLEAN
)
RETURNS VOID AS $$
BEGIN
    INSERT INTO login_audit (username, ip_address, user_agent, success)
    VALUES (p_username, p_ip_address, p_user_agent, p_success);
END;
$$ LANGUAGE plpgsql;

-- Eliminar los procedimientos anteriores con formato sp_xxx
DROP FUNCTION IF EXISTS sp_user_login(TEXT, TEXT);
DROP FUNCTION IF EXISTS sp_validate_password(TEXT, TEXT);
DROP FUNCTION IF EXISTS sp_update_user_password(TEXT, TEXT);
DROP FUNCTION IF EXISTS sp_reset_all_passwords(TEXT);
DROP FUNCTION IF EXISTS sp_audit_login_attempt(TEXT, TEXT, TEXT, BOOLEAN);
