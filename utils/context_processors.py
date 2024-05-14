from django.conf import settings


def open_ai_api_key(request):
    return {
        "open_ai_api_key": settings.OPEN_AI_API_KEY,
    }
