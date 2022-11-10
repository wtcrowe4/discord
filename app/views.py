from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic
from .forms import RoomForm

def register_page(req):
    page = 'register'
    if req.user.is_authenticated:
        return redirect('home')
    if req.method == 'POST':
        first_name = req.POST.get('first_name')
        last_name = req.POST.get('last_name')
        username = req.POST.get('username')
        email = req.POST.get('email')
        password = req.POST.get('password')
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password)
        user.save()
        messages.success(req, 'Account was created for ' + username)
        login(req, user)
        # add error handling for registration form
        return redirect('home')
    context = {'page': page}
    return render(req, 'app/register_login.html', context)

def login_page(req):
    page = 'login'
    if req.user.is_authenticated:
        return redirect('home')
    if req.method == 'POST':
        username = req.POST.get('username')
        password = req.POST.get('password')
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('home')
        else:
            messages.info(req, 'Username or password is incorrect')
    context = {'page': page}
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
    room_messages = room.message_set.all().order_by('-created')
    context = { 'room': room, 'room_messages': room_messages }
    return render(req, 'app/room.html', context)

@login_required(login_url='login')
def create_room(req):
    form = RoomForm()
    if req.method == 'POST':
        form = RoomForm(req.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        
    context = {'form': form}
    return render(req, 'app/room_form.html', context)

@login_required(login_url='login')
def update_room(req, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if req.user != room.host:
        messages.info(req, 'You are not allowed to update this room')
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    if req.method == 'POST':
        form = RoomForm(req.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(req, 'app/room_form.html', context)

@login_required(login_url='login')
def delete_room(req, pk):
    room = Room.objects.get(id=pk)
    if req.user != room.host:
        messages.info(req, 'You are not allowed to delete this room')
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    if req.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room': room}
    return render(req, 'app/delete.html', context)