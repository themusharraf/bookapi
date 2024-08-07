# BookAPI Project architecture
## Author: Musharraf 👽

## BooksAPI endpoints

![image](https://github.com/themusharraf/FastAPIBooks/assets/122869450/1517ab38-808e-4848-b8bb-9cd2667fe1bd)

## BooksAPI ORM

![image](https://github.com/themusharraf/FastAPIBooks/assets/122869450/aae7e4d1-2eb5-4efa-a9f8-74937c6a319d)

## runner

```shell
uvicorn main:app --reload
```


## Example Endpoint for test User:

```python
def test_get_user():
    requests = client.get("/users/1")
    assert requests.status_code == 200
    assert type(requests.json()['email']) == str
    assert type(requests.json()['is_active']) == bool

```
## Example Endpoint for test Books:

```python
def test_get_books():
    requests = client.get("/books/")
    assert requests.status_code == 200
    assert type(requests.json()) == list
```
   
## Example Request for Updating User:
### http

```http
PUT /users/1
Content-Type: application/json

{
  "username": "new_username",
  "email": "new_email@example.com",
  "is_active": true,
  "password": "new_password"
}
```
## Example Request for Updating Book:
### http

```http
PUT /books/1
Content-Type: application/json

{
  "title": "Updated Title",
  "language": "English",
  "isbn": "978-3-16-148410-0",
  "pages": 250
}
```
