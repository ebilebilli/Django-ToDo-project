from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Note, Label

def home_page(request):
    user = request.user
    view_control = Label.objects.get(user=user)
    notes = Note.objects.filter(label=view_control).order_by('-is_pinned', '-created_at')
    context = {'note_list': notes}
    return render(request, 'home.html', context)


def detail_page(request, pk):
    note = get_object_or_404(Note, id=pk)
    context = {'note': note}
    return render(request, 'detail_page.html', context)

def create_new_note(request):
    user = request.user
    label = Label.objects.get(user=user)
    note_context = request.POST.get('note')
    Note.objects.create(label=label, context=note_context)
    return redirect(reverse('app:index'))  


def complete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == 'POST':
        note.is_completed = 'is_completed' in request.POST
        note.save()
    return redirect(reverse('app:index'))


def delete_note(request, pk):
    note = get_object_or_404(Note, id=pk) 
    note.delete()
    messages.success(request, 'Note deleted successfully.')
    return redirect(reverse('app:index'))  


def pin_note(request, pk):
    note = Note.objects.get(id=pk)
    if request.method == 'POST':
        note.is_pinned = not note.is_pinned 
        note.save()        
    return redirect(reverse('app:index'))  


#pipenv run python manage.py runserver