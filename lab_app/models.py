from django.db import models

# Create your models here.
class BannerImage(models.Model):
    image = models.ImageField(upload_to='banner/images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class PeopleCategory(models.Model):
    category = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.category
    

class PeopleProfile(models.Model):
    category = models.ForeignKey(PeopleCategory,on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True,blank=True)
    position = models.CharField(max_length=200,null=True,blank=True)
    affiliation = models.CharField(max_length=200,null=True,blank=True)
    profile_photo = models.ImageField(upload_to='profileImages')
    # project = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return self.name

class Publication(models.Model):
    author = models.ForeignKey(PeopleProfile,on_delete=models.CASCADE)
    title = models.CharField(max_length=255,null=True,blank=True)
    doi_link = models.CharField(max_length=300,null=True,blank=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


