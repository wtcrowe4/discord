from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# rooms = [
#     {'id': 1, 'name': 'Room 1'},
#     {'id': 2, 'name': 'Room 2'},
#     {'id': 3, 'name': 'Room 3'},
# ]

def home(req):
    rooms = Room.objects.all()
    context = { 'rooms': rooms }
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