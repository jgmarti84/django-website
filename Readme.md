If running from vscode devcontainer create `.devcontainer` folder at base level directory and inside create a file named `devcontainer.json` with the following inside:
```
// For format details, see https://aka.ms/devcontainer.json. For config options, see the
// README at: https://github.com/devcontainers/templates/tree/main/src/python
{
	"name": "Python 3",
	// Or use a Dockerfile or Docker Compose file. More info: https://containers.dev/guide/dockerfile
	"image": "mcr.microsoft.com/devcontainers/python:1-3.12-bullseye",

	// Features to add to the dev container. More info: https://containers.dev/features.
	// "features": {},

	// Use 'forwardPorts' to make a list of ports inside the container available locally.
	// "forwardPorts": [],

	// Use 'postCreateCommand' to run commands after the container is created.
	"postCreateCommand": "chmod +x postCreateCommand.sh && ./postCreateCommand.sh"

	// Configure tool-specific properties.
	// "customizations": {},

	// Uncomment to connect as root instead. More info: https://aka.ms/dev-containers-non-root.
	// "remoteUser": "root"
}
```
Then ctrl + shift + P (or cmd + shift + P in mac) and look for the reopen in container option. Click on that and wait until the Dev Container is up and running. When building, the container should install the libraries inside the requirements.txt file, which means that you should have Django already installed. To check this run the following command in the terminal:
```
django-admin --version
```
which should print out the specific version of django installed. If not then rebuild container in order to get the libraries listed in the requirements.txt file installed during build.

Once the environment with django is installed you should be able to open a terminal and run django commands to start the django project. In the terminal, be sure to be at the lowest folder level where the postCreateCommand.sh and the requirements.txt files are placed and run the following command:
```
django-admin startproject django_website
```
This should create a folder named `django_website`. Inside this folder some files and folder structure for starting the django project are created:
```
├─ django_website
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ manage.py
```

* The outer directory `django_website` is just a simple container for the project. The name does not affect Django at all and this name could be chnaged to anything you want.

* `manage.py`: Command line utility that allows you to interact with the Django project in different ways. You can read the details about this file at `/ref/django-admin`.

* The inner directory `django_website` is the python package for the project. It's name is the name of the Python package that you should always use to import anything that is inside the project (e.g. `django_website.urls`).

* `django_website/__init__.py` is an empty file that tells Python that the directory must be considered as a Python package (if you are new to Python, you could read more about Python packages at the official Python documentation).

* `django_website/settings.py` is the settings/configuration file for this Django project. This is a normal Python module that define module-level variables that will represent the settings of the Django project.

* `django_website/urls.py` is where the declaration of the URLs for this Django project are stored, something like a "table of contents" for the project. 

* `django_website/wsgi.py` is the entripoint for serving the project through a web server compatible with WSGI.

Let's quickly add a folder titled templates into the directory with `django_website/` and `manage.py` in order that the folder structure should look like the following:
```
├─ templates
├─ django_website
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ manage.py
```

### The Settings
A proper initial settings setup will prevent bugs in the future. In your `settings.py` file, at the top of the file after the docstring ends, add `import os`. Next scroll down to the `TEMPLATES` section and make the following change in `DIRS`:
```
'DIRS': [os.path.join(BASE_DIR, 'templates')],
```
This allows you to forward the root template of the project to the main templates directory, for future reference to the base.html file.

#### Static and Media
##### static assets
These are files or objects that you display to a user on your webpage that the user does not have the ability to edit(either to change or to delete them). They are displayed to the user the way you sent them. They include CSS files(*.css), video/audio files(*.mp4, *.mp3, *.webm), images such as page banners, logos(*.png, *.gif, *.jpg) or even JSON files (*.json).

##### media assets
Media assets/files on the other hand are files that users are asked to upload on your application. They typically are images such as profile pictures, or documents that the user upload themselves.

We need too make some changes in the `settings.py` file in order to have the appropriate folders created. Below the defined `STATIC_URL` in the `settings.py`, add
```
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)
```

#### Databases
By default, the configuration uses SQLite. If you only want to try django out, leave it as it is, as this is the most simple option. SQLite is included in Python so its not necessary to install extra libraries. When building a more serious you may consider a more robust database such as PostgreSQL. 

If changing the database engine is the way to go, you'll need to install the appropriate bindings and change the `'default'` values in the `DATABASES` part of the `settings.py` file so that they match the configuration of your database conection. 

I'll use a postgres example here, so the `settings.py` file should contain the configuration of a previously created postgres database eventually running on localhost. A good option at this point is to not keep sensitive data in the `settings.py`, thus we'll use environment variables through a .env file.

##### configuration using dynaconf
As previously mentioned, any secret or sensitive data should be kept as outside the repository. Also sometimes, different running environments should have different configurations. All of this can be achieved by using the `dynaconf` library. To start to use it, we first need to install it:
```
pip install dynaconf==3.2.6
```
Again, if the library is already installed because you're using the devcontainer which installs from requirements.txt, then you should see it printed out. The next step is to create a yaml file called `settings.yaml` at the root folder with the following configuraions:
```
default:
  postgres_db:
    host: "localhost"
    port: "5432"
    database: "django_website"

devcontainer:
  postgres_db:
    host: "host.docker.internal"
```

This file basically defines two different configuration environments, the default one which will load the configurations by default, and the devcontainer one, which will only load (and overwrite default configurations) when explicitly told so by the use of the `ENV_FOR_DYNACONF` environment variable setup. Whenever this environment variable is set to `devcontainer`, the configs from this environment will be loaded and those that where loaded from default are replaced.

The other important file from which dynaconf will read secret configs is the `.secrets.yaml`. This file shold have the following structure:
```
default:
  SECRET_KEY: "your django secret key which should be present in the settings.py generated by the django-admin command run"
  postgres_db:
    user: "your postgres user"
    password: "your postgres password"
```
This file has the same kind of structure as the `settings.yaml`, with the difference that this is the one holding the passwords and secret values that should never be commited to a repository. That's why we should always have the patter `.secrets.*` in our `.gitignore` file.
```
*.pyc
__pycache__
db.sqlite3
/env
*.env
.vscode
.devcontainer
```

The final version of settings.py should look like this:
```
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = settings.SECRET_KEY

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": settings.postgres_db.database,
        "USER": settings.postgres_db.user,
        "PASSWORD": settings.postgres_db.password,
        "HOST": settings.postgres_db.host,
        "PORT": settings.postgres_db.port,
    }
}
```
Also, before doing anything further, be sure to install the postgres bindings for running databases:
```
pip install psycopg2==2.9.4
```
It may be the case that this library has already been installed when building the devcontainer if this is already in the requirements.txt file. You may tell if the output for the previous command is that the library is already installed.

Once all of this has been set, we can start populating the database with tables by creating apps and models, and then running the command: `ENV_FOR_DYNACONF="devcontainer" python manage.py makemigrations`, remember to set the env variable `ENV_FOR_DYNACONF` if not default environment is being used. After this, we should also run the following command: `ENV_FOR_DYNACONF="devcontainer" python manage.py migrate`. This will create new tables in the database, based on the migrations detected when running the first command. 

The `INSTALLED_APPS` from the `settings.py` file, registers all the names of the active Django applications in this instance. The apps can be used in multiple projects and they can be packaged and distributed for their use by others in their respective projects. By default, `INSTALLED_APPS` contains the following applications, all provided by Django:

* `django.contrib.admin` -> The project administration site
* `django.contrib.auth` -> Authentication system
* `django.contrib.contenttypes` -> A specific framework to work with different types of contents
* `django.contrib.sessions` -> A specific framework to handle sessions
* `django.contrib.messages` -> A specific framework for messages
* `django.contrib.staticfiles` -> A specific framework to manage static files

Some of these applications use at least a table in the database, so these tables will need to be created before they can be used. Thus the `migrate` command checks the `INSTALLED_APPS` from the `settings.py` file and creates the necessary tables in the database according to the active apps.
