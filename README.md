# django-htmx-todomvc

Here is an example of TodoMVC implementation using Django and htmx, with a little bit of hyperscript.

This implementation is only an example and there are many other ways to do it.

The objectives of this project were the following:
 - to use the generic django classes for the views
 - try to keep the same "logic" as the generic Django views (e.g. make redirects after the create/update/delete/... using HX-Location from htmx 1.8)
 - use as few "partial" views as possible

demo : https://django-htmx-todomvc.herokuapp.com/

# HTMX 1.8

Documentation of the HTMX "HX-Location" attribute: https://htmx.org/headers/hx-location/
