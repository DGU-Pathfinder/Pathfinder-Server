from django.db import models
from django.conf import settings


class RtImage(models.Model):
    uploader    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    image       = models.ImageField(upload_to='pathfinder_app/images/%Y/%m/%d')

    class Meta:
        db_table = 'rt_image'


class AiModel(models.Model):
    rt_image        = models.ForeignKey(RtImage, on_delete=models.CASCADE)
    ai_model_name   = models.CharField(max_length=20)
    score           = models.FloatField()
    expert_check    = models.BooleanField(default=False)

    class Meta:
        db_table = 'ai_model'


class Defect(models.Model):
    ai_model    = models.ForeignKey(AiModel, on_delete=models.CASCADE)
    modifier    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    defect_type = models.CharField(max_length=20)
    xmin        = models.IntegerField()
    ymin        = models.IntegerField()
    xmax        = models.IntegerField()
    ymax        = models.IntegerField()

    class Meta:
        db_table = 'defect'