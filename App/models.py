from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Job_Seeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    
    def __str__(self):
        return self.user.first_name +' '+ self.user.last_name
    

class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13)
    company = models.CharField(max_length=50)

    def __str__(self):
        return self.company 

class Job_Post(models.Model):
    user = models.ForeignKey("Recruiter", on_delete=models.CASCADE)
    post = models.CharField(max_length=50)
    salary = models.IntegerField()
    description = models.TextField()
    posted_on = models.DateField()
    upto = models.DateField()

    def __str__(self):
        return self.post

    
class AppliedPost(models.Model):
    applied_by = models.ForeignKey("Job_Seeker", on_delete=models.CASCADE)
    job = models.ForeignKey("Job_Post", on_delete=models.CASCADE)
    applied_on = models.DateField()

    def __str__(self):
        return str(self.applied_by)
    

class Feedback(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    feedback = models.TextField()

    def __str__(self):
        return self.name
    

    




