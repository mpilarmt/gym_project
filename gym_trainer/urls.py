from django.urls import path
from . import views

app_name = 'gym_trainer'

urlpatterns = [
    path('routine/create/', views.create_edit_routine, name='create_routine'),
    path('routine/edit/<str:routine_id>/', views.create_edit_routine, name='edit_routine'),
    path('routine/list/', views.routine_list, name='routine_list'),
    path('routine/delete/<str:routine_id>/', views.delete_routine, name='delete_routine'),
    path('routine/details/<str:routine_id>/', views.routine_detail, name='routine_details'),
    path('exercises/create/', views.create_exercise, name='create_exercise'),
    path('exercises/list/', views.exercise_list, name='exercise_list'),
    path('exercise/edit/<int:exercise_id>/', views.edit_exercise, name='edit_exercise'),
    path('exercise/delete/<int:exercise_id>/', views.delete_exercise, name='delete_exercise'),
    path('schedule/', views.schedule, name='schedule'),
    path('schedule/delete/<str:schedule_id>/', views.delete_schedule, name='delete_schedule'),


    #path('edit-routine/<int:routine_id>/', views.edit_routine, name='edit_routine'),
]
