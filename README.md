# Flask User Management API

A RESTful API built with Flask and MongoDB that handles user management operations. The API provides secure endpoints for creating, reading, updating, and deleting user resources with JWT authentication and proper input validation.

## Design Decisions

### Core Framework & Extensions
- **Flask**: Lightweight WSGI framework that allows for modular design through blueprints
- **flask-smorest**: Modern approach to building REST APIs with automatic OpenAPI documentation and robust request/response validation
- **flask-jwt-extended**: JWT implementation for secure authentication
- **marshmallow**: Schema-based serialization/deserialization and validation

### Database
- **MongoDB**: Document database that provides flexibility for future schema changes
- **pymongo**: Python driver for MongoDB

### Security
- **passlib**: Password hashing using PBKDF2-SHA256 (chosen over bcrypt due to better performance characteristics on modern hardware)
- **python-dotenv**: Environment variable management, separating configuration from code


## Development Setup

1. Clone the repository
2. Generate a random secret key for JWT_SECRET_KEY:
```bash
python -c 'import secrets; print(secrets.token_hex(64))'
```
2. Create `.env` file with key `JWT_SECRET_KEY`
4. Run with Docker:
```bash
docker compose up --build
```
5. Use `sudo` if you get permission error:
```bash
sudo docker compose up --build
```

## API Documentation

Available at `0.0.0.0:5000/swagger-ui` when running in development mode.

### Endpoints
- `POST /api/v1/users` - Create user
- `GET /api/v1/users` - List users (requires auth)
- `GET /api/v1/users/<id>` - Get user (requires auth)
- `PUT /api/v1/users/<id>` - Update user (requires auth)
- `DELETE /api/v1/users/<id>` - Delete user (requires auth)
- `POST /api/v1/login` - Authenticate user

## Testing
In a new Terminal:
```bash
poetry run pytest
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Submit pull request with tests

## License

MIT


## Following are my mental notes that I made while reading for this project
### Flask
[Watchdog](https://pythonhosted.org/watchdog/) provides a faster, more efficient reloader for the development server.

> https://flask.palletsprojects.com/en/stable/cli/
`.flaskenv` should be used for public variables, such as `FLASK_APP`, while `.env` should not be committed to your repository so that it can set private variables.
...
The files are only loaded by the `flask` command or calling [`run()`](https://flask.palletsprojects.com/en/stable/api/#flask.Flask.run "flask.Flask.run"). If you would like to load these files when running in production, you should call [`load_dotenv()`](https://flask.palletsprojects.com/en/stable/api/#flask.cli.load_dotenv "flask.cli.load_dotenv") manually.


### Flask Extensions considered for RESTful API
https://github.com/spec-first/connexion -> doesnt really need Flask. Supports Flask.\
https://github.com/noirbizarre/flask-restplus -> unmaintained\
https://github.com/flask-restful/flask-restful -> unmaintained\
**https://github.com/marshmallow-code/flask-smorest -> chosen**\
https://github.com/python-restx/flask-restx -> doesnt support latest OpenAPI spec\
https://github.com/apiflask/apiflask -> isn't specific to RESTful APIs\


### Blogs I read (kinda in order)
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis


> https://www.reddit.com/r/flask/comments/1e6ct0s/comment/ldsle2p/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
Why use a library to build REST APIs? Because they do a lot of heavy lifting. Good API libraries have robust data validation models, handle URL and query parameters, support OpenAPI semantics, and generate documentation from code.
>
In principle, REST APIs are pretty simple. Just a collection of endpoints, query and path parameters, and payloads. The devil is in the details. What happens if your API accepts the wrong data type or format in a payload? What if it accepts malformed data? What about additional properties? There are so many things that can go wrong from a functional and especially a security perspective. Good API libraries don't take these problems away, but they give you the tools to work through them.


https://apiflask.com/comparison/ \
https://www.mongodb.com/developer/languages/python/flask-python-mongodb/ \
https://realpython.com/flask-connexion-rest-api/ \
https://python.plainenglish.io/flask-restful-apis-72e05f8d41fa \

> _“As long as the method is being used according to its own definition, REST doesn’t have much to say about it.” — Roy Fielding_


### Best Tutorial ever on Flask and RESTful APIs (goldmine of information on just about everything related to Flask and RESTful APIs)

https://aaronluna.dev/series/flask-api-tutorial/overview/ \
https://aaronluna.dev/series/flask-api-tutorial/part-5/ \
	-> https://roy.gbiv.com/untangled/2008/rest-apis-must-be-hypertext-driven \

https://aaronluna.dev/series/flask-api-tutorial/part-3/ \
-> https://stackoverflow.com/questions/2001773/understanding-rest-verbs-error-codes-and-authentication?noredirect=1&lq=1
	
### How to version an API

https://dev.to/sparkpost/restful-api-versioning-best-practices-why-v1-is-1
- Breaking Changes (Very Bad)
    
    - A new required parameter
    - A new required key in POST bodies
    - Removal of an existing endpoint
    - Removal of an existing endpoint request method
    - A materially different internal behavior of an API call – such as a change to the default behavior.
- NOT Breaking Changes (Good)
    
    - A new resource or API endpoint
    - A new optional parameter
    - A change to a non-public API endpoint
    - A new optional key in the JSON POST body
    - A new key returned in the JSON response body
    
- Separating Deployment from Release


### JWT
https://datatracker.ietf.org/doc/html/rfc7519
https://jwt.io/

### Selecting a hashing algorithm
http://www.unlimitednovelty.com/2012/03/dont-use-bcrypt.html


### Tried Mongo Atlas Cluster
failed to connect to cluster. Then switced to local mongoDB.
