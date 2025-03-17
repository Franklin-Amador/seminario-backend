from locust import HttpUser, task, between, TaskSet


class GraphQLUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre solicitudes

    # Consultas básicas
    @task(3)  # Mayor peso para operaciones comunes
    def test_graphql_query(self):
        query = """
        query {
            users {
                id
                username
                email
            }
        }
        """
        self.client.post("/graphql", json={"query": query}, headers={"Content-Type": "application/json"})
         
    @task(2)
    def test_get_users(self):
        query = """
        query {
            users {
                id
                username
                email
                firstname
                lastname
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(2)
    def test_get_categories(self):
        query = """
        query {
            categories {
                id
                name
                description
                parent
                sortorder
                visible
                path
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(3)
    def test_get_courses(self):
        query = """
        query {
            courses {
                id
                fullname
                shortname
                summary
                format
                startdate
                enddate
                visible
                category
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(1)
    def test_get_roles(self):
        query = """
        query {
            roles {
                id
                name
                shortname
                description
                sortorder
                archetype
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Elementos individuales por ID
    @task(2)
    def test_get_course_by_id(self):
        # Suponiendo que existe un curso con ID 1
        query = """
        query {
            course(courseId: 1) {
                id
                fullname
                shortname
                summary
                format
                startdate
                enddate
                visible
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(1)
    def test_get_category_by_id(self):
        # Suponiendo que existe una categoría con ID 1
        query = """
        query {
            category(categoryId: 1) {
                id
                name
                description
                parent
                sortorder
                visible
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)

    # Tests de login actualizados con la nueva estructura de respuesta
    @task(4)  # Los logins son frecuentes, así que aumentamos el peso
    def test_login_frank(self):
        mutation = """
        mutation {
            login(email: "frank@unah.edu.hn", password: "1234") {
                user {
                    id
                    username
                    email
                    firstname
                    lastname
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)

    @task(4)
    def test_login_daniel(self):
        mutation = """
        mutation {
            login(email: "daniel@unah.edu.hn", password: "1234") {
                user {
                    id
                    username
                    email
                    firstname
                    lastname
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)

    @task(3)
    def test_login_elvis(self):
        mutation = """
        mutation {
            login(email: "elvis@unah.edu.hn", password: "1234") {
                user {
                    id
                    username
                    email
                    firstname
                    lastname
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)

    @task(3)
    def test_login_edwar(self):
        mutation = """
        mutation {
            login(email: "edwar@unah.edu.hn", password: "1234") {
                user {
                    id
                    username
                    email
                    firstname
                    lastname
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Test de login con credenciales incorrectas
    @task(2)
    def test_login_incorrect_password(self):
        mutation = """
        mutation {
            login(email: "frank@unah.edu.hn", password: "password_incorrecto") {
                user {
                    id
                    username
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(2)
    def test_login_nonexistent_user(self):
        mutation = """
        mutation {
            login(email: "usuario_que_no_existe@unah.edu.hn", password: "1234") {
                user {
                    id
                    username
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Prueba de cambio de contraseña
    @task(1)
    def test_change_password(self):
        mutation = """
        mutation {
            changePassword(email: "frank@unah.edu.hn", newPassword: "1234") {
                user {
                    id
                    username
                    email
                }
                error {
                    message
                    code
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": mutation}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Pruebas adicionales para estresar el sistema
    @task(2)
    def test_get_sections_for_course(self):
        query = """
        query {
            sections(courseId: 1) {
                id
                course
                section
                name
                summary
                visible
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(2)
    def test_get_assignments_for_course(self):
        query = """
        query {
            assignments(courseId: 1) {
                id
                course
                name
                intro
                section
                duedate
                grade
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(1)
    def test_get_course_enrollments(self):
        query = """
        query {
            courseEnrollments(courseId: 1) {
                id
                userid
                courseid
                status
                timestart
                timeend
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    @task(1)
    def test_get_user_enrollments(self):
        query = """
        query {
            userEnrollments(userId: 1) {
                id
                userid
                courseid
                status
                course {
                    id
                    fullname
                    shortname
                }
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Prueba de consulta compleja que simula carga del dashboard
    @task(1)
    def test_complex_dashboard_query(self):
        query = """
        query {
            user(userId: 1) {
                id
                username
                firstname
                lastname
                email
            }
            userEnrollments(userId: 1) {
                courseid
                status
                course {
                    id
                    fullname
                    shortname
                    category
                    visible
                }
            }
            categories {
                id
                name
                parent
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
    
    # Prueba de operaciones en lote (batch)
    @task(1)
    def test_batch_operations(self):
        # Enviar múltiples operaciones en una sola solicitud
        query = """
        query BatchQuery {
            users {
                id
                username
            }
            courses {
                id
                fullname
            }
            roles {
                id
                name
            }
        }
        """
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
