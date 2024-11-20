from django import forms
from .models import Routine, Exercise, RoutineSchedule
from bson import ObjectId


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'duration_minutes']

class ExerciseEditForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description', 'duration_minutes']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afegim classes per l'estil i placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })
class RoutineExerciseForm(forms.Form):
    exercise_name = forms.CharField(max_length=100)
    duration_minutes = forms.IntegerField()
    order = forms.IntegerField()

class RoutineForm(forms.ModelForm):
    class Meta:
        model = Routine
        fields = ['name', 'description']
        widgets = {
            'exercises': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Afegim classes per l'estil i placeholders
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': self.fields[field].label
            })

# class RoutineScheduleForm(forms.ModelForm):
#     routine = forms.CharField(widget=forms.Select())
    
#     class Meta:
#         model = RoutineSchedule
#         fields = ['routine', 'weekday', 'time_slot']
        
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         routines = Routine.objects.all()
        
#         # Creem les opcions pel select de rutines
#         routine_choices = [(str(r._id), r.name) for r in routines]
#         self.fields['routine'].widget.choices = routine_choices
        
#         # Configurem els altres camps
#         self.fields['weekday'].choices = RoutineSchedule.WEEKDAYS
#         self.fields['time_slot'].choices = RoutineSchedule.TIME_SLOTS
        
#         # Afegim classes Bootstrap
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'

#     def clean_routine(self):
#         routine_id = self.cleaned_data.get('routine')
#         try:
#             # Convertim l'string a ObjectId
#             object_id = ObjectId(routine_id)
#             routine = Routine.objects.get(_id=object_id)
#             return routine
#         except (Routine.DoesNotExist, Exception) as e:
#             print(f"Error processing routine: {e}")
#             raise forms.ValidationError("La rutina seleccionada no és vàlida")

#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         instance.routine = self.cleaned_data['routine']
#         if commit:
#             instance.save()
#         return instance

    # Definim el camp routine com a ChoiceField en lloc de ModelChoiceField
class RoutineScheduleForm(forms.ModelForm):
    routine = forms.ChoiceField()

    class Meta:
        model = RoutineSchedule
        fields = ['routine', 'weekday', 'time_slot']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        routines = Routine.objects.all()
        self.fields['routine'].choices = [
            (str(routine._id), routine.name) for routine in routines
        ]
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean_routine(self):
        routine_id = self.cleaned_data.get('routine')
        try:
            return ObjectId(routine_id)
        except Exception as e:
            raise forms.ValidationError("ID de rutina no vàlid")

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.routine_id = self.cleaned_data['routine']
        if commit:
            instance.save()
        return instance