from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout

from .models import *
from openai import OpenAI
import os
import json


# Create your views here.

# Auth
def login_(request):
    if request.user.is_authenticated:
        return redirect(index)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(index)
        else:
            msg = 'Datos incorrectos, intente de nuevo'
            return render(request, 'auth/login.html', {'msg':msg})
    else:
        return render(request, 'auth/login.html')
    
def logout_(request):
    logout(request)
    return redirect(index)

#@login_required(login_url='/login')
def index(request):
    return render(request, 'index.html')

#AI
# @csrf_exempt
# def chatbot(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         user_message = data.get("message")

#         response = openai.Completion.create(
#             engine="text-davinci-003",  # puedes cambiar a otro modelo si es necesario
#             prompt=user_message,
#             max_tokens=150,
#             n=1,
#             stop=None,
#             temperature=0.7,
#         )

#         bot_message = response.choices[0].text.strip()
#         return JsonResponse({"response": bot_message})

#     return JsonResponse({"error": "Invalid request method"}, status=400)

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_message = data.get("message")
        print(user_message)
        print(settings.OPENAI_API_KEY)
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente Goty."},
            ]
        )
        print(completion.choices[0].message)
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)