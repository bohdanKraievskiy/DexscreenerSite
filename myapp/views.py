from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from pymongo.errors import DuplicateKeyError
import re
import uuid
from django.utils import timezone
db = settings.MONGO_DB
users_collection = settings.MONGO_DB['users']
groups_collection = settings.MONGO_DB['groups']

def home(request):
    return render(request, 'auth/home.html')

class CustomUser:
    def __init__(self, id, username):
        self.id = id
        self.username = username
        self.is_authenticated = True

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        user = users_collection.find_one({'username': username, 'password': password})
        if user:
            custom_user = CustomUser(id=user['_id'], username=user['username'])
            refresh = RefreshToken.for_user(custom_user)
            access_token = str(refresh.access_token)

            # Обновлення інформації в MongoDB
            users_collection.update_one({'username': username},
                                        {'$set': {'auth_status': 'authorized', 'token': access_token}})

            messages.success(request, 'Login successful')
            response = redirect('login')
            response.set_cookie('access_token', access_token)
            return response
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'auth/login.html')

def enter_name_view(request):
    if request.method == 'POST':
        group_name = request.POST.get('group_name').strip()

        if not group_name:
            messages.error(request, 'Group name cannot be empty')
            return redirect('enter_name')

        # Приводим имя группы к нижнему регистру для проверки дубликатов
        group_name_lower = group_name.lower()

        # Проверяем, существует ли уже группа с таким именем (независимо от регистра)
        if groups_collection.find_one({'name_lower': group_name_lower}):
            return render(request, 'auth/enter_name.html', {'group_name_taken': True})

        # Создаем новый документ группы с полем для имени в нижнем регистре
        new_group = {
            'name': group_name,
            'name_lower': group_name_lower,
            'created_at': timezone.now(),
        }

        groups_collection.insert_one(new_group)

        messages.success(request, 'Group created successfully')
        return redirect('login')

    return render(request, 'auth/enter_name.html')



def group_list_view(request):
    # Retrieve all groups from the database
    groups = list(groups_collection.find({}))
    return render(request, 'auth/group_list.html', {'groups': groups})