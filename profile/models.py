from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user            =       models.ForeignKey(User, primary_key=True)
    dob             =       models.DateField("Date of Birth", blank=True, default="1900-01-01")
    #resume         =       models.FileField(upload_to="resume/")
