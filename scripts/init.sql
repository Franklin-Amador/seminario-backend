-- Inserta los roles si no existen
INSERT IGNORE INTO `mdl_role` (`name`, `shortname`, `description`, `sortorder`, `archetype`)
VALUES 
    ('Administrador', 'admin', 'Rol para los administradores', 1, 'manager'),
    ('Maestro', 'teacher', 'Rol para los docentes', 2, 'teacher'),
    ('Estudiante', 'student', 'Rol para los estudiantes', 3, 'student');

-- Inserción de categorías de cursos (si no existe)
INSERT IGNORE INTO `mdl_course_categories` (`name`, `description`, `parent`, `sortorder`, `visible`, `visibleold`, `timemodified`, `depth`, `path`)
SELECT 'Ingeniería en Sistemas', 'Departamento de Ingeniería en Sistemas', 0, 1, 1, 1, CURRENT_TIMESTAMP, 1, '/1'
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM `mdl_course_categories` WHERE `name` = 'Ingeniería en Sistemas'
);

-- Inserción de cursos (si no existen)
INSERT IGNORE INTO `mdl_course` (`category`, `sortorder`, `fullname`, `shortname`, `summary`, `format`, `startdate`, `visible`, `timecreated`, `timemodified`)
SELECT 1, 1, 'Programación Orientada a Objetos', 'POO', 'Curso de Programación Orientada a Objetos', 'topics', CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM `mdl_course` WHERE `shortname` = 'POO'
);

INSERT IGNORE INTO `mdl_course` (`category`, `sortorder`, `fullname`, `shortname`, `summary`, `format`, `startdate`, `visible`, `timecreated`, `timemodified`)
SELECT 1, 2, 'Ingeniería de Software', 'IS', 'Curso de Ingeniería de Software', 'topics', CURRENT_TIMESTAMP, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
FROM DUAL
WHERE NOT EXISTS (
    SELECT 1 FROM `mdl_course` WHERE `shortname` = 'IS'
);

DROP PROCEDURE IF EXISTS initialize_data;

-- Crear procedimiento almacenado para el resto de las operaciones
DELIMITER //
CREATE PROCEDURE initialize_data()
BEGIN
    DECLARE admin_exists INT;
    DECLARE claude_exists INT;
    DECLARE frank_exists INT;
    DECLARE edwar_exists INT;
    DECLARE daniel_exists INT;
    DECLARE elvis_exists INT;
    
    DECLARE admin_id INT;
    DECLARE claude_id INT;
    DECLARE frank_id INT;
    DECLARE edwar_id INT;
    DECLARE daniel_id INT;
    DECLARE elvis_id INT;
    
    DECLARE poo_id INT;
    DECLARE is_id INT;
    
    -- Verificar si los usuarios existen
    SELECT COUNT(*) INTO admin_exists FROM `mdl_user` WHERE `username` = 'admin';
    SELECT COUNT(*) INTO claude_exists FROM `mdl_user` WHERE `username` = 'claude';
    SELECT COUNT(*) INTO frank_exists FROM `mdl_user` WHERE `username` = 'frank';
    SELECT COUNT(*) INTO edwar_exists FROM `mdl_user` WHERE `username` = 'edwar';
    SELECT COUNT(*) INTO daniel_exists FROM `mdl_user` WHERE `username` = 'daniel';
    SELECT COUNT(*) INTO elvis_exists FROM `mdl_user` WHERE `username` = 'elvis';
    
    -- Insertar usuarios solo si no existen
    IF admin_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('admin', '1234', 'Administrador', 'Sistema', 'admin@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF claude_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('claude', '1234', 'Claude', 'Docente', 'claude@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF frank_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('frank', '1234', 'Frank', 'Estudiante', 'frank@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF edwar_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('edwar', '1234', 'Edwar', 'Estudiante', 'edwar@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF daniel_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('daniel', '1234', 'Daniel', 'Estudiante', 'daniel@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    IF elvis_exists = 0 THEN
        INSERT INTO `mdl_user` (`username`, `password`, `firstname`, `lastname`, `email`, `auth`, `confirmed`, `lang`, `timezone`, `institution`, `department`, `timecreated`, `timemodified`)
        VALUES ('elvis', '1234', 'Elvis', 'Estudiante', 'elvis@unah.edu.hn', 'manual', 1, 'es', '99', 'UNAH', 'IS', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    END IF;
    
    -- Obtener IDs de usuarios
    SELECT id INTO admin_id FROM `mdl_user` WHERE `username` = 'admin';
    SELECT id INTO claude_id FROM `mdl_user` WHERE `username` = 'claude';
    SELECT id INTO frank_id FROM `mdl_user` WHERE `username` = 'frank';
    SELECT id INTO edwar_id FROM `mdl_user` WHERE `username` = 'edwar';
    SELECT id INTO daniel_id FROM `mdl_user` WHERE `username` = 'daniel';
    SELECT id INTO elvis_id FROM `mdl_user` WHERE `username` = 'elvis';
    
    -- Obtener IDs de cursos
    SELECT id INTO poo_id FROM `mdl_course` WHERE `shortname` = 'POO';
    SELECT id INTO is_id FROM `mdl_course` WHERE `shortname` = 'IS';
    
    -- Insertar módulos si no existen
    INSERT IGNORE INTO `mdl_modules` (`name`, `cron`, `visible`)
    VALUES 
        ('assign', 0, 1),
        ('forum', 0, 1),
        ('resource', 0, 1),
        ('quiz', 0, 1);
    
    -- Asignar roles a los usuarios (si no están asignados)
    INSERT IGNORE INTO `mdl_role_assignments` (`roleid`, `contextid`, `userid`, `timemodified`, `modifierid`)
    VALUES 
        (1, 1, admin_id, CURRENT_TIMESTAMP, admin_id),
        (2, 1, claude_id, CURRENT_TIMESTAMP, admin_id),
        (3, 1, frank_id, CURRENT_TIMESTAMP, admin_id),
        (3, 1, edwar_id, CURRENT_TIMESTAMP, admin_id),
        (3, 1, daniel_id, CURRENT_TIMESTAMP, admin_id),
        (3, 1, elvis_id, CURRENT_TIMESTAMP, admin_id);
    
    -- Crear tabla mdl_userrole si no existe (para Prisma)
    SET @create_userrole = CONCAT(
        'CREATE TABLE IF NOT EXISTS `mdl_userrole` (',
        '`id` INT AUTO_INCREMENT PRIMARY KEY,',
        '`userid` INT NOT NULL,',
        '`roleid` INT NOT NULL,',
        '`timemodified` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,',
        'FOREIGN KEY (`userid`) REFERENCES `mdl_user`(`id`),',
        'FOREIGN KEY (`roleid`) REFERENCES `mdl_role`(`id`)',
        ')'
    );
    PREPARE stmt FROM @create_userrole;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    -- Insertar relaciones usuario-rol en la tabla intermedia
    INSERT IGNORE INTO `mdl_userrole` (`userid`, `roleid`)
    VALUES 
        (admin_id, 1),
        (claude_id, 2),
        (frank_id, 3),
        (edwar_id, 3),
        (daniel_id, 3),
        (elvis_id, 3);
    
    -- Matricular estudiantes en cursos (si no están matriculados)
    INSERT IGNORE INTO `mdl_user_enrolments` (`enrolid`, `userid`, `courseid`, `status`, `timecreated`, `timemodified`)
    VALUES 
        (1, frank_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (1, edwar_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (1, daniel_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (1, elvis_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, frank_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, edwar_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, daniel_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (2, elvis_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (3, claude_id, poo_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
        (4, claude_id, is_id, 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
    
    -- Crear secciones para los cursos (si no existen)
    -- POO
    INSERT IGNORE INTO `mdl_course_sections` (`course`, `section`, `name`, `summary`, `visible`, `timemodified`)
    VALUES 
        (poo_id, 0, 'General', 'Sección general del curso', 1, CURRENT_TIMESTAMP),
        (poo_id, 1, 'Introducción a POO', 'Conceptos básicos de la programación orientada a objetos', 1, CURRENT_TIMESTAMP),
        (poo_id, 2, 'Clases y Objetos', 'Definición de clases y creación de objetos', 1, CURRENT_TIMESTAMP),
        (poo_id, 3, 'Herencia', 'Herencia y polimorfismo', 1, CURRENT_TIMESTAMP),
        (poo_id, 4, 'Interfaces', 'Interfaces y clases abstractas', 1, CURRENT_TIMESTAMP);
    
    -- IS
    INSERT IGNORE INTO `mdl_course_sections` (`course`, `section`, `name`, `summary`, `visible`, `timemodified`)
    VALUES 
        (is_id, 0, 'General', 'Sección general del curso', 1, CURRENT_TIMESTAMP),
        (is_id, 1, 'Fundamentos de IS', 'Introducción a la ingeniería de software', 1, CURRENT_TIMESTAMP),
        (is_id, 2, 'Requerimientos', 'Análisis y especificación de requerimientos', 1, CURRENT_TIMESTAMP),
        (is_id, 3, 'Diseño de Software', 'Principios y patrones de diseño', 1, CURRENT_TIMESTAMP),
        (is_id, 4, 'Pruebas', 'Metodologías de pruebas de software', 1, CURRENT_TIMESTAMP);
END //
DELIMITER ;

-- Ejecutar el procedimiento almacenado
CALL initialize_data();

-- Limpiar (opcional)
DROP PROCEDURE IF EXISTS initialize_data;
