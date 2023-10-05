from fastapi import FastAPI, Depends, Response, status, HTTPException
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


@app.get("/blogs/{id}", status_code=status.HTTP_200_OK)
def get_by_id(id, response: Response, db: Session = Depends(get_db)):
    my_blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not my_blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Blog not found."}
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog not found")
    return my_blog


@app.delete("/blogs/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id, db: Session = Depends(get_db)):
    my_item = db.query(models.Blog).get(id)
    if not my_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog not found")
    db.delete(my_item)
    db.commit()
    return my_item


@app.put("/blogs/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(request: schemas.Blog, id, db: Session = Depends(get_db)):
    my_item = db.query(models.Blog).filter(
        models.Blog.id == id)
    if not my_item.first():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Blog not found")

    my_item.update(request.model_dump())
    db.commit()

    return my_item.first()
