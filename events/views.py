from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count, Sum 
from datetime import date, time, datetime 
from .models import Event, Participant, Category
from events.forms import EventForm, ParticipantForm, CategoryForm


def category_list(request):
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories, 'title': 'All Categories'}
    return render(request, 'events/category_list.html', context)

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category created successfully!")
            return redirect('category-list')
    else:
        form = CategoryForm()
    context = {'form': form, 'title': 'Create Category'}
    return render(request, 'events/category_form.html', context)

def category_update(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f"Category '{category.name}' updated successfully!")
            return redirect('category-list')
    else:
        form = CategoryForm(instance=category)
    context = {'form': form, 'title': f'Update Category: {category.name}'}
    return render(request, 'events/category_form.html', context)

def category_delete(request, pk):
    category = Category.objects.get(pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.info(request, f"Category '{category.name}' deleted successfully!")
        return redirect('category-list')
    context = {'category': category, 'title': f'Delete Category: {category.name}'}
    return render(request, 'events/category_confirm_delete.html', context)

def participant_list(request):
    participants = Participant.objects.all().order_by('name')
    context = {'participants': participants, 'title': 'All Participants'}
    return render(request, 'events/participant_list.html', context)

def participant_create(request):
    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Participant created successfully!")
            return redirect('participant-list')
    else:
        form = ParticipantForm()
    context = {'form': form, 'title': 'Add Participant'}
    return render(request, 'events/participant_form.html', context)

def participant_update(request, pk):
    participant = Participant.objects.get(pk=pk)
    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            form.save()
            messages.success(request, f"Participant '{participant.name}' updated successfully!")
            return redirect('participant-list')
    else:
        form = ParticipantForm(instance=participant)
    context = {'form': form, 'title': f'Update Participant: {participant.name}'}
    return render(request, 'events/participant_form.html', context)

def participant_delete(request, pk):
    participant = Participant.objects.get(pk=pk)
    if request.method == 'POST':
        participant.delete()
        messages.info(request, f"Participant '{participant.name}' deleted successfully!")
        return redirect('participant-list')
    context = {'participant': participant, 'title': f'Delete Participant: {participant.name}'}
    return render(request, 'events/participant_confirm_delete.html', context)

def event_list(request):
    events = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants', distinct=True)
    ).all().order_by('date', 'time')
    
    search_query = request.GET.get('search', '')
    if search_query:
        events = events.filter(name__icontains=search_query) | events.filter(location__icontains=search_query)
    
    category_id = request.GET.get('category')
    if category_id:
        events = events.filter(category_id=category_id)
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if start_date_str and end_date_str:
        start_date = date.fromisoformat(start_date_str)
        end_date = date.fromisoformat(end_date_str)
        events = events.filter(date__range=[start_date, end_date])
    elif start_date_str:
        start_date = date.fromisoformat(start_date_str)
        events = events.filter(date__gte=start_date)
    elif end_date_str:
        end_date = date.fromisoformat(end_date_str)
        events = events.filter(date__lte=end_date)
    
    total_participants_for_current_list = events.aggregate(total=Count('participants', distinct=True))['total'] or 0
    
    categories = Category.objects.all() 

    current_date = date.today()
    current_time = datetime.now().time()

    context = {
        'events': events,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id,
        'start_date': start_date_str,
        'end_date': end_date_str,
        'total_participants_all_events': total_participants_for_current_list, 
        'current_date': current_date,
        'current_time': current_time,
        'title': 'All Events'
    }
    return render(request, 'events/event_list.html', context)

def event_detail(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants', distinct=True)
    ).get(pk=pk)
    current_date = date.today()
    current_time = datetime.now().time() 
    context = {
        'event': event, 
        'current_date': current_date,
        'current_time': current_time,
        'title': f'Event Details: {event.name}'
    }
    return render(request, 'events/event_detail.html', context)

def organizer_dashboard(request):
    total_events = Event.objects.count()
    upcoming_events_count = Event.objects.filter(date__gte=date.today()).count() 
    past_events_count = Event.objects.filter(date__lt=date.today()).count()
    total_participants = Participant.objects.count() 
    
    filter_type = request.GET.get('filter', 'all')
    events_filtered = Event.objects.select_related('category').prefetch_related('participants').annotate(
        participant_count=Count('participants', distinct=True)
    )

    if filter_type == 'upcoming':
        events_filtered = events_filtered.filter(date__gte=date.today()).order_by('date', 'time')
    elif filter_type == 'past':
        events_filtered = events_filtered.filter(date__lt=date.today()).order_by('-date', '-time')
    elif filter_type == 'today':
        events_filtered = events_filtered.filter(date=date.today()).order_by('time')
    else: 
        events_filtered = events_filtered.order_by('date', 'time')

    current_date = date.today()
    current_time = datetime.now().time()

    context = {
        'total_events': total_events,
        'upcoming_events_count': upcoming_events_count,
        'past_events_count': past_events_count,
        'total_participants': total_participants, 
        'events_filtered': events_filtered, 
        'filter_type': filter_type, 
        'current_date': current_date,
        'current_time': current_time,
        'title': 'Organizer Dashboard'
    }
    return render(request, 'events/organizer_dashboard.html', context)

def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.name}' created successfully!")
            return redirect('event-list')
    else:
        form = EventForm()
    context = {'form': form, 'title': 'Create New Event'}
    return render(request, 'events/event_form.html', context)

def event_update(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            event = form.save()
            messages.success(request, f"Event '{event.name}' updated successfully!")
            return redirect('event-list')
    else:
        form = EventForm(instance=event)
    context = {'form': form, 'title': f'Update Event: {event.name}'}
    return render(request, 'events/event_form.html', context)

def event_delete(request, pk):
    event = Event.objects.select_related('category').prefetch_related('participants').get(pk=pk)
    if request.method == 'POST':
        event.delete()
        messages.info(request, f"Event '{event.name}' deleted successfully!")
        return redirect('event-list')
    context = {'event': event, 'title': f'Delete Event: {event.name}'}
    return render(request, 'events/event_confirm_delete.html', context)
