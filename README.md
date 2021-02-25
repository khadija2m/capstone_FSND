# Capstone project - Casting Agency
This is the last project for FULL STACK WEB DEVELOPMENT NANODEGREE.

Casting Agency is a company that is responsible for creating movies and managing and assigning actors to those movies. This app handling creating a system to simplify and streamline the process.

## Motivation:
After completing lessons in FULL STACK WEB DEVELOPMENT, this project was the one that handle the main topics in the Nanodegree:
- SQL, SQLAlchemy and Data Modeling for web app.
- using FLASK.
- API Development & Documentation.
- Identity and Access Management using AUTH0 as a third party.
- Role-Base Access Control (RBAC)
- testeng the application using Unittest.
- Deployment using Heroku.

# Deployment
This APP is deployed using Heroku. and it can bee seen and checked using the following link:
https://kcastingagency.herokuapp.com/

### Dependencies

#### Python 3.7
The latest version of python [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

## Main Files: Project Structure

  ```sh
  ├── README.md
  ├── app.py *** the main driver of the app.
  ├── models.py *** Database URLs, Models: Actors, Movies, Casting.
  ├── auth.py *** to get the JWT, and generate the permission.
  ├── test_app.py *** Unittest of the endpoints.
  └── templates
      └── index
  ```

## Running the server

Each time you open a new terminal session, run:
```bash
export FLASK_APP=app.py;
```

To run the server, execute:
```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Roles
- Casting Assistant
Can view actors and movies. His permission as following:
`get:movies`
`get:actors`

Credentials:
Email: assistant@agency.com
Password: 123456@a

- Casting Director
All permissions a Casting Assistant has. In addition to adding or deleting an actor from the database, modifying actors or movies:
`get:movies`
`get:actors`
`post:movies`
`post:actors`
`delete:movies`
`delete:actors`

Credentials:
Email: director@agency.com
Password: 123456@d

- Executive Producer
All permissions a Casting Director has. In addition to add or delete a movie from the database:
`get:movies`
`get:actors`
`post:movies`
`post:actors`
`delete:movies`
`delete:actors`
`patch:movies`
`patch:actors`

Credentials:
Email: producer@agency.com
Password: 123456@p

## Endpoints


#### GET '/actors'
This endpoint will return all actors in the casting agency

"actors": [
        {
          "age": "35",
          "gender": "male",
          "id": 1,
          "name": "Ali"
        },
        {
          "age": "25",
          "gender": "female",
          "id": 2,
          "name": "Sara"
        }
    ],
    "success": true
}

#### POST '/actors'
This endpoint can add new actor to the list

{
    "message": "New record has been added !",
    "movies": {
        "age": "25",
        "gender": "female",
        "name": "sara"
    },
    "success": true
}

#### PATCH '/actors'
This endpoint can edit actor information

{
    "message": "actor #1 has been edited !",
    "success": true
}

#### DELETE '/actors/<int:actor_id>'
This endpoint will delete an actor got by actor ID

{
    "message": "1 deleted...",
    "success": true
}

#### GET '/movies'
This endpoint will return all movies in the casting agency

"movies": [
        {
            "id": 1,
            "release": "1979",
            "title": "The Girl"
        },
        {
            "id": 2,
            "release": "2001",
            "title": "How to do !"
        }
    ],
    "success": true
}

#### POST '/movies'
This endpoint can add new movie to the list

{
    "message": "New record has been added !",
    "Movies": {
        "release": "2001",
        "title": "How to do !"
    },
    "success": true
}

#### PATCH '/movies'
This endpoint can edit movie information

{
    "message": "movie #1 has been edited !",
    "success": true
}

#### DELETE '/movies/<int:movie_id>'
This endpoint will delete a movie got by actor ID

{
    "message": "1 deleted...",
    "success": true
}

## Error handlers:

400 - Bad reqest

401 - token expired / invalid claims / invalid header

403 - unauthorized

404 - Resource not found

422 - Unprocessable entity

500 - Internal Server error

406 - Could not create a resource

##### Sample Response for 404

{
  "error": 404,
  "message": "Resource was not found",
  "success": false
}

##### Sample Response for 404

{
  "error": 404,
  "message": "Resource was not found",
  "success": false
}

##### Sample Response for 401 Unauthorized Access
{
  "error":401,
  "message":{
    "code":"authorization_header_missing",
    "description":"Authorization header is expected."
  },
  "success":false
}

#Tests:
The API Testing using Unittest in the file test_app.py. Having Tests for success behavior of each endpoint, error behavior of each endpoint, and tests of RBAC.

To run the file, open the Terminal and in the directory folder run the following command:

```bash
python test_app.py
```
