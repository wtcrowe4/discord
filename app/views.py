from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm


def login_page(req):
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.info(req, 'Username or password is incorrect')
    context = {}
    return render(req, 'app/register_login.html', context)

def logout_user(req):
    logout(req)
    return redirect('login')

def home(req):
    q = req.GET.get('q') if req.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = { 'rooms': rooms, 'topics': topics, 'room_count': room_count }
    return render(req, 'app/home.html', context)

def room(req, pk):
    room = Room.objects.get(id=pk)
    context = { 'room': room }
    return render(req, 'app/room.html', context)

def create_room(req):
    form = RoomForm()
    if req.method == 'POST':
        form = RoomForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(req, 'app/room_form.html', context)

def update_room(req, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if req.method == 'POST':
        form = RoomForm(req.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(req, 'app/room_form.html', context)

def delete_room(req, pk):
    room = Room.objects.get(id=pk)
    if req.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(req, 'app/delete.html', context)