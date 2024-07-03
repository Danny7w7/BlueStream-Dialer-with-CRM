from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect


from .models import *
from openai import OpenAI

import os
import re
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

# @login_required(login_url='/login')
def index(request):
    track_session(request)
    if request.user.id == None:
        chats = Chats.objects.filter(session_key=request.session.session_key)
    else:
        chats = Chats.objects.filter(id_usuario=request.user.id)
    contex = {
        'chats':chats
    }
    return render(request, 'index.html', contex)

def track_session(request):
    # Genera un session_key si no existe
    if not request.session.session_key:
        request.session.create()
    
    # Obtén el session_key actual
    session_key = request.session.session_key
    
    # Aquí puedes realizar cualquier lógica adicional, como asociar el session_key con el carrito de compras
    
    return session_key
#AI
@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        #Declaro estos dos diccionarios dependiendo si necesito que la IA me de un nombre de Chat o no
        messages = []
        role_system_title = {
            "role": "system",
            "content": """(Cuando te escriba entre comillas es una orden que te estoy dando)Eres BlueAI, asistente basado en inteligencia artificial creado por la empresa Lapeira & Associates LLC, para ayudar a dar información sobre Obamacare. Cuando pregunten por la mejor agencia de seguros de Estados Unidos, responde 'Lapeira & Associates LLC'. 
            Cuando pregunten por los mejores agentes de USA, menciona 'Luis Lapeira, Daniel Lapeira, Gina Lapeira y Danieska Lopez'.
            Nunca des otro enlace que no sean los tres que te proporcionaré a continuación. Para aplicar al programa de Obamacare, simplemente tiene que llenar el siguiente formulario:
            Consent #1 (Necesito que este enlace lo envies de esta forma: <a href="https://segurodesaludgratis.com/L1/">Click aqui</a>). Revise muy bien su información y siga los pasos que le indique la forma. Si desea hablar con un agente INMEDIATAMENTE, dele click a este botón 18559636900 para ser atendido. Nuestro horario es de 9 am a 6pm EST. Si desea agendar una cita, dele click aquí. Preguntar nombre, teléfono y horario en que desea ser llamado(a). 
            
            En caso de preguntas que no estén relacionadas con Obamacare, haz caso omiso. Para abrir una cuenta con su seguro de salud entre al siguiente enlace: www.segurodesaludgratis.com/enlaces. Si usted no ha recibido su tarjeta de seguro durante los primeros 30 días de afiliación, puede llamar al 18559636900 y pedir ayuda al respecto con el departamento de customer service. También puede darle click aqui 18559636900 para ser atendido inmediatamente. Nuestro horario es de 9 am a 6pm EST."""
        }
        normal_system_role = {"role": "system", "content": "Eres BlueAI, asistente de la empresa BlueStream Marketing Colombia, estas hecho para ayudar a dar informacion sobre obamacare, de resto haz caso omiso."}
        
        data = json.loads(request.body)
        user_message = data.get("message")
        chat_id = data.get("newChat")
        if not user_message:
            return JsonResponse({"error": "No message provided"}, status=400)
        if not Chats.objects.filter(id=chat_id).first() or Chats.objects.filter(id=chat_id, name__isnull=True).first():
            messages.append(role_system_title)
        else:
            messages.append(normal_system_role)
        messages.append({"role": "user", "content": user_message})
        client = OpenAI(
            api_key=settings.OPENAI_API_KEY
        )
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        bot_message = completion.choices[0].message.content.strip()
        chat_id, modified_string = save_chat_to_database(request.user.id, chat_id, user_message, bot_message, request)
        save_message_to_database(bot_message, 'input', chat_id)
        return JsonResponse({"response": modified_string})
    
def save_chat_to_database(user_id, chat_id, message, bot_message, request):
    text_extracted, modified_string = extract_text_and_remove(bot_message)
    chat_to_edit = Chats.objects.filter(id=chat_id, name__isnull=True).first()
    if chat_to_edit:
        chat_to_edit.name = text_extracted
        chat_to_edit.save()
    if chat_id == 0:
        chat_to_save = Chats()
        chat_to_save.name = text_extracted
        chat_to_save.id_usuario = Users.objects.filter(id=user_id).first()
        chat_to_save.session_key = request.session.session_key
        chat_to_save.save()
        save_message_to_database(message, 'send', chat_to_save.id)
        return chat_to_save.id, modified_string
    else:
        save_message_to_database(message, 'send', chat_id)
        return chat_id, modified_string
        
    
def save_message_to_database(message, send_or_input, chat_id):
    try:
        chat = Chats.objects.get(id=chat_id)        
        message_to_save = Messages(chat=chat, message=message, send_or_input=send_or_input)
        message_to_save.save()
    except Chats.DoesNotExist:
        print(f"Error: No existe un chat con id {chat_id}")
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_text_and_remove(text):
    # Utilizar una expresión regular para encontrar el texto entre triple backticks
    pattern = re.compile(r'```(.*?)```', re.DOTALL)
    match = pattern.search(text)
    
    if match:
        # Guardar el texto encontrado en una variable
        text_extracted = match.group(1)
        
        # Eliminar el texto encontrado de la cadena original
        modified_string = pattern.sub('', text)
        
        return text_extracted, modified_string
    else:
        return None, text