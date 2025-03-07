-- Inserta los roles si no existen
INSERT INTO "mdl_role" ("name", "shortname", "description", "sortorder", "archetype")
VALUES 
    ('Administrador', 'admin', 'Rol para los administradores', 1, 'manager'),
    ('Maestro', 'teacher', 'Rol para los docentes', 2, 'teacher'),
    ('Estudiante', 'student', 'Rol para los estudiantes', 3, 'student')
ON CONFLICT ("shortname") DO NOTHING;
