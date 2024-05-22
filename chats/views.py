from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import json
from openai import OpenAI
from django.conf import settings

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('query')

        if not user_query:
            return JsonResponse({'error': 'No query provided'}, status=400)

        try:
            client = OpenAI(api_key=settings.OPEN_AI_API_KEY)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_query},
                ],
                temperature=0.7,
                max_tokens=150
            )

            answer = response.choices[0].message.content
            return JsonResponse({'response': answer})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
