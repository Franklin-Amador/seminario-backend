from locust import HttpUser, between, task


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)
    
    @task
    def login(self):
        self.client.post("/login", json={
            "username": "frank",
            "password": "1234"
        })
    
    @task
    def index(self):
        self.client.get("/")
        self.client.get("/api/courses")
        self.client.get("/api/categories")
        self.client.get("/api/roles")
        self.client.get("/api/users")
        
        

    
# Run the test
# ```bash  
# locust -f test/locust.py --host=http://localhost:8000
# ``` 
# - Open the browser and go to `http://localhost:8089/` to see the test results
# - Enter the number of users to simulate and the hatch rate  
    
        