from django.shortcuts import render
from .models import StudentSpeech


def StudentSpeeches(request):
    speeches = StudentSpeech.objects.all()
    return render(request, "home/home.html", {"speeches": speeches})
    

