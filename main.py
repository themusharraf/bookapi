from fastapi import FastAPI, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from utils.main import send_email
from database import SessionLocal
from datetime import datetime
from typing import List
import logging
import schemas
import crud

app = FastAPI(title="BooksApi")

# Log konfiguratsiyasi # noqa
logging.basicConfig(
    filename="access.log",
    format="%(asctime)s - %(message)s",  # noqa
    level=logging.INFO
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def get_client_ip(request: Request):
    # Foydalanuvchi IP manzilini olish  # noqa
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        client_ip = forwarded_for.split(',')[0]
    else:
        client_ip = request.client.host

    # Logga write
    logging.info(f"Client IP: {client_ip}, Accessed at: {datetime.now()}")

    return {"client_ip": client_ip}


@app.get("/users/", response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = crud.get_all_users(db=db)
    return users


@app.get("/users/{user_id}", response_model=schemas.UserResponse)
async def get_one_user(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user


@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    email = user.email
    send_email(email, 'utils/msg.html')
    return db_user


@app.post("/books/", response_model=schemas.BookResponse)
async def create_book(user_id: int, book: schemas.BookCreate, db: Session = Depends(get_db)):
    db_book = crud.create_book(db=db, book=book, user_id=user_id)
    return db_book


@app.get("/books/", response_model=List[schemas.BookResponse])
async def get_books(db: Session = Depends(get_db)):
    books = crud.get_all_books(db=db)
    return books


@app.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_one_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return book


@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    return crud.update_user(db, user_id, user_update)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    if user_id is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return crud.delete_user(db, user_id)


@app.put("/books/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    return crud.update_book(db, book_id, book_update)


@app.delete("/books/{book_id}", response_model=schemas.Book)
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    if book_id is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found.")
    return crud.delete_book(db, book_id)
