-- Inserta los roles si no existen
SET NOCOUNT ON;

-- Crear las tablas primero, luego llenarlas para evitar problemas de restricciones
-- Insertar roles primero (debido a la restricción FK en role_assignments)
IF NOT EXISTS (SELECT 1 FROM [mdl_role] WHERE [shortname] = 'admin')
BEGIN
    INSERT INTO [mdl_role] ([name], [shortname], [description], [sortorder], [archetype])
    VALUES ('Administrador', 'admin', 'Rol para los administradores', 1, 'manager')
END

IF NOT EXISTS (SELECT 1 FROM [mdl_role] WHERE [shortname] = 'teacher')
BEGIN
    INSERT INTO [mdl_role] ([name], [shortname], [description], [sortorder], [archetype])
    VALUES ('Maestro', 'teacher', 'Rol para los docentes', 2, 'teacher')
END

IF NOT EXISTS (SELECT 1 FROM [mdl_role] WHERE [shortname] = 'student')
BEGIN
    INSERT INTO [mdl_role] ([name], [shortname], [description], [sortorder], [archetype])
    VALUES ('Estudiante', 'student', 'Rol para los estudiantes', 3, 'student')
END

-- Inserción de categorías de cursos (si no existe)
IF NOT EXISTS (SELECT 1 FROM [mdl_course_categories] WHERE [name] = 'Ingeniería en Sistemas')
BEGIN
    INSERT INTO [mdl_course_categories] ([name], [description], [parent], [sortorder], [visible], [visibleold], [timemodified], [depth], [path])
    VALUES ('Ingeniería en Sistemas', 'Departamento de Ingeniería en Sistemas', 0, 1, 1, 1, GETDATE(), 1, '/1')
END

-- Inserción de cursos (si no existen)
IF NOT EXISTS (SELECT 1 FROM [mdl_course] WHERE [shortname] = 'POO')
BEGIN
    INSERT INTO [mdl_course] ([category], [sortorder], [fullname], [shortname], [summary], [format], [startdate], [visible], [timecreated], [timemodified])
    VALUES (1, 1, 'Programación Orientada a Objetos', 'POO', 'Curso de Programación Orientada a Objetos', 'topics', GETDATE(), 1, GETDATE(), GETDATE())
END

IF NOT EXISTS (SELECT 1 FROM [mdl_course] WHERE [shortname] = 'IS')
BEGIN
    INSERT INTO [mdl_course] ([category], [sortorder], [fullname], [shortname], [summary], [format], [startdate], [visible], [timecreated], [timemodified])
    VALUES (1, 2, 'Ingeniería de Software', 'IS', 'Curso de Ingeniería de Software', 'topics', GETDATE(), 1, GETDATE(), GETDATE())
END

-- Insertar módulos si no existen
IF NOT EXISTS (SELECT 1 FROM [mdl_modules] WHERE [name] = 'assign')
BEGIN
    INSERT INTO [mdl_modules] ([name], [cron], [visible])
    VALUES ('assign', 0, 1);
END

IF NOT EXISTS (SELECT 1 FROM [mdl_modules] WHERE [name] = 'forum')
BEGIN
    INSERT INTO [mdl_modules] ([name], [cron], [visible])
    VALUES ('forum', 0, 1);
END

IF NOT EXISTS (SELECT 1 FROM [mdl_modules] WHERE [name] = 'resource')
BEGIN
    INSERT INTO [mdl_modules] ([name], [cron], [visible])
    VALUES ('resource', 0, 1);
END

IF NOT EXISTS (SELECT 1 FROM [mdl_modules] WHERE [name] = 'quiz')
BEGIN
    INSERT INTO [mdl_modules] ([name], [cron], [visible])
    VALUES ('quiz', 0, 1);
END

-- Crear procedimiento almacenado para inicializar datos
IF EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[initialize_data]') AND type in (N'P'))
    DROP PROCEDURE [dbo].[initialize_data]
GO

CREATE PROCEDURE [dbo].[initialize_data]
AS
BEGIN
    SET NOCOUNT ON;
    
    DECLARE @admin_exists INT;
    DECLARE @claude_exists INT;
    DECLARE @frank_exists INT;
    DECLARE @edwar_exists INT;
    DECLARE @daniel_exists INT;
    DECLARE @elvis_exists INT;
    
    DECLARE @admin_id INT;
    DECLARE @claude_id INT;
    DECLARE @frank_id INT;
    DECLARE @edwar_id INT;
    DECLARE @daniel_id INT;
    DECLARE @elvis_id INT;
    
    DECLARE @poo_id INT;
    DECLARE @is_id INT;
    
    DECLARE @admin_role_id INT;
    DECLARE @teacher_role_id INT;
    DECLARE @student_role_id INT;
    
    -- Obtener IDs de roles
    SELECT @admin_role_id = id FROM [mdl_role] WHERE [shortname] = 'admin';
    SELECT @teacher_role_id = id FROM [mdl_role] WHERE [shortname] = 'teacher';
    SELECT @student_role_id = id FROM [mdl_role] WHERE [shortname] = 'student';
    
    -- Verificar si los usuarios existen
    SELECT @admin_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'admin';
    SELECT @claude_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'claude';
    SELECT @frank_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'frank';
    SELECT @edwar_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'edwar';
    SELECT @daniel_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'daniel';
    SELECT @elvis_exists = COUNT(*) FROM [mdl_user] WHERE [username] = 'elvis';
    
    -- Insertar usuarios solo si no existen
    IF @admin_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('admin', '1234', 'Administrador', 'Sistema', 'admin@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    IF @claude_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('claude', '1234', 'Claude', 'Docente', 'claude@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    IF @frank_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('frank', '1234', 'Frank', 'Estudiante', 'frank@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    IF @edwar_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('edwar', '1234', 'Edwar', 'Estudiante', 'edwar@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    IF @daniel_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('daniel', '1234', 'Daniel', 'Estudiante', 'daniel@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    IF @elvis_exists = 0
    BEGIN
        INSERT INTO [mdl_user] ([username], [password], [firstname], [lastname], [email], [auth], [confirmed], [lang], [timezone], [institution], [department], [timecreated], [timemodified])
        VALUES ('elvis', '1234', 'Elvis', 'Estudiante', 'elvis@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', GETDATE(), GETDATE());
    END
    
    -- Obtener IDs de usuarios
    SELECT @admin_id = id FROM [mdl_user] WHERE [username] = 'admin';
    SELECT @claude_id = id FROM [mdl_user] WHERE [username] = 'claude';
    SELECT @frank_id = id FROM [mdl_user] WHERE [username] = 'frank';
    SELECT @edwar_id = id FROM [mdl_user] WHERE [username] = 'edwar';
    SELECT @daniel_id = id FROM [mdl_user] WHERE [username] = 'daniel';
    SELECT @elvis_id = id FROM [mdl_user] WHERE [username] = 'elvis';
    
    -- Obtener IDs de cursos
    SELECT @poo_id = id FROM [mdl_course] WHERE [shortname] = 'POO';
    SELECT @is_id = id FROM [mdl_course] WHERE [shortname] = 'IS';
    
    -- Asignar roles a los usuarios (si no están asignados)
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @admin_role_id AND [userid] = @admin_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@admin_role_id, 1, @admin_id, GETDATE(), @admin_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @teacher_role_id AND [userid] = @claude_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@teacher_role_id, 1, @claude_id, GETDATE(), @admin_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @student_role_id AND [userid] = @frank_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@student_role_id, 1, @frank_id, GETDATE(), @admin_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @student_role_id AND [userid] = @edwar_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@student_role_id, 1, @edwar_id, GETDATE(), @admin_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @student_role_id AND [userid] = @daniel_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@student_role_id, 1, @daniel_id, GETDATE(), @admin_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_role_assignments] WHERE [roleid] = @student_role_id AND [userid] = @elvis_id)
    BEGIN
        INSERT INTO [mdl_role_assignments] ([roleid], [contextid], [userid], [timemodified], [modifierid])
        VALUES (@student_role_id, 1, @elvis_id, GETDATE(), @admin_id);
    END
    
    -- Insertar relaciones usuario-rol en la tabla intermedia
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @admin_id AND [roleid] = @admin_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@admin_id, @admin_role_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @claude_id AND [roleid] = @teacher_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@claude_id, @teacher_role_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @frank_id AND [roleid] = @student_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@frank_id, @student_role_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @edwar_id AND [roleid] = @student_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@edwar_id, @student_role_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @daniel_id AND [roleid] = @student_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@daniel_id, @student_role_id);
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_userrole] WHERE [userid] = @elvis_id AND [roleid] = @student_role_id)
    BEGIN
        INSERT INTO [mdl_userrole] ([userid], [roleid])
        VALUES (@elvis_id, @student_role_id);
    END
    
    -- Matricular estudiantes en cursos (si no están matriculados)
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @frank_id AND [courseid] = @poo_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (1, @frank_id, @poo_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @edwar_id AND [courseid] = @poo_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (1, @edwar_id, @poo_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @daniel_id AND [courseid] = @poo_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (1, @daniel_id, @poo_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @elvis_id AND [courseid] = @poo_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (1, @elvis_id, @poo_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @frank_id AND [courseid] = @is_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (2, @frank_id, @is_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @edwar_id AND [courseid] = @is_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (2, @edwar_id, @is_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @daniel_id AND [courseid] = @is_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (2, @daniel_id, @is_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @elvis_id AND [courseid] = @is_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (2, @elvis_id, @is_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @claude_id AND [courseid] = @poo_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (3, @claude_id, @poo_id, 0, GETDATE(), GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_user_enrolments] WHERE [userid] = @claude_id AND [courseid] = @is_id)
    BEGIN
        INSERT INTO [mdl_user_enrolments] ([enrolid], [userid], [courseid], [status], [timecreated], [timemodified])
        VALUES (4, @claude_id, @is_id, 0, GETDATE(), GETDATE());
    END
    
    -- Crear secciones para los cursos (si no existen)
    -- POO
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @poo_id AND [section] = 0)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@poo_id, 0, 'General', 'Sección general del curso', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @poo_id AND [section] = 1)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@poo_id, 1, 'Introducción a POO', 'Conceptos básicos de la programación orientada a objetos', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @poo_id AND [section] = 2)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@poo_id, 2, 'Clases y Objetos', 'Definición de clases y creación de objetos', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @poo_id AND [section] = 3)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@poo_id, 3, 'Herencia', 'Herencia y polimorfismo', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @poo_id AND [section] = 4)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@poo_id, 4, 'Interfaces', 'Interfaces y clases abstractas', 1, GETDATE());
    END
    
    -- IS
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @is_id AND [section] = 0)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@is_id, 0, 'General', 'Sección general del curso', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @is_id AND [section] = 1)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@is_id, 1, 'Fundamentos de IS', 'Introducción a la ingeniería de software', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @is_id AND [section] = 2)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@is_id, 2, 'Requerimientos', 'Análisis y especificación de requerimientos', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @is_id AND [section] = 3)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@is_id, 3, 'Diseño de Software', 'Principios y patrones de diseño', 1, GETDATE());
    END
    
    IF NOT EXISTS (SELECT 1 FROM [mdl_course_sections] WHERE [course] = @is_id AND [section] = 4)
    BEGIN
        INSERT INTO [mdl_course_sections] ([course], [section], [name], [summary], [visible], [timemodified])
        VALUES (@is_id, 4, 'Pruebas', 'Metodologías de pruebas de software', 1, GETDATE());
    END
END
GO

-- Ejecutar el procedimiento almacenado
EXEC [dbo].[initialize_data]
GO