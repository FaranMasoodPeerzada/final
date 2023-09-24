from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from chatapp.models import Registeration,Admin
from django.http import HttpResponse
from django.core.mail import send_mail
import PyPDF2
import os
from django.contrib.auth.views import PasswordChangeView

#import magic
from .models import Conversation, Message
#from .models import Conversation,Message
# Create your views here.

# Create your views here.
from django.http import JsonResponse
from django.utils import timezone
import openai
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
import os
from django.http import HttpResponse
import json
from datetime import datetime,timedelta
from .models import Conversation, Message
import datetime
from django.views.decorators.csrf import csrf_exempt

from .forms import ConversationForm, PasswordChangingForm

from datetime import date, timedelta

#Other Task Functions
#Function to convert file size to human readable format
def convert_bytes_to_human_readable(bytes):
    # Define the suffixes for KB, MB, GB, etc.
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']

    # Determine the appropriate suffix and scale the size down
    index = 0
    while bytes >= 1024 and index < len(suffixes) - 1:
        bytes /= 1024
        index += 1

    # Format the size with the determined suffix
    size_formatted = "{:.2f} {}".format(bytes, suffixes[index])
    return size_formatted


#Function to extract information of active conversation
def conversationinfo(conversations):
    file_list = []
    for conversation in conversations:
        file_path = conversation.document.name
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(conversation.document.path)  # Get file size in bytes
        file_size_readable = convert_bytes_to_human_readable(file_size)
        user = conversation.user
        chat_title = conversation.chat_title
        conv_id=conversation.id
        conversation_info = {'file_name': file_name, 'user': user,'chat_title':chat_title,'file_size': file_size_readable,'conv_id':conv_id}
        file_list.append(conversation_info)
    return file_list














#Function to redirect the user to registeration page
def registeration(request):
    return render(request, 'auth-register.html')

#Function to handle signup request
def signuprequest(request):
    if request.method=="POST":
        print("got it")
        #Get the post parameters
        username= request.POST['username']
        fname= request.POST['fname']
        lname= request.POST['lname']
        email= request.POST['email']
        password1= request.POST['password1']
        password2= request.POST['password2']
        
        # Check for errorneous inputs
        errors = []

        if not username:
            errors.append("Username is required.")

        if not fname:
            errors.append("First name is required.")

        if not lname:
            errors.append("Last name is required.")

        if not email:
            errors.append("Email is required.")

        if not password1:
            errors.append("Password is required.")

        if len(username)>10:
            errors.append("Username must be under 10 characters.")

        if password1 != password2:
            errors.append("Passwords do not match.")

        # Check if the username and email are already in use
        if Registeration.objects.filter(user_name=username).exists():
            errors.append("This username is already taken.")

        if Registeration.objects.filter(user_email=email).exists():
            errors.append("This email address is already in use.")

        if not errors:
            # If there are no errors, create a new user
            registeration = Registeration(user_name=username, first_name=fname,last_name=lname, user_email=email,user_password=password1)
            registeration.save()

            # Redirect to a success page or do something else
            messages.warning(request,"Registration Request Submitted, Kindly Wait For Approval")
            return redirect('login_page')
        else:
            # Display error messages
            for error in errors:
                messages.warning(request, error)
        
        return redirect('user_registeration')




#Function to redirect the user to login page

def loginpage(request):
    return render(request, "auth-login.html")



#Function to handle the user login request
def userloginrequest(request):
    if request.method == "POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('user_home')
        else:
            messages.warning(request, "Invalid username or password. Please try again.")
            return redirect('login_page')

    return render(request, 'auth-login.html')
chat_file = r'static/assets/js/dir/userchats.json'
@login_required
def userhome(request):
    today = datetime.date.today() # Get today's date
    yesterday = today - timedelta(days=1)  # Calculate yesterday's date
    
    #File upload form request
    if request.method == 'POST':
        dtypes= request.POST.get('form_type')
        print(f"type {dtypes}")
        form = ConversationForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            conversation = form.save(commit=False)
            conversation.user = request.user
            conversation.chat_title =title
            conversation.save()
            return redirect('user_home')
    else:
        form = ConversationForm()
    user = request.user
    users_conversation = Conversation.objects.filter(user=user)

    #Conversation detail handling
    file_list=conversationinfo(users_conversation)
    print(f"List detail {file_list}")

    #File upload form request
    conversations = Conversation.objects.all()
    # Create a dictionary structure to match the desired format
    data_to_write = {
        "today": [],
        "yesterday": [],
        "previous": []
    }

    # Get the current date
    # datetime.today().date()
    today = datetime.date.today()
    print(f"today date ",today)
    sorted_conversations = sorted(conversations, key=lambda re: re.id, reverse=True)
    for re in sorted_conversations:
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

    return render(request, 'index.html',{'form':form})
    #return render(request, 'index.html',{'conversations': conversations,'form': form,'today':today,'yesterday':yesterday,'file_list':file_list})


import openai
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        data = request.POST
        conversation_id = data.get("conversationId")
        user_message = data.get("message")

        response_message = "Thank you"
        print(response_message)

        # You can save the response_message in your database if needed
        print("iddd",conversation_id)

        conversation = Conversation.objects.get(id=conversation_id)
        user_message_obj = Message(conversation=conversation, question=user_message,answer=response_message, is_user_message=True)
        user_message_obj.save()


        return JsonResponse({"response": response_message})

    return JsonResponse({"error": "Invalid request method"})


def get_chat_messages(request, conversation_id):
    print(conversation_id)
    conversation = get_object_or_404(Conversation, id=conversation_id)
    print("con",conversation)
    messages = Message.objects.filter(conversation=conversation)
    # Serialize the messages data
    message_data = [{'question': message.question, 'answer': message.answer, 'created_at': message.created_at} for message in messages]

    return JsonResponse({'messages': message_data})



def chat_detail(request, conversation_id):
    active_conversation = get_object_or_404(Conversation, id=conversation_id)
    active_conversation_id= active_conversation.id
        # Other context data
    return redirect(f'/userhome/?chat_id={active_conversation.id}') 

# def chat_list(request):
#     conversations = Conversation.objects.all()
#     return render(request, 'chat_list.html', {'conversations': conversations})

# def get_chat_messages(request, conversation_id):
#     print('yes')
#     conversation = get_object_or_404(Conversation, id=conversation_id)
#     messages = Message.objects.filter(conversation=conversation)
#     print(f'messages {messages}')
#     # Serialize the messages data
#     message_data = [{'user': message.text, 'content': message.response, 'created_at': message.created_at} for message in messages]

#     return JsonResponse({'messages': message_data})












# chat_file = r'static/assets/js/dir/userchats.json'

# chat_detail_file = r'static/assets/js/dir/chats.json'
# #Admin Panel

# # Admin Panel

# @csrf_exempt
# def server_endpoint(request):
#     if request.method == 'POST':
#         try:
#             # Get the value of 't' from the POST data
#             data = json.loads(request.body.decode('utf-8'))
#             t_value = data.get('t')
#             print(t_value)
#             conversation = Conversation.objects.get(id=t_value)
#             user_id=conversation.user.id
#             chat_data_to_write = {
#         "chats": [],
#         "channel_chat": [],}
#             messages = Message.objects.filter(conversation=conversation)
#             message_id_counter = 1  # Initialize the ID counter
#             for message in messages:
#                 message_content = {
#                  "id": message_id_counter,
#                  "from_id":user_id,
#                  "to_id": user_id + 1,
#                  "msg": message.text,
#                  "has_dropDown": False,  # You need to determine this based on your data
#                  "has_images": [],  # You need to determine this based on your data
#                  "has_files": [],  # You need to determine this based on your data
#                  "datetime": message.created_at.strftime('%Y-%m-%d'),
#                  "isReplied": None,  # You need to determine this based on your data
#                 }
#                 message_response = {
#                  "id": message_id_counter + 1,
#                  "from_id": user_id + 1,
#                  "to_id": user_id,
#                  "msg": message.response,
#                  "has_dropDown": False,  # You need to determine this based on your data
#                  "has_images": [],  # You need to determine this based on your data
#                  "has_files": [],  # You need to determine this based on your data
#                  "datetime": message.created_at.strftime("%I:%M %p"),
#                  "isReplied": None,  # You need to determine this based on your data
#                 }
#                 chat_data_to_write["chats"].append(message_content)
#                 chat_data_to_write["chats"].append(message_response)
#                 message_id_counter += 2 
            
#             print(chat_data_to_write)
#             with open(chat_detail_file, 'w') as json_file:
#                 json.dump([chat_data_to_write], json_file)
           
#             # Process the data as needed
#             # Return a JSON response if needed
#             response_data = {'message': 'Value received successfully'}
#             return JsonResponse(response_data)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)

#     # Handle other HTTP methods or return an appropriate response
#     return render(request, 'index.html')














# # Define the path to the JSON file
# def userhomex(request):
#     today = datetime.date.today()  # Get today's date
#     yesterday = today - timedelta(days=1)  # Calculate yesterday's date
#     #File upload form request
#     conversations = Conversation.objects.all()
#     # Create a dictionary structure to match the desired format
#     data_to_write = {
#         "today": [],
#         "yesterday": [],
#         "previous": []
#     }

#     # Get the current date
#     today = datetime.today().date()

#     for re in conversations:
#         user_data = {
#             "id": re.id,  # Assuming 'id' is a unique identifier
#             "name": re.chat_title,
#             "created_date": re.created_at.strftime('%Y-%m-%d'),  # Format the date as needed
#             "status": "online",
#             "profile": ""
#         }

#         # Decide which category to add the user to based on your logic
#         if user_data["created_date"] == today.strftime('%Y-%m-%d'):
#             data_to_write["today"].append(user_data)
#         elif user_data["created_date"] == (today - timedelta(days=1)).strftime('%Y-%m-%d'):
#             data_to_write["yesterday"].append(user_data)
#         else:
#             data_to_write["previous"].append(user_data)

#     # Write the data to the JSON file
#     with open(chat_file, 'w') as json_file:
#         json.dump([data_to_write], json_file)

#     # Optionally, you can return a response or perform other actions here

#     # Optionally, you can return a response or perform other actions here


#     conversations = Conversation.objects.all()
    
    
# # file detail handling name and type
    
#     return render(request, 'index.html')



# def get_chat_messages(request, conversation_id):
#     print('yes',conversation_id)
#     conversation = get_object_or_404(Conversation, id=conversation_id)
#     messages = Message.objects.filter(conversation=conversation)
#     for mes in messages:
#         print(mes.text)
#     # Serialize the messages data
#     message_data = [{'user': message.text, 'content': message.response, 'created_at': message.created_at} for message in messages]

#     return JsonResponse({'messages': message_data})



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
    today = datetime.date.today()  # Get today's date
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
    
    return render(request, 'index.html', {'conversations': conversations,'conversation': conversation, 'messages': messages,'form': form, 'today':today, 'yesterday':yesterday,'active_conversation_id':active_conversation_id, 'document_file':filename,'file_list':file_list})
    
       