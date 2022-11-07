from django.shortcuts import render
from .models import Room

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