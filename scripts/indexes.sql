-- Archivo: indexes.sql
-- Descripción: Índices optimizados para mejorar el rendimiento de consultas frecuentes

-- Índice para búsquedas por username (ya filtrado por deleted = FALSE)
CREATE INDEX IF NOT EXISTS idx_mdl_user_username ON mdl_user(username) 
WHERE deleted = FALSE;

-- Índice para búsquedas por email (ya filtrado por deleted = FALSE)
CREATE INDEX IF NOT EXISTS idx_mdl_user_email ON mdl_user(email) 
WHERE deleted = FALSE;

-- Índice para búsquedas de roles por usuario
CREATE INDEX IF NOT EXISTS idx_mdl_role_assignments_userid ON mdl_role_assignments(userid);

-- Índice para búsquedas en tabla de auditoría
CREATE INDEX IF NOT EXISTS idx_login_audit_username ON login_audit(username);
CREATE INDEX IF NOT EXISTS idx_login_audit_timestamp ON login_audit(timestamp);
CREATE INDEX IF NOT EXISTS idx_login_audit_success ON login_audit(success);

-- Índice para búsquedas frecuentes en mdl_user
CREATE INDEX IF NOT EXISTS idx_mdl_user_lastname_firstname ON mdl_user(lastname, firstname)
WHERE deleted = FALSE;

-- Índice para optimizar joins con la tabla de roles
CREATE INDEX IF NOT EXISTS idx_mdl_role_name ON mdl_role(name);
CREATE INDEX IF NOT EXISTS idx_mdl_role_shortname ON mdl_role(shortname);

-- Índice para buscar por ID de usuario (para actualizaciones frecuentes)
CREATE INDEX IF NOT EXISTS idx_mdl_user_id_active ON mdl_user(id)
WHERE deleted = FALSE;

-- Análisis de tablas para optimizar el planificador de consultas
ANALYZE mdl_user;
ANALYZE mdl_role;
ANALYZE mdl_role_assignments;
ANALYZE login_audit;