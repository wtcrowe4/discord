from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('profile/<int:pk>', views.profile, name='profile'),
    
    path('', views.home, name='home'),
    path('room/<int:pk>', views.room, name='room'),
    
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<int:pk>', views.update_room, name='update-room'),
    path('delete-room/<int:pk>', views.delete_room, name='delete-room'),
    path('delete-message/<int:pk>', views.delete_message, name='delete-message'),
] 
