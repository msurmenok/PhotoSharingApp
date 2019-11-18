from locust import HttpLocust, TaskSet, task, between


class UserBehavior(TaskSet):
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        self.logout()

    def login(self):
        self.client.post("/login", {"username": "maria", "password": "11111111"})

    def logout(self):
        self.client.get("/logout")

    @task(1)
    def index(self):
        self.client.get("/")

    # @task(1)
    # def news_feed(self):
    #     self.client.get("/newsfeed")


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    wait_time = between(5, 9)
