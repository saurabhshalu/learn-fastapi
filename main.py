from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Hello World"}


@app.get("/blogs")
def blogs():
    return "This is a blog list"


@app.get("/blogs/{id}")
def blog_by_id(id):
    return f'This is blog: {id}'


@app.get("/blogswithtype/{id}")
def blog_by_id(id: int):
    return f'This is blog: {id}, and this id can only be number, else it will not work.'


@app.get("/blogsquery")
def filters(limit, sort: str | None = None):
    return f'This blog will contain the list of blogs, with the query params values passed in the url, we have to pass it in function parameter. Limit: {limit}, sort: {sort}'


@app.get("/params_query/{username}/details")
def bothtogether(username, sensitiveInformation: str | None = None):
    print(sensitiveInformation)
    return {
        username
    }
