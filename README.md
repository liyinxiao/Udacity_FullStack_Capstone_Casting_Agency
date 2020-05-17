# Casting Agency Full Stack Capstone Project

## How to run

* Installation
    * virtualenv env
    * source env/bin/activate
    * pip install -r requirements.txt
* Run
    * export FLASK_APP=app.py
    * export FLASK_ENV=development
    * flask run
* Auth0
    * Create account, create domain
    * create web application (regular web applications), edit Allowed Callback URLs for this application
    * Create API, create API permissions in Permissions, enable RBAC, create new roles in Users & Roles
    * Go to Auth0 Authorize Link to register 3 users and come back to Auth0
    * Assign roles to the three new users
    * Go to Auth0 Authorize Link to get the tokens (modify token expiration time if needed)
* Auth0 Authorize Link
    * https://{{YOUR_DOMAIN}}/authorize?audience={{API_IDENTIFIER}}&response_type=token&client_id={{YOUR_CLIENT_ID}}&redirect_uri={{YOUR_CALLBACK_URI}}
    * https://dev-83hrju-h.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=vt2UlbAwfwoG9kS0MIKzSogCY9k4I38r&redirect_uri=http://localhost:8080/login-results
* Testing
    * dropdb casting_agency
    * createdb casting_agency
    * psql casting_agency < casting_agency.psql
    * python test_app.py


## API

#### GET '/actors'
- Fetches a paginated list of actors.
- Request Arguments: page: 1(default), limit: 30(default).
- Returns: list of actors ordered by id.
```

{
  'success': True,
  'actors': [
    {
      id: 1,
      name: 'Actor 1',
      age: 30,
      gender: 'male'
    }
  ]
}
```

#### GET '/movies'
- Fetches a paginated list of movies.
- Request Arguments: page: 1(default), limit: 30(default).
- Returns: list of movies ordered by id.
```
{
  'success': True,
  'movies': [
    {
      id: 1,
      title: 'New Movie 1',
      release_date: '2021-10-1 04:22'
    }
  ]
}
```

#### POST '/actors'
- Create a new actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the new actor inside an array.
```
{
  'success': True,
  'actors': [
    {
      id: 2,
      name: 'Actor 2',
      age: 28,
      gender: 'Female'
    }
  ]
}
```

#### POST '/movies'
- Create a new movie.
- Request Arguments: { title: String, release_date: DateTime }.
- Returns: An object with `success: True` and the new movie inside an array.
```
{
  'success': True,
  'movies': [
    {
      id: 2,
      title: 'New Movie 2',
      release_date: '2022-10-1 04:22'
    }
  ]
}
```

#### Patch '/actors/<actor_id>'
- Update an actor.
- Request Arguments: { name: String, age: Integer, gender: String }.
- Returns: An object with `success: True` and the updated actor inside an array.
```
{
  'success': True,
  'actors': [
    {
      id: 1,
      name: 'Updated Actor',
      age: 50,
      gender: 'Male'
    }
  ]
}
```

#### Patch '/movies/<movie_id>'
- Update a movie.
- Request Arguments: { title: String, release_date: DateTime }.
- Returns: An object with `success: True` and the updated movie inside an array.
```
{
  'success': True,
  'movies': [
    {
      id: 1,
      title: 'Updated Movie 1',
      release_date: '2030-10-1 04:22'
    }
  ]
}
```

#### DELETE '/actors/<actor_id>'
- Removes an actor from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted actor
```
{
  'success': True,
  'id': 1
}
```

#### DELETE '/movies/<movie_id>'
- Removes a movie from the database.
- Request Parameters: question id slug.
- Returns: An object with `success: True` and the id of the deleted movie
```
{
  'success': True,
  'id': 1
}
```
