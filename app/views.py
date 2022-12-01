from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, Message
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
    users = User.objects.filter(Q(username__icontains=q) | Q(first_name__icontains=q) | Q(last_name__icontains=q))
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) |
        Q(host__username__icontains=q))
    topics = Topic.objects.all()
    room_count = rooms.count()
    recent_messages = Message.objects.all().order_by('-created')[:5]
    topic_messages = Message.objects.filter(Q(room__topic__name__icontains=q)).order_by('-created')[:5]
    context = { 'users': users, 'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'recent_messages': recent_messages,
               'topic_messages': topic_messages }
    return render(req, 'app/home.html', context)

def room(req, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('created')
    participants = room.participants.all()
    if req.method == 'POST':
        message = Message.objects.create(
            user = req.user,
            room = room,
            message = req.POST.get('message')
        )
        # this is not rendering the new message participant on page 3.22
        room.participants.add(req.user)
        return redirect('room', pk=room.id)
    context = { 'room': room, 'room_messages': room_messages, 'participants': participants }
    return render(req, 'app/room.html', context)

def profile(req, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    topics = Topic.objects.all()
    recent_messages = user.message_set.all().order_by('-created')[:5]
    topic_messages = user.message_set.order_by('-created')[:5]
    context = { 'user': user, 'rooms': rooms, 'topics': topics,
               'recent_messages': recent_messages, 'topic_messages': topic_messages }
    return render(req, 'app/profile.html', context)

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
    context = {'obj': room}
    return render(req, 'app/delete.html', context)

@login_required(login_url='login')
def delete_message(req, pk):
    message = Message.objects.get(id=pk)
    if req.user != message.user:
        messages.info(req, 'You are not allowed to delete this message')
        return HttpResponseRedirect(req.META.get('HTTP_REFERER'))
    if req.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
    return render(req, 'app/delete.html', {'obj': message})
    