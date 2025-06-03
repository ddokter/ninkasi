# Installation

To run Ninkasi, you'll need Django. There is several ways of deploying
a Django app, one of which is using _virtualenv_.



## Virtualenv

Make sure your system has the virtualenv program installed. Pick a
directory to work in and run:

    virtualenv <target directory>
	
Check out Ninkasi from GitHub:

    git clone <>
	
Now move into the virtual environment you created:

    cd <target directory>

Activate the environment:

    . ./bin/activate
	
Install Ninkasi in (development mode):

    pip install -e <path to Ninkasi checkout dir>
	
Set settings module for running the app:

    export DJANGO_SETTINGS_MODULE=ninkasi.settings

Now the last step is to create the database. Default is sqldb:

    ./bin/django-admin migrate

This should give you a working Django server.



## Thirs party JS and CSS

You'll also need some 3d party packages, like Bootstrap and
Fontawesome. These are easily managed using _NPM_. In your virtual
env, install like:

    npm install bootstrap
	npm install fontawesome

