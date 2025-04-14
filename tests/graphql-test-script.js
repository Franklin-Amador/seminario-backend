import http from "k6/http";
import { check, sleep } from "k6";
import { Trend, Counter, Rate } from "k6/metrics";
import { randomIntBetween } from "https://jslib.k6.io/k6-utils/1.2.0/index.js";

// URL base para las peticiones GraphQL
const GRAPHQL_URL = "http://app:8000/graphql";

// Definir métricas personalizadas para cada operación GraphQL
// Query metrics
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

// Mutation metrics
let responseTimeMutationCreateAssignment = new Trend(
  "response_time_create_assignment",
);
let responseTimeMutationCreateCourse = new Trend("response_time_create_course");
let responseTimeMutationCreateEnrollment = new Trend(
  "response_time_create_enrollment",
);
let responseTimeMutationCreateRole = new Trend("response_time_create_role");
let responseTimeMutationCreateSection = new Trend(
  "response_time_create_section",
);
let responseTimeMutationUpdateAssignment = new Trend(
  "response_time_update_assignment",
);
let responseTimeMutationUpdateCourse = new Trend("response_time_update_course");
let responseTimeMutationUpdateEnrollment = new Trend(
  "response_time_update_enrollment",
);
let responseTimeMutationUpdateSection = new Trend(
  "response_time_update_section",
);
let responseTimeMutationDeleteEnrollment = new Trend(
  "response_time_delete_enrollment",
);
let responseTimeMutationDeleteRole = new Trend("response_time_delete_role");
let responseTimeMutationDeleteSection = new Trend(
  "response_time_delete_section",
);
let responseTimeMutationLogin = new Trend("response_time_login");
let responseTimeMutationChangePassword = new Trend(
  "response_time_change_password",
);

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
  createdRoleId: 0,
  createdSectionId: 0,

  // IDs existentes en la base de datos (supuestos)
  existingCourseId: 1,
  existingUserId: 1,
  existingAssignmentId: 1,
  existingSectionId: 1,
};

// Definir opciones de carga
export let options = {
  vus: 50, // Número de usuarios virtuales
  duration: "30s", // Duración de la prueba (30 segundos)
  thresholds: {
    error_rate: ["rate<0.1"], // Tasa de error menor al 10%
    http_req_duration: ["p(95)<2000"], // 95% de las solicitudes por debajo de 2s
  },
};

// GraphQL queries adaptadas según los modelos de types_graphql.py
const queries = {
  // User queries - Agregados todos los campos del modelo User
  users: `query {
    users {
      id
      username
      firstname
      lastname
      email
      confirmed
      deleted
      suspended
      institution
      department
      timecreated
      timemodified
    }
  }`,

  user: (userId) => `query {
    user(userId: ${userId}) {
      id
      username
      firstname
      lastname
      email
      confirmed
      deleted
      suspended
      institution
      department
      timecreated
      timemodified
    }
  }`,

  // Course queries - Adaptados a los campos del modelo Course
  courses: `query {
    courses {
      id
      category
      sortorder
      fullname
      shortname
      idnumber
      summary
      format
      showgrades
      newsitems
      startdate
      enddate
      visible
      groupmode
      timecreated
      timemodified
    }
  }`,

  course: (courseId) => `query {
    course(courseId: ${courseId}) {
      id
      category
      sortorder
      fullname
      shortname
      idnumber
      summary
      format
      showgrades
      newsitems
      startdate
      enddate
      visible
      groupmode
      timecreated
      timemodified
    }
  }`,

  // Section queries - Agregados todos los campos disponibles en el modelo Section
  courseSections: (courseId) => `query {
    courseSections(courseId: ${courseId}) {
      id
      course
      section
      name
      summary
      sequence
      visible
      availability
      timemodified
    }
  }`,

  // Category queries - Agregados todos los campos disponibles
  categories: `query {
    categories {
      id
      name
      idnumber
      description
      parent
      sortorder
      coursecount
      visible
      visibleold
      timemodified
      depth
      path
      theme
    }
  }`,

  category: (categoryId) => `query {
    category(categoryId: ${categoryId}) {
      id
      name
      idnumber
      description
      parent
      sortorder
      coursecount
      visible
      visibleold
      timemodified
      depth
      path
      theme
    }
  }`,

  // Role queries - Adaptados al modelo Role
  roles: `query {
    roles {
      id
      name
      shortname
      description
      sortorder
      archetype
    }
  }`,

  role: (roleId) => `query {
    role(roleId: ${roleId}) {
      id
      name
      shortname
      description
      sortorder
      archetype
    }
  }`,

  // Assignment queries - Adaptados al modelo Assignment
  assignments: (courseId, sectionId) => {
    if (courseId && sectionId) {
      return `query {
        assignments(courseId: ${courseId}, sectionId: ${sectionId}) {
          id
          course
          name
          intro
          section
          duedate
          allowsubmissionsfromdate
          grade
          timemodified
          completionsubmit
          cutoffdate
          gradingduedate
        }
      }`;
    } else {
      return `query {
        assignments {
          id
          course
          name
          intro
          section
          duedate
          allowsubmissionsfromdate
          grade
          timemodified
          completionsubmit
          cutoffdate
          gradingduedate
        }
      }`;
    }
  },

  allAssignments: `query {
    AllAssigments {
      id
      course
      name
      intro
      section
      duedate
      allowsubmissionsfromdate
      grade
      timemodified
      completionsubmit
      cutoffdate
      gradingduedate
    }
  }`,

  allAssignmentsProx: `query {
    AllAssigmentsProx {
      id
      course
      name
      intro
      section
      duedate
      allowsubmissionsfromdate
      grade
      timemodified
      completionsubmit
      cutoffdate
      gradingduedate
    }
  }`,

  courseAssignmentsProx: (courseId) => `query {
    CourseAssignmentsProx(courseId: ${courseId}) {
      id
      course
      name
      intro
      section
      duedate
      allowsubmissionsfromdate
      grade
      timemodified
      completionsubmit
      cutoffdate
      gradingduedate
    }
  }`,

  assignment: (assignmentId) => `query {
    assignment(assignmentId: ${assignmentId}) {
      id
      course
      name
      intro
      section
      duedate
      allowsubmissionsfromdate
      grade
      timemodified
      completionsubmit
      cutoffdate
      gradingduedate
    }
  }`,

  // Submission queries - Adaptados al modelo Submission
  submissions: (assignmentId) => `query {
    submissions(assignmentId: ${assignmentId}) {
      id
      assignment
      userid
      timecreated
      timemodified
      status
      groupid
      attemptnumber
      latest
    }
  }`,

  userSubmissions: (userId) => `query {
    userSubmissions(userId: ${userId}) {
      id
      assignment
      userid
      timecreated
      timemodified
      status
      groupid
      attemptnumber
      latest
    }
  }`,

  // Enrollment queries - Adaptados al modelo Enrollment
  courseEnrollments: (courseId) => `query {
    courseEnrollments(courseId: ${courseId}) {
      id
      enrolid
      userid
      courseid
      status
      timestart
      timeend
      timecreated
      timemodified
    }
  }`,

  // La query userEnrollments incluye campos de Course anidados
  userEnrollments: (userId) => `query {
    userEnrollments(userId: ${userId}) {
      id
      enrolid
      userid
      courseid
      status
      timestart
      timeend
      timecreated
      timemodified
      course {
        id
        fullname
        shortname
        visible
        startdate
        enddate
      }
    }
  }`,

  // Section queries - Adaptados al modelo Section
  sections: (courseId) => `query {
    sections(courseId: ${courseId}) {
      id
      course
      section
      name
      summary
      sequence
      visible
      availability
      timemodified
    }
  }`,
};

// GraphQL mutations adaptadas a los campos de los modelos
const mutations = {
  createRole: (input) => `mutation {
    createRole(input: {
      name: "${input.name}",
      shortname: "${input.shortname}",
      description: ${input.description ? `"${input.description}"` : "null"},
      sortorder: ${input.sortorder},
      archetype: ${input.archetype ? `"${input.archetype}"` : "null"}
    }) {
      id
      name
      shortname
      description
      sortorder
      archetype
    }
  }`,

  updateRole: (roleId, input) => `mutation {
    updateRole(
      roleId: ${roleId},
      input: {
        name: "${input.name}",
        shortname: "${input.shortname}",
        description: ${input.description ? `"${input.description}"` : "null"},
        sortorder: ${input.sortorder},
        archetype: ${input.archetype ? `"${input.archetype}"` : "null"}
      }
    ) {
      id
      name
      shortname
      description
      sortorder
      archetype
    }
  }`,

  deleteRole: (roleId) => `mutation {
    deleteRole(roleId: ${roleId}) {
      id
      name
      shortname
      description
      sortorder
      archetype
    }
  }`,

  createUser: (input) => `mutation {
    createUser(input: {
      username: "${input.username}",
      password: "${input.password}",
      firstname: "${input.firstname}",
      lastname: "${input.lastname}",
      email: "${input.email}",
      institution: ${input.institution ? `"${input.institution}"` : "null"},
      department: ${input.department ? `"${input.department}"` : "null"}
    }) {
      id
      username
      firstname
      lastname
      email
      confirmed
      deleted
      suspended
      institution
      department
      timecreated
      timemodified
    }
  }`,

  createCourse: (input) => `mutation {
    createCourse(input: {
      category: ${input.category},
      sortorder: ${input.sortorder},
      fullname: "${input.fullname}",
      shortname: "${input.shortname}",
      idnumber: ${input.idnumber ? `"${input.idnumber}"` : "null"},
      summary: ${input.summary ? `"${input.summary}"` : "null"},
      format: "${input.format}",
      showgrades: ${input.showgrades || true},
      newsitems: ${input.newsitems || 5},
      startdate: "${input.startdate.toISOString()}",
      enddate: ${input.enddate ? `"${input.enddate.toISOString()}"` : "null"},
      visible: ${input.visible}
    }) {
      id
      fullname
      shortname
      category
      sortorder
      visible
      startdate
      enddate
      timemodified
    }
  }`,

  updateCourse: (courseId, input) => `mutation {
    updateCourse(
      courseId: ${courseId},
      input: {
        category: ${input.category},
        sortorder: ${input.sortorder},
        fullname: "${input.fullname}",
        shortname: "${input.shortname}",
        idnumber: ${input.idnumber ? `"${input.idnumber}"` : "null"},
        summary: ${input.summary ? `"${input.summary}"` : "null"},
        format: "${input.format}",
        showgrades: ${input.showgrades || true},
        newsitems: ${input.newsitems || 5},
        startdate: "${input.startdate.toISOString()}",
        enddate: ${input.enddate ? `"${input.enddate.toISOString()}"` : "null"},
        visible: ${input.visible}
      }
    ) {
      id
      fullname
      shortname
      category
      visible
      startdate
      enddate
      timemodified
    }
  }`,

  createAssignment: (input) => `mutation {
    createAssignment(input: {
      course: ${input.course},
      section: ${input.section},
      name: "${input.name}",
      intro: "${input.intro}",
      duedate: ${input.duedate ? `"${input.duedate.toISOString()}"` : "null"},
      allowsubmissionsfromdate: ${
        input.allowsubmissionsfromdate
          ? `"${input.allowsubmissionsfromdate.toISOString()}"`
          : "null"
      },
      grade: ${input.grade ?? "null"},
      completionsubmit: ${input.completionsubmit || true},
      cutoffdate: ${
        input.cutoffdate ? `"${input.cutoffdate.toISOString()}"` : "null"
      },
      gradingduedate: ${
        input.gradingduedate
          ? `"${input.gradingduedate.toISOString()}"`
          : "null"
      }
    }) {
      id
      name
      course
      section
      duedate
      grade
      timemodified
    }
  }`,

  updateAssignment: (assignmentId, input) => `mutation {
    updateAssignment(
      assignmentId: ${assignmentId},
      input: {
        course: ${input.course},
        section: ${input.section},
        name: "${input.name}",
        intro: "${input.intro}",
        duedate: ${input.duedate ? `"${input.duedate.toISOString()}"` : "null"},
        allowsubmissionsfromdate: ${
          input.allowsubmissionsfromdate
            ? `"${input.allowsubmissionsfromdate.toISOString()}"`
            : "null"
        },
        grade: ${input.grade ?? "null"},
        completionsubmit: ${input.completionsubmit || true},
        cutoffdate: ${
          input.cutoffdate ? `"${input.cutoffdate.toISOString()}"` : "null"
        },
        gradingduedate: ${
          input.gradingduedate
            ? `"${input.gradingduedate.toISOString()}"`
            : "null"
        }
      }
    ) {
      id
      name
      course
      section
      duedate
      grade
      timemodified
    }
  }`,

  createEnrollment: (input) => `mutation {
    createEnrollment(input: {
      enrolid: ${input.enrolid},
      userid: ${input.userid},
      courseid: ${input.courseid},
      status: ${input.status},
      timestart: ${
        input.timestart ? `"${input.timestart.toISOString()}"` : "null"
      },
      timeend: ${input.timeend ? `"${input.timeend.toISOString()}"` : "null"}
    }) {
      id
      enrolid
      userid
      courseid
      status
      timestart
      timeend
      timecreated
      timemodified
    }
  }`,

  updateEnrollment: (enrollmentId, input) => `mutation {
    updateEnrollment(
      enrollmentId: ${enrollmentId},
      input: {
        enrolid: ${input.enrolid},
        userid: ${input.userid},
        courseid: ${input.courseid},
        status: ${input.status},
        timestart: ${
          input.timestart ? `"${input.timestart.toISOString()}"` : "null"
        },
        timeend: ${input.timeend ? `"${input.timeend.toISOString()}"` : "null"}
      }
    ) {
      id
      enrolid
      userid
      courseid
      status
      timestart
      timeend
      timemodified
    }
  }`,

  deleteEnrollment: (enrollmentId) => `mutation {
    deleteEnrollment(enrollmentId: ${enrollmentId}) {
      id
      enrolid
      userid
      courseid
      status
    }
  }`,

  createSection: (input) => `mutation {
    createSection(input: {
      course: ${input.course},
      name: "${input.name}",
      summary: ${input.summary ? `"${input.summary}"` : "null"},
      sequence: ${input.sequence ? `"${input.sequence}"` : "null"},
      visible: ${input.visible}
    }) {
      id
      course
      section
      name
      summary
      sequence
      visible
      availability
      timemodified
    }
  }`,

  updateSection: (sectionId, input) => `mutation {
    updateSection(
      sectionId: ${sectionId},
      input: {
        course: ${input.course},
        name: "${input.name}",
        summary: ${input.summary ? `"${input.summary}"` : "null"},
        sequence: ${input.sequence ? `"${input.sequence}"` : "null"},
        visible: ${input.visible}
      }
    ) {
      id
      course
      section
      name
      summary
      sequence
      visible
      availability
      timemodified
    }
  }`,

  deleteSection: (sectionId) => `mutation {
    deleteSection(sectionId: ${sectionId}) {
      id
      course
      section
      name
      visible
    }
  }`,

  login: (email, password) => `mutation {
    login(email: "${email}", password: "${password}") {
      user {
        id
        username
        email
        firstname
        lastname
        confirmed
        deleted
        suspended
        institution
        department
        timecreated
        timemodified
      }
      error {
        message
        code
      }
    }
  }`,

  changePassword: (email, newPassword) => `mutation {
    changePassword(email: "${email}", newPassword: "${newPassword}") {
      user {
        id
        username
        email
        firstname
        lastname
        confirmed
      }
      error {
        message
        code
      }
    }
  }`,
};

// Función para ejecutar consultas GraphQL
function executeGraphQLQuery(query) {
  const payload = JSON.stringify({
    query: query,
  });

  const params = {
    headers: {
      "Content-Type": "application/json",
    },
  };

  return http.post(GRAPHQL_URL, payload, params);
}

// Función principal
export default function () {
  // Aleatorizamos qué tipo de operación ejecutamos para diversificar la carga
  let operationType = Math.random();

  if (operationType < 0.7) {
    // 70% de las veces realizamos operaciones Query (GET equivalente)
    testGraphQLQueries();
  } else if (operationType < 0.85) {
    // 15% de las veces realizamos operaciones Mutation Create (POST equivalente)
    testGraphQLCreateMutations();
  } else if (operationType < 0.95) {
    // 10% de las veces realizamos operaciones Mutation Update (PUT equivalente)
    testGraphQLUpdateMutations();
  } else {
    // 5% de las veces realizamos operaciones Mutation Delete (DELETE equivalente)
    testGraphQLDeleteMutations();
  }

  // Pequeña pausa entre iteraciones para simular comportamiento más realista
  sleep(randomIntBetween(1, 3));
}

function testGraphQLQueries() {
  // Grupo de operaciones Query para APIs más utilizadas
  let responses = {};

  // Página principal - solo para efectos de prueba
  responses.home = http.get("http://app:8000/");

  // Ejecutar consultas GraphQL más comunes
  responses.users = executeGraphQLQuery(queries.users);
  responses.categories = executeGraphQLQuery(queries.categories);
  responses.roles = executeGraphQLQuery(queries.roles);
  responses.courses = executeGraphQLQuery(queries.courses);
  responses.assignments = executeGraphQLQuery(queries.assignments());
  responses.assignmentsProx = executeGraphQLQuery(queries.allAssignmentsProx);

  // Grupo de operaciones Query para APIs menos utilizadas (con probabilidad)
  if (Math.random() < 0.3) {
    responses.userById = executeGraphQLQuery(
      queries.user(testData.existingUserId),
    );
    responses.roleById = executeGraphQLQuery(
      queries.role(randomIntBetween(1, 5)),
    );
    responses.courseById = executeGraphQLQuery(
      queries.course(testData.existingCourseId),
    );
    responses.courseSections = executeGraphQLQuery(
      queries.courseSections(testData.existingCourseId),
    );
    responses.cursoAssignments = executeGraphQLQuery(
      queries.courseAssignmentsProx(testData.existingCourseId),
    );
    responses.seccionAssignments = executeGraphQLQuery(
      queries.assignments(
        testData.existingCourseId,
        testData.existingSectionId,
      ),
    );
    responses.allAssignments = executeGraphQLQuery(queries.allAssignments);
    responses.enrollmentsByCourse = executeGraphQLQuery(
      queries.courseEnrollments(testData.existingCourseId),
    );
    responses.enrollmentsByUser = executeGraphQLQuery(
      queries.userEnrollments(testData.existingUserId),
    );
    responses.submissionsByAssignment = executeGraphQLQuery(
      queries.submissions(testData.existingAssignmentId),
    );
    responses.submissionsByUser = executeGraphQLQuery(
      queries.userSubmissions(testData.existingUserId),
    );
    responses.sections = executeGraphQLQuery(
      queries.sections(testData.existingCourseId),
    );
  }

  // Verificar respuestas de las operaciones principales
  // En GraphQL, el código de estado es típicamente 200 incluso con errores, necesitamos verificar la estructura de la respuesta
  let checks = {
    "home endpoint is status 200": (r) => responses.home.status === 200,
    "users query successful": (r) => {
      let body = JSON.parse(responses.users.body);
      return (
        responses.users.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.users
      );
    },
    "categories query successful": (r) => {
      let body = JSON.parse(responses.categories.body);
      return (
        responses.categories.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.categories
      );
    },
    "roles query successful": (r) => {
      let body = JSON.parse(responses.roles.body);
      return (
        responses.roles.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.roles
      );
    },
    "courses query successful": (r) => {
      let body = JSON.parse(responses.courses.body);
      return (
        responses.courses.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.courses
      );
    },
    "assignments query successful": (r) => {
      let body = JSON.parse(responses.assignments.body);
      return (
        responses.assignments.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.assignments !== undefined
      );
    },
    "assignmentsProx query successful": (r) => {
      let body = JSON.parse(responses.assignmentsProx.body);
      return (
        responses.assignmentsProx.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.AllAssigmentsProx !== undefined
      );
    },
  };

  // Verificar endpoints adicionales si se ejecutaron
  if (responses.userById) {
    checks["userById query successful"] = (r) => {
      let body = JSON.parse(responses.userById.body);
      return (
        responses.userById.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.user
      );
    };
  }

  if (responses.roleById) {
    checks["roleById query successful"] = (r) => {
      let body = JSON.parse(responses.roleById.body);
      return (
        responses.roleById.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.role
      );
    };
  }

  if (responses.courseById) {
    checks["courseById query successful"] = (r) => {
      let body = JSON.parse(responses.courseById.body);
      return (
        responses.courseById.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.course
      );
    };
  }

  if (responses.courseSections) {
    checks["courseSections query successful"] = (r) => {
      let body = JSON.parse(responses.courseSections.body);
      return (
        responses.courseSections.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.courseSections !== undefined
      );
    };
  }

  if (responses.cursoAssignments) {
    checks["cursoAssignments query successful"] = (r) => {
      let body = JSON.parse(responses.cursoAssignments.body);
      return (
        responses.cursoAssignments.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.CourseAssignmentsProx !== undefined
      );
    };
  }

  if (responses.seccionAssignments) {
    checks["seccionAssignments query successful"] = (r) => {
      let body = JSON.parse(responses.seccionAssignments.body);
      return (
        responses.seccionAssignments.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.assignments !== undefined
      );
    };
  }

  if (responses.allAssignments) {
    checks["allAssignments query successful"] = (r) => {
      let body = JSON.parse(responses.allAssignments.body);
      return (
        responses.allAssignments.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.AllAssigments !== undefined
      );
    };
  }

  if (responses.enrollmentsByCourse) {
    checks["enrollmentsByCourse query successful"] = (r) => {
      let body = JSON.parse(responses.enrollmentsByCourse.body);
      return (
        responses.enrollmentsByCourse.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.courseEnrollments !== undefined
      );
    };
  }

  if (responses.enrollmentsByUser) {
    checks["enrollmentsByUser query successful"] = (r) => {
      let body = JSON.parse(responses.enrollmentsByUser.body);
      return (
        responses.enrollmentsByUser.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.userEnrollments !== undefined
      );
    };
  }

  if (responses.submissionsByAssignment) {
    checks["submissionsByAssignment query successful"] = (r) => {
      let body = JSON.parse(responses.submissionsByAssignment.body);
      return (
        responses.submissionsByAssignment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.submissions !== undefined
      );
    };
  }

  if (responses.submissionsByUser) {
    checks["submissionsByUser query successful"] = (r) => {
      let body = JSON.parse(responses.submissionsByUser.body);
      return (
        responses.submissionsByUser.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.userSubmissions !== undefined
      );
    };
  }

  if (responses.sections) {
    checks["sections query successful"] = (r) => {
      let body = JSON.parse(responses.sections.body);
      return (
        responses.sections.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.sections !== undefined
      );
    };
  }

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

  // Registrar métricas para endpoints adicionales
  if (responses.userById)
    responseTimeTrendUserById.add(responses.userById.timings.duration);
  if (responses.roleById)
    responseTimeTrendRolById.add(responses.roleById.timings.duration);
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
  if (responses.sections)
    responseTimeTrendSections.add(responses.sections.timings.duration);

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testGraphQLCreateMutations() {
  // Creamos un timestamp único para evitar colisiones
  const timestamp = Date.now();

  // Preparamos los payloads para las operaciones de creación
  const assignmentInput = {
    course: testData.existingCourseId,
    section: testData.existingSectionId,
    name: `Test Assignment ${timestamp}`,
    intro: "Esta es una asignación de prueba creada por k6",
    duedate: new Date(Date.now() + 604800000), // Una semana en el futuro
    allowsubmissionsfromdate: new Date(),
    grade: 100,
  };

  const courseInput = {
    category: 1,
    sortorder: 1,
    fullname: `Test Course ${timestamp}`,
    shortname: `TC${timestamp}`,
    idnumber: `TC-${timestamp}`,
    summary: "Este es un curso de prueba creado por k6",
    format: "topics",
    startdate: new Date(),
    enddate: new Date(Date.now() + 2592000000), // 30 días
    visible: true,
  };

  const enrollmentInput = {
    enrolid: 1,
    userid: testData.existingUserId,
    courseid: testData.existingCourseId,
    status: 0,
    timestart: new Date(),
    timeend: new Date(Date.now() + 2592000000), // 30 días
  };

  const roleInput = {
    name: `Test Role ${timestamp}`,
    shortname: `testrole-${timestamp}`,
    description: "Este es un rol de prueba creado por k6",
    sortorder: 1,
    archetype: "student",
  };

  const sectionInput = {
    course: testData.existingCourseId,
    name: `Test Section ${timestamp}`,
    summary: "Esta es una sección de prueba creada por k6",
    visible: true,
  };

  // Ejecutar mutaciones de creación con probabilidad
  let responses = {};

  if (Math.random() < 0.3) {
    responses.createAssignment = executeGraphQLQuery(
      mutations.createAssignment(assignmentInput),
    );
  }

  if (Math.random() < 0.2) {
    responses.createCourse = executeGraphQLQuery(
      mutations.createCourse(courseInput),
    );
  }

  if (Math.random() < 0.3) {
    responses.createEnrollment = executeGraphQLQuery(
      mutations.createEnrollment(enrollmentInput),
    );
  }

  if (Math.random() < 0.2) {
    responses.createRole = executeGraphQLQuery(mutations.createRole(roleInput));
  }

  if (Math.random() < 0.3) {
    responses.createSection = executeGraphQLQuery(
      mutations.createSection(sectionInput),
    );
  }

  // Verificar respuestas y extraer IDs de los elementos creados
  let checks = {};

  if (responses.createAssignment) {
    checks["create assignment successful"] = (r) => {
      let body = JSON.parse(responses.createAssignment.body);
      if (
        responses.createAssignment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.createAssignment
      ) {
        testData.createdAssignmentId =
          body.data.createAssignment.id || testData.existingAssignmentId;
        return true;
      }
      return false;
    };
  }

  if (responses.createCourse) {
    checks["create course successful"] = (r) => {
      let body = JSON.parse(responses.createCourse.body);
      if (
        responses.createCourse.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.createCourse
      ) {
        testData.createdCourseId =
          body.data.createCourse.id || testData.existingCourseId;
        return true;
      }
      return false;
    };
  }

  if (responses.createEnrollment) {
    checks["create enrollment successful"] = (r) => {
      let body = JSON.parse(responses.createEnrollment.body);
      if (
        responses.createEnrollment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.createEnrollment
      ) {
        testData.createdEnrollmentId = body.data.createEnrollment.id || 0;
        return true;
      }
      return false;
    };
  }

  if (responses.createRole) {
    checks["create role successful"] = (r) => {
      let body = JSON.parse(responses.createRole.body);
      if (
        responses.createRole.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.createRole
      ) {
        testData.createdRoleId = body.data.createRole.id || 0;
        return true;
      }
      return false;
    };
  }

  if (responses.createSection) {
    checks["create section successful"] = (r) => {
      let body = JSON.parse(responses.createSection.body);
      if (
        responses.createSection.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.createSection
      ) {
        testData.createdSectionId =
          body.data.createSection.id || testData.existingSectionId;
        return true;
      }
      return false;
    };
  }

  // Ejecutar verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta
  if (responses.createAssignment)
    responseTimeMutationCreateAssignment.add(
      responses.createAssignment.timings.duration,
    );
  if (responses.createCourse)
    responseTimeMutationCreateCourse.add(
      responses.createCourse.timings.duration,
    );
  if (responses.createEnrollment)
    responseTimeMutationCreateEnrollment.add(
      responses.createEnrollment.timings.duration,
    );
  if (responses.createRole)
    responseTimeMutationCreateRole.add(responses.createRole.timings.duration);
  if (responses.createSection)
    responseTimeMutationCreateSection.add(
      responses.createSection.timings.duration,
    );

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testGraphQLUpdateMutations() {
  // Creamos un timestamp único para evitar colisiones
  const timestamp = Date.now();

  // Preparamos los payloads para las operaciones de actualización
  const assignmentInput = {
    course: testData.existingCourseId,
    section: testData.existingSectionId,
    name: `Updated Assignment ${timestamp}`,
    intro: "Esta es una asignación actualizada por k6",
    duedate: new Date(Date.now() + 1209600000), // Dos semanas en el futuro
    allowsubmissionsfromdate: new Date(),
    grade: 90,
  };

  const courseInput = {
    category: 1,
    sortorder: 2,
    fullname: `Updated Course ${timestamp}`,
    shortname: `UC${timestamp}`,
    idnumber: `UC-${timestamp}`,
    summary: "Este es un curso actualizado por k6",
    format: "topics",
    startdate: new Date(),
    enddate: new Date(Date.now() + 5184000000), // 60 días
    visible: true,
  };

  const enrollmentInput = {
    enrolid: 1,
    userid: testData.existingUserId,
    courseid: testData.existingCourseId,
    status: 0,
    timestart: new Date(),
    timeend: new Date(Date.now() + 5184000000), // 60 días
  };

  const roleInput = {
    name: `Updated Role ${timestamp}`,
    shortname: `updatedrole-${timestamp}`,
    description: "Este es un rol actualizado por k6",
    sortorder: 2,
    archetype: "teacher",
  };

  const sectionInput = {
    course: testData.existingCourseId,
    name: `Updated Section ${timestamp}`,
    summary: "Esta es una sección actualizada por k6",
    visible: true,
  };

  // Ejecutar mutaciones de actualización con probabilidad
  let responses = {};
  let targetId = 0;

  // Actualización de Assignment
  if (testData.createdAssignmentId > 0 && Math.random() < 0.25) {
    targetId = testData.createdAssignmentId;
  } else {
    targetId = testData.existingAssignmentId;
  }

  if (Math.random() < 0.25) {
    responses.updateAssignment = executeGraphQLQuery(
      mutations.updateAssignment(targetId, assignmentInput),
    );
  }

  // Actualización de Course
  if (testData.createdCourseId > 0 && Math.random() < 0.25) {
    targetId = testData.createdCourseId;
  } else {
    targetId = testData.existingCourseId;
  }

  if (Math.random() < 0.25) {
    responses.updateCourse = executeGraphQLQuery(
      mutations.updateCourse(targetId, courseInput),
    );
  }

  // Actualización de Enrollment
  if (testData.createdEnrollmentId > 0 && Math.random() < 0.25) {
    targetId = testData.createdEnrollmentId;

    if (Math.random() < 0.25) {
      responses.updateEnrollment = executeGraphQLQuery(
        mutations.updateEnrollment(targetId, enrollmentInput),
      );
    }
  }

  // Actualización de Role
  if (testData.createdRoleId > 0 && Math.random() < 0.25) {
    targetId = testData.createdRoleId;

    if (Math.random() < 0.25) {
      responses.updateRole = executeGraphQLQuery(
        mutations.updateRole(targetId, roleInput),
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
    responses.updateSection = executeGraphQLQuery(
      mutations.updateSection(targetId, sectionInput),
    );
  }

  // Verificar respuestas
  let checks = {};

  if (responses.updateAssignment) {
    checks["update assignment successful"] = (r) => {
      let body = JSON.parse(responses.updateAssignment.body);
      return (
        responses.updateAssignment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.updateAssignment
      );
    };
  }

  if (responses.updateCourse) {
    checks["update course successful"] = (r) => {
      let body = JSON.parse(responses.updateCourse.body);
      return (
        responses.updateCourse.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.updateCourse
      );
    };
  }

  if (responses.updateEnrollment) {
    checks["update enrollment successful"] = (r) => {
      let body = JSON.parse(responses.updateEnrollment.body);
      return (
        responses.updateEnrollment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.updateEnrollment
      );
    };
  }

  if (responses.updateRole) {
    checks["update role successful"] = (r) => {
      let body = JSON.parse(responses.updateRole.body);
      return (
        responses.updateRole.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.updateRole
      );
    };
  }

  if (responses.updateSection) {
    checks["update section successful"] = (r) => {
      let body = JSON.parse(responses.updateSection.body);
      return (
        responses.updateSection.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.updateSection
      );
    };
  }

  // Ejecutar verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta
  if (responses.updateAssignment)
    responseTimeMutationUpdateAssignment.add(
      responses.updateAssignment.timings.duration,
    );
  if (responses.updateCourse)
    responseTimeMutationUpdateCourse.add(
      responses.updateCourse.timings.duration,
    );
  if (responses.updateEnrollment)
    responseTimeMutationUpdateEnrollment.add(
      responses.updateEnrollment.timings.duration,
    );
  if (responses.updateSection)
    responseTimeMutationUpdateSection.add(
      responses.updateSection.timings.duration,
    );

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

function testGraphQLDeleteMutations() {
  let responses = {};

  // Solo realizamos operaciones DELETE en elementos que hemos creado durante la prueba
  if (testData.createdEnrollmentId > 0 && Math.random() < 0.2) {
    responses.deleteEnrollment = executeGraphQLQuery(
      mutations.deleteEnrollment(testData.createdEnrollmentId),
    );
    testData.createdEnrollmentId = 0; // Limpiamos el ID después de eliminar
  }

  if (testData.createdRoleId > 0 && Math.random() < 0.2) {
    responses.deleteRole = executeGraphQLQuery(
      mutations.deleteRole(testData.createdRoleId),
    );
    testData.createdRoleId = 0;
  }

  if (testData.createdSectionId > 0 && Math.random() < 0.2) {
    responses.deleteSection = executeGraphQLQuery(
      mutations.deleteSection(testData.createdSectionId),
    );
    testData.createdSectionId = 0;
  }

  // Verificar respuestas
  let checks = {};

  if (responses.deleteEnrollment) {
    checks["delete enrollment successful"] = (r) => {
      let body = JSON.parse(responses.deleteEnrollment.body);
      return (
        responses.deleteEnrollment.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.deleteEnrollment
      );
    };
  }

  if (responses.deleteRole) {
    checks["delete role successful"] = (r) => {
      let body = JSON.parse(responses.deleteRole.body);
      return (
        responses.deleteRole.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.deleteRole
      );
    };
  }

  if (responses.deleteSection) {
    checks["delete section successful"] = (r) => {
      let body = JSON.parse(responses.deleteSection.body);
      return (
        responses.deleteSection.status === 200 &&
        !body.errors &&
        body.data &&
        body.data.deleteSection
      );
    };
  }

  // Ejecutar verificaciones si hay alguna
  if (Object.keys(checks).length > 0) {
    const checkResult = check(null, checks);

    if (checkResult) {
      successCounter.add(1);
    } else {
      errorCounter.add(1);
      errorRate.add(1);
    }
  }

  // Registrar métricas de tiempo de respuesta
  if (responses.deleteEnrollment)
    responseTimeMutationDeleteEnrollment.add(
      responses.deleteEnrollment.timings.duration,
    );
  if (responses.deleteRole)
    responseTimeMutationDeleteRole.add(responses.deleteRole.timings.duration);
  if (responses.deleteSection)
    responseTimeMutationDeleteSection.add(
      responses.deleteSection.timings.duration,
    );

  // Registrar en la métrica combinada
  Object.values(responses).forEach((response) => {
    responseTimeTrendCombined.add(response.timings.duration);
  });
}

// function testGraphQLCreateMutations() {
//   // Creamos un timestamp único para evitar colisiones
//   const timestamp = Date.now();

//   // Preparamos los payloads para las operaciones de creación
//   const assignmentInput = {
//     course: testData.existingCourseId,
//     section: testData.existingSectionId,
//     name: `Test Assignment ${timestamp}`,
//     intro: "Esta es una asignación de prueba creada por k6",
//     duedate: new Date(Date.now() + 604800000), // Una semana en el futuro
//     allowsubmissionsfromdate: new Date(),
//     grade: 100
//   };

//   const courseInput = {
//     category: 1,
//     sortorder: 1,
//     fullname: `Test Course ${timestamp}`,
//     shortname: `TC${timestamp}`,
//     idnumber: `TC-${timestamp}`,
//     summary: "Este es un curso de prueba creado por k6",
//     format: "topics",
//     startdate: new Date(),
//     enddate: new Date(Date.now() + 2592000000), // 30 días
//     visible: true
//   };

//   const enrollmentInput = {
//     enrolid: 1,
//     userid: testData.existingUserId,
//     courseid: testData.existingCourseId,
//     status: 0,
//     timestart: new Date(),
//     timeend: new Date(Date.now() + 2592000000) // 30 días
//   };

//   const roleInput = {
//     name: `Test Role ${timestamp}`,
//     shortname: `testrole-${timestamp}`,
//     description: "Este es un rol de prueba creado por k6",
//     sortorder: 1,
//     archetype: "student"
//   };

//   const sectionInput = {
//     course: testData.existingCourseId,
//     name: `Test Section ${timestamp}`,
//     summary: "Esta es una sección de prueba creada por k
