from fastapi import FastAPI, Depends
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog')
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blogs")
def get_all_blogs(db: Session = Depends(get_db)):
    blog_items = db.query(models.Blog).all()
    return blog_items


@app.get("/blogs/{id}")
def get_by_id(id, db: Session = Depends(get_db)):
    my_blog = db.query(models.Blog).filter(models.Blog.id == id)
    return my_blog.first()
