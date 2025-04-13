import http from "k6/http";
import { check, sleep } from "k6";
import { Trend, Counter, Rate } from "k6/metrics";
import { randomIntBetween } from "https://jslib.k6.io/k6-utils/1.2.0/index.js";

// Definir métricas personalizadas para cada endpoint
// GET endpoints
let responseTimeTrendUsers = new Trend("response_time_users");
let responseTimeTrendCategories = new Trend("response_time_categories");
let responseTimeTrendAssignments = new Trend("response_time_assignments");
let responseTimeTrendAssignmentsProx = new Trend(
  "response_time_assignments_prox",
);
let responseTimeTrendRoles = new Trend("response_time_roles");
let responseTimeTrendSections = new Trend("response_time_sections");
let responseTimeTrendCursoAssignments = new Trend(
  "response_time_curso_assignments",
);
let responseTimeTrendSeccionAssignments = new Trend(
  "response_time_seccion_assignments",
);
let responseTimeTrendAllAssignments = new Trend(
  "response_time_all_assignments",
);
let responseTimeTrendCourses = new Trend("response_time_courses");
let responseTimeTrendCourseById = new Trend("response_time_course_by_id");
let responseTimeTrendEnrollmentsByCourse = new Trend(
  "response_time_enrollments_by_course",
);
let responseTimeTrendEnrollmentsByUser = new Trend(
  "response_time_enrollments_by_user",
);
let responseTimeTrendHome = new Trend("response_time_home");
let responseTimeTrendRolById = new Trend("response_time_rol_by_id");
let responseTimeTrendSectionsByCourse = new Trend(
  "response_time_sections_by_course",
);
let responseTimeTrendSubmissionsByAssignment = new Trend(
  "response_time_submissions_by_assignment",
);
let responseTimeTrendSubmissionsByUser = new Trend(
  "response_time_submissions_by_user",
);
let responseTimeTrendUserById = new Trend("response_time_user_by_id");

// POST endpoints
let responseTimePostAssignment = new Trend("response_time_post_assignment");
let responseTimePostCourse = new Trend("response_time_post_course");
let responseTimePostEnrollment = new Trend("response_time_post_enrollment");
let responseTimePostRol = new Trend("response_time_post_rol");
let responseTimePostSection = new Trend("response_time_post_section");
let responseTimePostSubmission = new Trend("response_time_post_submission");

// PUT endpoints
let responseTimePutAssignment = new Trend("response_time_put_assignment");
let responseTimePutCourse = new Trend("response_time_put_course");
let responseTimePutEnrollment = new Trend("response_time_put_enrollment");
let responseTimePutSection = new Trend("response_time_put_section");

// DELETE endpoints
let responseTimeDeleteAssignment = new Trend("response_time_delete_assignment");
let responseTimeDeleteEnrollment = new Trend("response_time_delete_enrollment");
let responseTimeDeleteRol = new Trend("response_time_delete_rol");
let responseTimeDeleteSection = new Trend("response_time_delete_section");
let responseTimeDeleteSubmission = new Trend("response_time_delete_submission");

// Métricas combinadas y de errores
let responseTimeTrendCombined = new Trend("response_time_combined");
let errorRate = new Rate("error_rate");
let errorCounter = new Counter("error_count");
let successCounter = new Counter("success_count");

// Datos para pruebas de creación
let testData = {
  // ID iniciales de elementos creados para usar en operaciones posteriores
  createdAssignmentId: 0,
  createdCourseId: 0,
  createdEnrollmentId: 0,
  createdRolId: 0,
  createdSectionId: 0,
  createdSubmissionId: 0,

  // IDs existentes en la base de datos (supuestos)
  existingCourseId: 1,
  existingUserId: 1,
  existingAssignmentId: 1,
  existingSectionId: 1,
};

// Definir opciones de carga
export let options = {
  vus: 1300, // Número de usuarios virtuales 200-600-1000
  duration: "600s", // Duración de la prueba (30 minutos)
  thresholds: {
    error_rate: ["rate<0.1"], // Tasa de error menor al 10%
    http_req_duration: ["p(95)<2000"], // 95% de las solicitudes por debajo de 2s
  },
};

// Función principal
export default function () {
  // Aleatorizamos qué tipo de operación ejecutamos para diversificar la carga
  let operationType = Math.random();

  if (operationType < 0.7) {
    // 70% de las veces realizamos operaciones GET (más comunes en aplicaciones reales)
    testGetEndpoints();
  } else if (operationType < 0.85) {
    // 15% de las veces realizamos operaciones POST
    testPostEndpoints();
  } else if (operationType < 0.95) {
    // 10% de las veces realizamos operaciones PUT
    testPutEndpoints();
  } else {
    // 5% de las veces realizamos operaciones DELETE
    testDeleteEndpoints();
  }

  // Pequeña pausa entre iteraciones para simular comportamiento más realista
  sleep(randomIntBetween(1, 3));
}

function testGetEndpoints() {
  // Grupo de operaciones GET para APIs más utilizadas
  let responses = {
    home: http.get("http://app:8000/"),
    users: http.get("http://app:8000/api/users"),
    categories: http.get("http://app:8000/api/categories"),
    roles: http.get("http://app:8000/api/roles"),
    courses: http.get("http://app:8000/api/courses"),
    assignments: http.get(
      `http://app:8000/api/assignments/${testData.existingAssignmentId}`,
    ),
    // La versión "assignmentsProx" no tiene equivalente directo en los nuevos endpoints,
    // usaremos el endpoint general de assignments
    assignmentsProx: http.get("http://app:8000/api/assignments"),
    sections: http.get("http://app:8000/api/sections"),
  };

  // Grupo de operaciones GET para APIs menos utilizadas (con probabilidad)
  if (Math.random() < 0.3) {
    responses.userById = http.get(
      `http://app:8000/api/users/${testData.existingUserId}`,
    );
    responses.rolById = http.get(
      `http://app:8000/api/roles/${randomIntBetween(1, 5)}`,
    );
    responses.courseById = http.get(
      `http://app:8000/api/courses/${testData.existingCourseId}`,
    );
    responses.courseSections = http.get(
      `http://app:8000/api/sections/${testData.existingCourseId}`,
    );
    responses.cursoAssignments = http.get(
      `http://app:8000/api/courses/${testData.existingCourseId}/assignments`,
    );
    // Para asignaciones por sección, no hay endpoint directo, usamos el de curso
    responses.seccionAssignments = http.get(
      `http://app:8000/api/courses/${testData.existingCourseId}/assignments`,
    );
    // Para todas las asignaciones, usamos el endpoint general
    responses.allAssignments = http.get("http://app:8000/api/assignments");
    responses.enrollmentsByCourse = http.get(
      `http://app:8000/api/courses/${testData.existingCourseId}/enrollments`,
    );
    responses.enrollmentsByUser = http.get(
      `http://app:8000/api/users/${testData.existingUserId}/enrollments`,
    );
    responses.submissionsByAssignment = http.get(
      `http://app:8000/api/assignments/${testData.existingAssignmentId}/submissions`,
    );
    responses.submissionsByUser = http.get(
      `http://app:8000/api/users/${testData.existingUserId}/submissions`,
    );
  }

  // Verificar respuestas de las operaciones principales
  let checks = {
    "home endpoint is status 200": (r) => responses.home.status === 200,
    "users endpoint is status 200": (r) => responses.users.status === 200,
    "categories endpoint is status 200": (r) =>
      responses.categories.status === 200,
    "roles endpoint is status 200": (r) => responses.roles.status === 200,
    "courses endpoint is status 200": (r) => responses.courses.status === 200,
    "assignments endpoint is status 200": (r) =>
      responses.assignments.status === 200,
    "assignmentsProx endpoint is status 200": (r) =>
      responses.assignmentsProx.status === 200,
    "sections endpoint is status 200": (r) => responses.sections.status === 200,
  };

  // Verificar endpoints adicionales si se ejecutaron
  if (responses.userById)
    checks["userById endpoint is status 200"] = (r) =>
      responses.userById.status === 200;
  if (responses.rolById)
    checks["rolById endpoint is status 200"] = (r) =>
      responses.rolById.status === 200;
  if (responses.courseById)
    checks["courseById endpoint is status 200"] = (r) =>
      responses.courseById.status === 200;
  if (responses.courseSections)
    checks["courseSections endpoint is status 200"] = (r) =>
      responses.courseSections.status === 200;
  if (responses.cursoAssignments)
    checks["cursoAssignments endpoint is status 200"] = (r) =>
      responses.cursoAssignments.status === 200;
  if (responses.seccionAssignments)
    checks["seccionAssignments endpoint is status 200"] = (r) =>
      responses.seccionAssignments.status === 200;
  if (responses.allAssignments)
    checks["allAssignments endpoint is status 200"] = (r) =>
      responses.allAssignments.status === 200;
  if (responses.enrollmentsByCourse)
    checks["enrollmentsByCourse endpoint is status 200"] = (r) =>
      responses.enrollmentsByCourse.status === 200;
  if (responses.enrollmentsByUser)
    checks["enrollmentsByUser endpoint is status 200"] = (r) =>
      responses.enrollmentsByUser.status === 200;
  if (responses.submissionsByAssignment)
    checks["submissionsByAssignment endpoint is status 200"] = (r) =>
      responses.submissionsByAssignment.status === 200;
  if (responses.submissionsByUser)
    checks["submissionsByUser endpoint is status 200"] = (r) =>
      responses.submissionsByUser.status === 200;

  // Ejecutar todas las verificaciones
  const checkResult = check(null, checks);

  // Registrar éxitos y errores
  if (checkResult) {
    successCounter.add(1);
  } else {
    errorCounter.add(1);
    errorRate.add(1);
  }

  // Registrar métricas de tiempo de respuesta para cada endpoint
  responseTimeTrendHome.add(responses.home.timings.duration);
  responseTimeTrendUsers.add(responses.users.timings.duration);
  responseTimeTrendCategories.add(responses.categories.timings.duration);
  responseTimeTrendRoles.add(responses.roles.timings.duration);
  responseTimeTrendCourses.add(responses.courses.timings.duration);
  responseTimeTrendAssignments.add(responses.assignments.timings.duration);
  responseTimeTrendAssignmentsProx.add(
    responses.assignmentsProx.timings.duration,
  );
  responseTimeTrendSections.add(responses.sections.timings.duration);

  // Registrar métricas para endpoints adicionales
  if (responses.userById)
    responseTimeTrendUserById.add(responses.userById.timings.duration);
  if (responses.rolById)
    responseTimeTrendRolById.add(responses.rolById.timings.duration);
  if (responses.courseById)
    responseTimeTrendCourseById.add(responses.courseById.timings.duration);
  if (responses.courseSections)
    responseTimeTrendSectionsByCourse.add(
      responses.courseSections.timings.duration,
    );
  if (responses.cursoAssignments)
    responseTimeTrendCursoAssignments.add(
      responses.cursoAssignments.timings.duration,
    );
  if (responses.seccionAssignments)
    responseTimeTrendSeccionAssignments.add(
      responses.seccionAssignments.timings.duration,
    );
  if (responses.allAssignments)
    responseTimeTrendAllAssignments.add(
      responses.allAssignments.timings.duration,
    );
  if (responses.enrollmentsByCourse)
    responseTimeTrendEnrollmentsByCourse.add(
      responses.enrollmentsByCourse.timings.duration,
    );
  if (responses.enrollmentsByUser)
    responseTimeTrendEnrollmentsByUser.add(
      responses.enrollmentsByUser.timings.duration,
    );
  if (responses.submissionsByAssignment)
    responseTimeTrendSubmissionsByAssignment.add(
      responses.submissionsByAssignment.timings.duration,
    );
  if (responses.submissionsByUser)
    responseTimeTrendSubmissionsByUser.add(
      responses.submissionsByUser.timings.duration,
    );

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testPostEndpoints() {
  // Creamos un timestamp único para evitar colisiones
  const timestamp = Date.now();

  // Preparamos los payloads para las operaciones POST
  const assignmentPayload = {
    course: testData.existingCourseId,
    name: `Test Assignment ${timestamp}`,
    intro: "Esta es una asignación de prueba creada por k6",
    section: testData.existingSectionId,
    duedate: Math.floor(Date.now() / 1000) + 604800, // Una semana en el futuro
    allowsubmissionsfromdate: Math.floor(Date.now() / 1000),
    grade: 100,
    introformat: 1,
  };

  const coursePayload = {
    category: 1,
    sortorder: 1,
    fullname: `Test Course ${timestamp}`,
    shortname: `TC${timestamp}`,
    idnumber: `TC-${timestamp}`,
    summary: "Este es un curso de prueba creado por k6",
    format: "topics",
    startdate: Math.floor(Date.now() / 1000),
    enddate: Math.floor(Date.now() / 1000) + 2592000, // 30 días
    visible: 1,
  };

  const enrollmentPayload = {
    enrolid: 1,
    userid: testData.existingUserId,
    courseid: testData.existingCourseId,
    status: 0,
    timestart: Math.floor(Date.now() / 1000),
    timeend: Math.floor(Date.now() / 1000) + 2592000, // 30 días
  };

  const rolPayload = {
    name: `Test Role ${timestamp}`,
    shortname: `testrole-${timestamp}`,
    description: "Este es un rol de prueba creado por k6",
    sortorder: 1,
    archetype: "student",
  };

  const sectionPayload = {
    course: testData.existingCourseId,
    name: `Test Section ${timestamp}`,
    summary: "Esta es una sección de prueba creada por k6",
    visible: 1,
  };

  const submissionPayload = {
    assignment: testData.existingAssignmentId,
    userid: testData.existingUserId,
    status: "submitted",
    groupid: 0,
    attemptnumber: 0,
  };

  // Ejecutar las operaciones POST
  let responses = {};

  // Utilizamos una estrategia aleatoria para no crear demasiados recursos en cada ejecución
  if (Math.random() < 0.3) {
    responses.assignment = http.post(
      `http://app:8000/api/courses/${testData.existingCourseId}/assignments`,
      JSON.stringify(assignmentPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  if (Math.random() < 0.2) {
    responses.course = http.post(
      "http://app:8000/api/courses",
      JSON.stringify(coursePayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  if (Math.random() < 0.3) {
    responses.enrollment = http.post(
      "http://app:8000/api/enrollments",
      JSON.stringify(enrollmentPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  if (Math.random() < 0.2) {
    responses.rol = http.post(
      "http://app:8000/api/roles",
      JSON.stringify(rolPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  if (Math.random() < 0.3) {
    responses.section = http.post(
      "http://app:8000/api/sections",
      JSON.stringify(sectionPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  if (Math.random() < 0.3) {
    responses.submission = http.post(
      `http://app:8000/api/assignments/${testData.existingAssignmentId}/submissions`,
      JSON.stringify(submissionPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  // Verificar respuestas
  let checks = {};
  if (responses.assignment) {
    checks["create assignment is status 201"] = (r) =>
      responses.assignment.status === 201 ||
      responses.assignment.status === 200;
    // Extraer el ID si la creación fue exitosa
    if (
      responses.assignment.status === 201 ||
      responses.assignment.status === 200
    ) {
      try {
        // Asumimos que la respuesta contiene alguna información sobre el elemento creado
        // Esto dependerá de cómo esté estructurada la respuesta de tu API
        testData.createdAssignmentId =
          responses.assignment.json().id || testData.existingAssignmentId;
      } catch (e) {
        // Si no podemos extraer el ID, seguimos usando el existente
      }
    }
  }

  if (responses.course) {
    checks["create course is status 201"] = (r) =>
      responses.course.status === 201 || responses.course.status === 200;
    if (responses.course.status === 201 || responses.course.status === 200) {
      try {
        testData.createdCourseId =
          responses.course.json().id || testData.existingCourseId;
      } catch (e) {}
    }
  }

  if (responses.enrollment) {
    checks["create enrollment is status 201"] = (r) =>
      responses.enrollment.status === 201 ||
      responses.enrollment.status === 200;
    if (
      responses.enrollment.status === 201 ||
      responses.enrollment.status === 200
    ) {
      try {
        testData.createdEnrollmentId = responses.enrollment.json().id || 0;
      } catch (e) {}
    }
  }

  if (responses.rol) {
    checks["create rol is status 201"] = (r) =>
      responses.rol.status === 201 || responses.rol.status === 200;
    if (responses.rol.status === 201 || responses.rol.status === 200) {
      try {
        testData.createdRolId = responses.rol.json().id || 0;
      } catch (e) {}
    }
  }

  if (responses.section) {
    checks["create section is status 201"] = (r) =>
      responses.section.status === 201 || responses.section.status === 200;
    if (responses.section.status === 201 || responses.section.status === 200) {
      try {
        testData.createdSectionId =
          responses.section.json().id || testData.existingSectionId;
      } catch (e) {}
    }
  }

  if (responses.submission) {
    checks["create submission is status 201"] = (r) =>
      responses.submission.status === 201 ||
      responses.submission.status === 200;
    if (
      responses.submission.status === 201 ||
      responses.submission.status === 200
    ) {
      try {
        testData.createdSubmissionId = responses.submission.json().id || 0;
      } catch (e) {}
    }
  }

  // Ejecutar todas las verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    // Registrar éxitos y errores
    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta para cada endpoint
  if (responses.assignment)
    responseTimePostAssignment.add(responses.assignment.timings.duration);
  if (responses.course)
    responseTimePostCourse.add(responses.course.timings.duration);
  if (responses.enrollment)
    responseTimePostEnrollment.add(responses.enrollment.timings.duration);
  if (responses.rol) responseTimePostRol.add(responses.rol.timings.duration);
  if (responses.section)
    responseTimePostSection.add(responses.section.timings.duration);
  if (responses.submission)
    responseTimePostSubmission.add(responses.submission.timings.duration);

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testPutEndpoints() {
  // Creamos un timestamp único para evitar colisiones
  const timestamp = Date.now();

  // Preparamos los payloads para las operaciones PUT
  const assignmentPayload = {
    course: testData.existingCourseId,
    name: `Updated Assignment ${timestamp}`,
    intro: "Esta es una asignación actualizada por k6",
    section: testData.existingSectionId,
    duedate: Math.floor(Date.now() / 1000) + 1209600, // Dos semanas en el futuro
    allowsubmissionsfromdate: Math.floor(Date.now() / 1000),
    grade: 90,
    introformat: 1,
  };

  const coursePayload = {
    category: 1,
    sortorder: 2,
    fullname: `Updated Course ${timestamp}`,
    shortname: `UC${timestamp}`,
    idnumber: `UC-${timestamp}`,
    summary: "Este es un curso actualizado por k6",
    format: "topics",
    startdate: Math.floor(Date.now() / 1000),
    enddate: Math.floor(Date.now() / 1000) + 5184000, // 60 días
    visible: 1,
  };

  const enrollmentPayload = {
    enrolid: 1,
    userid: testData.existingUserId,
    courseid: testData.existingCourseId,
    status: 0,
    timestart: Math.floor(Date.now() / 1000),
    timeend: Math.floor(Date.now() / 1000) + 5184000, // 60 días
  };

  const sectionPayload = {
    course: testData.existingCourseId,
    name: `Updated Section ${timestamp}`,
    summary: "Esta es una sección actualizada por k6",
    visible: 1,
  };

  // Ejecutar las operaciones PUT
  let responses = {};
  let targetId = 0;

  // Actualización de Assignment
  if (testData.createdAssignmentId > 0 && Math.random() < 0.25) {
    targetId = testData.createdAssignmentId;
  } else {
    targetId = testData.existingAssignmentId;
  }

  if (Math.random() < 0.25) {
    responses.assignment = http.put(
      `http://app:8000/api/assignments/${targetId}`,
      JSON.stringify(assignmentPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  // Actualización de Course
  if (testData.createdCourseId > 0 && Math.random() < 0.25) {
    targetId = testData.createdCourseId;
  } else {
    targetId = testData.existingCourseId;
  }

  if (Math.random() < 0.25) {
    responses.course = http.put(
      `http://app:8000/api/courses/${targetId}`,
      JSON.stringify(coursePayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  // Actualización de Enrollment
  if (testData.createdEnrollmentId > 0 && Math.random() < 0.25) {
    targetId = testData.createdEnrollmentId;

    if (Math.random() < 0.25) {
      responses.enrollment = http.put(
        `http://app:8000/api/enrollments/${targetId}`,
        JSON.stringify(enrollmentPayload),
        {
          headers: { "Content-Type": "application/json" },
        },
      );
    }
  }

  // Actualización de Section
  if (testData.createdSectionId > 0 && Math.random() < 0.25) {
    targetId = testData.createdSectionId;
  } else {
    targetId = testData.existingSectionId;
  }

  if (Math.random() < 0.25) {
    responses.section = http.put(
      `http://app:8000/api/sections/${targetId}`,
      JSON.stringify(sectionPayload),
      {
        headers: { "Content-Type": "application/json" },
      },
    );
  }

  // Verificar respuestas
  let checks = {};
  if (responses.assignment)
    checks["update assignment is status 200"] = (r) =>
      responses.assignment.status === 200;
  if (responses.course)
    checks["update course is status 200"] = (r) =>
      responses.course.status === 200;
  if (responses.enrollment)
    checks["update enrollment is status 200"] = (r) =>
      responses.enrollment.status === 200;
  if (responses.section)
    checks["update section is status 200"] = (r) =>
      responses.section.status === 200;

  // Ejecutar todas las verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    // Registrar éxitos y errores
    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta para cada endpoint
  if (responses.assignment)
    responseTimePutAssignment.add(responses.assignment.timings.duration);
  if (responses.course)
    responseTimePutCourse.add(responses.course.timings.duration);
  if (responses.enrollment)
    responseTimePutEnrollment.add(responses.enrollment.timings.duration);
  if (responses.section)
    responseTimePutSection.add(responses.section.timings.duration);

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testDeleteEndpoints() {
  let responses = {};

  // Solo realizamos operaciones DELETE en elementos que hemos creado durante la prueba
  if (testData.createdSubmissionId > 0 && Math.random() < 0.2) {
    responses.submission = http.del(
      `http://app:8000/api/submissions/${testData.createdSubmissionId}`,
    );
    testData.createdSubmissionId = 0; // Limpiamos el ID después de eliminar
  }

  if (testData.createdEnrollmentId > 0 && Math.random() < 0.2) {
    responses.enrollment = http.del(
      `http://app:8000/api/enrollments/${testData.createdEnrollmentId}`,
    );
    testData.createdEnrollmentId = 0;
  }

  if (testData.createdSectionId > 0 && Math.random() < 0.2) {
    responses.section = http.del(
      `http://app:8000/api/sections/${testData.createdSectionId}`,
    );
    testData.createdSectionId = 0;
  }

  if (testData.createdRolId > 0 && Math.random() < 0.2) {
    responses.rol = http.del(
      `http://app:8000/api/roles/${testData.createdRolId}`,
    );
    testData.createdRolId = 0;
  }

  if (testData.createdAssignmentId > 0 && Math.random() < 0.2) {
    responses.assignment = http.del(
      `http://app:8000/api/assignments/${testData.createdAssignmentId}`,
    );
    testData.createdAssignmentId = 0;
  }

  // Verificar respuestas
  let checks = {};
  if (responses.submission)
    checks["delete submission is status 200"] = (r) =>
      responses.submission.status === 200;
  if (responses.enrollment)
    checks["delete enrollment is status 200"] = (r) =>
      responses.enrollment.status === 200;
  if (responses.section)
    checks["delete section is status 200"] = (r) =>
      responses.section.status === 200;
  if (responses.rol)
    checks["delete rol is status 200"] = (r) => responses.rol.status === 200;
  if (responses.assignment)
    checks["delete assignment is status 200"] = (r) =>
      responses.assignment.status === 200;

  // Ejecutar todas las verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    // Registrar éxitos y errores
    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta para cada endpoint
  if (responses.submission)
    responseTimeDeleteSubmission.add(responses.submission.timings.duration);
  if (responses.enrollment)
    responseTimeDeleteEnrollment.add(responses.enrollment.timings.duration);
  if (responses.section)
    responseTimeDeleteSection.add(responses.section.timings.duration);
  if (responses.rol) responseTimeDeleteRol.add(responses.rol.timings.duration);
  if (responses.assignment)
    responseTimeDeleteAssignment.add(responses.assignment.timings.duration);

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}
