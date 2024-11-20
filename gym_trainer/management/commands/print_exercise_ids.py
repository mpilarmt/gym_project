from django.core.management.base import BaseCommand
from gym_trainer.models import Exercise

class Command(BaseCommand):
    help = 'Prints the IDs of all exercises'

    def handle(self, *args, **kwargs):
        exercises = Exercise.objects.all()
        for exercise in exercises:
            self.stdout.write(str(exercise._id))  # Imprimeix l'ID
