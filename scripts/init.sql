-- Inserta los roles si no existen
INSERT INTO "mdl_role" ("name", "shortname", "description", "sortorder", "archetype")
VALUES 
    ('Administrador', 'admin', 'Rol para los administradores', 1, 'manager'),
    ('Maestro', 'teacher', 'Rol para los docentes', 2, 'teacher'),
    ('Estudiante', 'student', 'Rol para los estudiantes', 3, 'student')
ON CONFLICT ("shortname") DO NOTHING;

-- Inserción de categorías de cursos (si no existe)
INSERT INTO "mdl_course_categories" ("name", "description", "parent", "sortorder", "visible", "visibleold", "timemodified", "depth", "path")
SELECT 'Ingeniería en Sistemas', 'Departamento de Ingeniería en Sistemas', 0, 1, true, true, CURRENT_TIMESTAMP, 1, '/1'
WHERE NOT EXISTS (
    SELECT 1 FROM "mdl_course_categories" WHERE "name" = 'Ingeniería en Sistemas'
);

-- Inserción de cursos (si no existen)
INSERT INTO "mdl_course" ("category", "sortorder", "fullname", "shortname", "summary", "format", "startdate", "visible", "timecreated", "timemodified")
SELECT 1, 1, 'Programación Orientada a Objetos', 'POO', 'Curso de Programación Orientada a Objetos', 'topics', CURRENT_TIMESTAMP, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM "mdl_course" WHERE "shortname" = 'POO'
);

INSERT INTO "mdl_course" ("category", "sortorder", "fullname", "shortname", "summary", "format", "startdate", "visible", "timecreated", "timemodified")
SELECT 1, 2, 'Ingeniería de Software', 'IS', 'Curso de Ingeniería de Software', 'topics', CURRENT_TIMESTAMP, true, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
WHERE NOT EXISTS (
    SELECT 1 FROM "mdl_course" WHERE "shortname" = 'IS'
);

-- Obtener IDs de usuarios existentes (para verificar si existen antes de insertar)
DO $$
DECLARE
    admin_exists BOOLEAN;
    claude_exists BOOLEAN;
    frank_exists BOOLEAN;
    edwar_exists BOOLEAN;
    daniel_exists BOOLEAN;
    elvis_exists BOOLEAN;
    
    admin_id INTEGER;
    claude_id INTEGER;
    frank_id INTEGER;
    edwar_id INTEGER;
    daniel_id INTEGER;
    elvis_id INTEGER;
    
    poo_id INTEGER;
    is_id INTEGER;
BEGIN
    -- Verificar si los usuarios existen
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'admin') INTO admin_exists;
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'claude') INTO claude_exists;
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'frank') INTO frank_exists;
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'edwar') INTO edwar_exists;
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'daniel') INTO daniel_exists;
    SELECT EXISTS(SELECT 1 FROM "mdl_user" WHERE "username" = 'elvis') INTO elvis_exists;
    
    -- Insertar usuarios solo si no existen
    IF NOT admin_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('admin', '1234', 'Administrador', 'Sistema', 'admin@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT claude_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('claude', '1234', 'Claude', 'Docente', 'claude@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT frank_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('frank', '1234', 'Frank', 'Estudiante', 'frank@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT edwar_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('edwar', '1234', 'Edwar', 'Estudiante', 'edwar@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT daniel_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('daniel', '1234', 'Daniel', 'Estudiante', 'daniel@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT elvis_exists THEN
        INSERT INTO "mdl_user" ("username", "password", "firstname", "lastname", "email", "auth", "confirmed", "lang", "timezone", "institution", "department", "timecreated", "timemodified")
        VALUES ('elvis', '1234', 'Elvis', 'Estudiante', 'elvis@unah.edu.hn', 'manual', true, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Obtener IDs de usuarios
    SELECT id INTO admin_id FROM "mdl_user" WHERE "username" = 'admin';
    SELECT id INTO claude_id FROM "mdl_user" WHERE "username" = 'claude';
    SELECT id INTO frank_id FROM "mdl_user" WHERE "username" = 'frank';
    SELECT id INTO edwar_id FROM "mdl_user" WHERE "username" = 'edwar';
    SELECT id INTO daniel_id FROM "mdl_user" WHERE "username" = 'daniel';
    SELECT id INTO elvis_id FROM "mdl_user" WHERE "username" = 'elvis';
    
    -- Obtener IDs de cursos
    SELECT id INTO poo_id FROM "mdl_course" WHERE "shortname" = 'POO';
    SELECT id INTO is_id FROM "mdl_course" WHERE "shortname" = 'IS';
    
    -- Insertar módulos si no existen
    INSERT INTO "mdl_modules" ("name", "cron", "visible")
    SELECT 'assign', 0, true
    WHERE NOT EXISTS (SELECT 1 FROM "mdl_modules" WHERE "name" = 'assign');
    
    INSERT INTO "mdl_modules" ("name", "cron", "visible")
    SELECT 'forum', 0, true
    WHERE NOT EXISTS (SELECT 1 FROM "mdl_modules" WHERE "name" = 'forum');
    
    INSERT INTO "mdl_modules" ("name", "cron", "visible")
    SELECT 'resource', 0, true
    WHERE NOT EXISTS (SELECT 1 FROM "mdl_modules" WHERE "name" = 'resource');
    
    INSERT INTO "mdl_modules" ("name", "cron", "visible")
    SELECT 'quiz', 0, true
    WHERE NOT EXISTS (SELECT 1 FROM "mdl_modules" WHERE "name" = 'quiz');
    
    -- Asignar roles a los usuarios (si no están asignados)
    -- Admin
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = admin_id AND "roleid" = 1) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (1, 1, admin_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Claude
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = claude_id AND "roleid" = 2) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (2, 1, claude_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Frank
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = frank_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (3, 1, frank_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Edwar
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = edwar_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (3, 1, edwar_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Daniel
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = daniel_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (3, 1, daniel_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Elvis
    IF NOT EXISTS (SELECT 1 FROM "mdl_role_assignments" WHERE "userid" = elvis_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_role_assignments" ("roleid", "contextid", "userid", "timemodified", "modifierid")
        VALUES (3, 1, elvis_id, CURRENT_TIMESTAMP, admin_id);
    END IF;
    
    -- Crear tabla mdl_userrole si no existe (para Prisma)
    EXECUTE 'CREATE TABLE IF NOT EXISTS "mdl_userrole" (
        "id" SERIAL PRIMARY KEY,
        "userid" INTEGER NOT NULL,
        "roleid" INTEGER NOT NULL,
        "timemodified" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY ("userid") REFERENCES "mdl_user"("id"),
        FOREIGN KEY ("roleid") REFERENCES "mdl_role"("id")
    )';
    
    -- Insertar relaciones usuario-rol en la tabla intermedia
    -- Admin
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = admin_id AND "roleid" = 1) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (admin_id, 1);
    END IF;
    
    -- Claude
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = claude_id AND "roleid" = 2) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (claude_id, 2);
    END IF;
    
    -- Frank
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = frank_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (frank_id, 3);
    END IF;
    
    -- Edwar
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = edwar_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (edwar_id, 3);
    END IF;
    
    -- Daniel
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = daniel_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (daniel_id, 3);
    END IF;
    
    -- Elvis
    IF NOT EXISTS (SELECT 1 FROM "mdl_userrole" WHERE "userid" = elvis_id AND "roleid" = 3) THEN
        INSERT INTO "mdl_userrole" ("userid", "roleid")
        VALUES (elvis_id, 3);
    END IF;
    
    -- Matricular estudiantes en cursos (si no están matriculados)
    -- Frank en POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = frank_id AND "courseid" = poo_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (1, frank_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Edwar en POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = edwar_id AND "courseid" = poo_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (1, edwar_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Daniel en POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = daniel_id AND "courseid" = poo_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (1, daniel_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Elvis en POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = elvis_id AND "courseid" = poo_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (1, elvis_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Frank en IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = frank_id AND "courseid" = is_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (2, frank_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Edwar en IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = edwar_id AND "courseid" = is_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (2, edwar_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Daniel en IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = daniel_id AND "courseid" = is_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (2, daniel_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Elvis en IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = elvis_id AND "courseid" = is_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (2, elvis_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Claude en POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = claude_id AND "courseid" = poo_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (3, claude_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Claude en IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_user_enrolments" WHERE "userid" = claude_id AND "courseid" = is_id) THEN
        INSERT INTO "mdl_user_enrolments" ("enrolid", "userid", "courseid", "status", "timecreated", "timemodified")
        VALUES (4, claude_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Crear secciones para los cursos (si no existen)
    -- POO
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = poo_id AND "section" = 0) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (poo_id, 0, 'General', 'Sección general del curso', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = poo_id AND "section" = 1) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (poo_id, 1, 'Introducción a POO', 'Conceptos básicos de la programación orientada a objetos', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = poo_id AND "section" = 2) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (poo_id, 2, 'Clases y Objetos', 'Definición de clases y creación de objetos', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = poo_id AND "section" = 3) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (poo_id, 3, 'Herencia', 'Herencia y polimorfismo', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = poo_id AND "section" = 4) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (poo_id, 4, 'Interfaces', 'Interfaces y clases abstractas', true, CURRENT_TIMESTAMP);
    END IF;
    
    -- IS
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = is_id AND "section" = 0) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (is_id, 0, 'General', 'Sección general del curso', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = is_id AND "section" = 1) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (is_id, 1, 'Fundamentos de IS', 'Introducción a la ingeniería de software', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = is_id AND "section" = 2) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (is_id, 2, 'Requerimientos', 'Análisis y especificación de requerimientos', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = is_id AND "section" = 3) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (is_id, 3, 'Diseño de Software', 'Principios y patrones de diseño', true, CURRENT_TIMESTAMP);
    END IF;
    
    IF NOT EXISTS (SELECT 1 FROM "mdl_course_sections" WHERE "course" = is_id AND "section" = 4) THEN
        INSERT INTO "mdl_course_sections" ("course", "section", "name", "summary", "visible", "timemodified")
        VALUES (is_id, 4, 'Pruebas', 'Metodologías de pruebas de software', true, CURRENT_TIMESTAMP);
    END IF;
END $$;
