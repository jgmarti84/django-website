If running from vscode devcontainer -> ctrl + shift + p -> create dev container -> python
Create a file called postCreateCommand.sh with the following in it: 
```
#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt
```
and change the line 15 (the right bellow `// Use 'postCreateCommand' to run commands after the container is created.`) in the devcontainer.json file inside .devcontainer to the following:
```
"postCreateCommand": "chmod +x postCreateCommand.sh && ./postCreateCommand.sh"
```
you should also have a requirements.txt file with at least the django app install:
`Django==5.1.2`

rebuild container in order to have the container environment with python and django installed.
Once the environment with django is installed you should be able to open a terminal and run django commands to start the django project. In the terminal, be sure to be at the lowest folder level where the postCreateCommand.sh and the requirements.txt files are placed and run the following command:
```
django-admin startproject project_test
```
This should create a folder named `project_test`. Inside this folder some files and folder structure for starting the django projects are created:
```
├─ project_test
│  ├─ __init__.py
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
├─ manage.py
```
These files represent the following:

* The outer directory `project_test` is just a simple container for the project. The name does not affect Django at all and this name could be chnaged to anything you want.

* `manage.py`: Command line utility that allows you to interact with the Django project in different ways. You can read the details about this file at `/ref/django-admin`.

* The inner directory `project_test` is the python package for the project. It's name is the name of the Python package that you should always use to import anything that is inside the project (e.g. `project_test.urls`).

* `project_test/__init__.py` is an empty file that tells Python that the directory must be considered as a Python package (if you are new to Python, you could read more about Python packages at the official Python documentation).

* `project_test/settings.py` is the settings/configuration file for this Django project. This is a normal Python module that define module-level variables that will represent the settings of the Django project.

* `project_test/urls.py` is where the declaration of the URLs for this Django project are stored, something like a "table of contents" for the project. 

* `project_test/wsgi.py` is the entripoint for serving the project through a web server compatible with WSGI.

Let's quickly add a folder titled templates into the directory with `project_test/` and `manage.py` in order that the folder structure should look like the following:
```
├─ templates
├─ project_test
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
Static and media will serve the images on our app. We need too make some changes in the `settings.py` file in order to have the appropriate folders created. Below the defined `STATIC_URL` in the `settings.py`, add
```
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
os.makedirs(STATIC_TMP, exist_ok=True)
os.makedirs(STATIC_ROOT, exist_ok=True)
os.makedirs(MEDIA_ROOT, exist_ok=True)
```