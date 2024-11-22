import logging
from django import forms

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Routine, Exercise, RoutineSchedule
from .forms import RoutineForm, ExerciseForm, RoutineScheduleForm, ExerciseEditForm
from bson import ObjectId

logger = logging.getLogger(__name__)

def is_trainer(user):
    return user.role == 'trainer'

@login_required
@user_passes_test(is_trainer)
def create_edit_routine(request, routine_id=None):
    
    if routine_id:
        routine = get_object_or_404(Routine, _id=ObjectId(routine_id)) #Routine.objects.get(id=routine_id)
        
    else:
        routine = None
        

    if request.method == 'POST':
        form = RoutineForm(request.POST, instance=routine)
        if form.is_valid():
            new_routine = form.save(commit=False)
            new_routine.trainer = request.user  # Assigna l'usuari actual com a entrenador
            new_routine.save()
            new_routine.exercises.clear()
            for exercise_id in request.POST.getlist('exercises'):
                #print(exercise_id)
                exercise = Exercise.objects.get(id=int(exercise_id))
                new_routine.exercises.add(exercise)
                
            messages.success(request, 'Rutina creada correctament!')
            
            return redirect('gym_trainer:routine_list')
    else:
        form = RoutineForm(instance=routine)
    
    exercises = Exercise.objects.all()
    
    

    return render(request, 'gym_trainer/create_edit_routine.html', 
                  {'form': form, 
                   'routine': routine, 
                   'exercises': exercises})    
    
@login_required
@user_passes_test(is_trainer)
def delete_routine(request, routine_id):
    print(routine_id)
    routine = get_object_or_404(Routine, _id=ObjectId(routine_id)) #Routine.objects.get(id=routine_id)
    if request.method == 'POST':
        # eliminem schdeules
        RoutineSchedule.objects.filter(routine_id=routine_id).delete()
        routine_name = routine.name
        routine.delete()
        messages.success(request, f'Rutina {routine_name} eliminada correctament!')
        return redirect('gym_trainer:routine_list')
    return render(request, 'gym_trainer/delete_routine.html', {'routine': routine})


@login_required
@user_passes_test(is_trainer)
def routine_detail(request, routine_id):
    routine = get_object_or_404(Routine, _id=ObjectId(routine_id)) #Routine.objects.get(id=routine_id)
    return render(request, 'gym_trainer/detail_routine.html', {'routine': routine})
@login_required
@user_passes_test(is_trainer)
def routine_list(request):
    routines = Routine.objects.all()
    # Obtenim totes les rutines
    for routine in routines:
        print(routine.name)
        
    return render(request, 'gym_trainer/routine_list.html', {'routines': routines})

@login_required
@user_passes_test(is_trainer)
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gym_trainer:exercise_list')  # Redirigeix a la llista d'exercicis (crea aquesta vista més tard)
    else:
        form = ExerciseForm()
    
    return render(request, 'gym_trainer/create_exercise.html', {'form': form})
@login_required
@user_passes_test(is_trainer)
def exercise_list(request):
    exercises = Exercise.objects.all()  # Recupera tots els exercicis
    return render(request, 'gym_trainer/exercise_list.html', {'exercises': exercises})

@login_required
@user_passes_test(is_trainer)
def edit_exercise(request, exercise_id):
    # Aquí anirà la lògica per editar un exercici existent
    exercise = get_object_or_404(Exercise, id=exercise_id)  # Recupera l'exercici per id

    if request.method == 'POST':
        # Actualitzem els camps de l'exercici amb les dades del formulari
        form = ExerciseEditForm(request.POST, instance=exercise)
        #logger.debug(form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Exercici actualitzat correctament!')
            return redirect('gym_trainer:exercise_list')
        else:
            print("Form errors:", form.errors)    
    else:
        form = ExerciseEditForm(instance=exercise)

    return render(request, 'gym_trainer/edit_exercise.html', {'form': form, 'edit': True})
    
    
@login_required
@user_passes_test(is_trainer)
def delete_exercise(request, exercise_id):
    
    exercise = get_object_or_404(Exercise, id=exercise_id)
    if request.method == 'POST':
        exercise.delete()
        messages.success(request, 'Exercici eliminat correctament!')
        return redirect('gym_trainer:exercise_list')
    
    
    return render(request, 'gym_trainer/delete_exercise.html', {'exercise': exercise})

@login_required
@user_passes_test(is_trainer)
def schedule(request):
    
    if request.method == 'POST':
        form = RoutineScheduleForm(request.POST)
        print("POST data:", request.POST)
        print("Available routines:", [(str(r._id), r.name) for r in Routine.objects.all()])
        
        if form.is_valid():
            try:
                weekday = form.cleaned_data['weekday']
                time_slot = form.cleaned_data['time_slot']
                print(f"Selected weekday: {weekday}, time slot: {time_slot}")
                
                existing_count = RoutineSchedule.objects.filter(
                    weekday=weekday,
                    time_slot=time_slot
                ).count()
                
                if existing_count > 0:
                    messages.error(request, 'Ja existeix una rutina en aquest horari')
                else:
                    form.save()
                    messages.success(request, 'Rutina programada correctament')
                    return redirect('gym_trainer:schedule')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')

        else:
            print("Form errors:", form.errors)
            print("Form cleaned data:", form.cleaned_data)
            print("Selected routine ID:", request.POST.get('routine'))
    else:
        form = RoutineScheduleForm()
    
    # Obtenir tots els horaris i filtrar els que tenen rutines vàlides
    all_schedules = RoutineSchedule.objects.all()
    valid_schedules = [schedule for schedule in all_schedules if schedule.routine is not None]
    
    time_slots = RoutineSchedule.TIME_SLOTS
    days = RoutineSchedule.WEEKDAYS
    
    # Crear un diccionari bidimensional per emmagatzemar els horaris
    schedule_dict = {
        day[0]: {slot[0]: [] for slot in time_slots} 
        for day in days
    }

    # Omplir el diccionari només amb els horaris vàlids
    for schedule in valid_schedules:
        schedule_dict[schedule.weekday][schedule.time_slot].append(schedule)
        
    pastel_colors = [
        '#FFB3BA',  # rosa pastel
        '#BAFFC9',  # verd pastel
        '#BAE1FF',  # blau pastel
        '#FFFFBA',  # groc pastel
        '#FFD9BA',  # taronja pastel
        '#E0BBE4',  # lila pastel
        '#957DAD',  # porpra pastel
        '#D4A5A5',  # rosat pàl·lid
        '#9EC1CF',  # blau cel pastel
        '#F9C6C9',  # coral pastel
        '#AEC6CF',  # blau grisós
        '#B4CFB0',  # verd sage
        '#E6E6FA',  # lavanda
        '#F0E6EF',  # rosa molt pàl·lid
        '#CCE2CB',  # verd menta
    ]
    
    # Assignar colors només a les rutines vàlides
    routine_colors = {}
    color_index = 0
    
    for day in schedule_dict.values():
        for slot in day.values():
            for schedule in slot:
                if schedule.routine and schedule.routine._id not in routine_colors:
                    routine_colors[schedule.routine._id] = pastel_colors[color_index % len(pastel_colors)]
                    color_index += 1
    
    # Netejar els horaris orfes
    orphan_schedules = [s for s in all_schedules if s.routine is None]
    for orphan in orphan_schedules:
        orphan.delete()
        
    return render(request, 'gym_trainer/schedule.html', {
        'form': form,
        'schedule_dict': schedule_dict,
        'time_slots': time_slots,
        'days': days,
        'routine_colors': routine_colors
    })

@login_required
@user_passes_test(is_trainer)
def delete_schedule(request, schedule_id):
    schedule = get_object_or_404(RoutineSchedule, _id=ObjectId(schedule_id)) #RoutineSchedule.objects.get(id=schedule_id)
    schedule.delete()
    messages.success(request, 'Rutina eliminada de l\'horari correctament.')
    return redirect('gym_trainer:schedule')

