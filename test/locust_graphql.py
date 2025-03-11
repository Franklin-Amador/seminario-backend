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
        headers = {"Content-Type": "application/json"}
        payload = {"query": query}

        self.client.post("/graphql", json=payload, headers=headers)
