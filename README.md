# Print Server

A simple print server for onsite programming contests and similar events.
It helps you to restrict users from direct access to printers by providing a
simple web-UI.

- [How to set up](#how-to-set-up)
- [Running the server](#running-the-server)
- [Adding users](#adding-users)
- [Configuration](#configuration)
- [Hacking](#hacking)
- [Contribution](#contribution)
- [License](#license)

## How to set up

This project is built on [Django](https://www.djangoproject.com/). It doesn't
require any specific Python version, but I recommend the latest one. Check the
[Github tests](./.github/workflows/tests.yml) to see which versions are passing.
You may find the dependencies in [requirements.txt](./requirements.txt).

You can compile and set up the project using
[GNU make](https://www.gnu.org/software/make/).
The system must have `lpr` installed from
[CUPS](https://www.cups.org/doc/man-lpr.html) for submitting the jobs to
the actual printers.

### Installation

The following command creates a Python virtual environment at `.venv` and
installs the required packages. Note that it uses `python3 -m venv` command.

```
make install
```

### Set up database

To create and apply _migrations_ to update database schema, run the following
command:

```
make migrate
```

### Set up static files

This project is set up to make Django serve static files. Unless you are serving
the static files by other means, run the following command to collect your
static files in the designated location.
See `STATIC_ROOT` in [settings.py](./printserver/settings.py) for more.

```
make collectstatic
```

### Create an administrator user

Utilize the Django `createsuperuser` command to create an admin user for the
server.

```
. .venv/bin/activate
./manage.py createsuperuser
```

## Running the server

Run the following command to run the server at port 8000:

```
make run
```

Make sure that the printers are accessible from the system on which
the server is being run.

## Adding users

Login to an admin account and head over to `/admin/accounts/siteuser/add-users/`
to add users in bulk. The text field accepts the details of an user per line in
a CSV format, separated by commas.

The details of an user:
- `username`: Login username of the user.
- `password`: Login password for the user. It must contain at least 8 characters
and cannot be entirely numeric.
- `name`: The full name of the user.
- `organization`: The organization of the user. This is optional and may be
left empty.
- `printer-name`: The printer to assign user's prints to. It must contain the
exact name of the desired printer. It may be left empty as well to use the
system default printer.

An example input to the text field may look like the following:

```csv
foo,fooPasswd,Team Foo,The Foo University,foo-printer
bar,barPasswd,Team Bar,The Bar Org,
tmp,tmpPasswd,Team TMP,,
```

This will create three users `foo`, `bar` and `tmp` with the specified details.
The printer named `foo-printer` will print `foo`'s prints while the default
printer will be used for `bar` and `tmp`.

Note that leading and trailing spaces are not trimmed.

## Configuration

You can find a list of configuration in
[settings.py](./printserver/settings.py).

### Database

This project by default uses a [sqlite3](https://www.sqlite.org/) database. You
may find the database file as `db.sqlite3` in your project root.
Should you want to use other database engines, change the `DATABASES` variable
accordingly. The 
[Django documentation](https://docs.djangoproject.com/en/4.2/ref/databases/)
may help you.

### Static files

This project is set up to make Django serve static files. You can change this
behavior and serve static files yourself. Take a look at the
[documentation](https://docs.djangoproject.com/en/4.2/howto/static-files/deployment/)
to learn how to do so.

`DEBUG` is by default set to `True` for the sole purpose of not bothering to
serve static files by ourselves. Set `DEBUG=False` if you don't need
Django to serve static files as the debug-mode is unsuitable for production
([official docs](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-DEBUG)).

### User-uploaded files

By default, this project does not serve media files.

The uploaded text is converted into a pdf file which is kept in the `MEDIA_ROOT`
directory. The pdf file is named with the sha256 hash of the content and sent
to the designated printer.

### Project title

Set `PROJECT_TITLE` to your preferred header. Default is "Print Server".

### Print limits

The maximum number of pages an user can print is set in `MAX_PAGES`.
The default value is 50 pages. 
Additionally an user can print no more than `MAX_PAGES_PER_PRINT` pages in one
request. The default limit is 10 pages.

### Internationalization

Set the `LANGUAGE_CODE`, `TIME_ZONE`, `USE_I18N` and `USE_TZ` variables.

## Hacking

See [HACKING.md](./HACKING.md).

## Contribution

This project was spearheaded by [@mahdihasnat](https://github.com/mahdihasnat/).
I forked [his repository](https://github.com/mahdihasnat/Print-Server) and
re-wrote the project mostly for restructuring.

### How to contribute?

Pull Requests are welcome! Please create an issue before, so that we are not
doing the same things in parallel.

## License

This project is licensed under
[GNU GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt).
See [LICENSE](./LICENSE).