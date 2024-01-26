from django.http import HttpResponse


def htmx_redirect(url):
    return HttpResponse(
        content="",
        status=204,
        headers={"HX-Location": url},
    )
