# Development

The web server needs to be set up with an SSL certificate. You can use [mkcert](https://github.com/FiloSottile/mkcert) for development.

## Assets

You can either build the assets once ...

```
npm run build:dev
npm run build:email
```

... or rebuild after every change

```
npm run watch
```

Run the migrations and create an admin user

```
./manage.py migrate
```

Start the actual server

```
./manage.py runserver
```

## Testing

You can run the tests either with `pytest` or with `./manage.py test`. The tests in `mainapp/tests/live` require a specific version of chrome to be installed.

There's a tox config to ensure 3.8 and 3.9 compatibility which can be run with `tox`.

## Dummy data

The dummy data is used for the tests, but can also be used for developement.

Loading:

```
./manage.py loaddata mainapp/fixtures/initdata.json mainapp/fixtures/socialapps.json
```

Saving:

```
./manage.py dumpdata mainapp -e mainapp.UserProfile --indent 4 > mainapp/fixtures/initdata.json
```

## Elasticsearch

To reindex the elasticsearch index (requires elastic search to be enabled):

```
./manage.py search_index --rebuild
```

## Translating strings

```
./manage.py makemessages --locale de
# translate django.po
./manage.py compilemessages
```

## Notifying users about new documents

The following script is meant to be run as an hourly cron job through the `./manage.py cron`:

```
./manage.py notify_users
```

However, for debugging purposes, it can be called stand alone, skipping the actual e-mail-sending and using a custom date range. The following commands dumps the search results of all users since 2017-09-10:

```
./manage.py notify_users --simulate --override-since 2017-09-10
```

## OCR'ing documents

Currently, OCR'ing documents is not done automatically, as this operation is being billed per execution. So for now, it is done manually on demand. The following commands are available to ocr a single file, or to ocr all files with no recognized text:

```
# OCR all empty files:
./manage.py ocr-file --empty
# OCR an individual file:
./manage.py ocr-file --id 23
```

## Creating a page with additional JS libraries

If we use a library on only one page and thus don't want to include it into the main JS-bundle (e.g. Isotope), this would the procedure:

- Normally install it using NPM
- Create a new entry JS script in [mainapp/assets/js](../mainapp/assets/js). Require the library from there.
- Register this new entry point in the [webpack-configuration](../etc/webpack.config.common.js).
- Load this new JS-file in a Django-template within the ``additional_js``-block using the ``render_bundle``-tag. (See [persons.html](../mainapp/templates/mainapp/persons.html) for an example)

If a separate CSS-file is needed (e.g. in the case of fullcalendar), this would be the additional procedure to the one above (which is necessary):

- Create a new SCSS-file in [mainapp/assets/css](../mainapp/assets/css).
- Require the SCSS-file from the corresponding JS entry script. This will automatically generate a compiled CSS-bundle with the name of the JS-bundle.
- Load this new CSS-file in a Django-template within the ``additional_css``-block using the ``render_bundle``-tag. (See [calendar.html](../mainapp/templates/mainapp/calendar.html) for an example)

## E-Mail-Notifications

The templates for the e-mail-notifications are created using [mjml](https://documentation.mjml.io/). So we don't edit the HTML/Django-templates like [user-alert.html](../mainapp/templates/email/user-alert.html) directly, but the source .mjml-files like [user-alert.heml](../mainapp/assets/email/user-alert.mjml) and compile them using:

```
npm run build:email
```

## Wagtail

Exporting:

```
./manage.py dumpdata --indent 4 wagtailcore.page wagtailcore.site
```

## Installation as python package

_This works but needs some more testing/polishing_

```
# First, update the tools so we don't fail due old versions not supporting what we want
pip install --upgrade pip virtualenv
virtualenv venv
. venv/bin/activate
pip install meine-stadt-transparent
```

Set `STATIC_ROOT` to the actual location (e.g. `static` or `/var/www/static`), otherwise configure it through `.env` the same way as for the other deployment methods.

```
mst-manage collectstatic
mst-manage migrate

gunicorn meine_stadt_transparent.wsgi:application -w 2 -b :8000 --capture-output
```

TODO: Customizations

Sidenote: The python package actually install 4 modules (meine-stadt-transparent, cms, importer, mainapp), so you should not try to combine with other python packages using these module names.
