# Hacking

## Django apps

This Django project has two major "apps": `accounts` and `prints`.

- `accounts` manages users. It implements a custom user class `SiteUser`.
It has no custom views of its own, rather uses the `django.contrib.auth` views
for login and logout.

- `prints` implements the `Prints` class and manages the printing operations.
As of this writing, it implements only the `submit_view` to submit the texts
for printing. It has a few helper functions defined in
[helpers.py](./prints/helpers.py).
Printer operations are defined in [printer.py](./prints/printer.py).

## Database schema

- Model [`SiteUser`](./accounts/models.py) contains user info.

  | siteuser |
  | - |
  | typical user info.. |
  | organization |
  | printer |
  | remaining_pages |

  Perhaps `remaining_pages` ought to be removed from here and put to somewhere
  else.

- Model [`Prints`](./prints/models.py) contains info about the print requests.

  | prints |
  | - |
  | created_at |
  | user (FK) |
  | content |
  | pages |
  | pdf_path |

## Others

Please go through the source code.
