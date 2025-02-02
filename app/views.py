from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .models import Note, Label, Trash_Bin
from django.utils import timezone
from datetime import timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='account:login')
def home_page(request):
    user = request.user
    labels = Label.objects.filter(user=user)
    notes = Note.objects.filter(label__in=labels,).order_by('-is_pinned', '-created_at')

    selected_label = labels.first() if labels.exists() else None

    context = {
        'label_list': labels, 
        'note_list': notes,
        'selected_label': selected_label,
    }
    return render(request, 'home.html', context)


def get_notes(request, label_id):
    notes = Note.objects.filter(label_id=label_id, is_trashed=False).values(
        'id', 'context', 'is_completed', 'is_pinned'
        ).order_by(
        '-is_pinned', '-created_at'
        )
    
    return JsonResponse({'notes': list(notes)})


def detail_page(request, pk):
    user = request.user
    note = get_object_or_404(Note, pk=pk, label__user=user)
    context = {'note': note}
    return render(request, 'detail_page.html', context)


def create_new_label(request):
    label_name = request.POST.get('label_name') 
    Label.objects.create(title=label_name, user=request.user)
    return redirect(reverse('app:index'))


def create_new_note(request):
    note_context = request.POST.get('context')
    label_id = request.POST.get('label_id')  

    label = Label.objects.filter(id=label_id).first() 
    Note.objects.create(context=note_context, label=label)
   
    return redirect(reverse('app:index'))
  
def edit_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    label_id = request.POST.get('label_id')
    label = Label.objects.filter(id=label_id).first()
    
    if request.method == 'POST':
        new_context = request.POST.get('context', '')
        note.context = new_context
        note.save()
        messages.success(request, 'Note has been updated successfully!')
        return redirect('app:index') 
    
    context = {'note': note}
    return render(request, 'detail_page.html', context, label=label)

def complete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    
    if request.method == 'POST':
        note.is_completed = not note.is_completed
        note.save()
    
    return JsonResponse({'status': 'success', 'is_completed': note.is_completed})


def delete_note(request, pk):
    user = request.user
    note = get_object_or_404(Note, pk=pk)
    Trash_Bin.objects.create(label=note.label, note=note, user=user, deleted_at=timezone.now())
    
    note.is_trashed = True
    note.save()
    
    messages.success(request, 'Note moved to trash successfully..')
    return redirect(reverse('app:index'))


def trash_bin(request):
    user = request.user
    trashed_notes = Trash_Bin.objects.filter(user=user)
    for note in trashed_notes:
        note.context = note.note.context
        note.label_title = note.label.title 
    
    return render(request, 'trash_bin.html', {'trashed_notes': trashed_notes})


def delete_note_permanently(request, pk):
    note = get_object_or_404(Trash_Bin, pk=pk)
    note.delete()

    messages.success(request, 'Note deleted permanently')
    return redirect('app:trash_bin')


def delete_old_note():
    limit_date = timezone.now() - timedelta(days=30)
    trash_bin = Trash_Bin.objects.filter(deleted_at_lte = limit_date )
    for trash in trash_bin:
        trash.note.delete()  
        trash.delete()  
        

def restore_note(request, pk):
    trash_note = get_object_or_404(Trash_Bin, pk=pk)
    note = trash_note.note
    note.is_trashed = False 
    note.save()
    
    trash_note.delete()

    messages.success(request, 'Note restored successfully')
    return redirect(reverse('app:trash_bin'))


def delete_label(request, pk):
    label = get_object_or_404(Label, pk=pk) 
    label.delete()
    
    messages.success(request, 'Label deleted successfully.')
    return redirect(reverse('app:index')) 


def pin_note(request, pk):
    note = Note.objects.get(id=pk)
    pin_limit = 6
    actual_pinned_note = Note.objects.filter(is_pinned=True).count()

    if request.method == 'POST':
        if not note.is_pinned and actual_pinned_note >= pin_limit:
            messages.error(request, 'Pin not is limit passed.')
            return render(redirect('app:index'))

        note.is_pinned = not note.is_pinned 
        note.save()
        return JsonResponse({'status': 'success', 'is_pinned': note.is_pinned})
        
    