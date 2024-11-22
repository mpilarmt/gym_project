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