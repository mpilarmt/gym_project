import uuid

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from bson import ObjectId
from djongo import models 

class Exercise(models.Model):
    id = models.ObjectIdField()
    #_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration_minutes = models.IntegerField(choices=[(5, '5 minuts'), (10, '10 minuts'), (15, '15 minuts'), (20, '20 minuts')])
    
    def __str__(self):
        return self.name
    
    def get_id(self):
        return int(self.id)  # Retorna l'ID com a int
    
    class Meta:
        abstract = False

class Routine(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    trainer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    exercises = models.ManyToManyField(Exercise, related_name='routines')
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def routine_id(self):
        return str(self._id)
    
    def __str__(self):
        return self.name
    
    class Meta:
       db_table = 'gym_trainer_routine'
class RoutineSchedule(models.Model):
    
    WEEKDAYS = [
        (0, 'Dilluns'),
        (1, 'Dimarts'),
        (2, 'Dimecres'),
        (3, 'Dijous'),
        (4, 'Divendres')
    ]
    
    TIME_SLOTS = [
        (16, '16:00'),
        (17, '17:00'),
        (18, '18:00'),
        (19, '19:00'),
        (20, '20:00'),
        (21, '21:00'),
    ]
    
    _id = models.ObjectIdField()
    routine_id = models.Field()
    weekday = models.IntegerField(choices=WEEKDAYS)
    time_slot = models.IntegerField(choices=TIME_SLOTS)
    
    def __str__(self):
        return f"{self.routine.name} - {self.get_weekday_display()} - {self.get_time_slot_display()}"
  
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    class Meta:
        
        db_table = 'gym_trainer_routineschedule'
         
         
    @property
    def routine(self):
        from .models import Routine
        try:
            return Routine.objects.get(_id=ObjectId(self.routine_id))
        except Routine.DoesNotExist:
            return None
    
    @property
    def schedule_id (self):
        return str(self._id)
