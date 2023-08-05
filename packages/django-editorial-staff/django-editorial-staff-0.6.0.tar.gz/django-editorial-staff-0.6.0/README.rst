django-editorial-staff
======================

``django-editorial-staff`` is a simple Django app to store and manage
editorial staffers, and the organizational hierarchy they work in.

It includes a robust API that other apps can treat as a “single source
of truth” for users in the organization.

It also includes a “data provider” feature that will quickly and
automatically ingest users’ data from third-party services (and ships
with a “data provider” for Slack organizations).

Detailed documentation will be added at a later date.

Quick start
-----------

1. Install this app:

   ::

        pip install django-editorial-staff

2. Add "editorial_staff" to your INSTALLED_APPS setting like this:

   ::

       INSTALLED_APPS = [
           ...
           'editorial_staff',
       ]

3. Include the editorial_staff URLconf in your project urls.py like
   this:

   ::

       url(r'^staff/', include('editorial_staff.urls')),

4. Run ``python manage.py migrate`` to create the staff models.

5. Start the development server and visit http://127.0.0.1:8000/staff/
   to see a list of staffers and add others.

6. Visit http://127.0.0.1:8000/staff/api/ to explore the app’s REST API.

Front-end development
---------------------

``django-editorial-staff`` front-end pages are built using ES6 and SCSS,
and this app includes a Gulp installation that converts files written in
these dialects to plain JavaScript and CSS, respectively.

When developing on the front-end, you’ll need to run this Gulp
installation yourself. Follow these steps to get started.

1. Open a terminal window and navigate to the root of this app.

2. Within the app, navigate to ``./editorial_staff/staticapp``.

3. If this is your first time running Gulp on this project, run
   ``npm install`` to install JS dependencies. This may take several
   minutes.

4. Once your dependencies are installed, run ``gulp`` to begin local
   development.

5. When your Gulp server says it’s up and running, visit
   http://127.0.0.1:3000/staff/ for a live preview of your front-end
   files.

6. Proceed to modify your front-end interface by changing files in
   ``./editorial_staff/staticapp/scss/`` and
   ``./editorial_staff/staticapp/js/``. Your changes will be applied to
   the Gulp server URL without the need for to reload the page manually.
