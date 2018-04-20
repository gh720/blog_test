# A blog punch bag

Testing various blog features and web technologies.

### The list of technologies/frameworks used:

* Django framework
* Bootstrap
* SASS/SCSS
* Docker
* PostgreSQL/SQLite
* Nginx
* RabbitMQ
* Celery

### The features currenly implemented:

* Blog posts by multiple users
* Registration/authentication
* Resetting passwords through e-mail
* User profiles
* Comments
* A nice dynamically generated image of lightning
* Markdown in blog posts
* Post editing preview
* Delayed information processing (AJAX + Celery)


### Requirements:

* Python 3
* Docker (optional)

# Installation and running in development mode:

 (using `virtualenvwrapper` package):

    mkvirtualenv blog
    git clone https://github.com/gh720/blog_test.git blog
    cd blog 
    mkdir logs
    # if not activated already:
    activate blog
    pip install -r requirements.txt

### Start the database 

In case you are not using the default SQLite engine, fix the settings in `blog/settings/base.py` accordingly and make sure the database is started.

### Create Django tables and run the dev server:

    python3 manage.py migrate
    python3 manage.py runserver localhost:8000

Now point your browser at http://localhost:8000 and see what it looks like

# Optional steps:

### Importing data

Before doing `runserver` you can import some data (which is complete gibberish)

    python3 manage.py loaddata init/auth.json
    python3 manage.py loaddata init/posts.json

### Starting Celery and RabbitMQ if needed

If you want to check the Celery-related code (actually a small snippet retrieving the number of post comments through AJAX from a Celery worker):

* Adjust `CELERY_BROKER_URL` setting in blog/settings/dev.py or prod.py to point at RabbitMQ server
* start RabbitMQ server
* start Celery:

**Windows:**

    celery -A blog worker --pool=solo -l info

**Unix-like:**

    celery -A blog worker -l info

# Tests

The tests can be run:

    python3 manage.py test

The tests cover most of the functionality and currently do not fail.


# Running in Docker:

Run this in Docker terminal, being in the root blog directory:

    docker -f docker/compose.yml up -d nginx web celery db rabbitmq

This should download necessary images, apply `dockerfile`s and start Nginx container serving on port 8000.


# Security warning

This demo project is not guaranteed to be secure. **You have been warned**.


