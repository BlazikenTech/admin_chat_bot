from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from openai import OpenAI
from django.conf import settings
from .models import Chat
from django.contrib.auth.models import User
from django.utils import timezone

@csrf_exempt
def chat_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_query = data.get('query')
        user_id = data.get('user_id')

        if not user_query:
            return JsonResponse({'error': 'No query provided'}, status=400)

        # Set user
        if user_id:
            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            if request.user.is_authenticated:
                user = request.user
            else:
                # Handle anonymous user case or return an error
                return JsonResponse({'error': 'User ID not provided and user is not authenticated'}, status=400)

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

            # Save user query to the Chat model
            Chat.objects.create(
                user=user,
                text=user_query,
                sender=Chat.USER,
                created_at=timezone.now()
            )

            # Save assistant response to the Chat model
            Chat.objects.create(
                user=user,
                text=answer,
                sender=Chat.BOT,
                created_at=timezone.now()
            )

            return JsonResponse({'response': answer})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
