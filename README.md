# Flask Pagination
Exploring pagination within a flask application using SQLite3 database as a backend. The dataset used for this project is the superstore data translated from `.xlsx` to `sqlite` database file.

# Before you get started
Having knowledge about `flask`, `heroku`, `sqlite` is essential for this project.

# Setup
**How to obtain this repository:**
```sh
git clone https://github.com/danielc92/flask_pagination.git
```
**Modules/dependencies:**
- `Flask==1.0.2`
- `gunicorn==19.9.0`
- `whitenoise==4.1.2`
- `Flask-SQLAlchemy==2.3.2`
- `SQLAlchemy==1.2.12`

It is encouraged to set up a `virtualenv` for this project, to separate your installations from your system level install of `python`.

Install the following dependences:
```sh
pip install requirements.txt
```

# Tests
- Hosted web application successfully on heroku platform
- Querying records
- Pagination of records

# Contributors
- Daniel Corcoran

# Sources
- [flask documentation](http://flask.pocoo.org/)
- [heroku website](https://heroku.com)