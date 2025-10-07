from django.db import models



class StudentSpeech(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    university = models.CharField(max_length=200, blank=True, null=True)
    photo = models.ImageField(upload_to='home/student-speeches/images/')
    speech = models.TextField()
    file = models.FileField(upload_to='student_speeches/files/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.university}"
    


class About(models.Model):
    title = models.TextField( blank=True, null=True)
    image1 = models.ImageField(upload_to='home/about/images/',blank=True, null=True)
    image2 = models.ImageField(upload_to='home/about/images/',blank=True, null=True)
    description = models.TextField(blank=True, null=True)