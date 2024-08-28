from django.urls import path
from . import views

urlpatterns = [
    path('waiting', views.login_view, name='login'),
    path('login/entername/', views.enter_name_view, name='enter_name'),
    path('groups/', views.group_list_view, name='group_list'),
    path('',views.main_view, name='main'),
]