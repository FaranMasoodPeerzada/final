from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from chatapp.models import Registeration,Admin
from django.http import HttpResponse
from django.core.mail import send_mail
import PyPDF2
import os
from datetime import datetime,timedelta
from django.contrib.auth.views import PasswordChangeView

#import magic
from django.shortcuts import render, redirect
from .models import Conversation, Message
#from .models import Conversation,Message
# Create your views here.

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
import openai
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


import os



# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from chatapp.models import Registeration,Admin
from django.http import HttpResponse
from django.core.mail import send_mail
import PyPDF2
import os
from datetime import datetime,timedelta
from django.contrib.auth.views import PasswordChangeView

#import magic
from django.shortcuts import render, redirect
from .models import Conversation, Message
#from .models import Conversation,Message
# Create your views here.

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
import openai
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required















def chat_list(request):
    conversations = Conversation.objects.all()
    return render(request, 'chat_list.html', {'conversations': conversations})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Conversation, Message

def get_chat_messages(request, conversation_id):
    print('yes')
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    print(f'messages {messages}')
    # Serialize the messages data
    message_data = [{'user': message.text, 'content': message.response, 'created_at': message.created_at} for message in messages]

    return JsonResponse({'messages': message_data})









# views.py
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse



import os
#os.environ['OPENAI_API_KEY'] =

# openai_api_key = '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'
# openai.api_key = openai_api_key

# def ask_openai(message):
#     response = openai.ChatCompletion.create(
#         model = "gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an helpful assistant."},
#             {"role": "user", "content": message},
#         ]
#     )
    
#     answer = response.choices[0].message.content.strip()
#     return answer




from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import textwrap

from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA, ConversationalRetrievalChain
from langchain.chains.conversation.memory import ConversationBufferMemory
import os
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
import json
chat_file = r'static/assets/js/dir/userchats.json'

chat_detail_file = r'static/assets/js/dir/chats.json'
import datetime
#Admin Panel

# Admin Panel
import json
from datetime import datetime, timedelta





from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def server_endpoint(request):
    if request.method == 'POST':
        try:
            # Get the value of 't' from the POST data
            data = json.loads(request.body.decode('utf-8'))
            t_value = data.get('t')
            print(t_value)
            conversation = Conversation.objects.get(id=t_value)
            user_id=conversation.user.id
            chat_data_to_write = {
        "chats": [],
        "channel_chat": [],}
            messages = Message.objects.filter(conversation=conversation)
            message_id_counter = 1  # Initialize the ID counter
            for message in messages:
                message_content = {
                 "id": message_id_counter,
                 "from_id":user_id,
                 "to_id": user_id + 1,
                 "msg": message.text,
                 "has_dropDown": False,  # You need to determine this based on your data
                 "has_images": [],  # You need to determine this based on your data
                 "has_files": [],  # You need to determine this based on your data
                 "datetime": message.created_at.strftime('%Y-%m-%d'),
                 "isReplied": None,  # You need to determine this based on your data
                }
                message_response = {
                 "id": message_id_counter + 1,
                 "from_id": user_id + 1,
                 "to_id": user_id,
                 "msg": message.response,
                 "has_dropDown": False,  # You need to determine this based on your data
                 "has_images": [],  # You need to determine this based on your data
                 "has_files": [],  # You need to determine this based on your data
                 "datetime": message.created_at.strftime("%I:%M %p"),
                 "isReplied": None,  # You need to determine this based on your data
                }
                chat_data_to_write["chats"].append(message_content)
                chat_data_to_write["chats"].append(message_response)
                message_id_counter += 2 
            
            print(chat_data_to_write)
            with open(chat_detail_file, 'w') as json_file:
                json.dump([chat_data_to_write], json_file)
            
            # Process the data as needed

            # Return a JSON response if needed





            response_data = {'message': 'Value received successfully'}
            return JsonResponse(response_data)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    # Handle other HTTP methods or return an appropriate response
    return render(request, 'index.html')














# Define the path to the JSON file
def home(request):
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    #File upload form request
    conversations = Conversation.objects.all()
    # Create a dictionary structure to match the desired format
    data_to_write = {
        "today": [],
        "yesterday": [],
        "previous": []
    }

    # Get the current date
    today = datetime.today().date()

    for re in conversations:
        user_data = {
            "id": re.id,  # Assuming 'id' is a unique identifier
            "name": re.chat_title,
            "created_date": re.created_at.strftime('%Y-%m-%d'),  # Format the date as needed
            "status": "online",
            "profile": ""
        }

        # Decide which category to add the user to based on your logic
        if user_data["created_date"] == today.strftime('%Y-%m-%d'):
            data_to_write["today"].append(user_data)
        elif user_data["created_date"] == (today - timedelta(days=1)).strftime('%Y-%m-%d'):
            data_to_write["yesterday"].append(user_data)
        else:
            data_to_write["previous"].append(user_data)

    # Write the data to the JSON file
    with open(chat_file, 'w') as json_file:
        json.dump([data_to_write], json_file)

    # Optionally, you can return a response or perform other actions here

    # Optionally, you can return a response or perform other actions here


    conversations = Conversation.objects.all()
    
    
# file detail handling name and type
    
    return render(request, 'index.html')



def get_chat_messages(request, conversation_id):
    print('yes',conversation_id)
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    for mes in messages:
        print(mes.text)
    # Serialize the messages data
    message_data = [{'user': message.text, 'content': message.response, 'created_at': message.created_at} for message in messages]

    return JsonResponse({'messages': message_data})



def chat_detail(request, conversation_id):
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
        # Other context data
    
    file_list = []
    user = request.user
    conversations = Conversation.objects.filter(user=user)

    for conversation in conversations:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat':chat,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    today = datetime.today().date()  # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    previous = today - timedelta(days=2)  # Calculate yesterday's date
    
    conversation = Conversation.objects.get(id=conversation_id)
    messages = Message.objects.filter(conversation=conversation)
    user = request.user
    conversations = Conversation.objects.filter(user=user)
    document_file = conversation.document.name
    file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
   
    filename = os.path.basename(document_file)
    file_path = os.path.join("media", document_file)
    print(file_path)
    
    # detected_type = check_file_type(file_path)
    # print(f"Typeeeeeeeeeeeeeee {detected_type}")
    # pdf_text = read_pdf(file_path)
    # print(pdf_text)
    if request.method == 'POST':
        form_type= request.POST.get('form_type')
        if form_type == 'chat_form':
            form = ConversationForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                conversation = form.save(commit=False)
                conversation.user = request.user
                conversation.chat_title =title
                conversation.save()
                return redirect('chat_detail', conversation_id=conversation.id)
    else:
        form = ConversationForm()
        user = request.user
        conversations = Conversation.objects.filter(user=user)
    
    if request.method == 'POST':
          user_message = request.POST.get('message')
          response='asd'
          #response=ask_openai(user_message)
          print(user_message)
          
          if user_message:
                message = Message.objects.create(
                conversation=conversation,
                text=user_message,
                response=response,
                is_user_message=True
             )
                return JsonResponse({'message':user_message, 'response':response})
            # Call ChatGPT API to generate AI response and create a message
            # Save AI-generated response message
            # messages.append(message)  # Add the AI-generated message to the list
    
    return render(request, 'tester.html', {'conversations': conversations,'conversation': conversation, 'messages': messages,'form': form, 'today':today, 'yesterday':yesterday,'active_conversation_id':active_conversation_id, 'document_file':filename,'file_list':file_list, 'chat_file_size':chat_file_size})
