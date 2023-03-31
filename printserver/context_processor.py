from django.conf import settings


def project_constants(request):
    return {
        "PROJECT_TITLE": settings.PROJECT_TITLE,
    }
