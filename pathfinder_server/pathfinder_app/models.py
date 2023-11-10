from django.db import models
from django.conf import settings

class RtImage(models.Model):
    # uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # upload_date = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(upload_to='pathfinder_app/images/%Y/%m/%d')
    # tag_set = models.ManyToManyField('Tag', blank=True)
    pass


class Tag(models.Model):
    # name = models.CharField(max_length=20)

    # def __str__(self):
        # return self.name
    pass


class Defect(models.Model):
    
    # class Meta:
        # abstract = True
    pass


class Slag(Defect):
    pass


class Porosity(Defect):
    pass


class Others(Defect):
    pass