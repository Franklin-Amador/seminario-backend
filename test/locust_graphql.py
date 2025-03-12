from locust import HttpUser, task, between


class GraphQLUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre solicitudes

    @task
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
         
    @task
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
    
    @task
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
    
    @task
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
    
    @task
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
    
    # También podemos agregar pruebas para obtener elementos individuales por ID
    
    @task
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
    
    @task
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


