from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TodoItem(models.Model):
    title = models.CharField(max_length=256, verbose_name="Tytuł")
    description = models.TextField(blank=True, null=True, verbose_name="Opis")
    is_completed = models.BooleanField(default=False, verbose_name="Zakończone")
    due_date = models.DateTimeField(blank=True, null=True, verbose_name="Termin wykonania")    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data ostatniej aktualizacji")
    priority = models.PositiveSmallIntegerField(
        choices=[
            (1, "Wysoki"),
            (2, "Średni"),
            (3, "Niski")
        ],
        default=2,
        verbose_name="Priorytet"
    )
    category = models.CharField(max_length=50, blank=True, verbose_name="Kategoria")

    
    class Meta:
        verbose_name = "Zadanie"
        verbose_name_plural = "Zadania"
        ordering = ["-priority", "due_date"]

    def __str__(self):
        return self.title