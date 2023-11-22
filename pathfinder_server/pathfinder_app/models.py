from django.db import models
from django.conf import settings


class RtImage(models.Model):
    uploader    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    image       = models.ImageField(upload_to='pathfinder_app/images/%Y/%m/%d')

    class Meta:
        db_table = 'rt_image'


class AiModel(models.Model):
    rt_image        = models.ForeignKey(RtImage, related_name='ai_model_set',on_delete=models.CASCADE)
    ai_model_name   = models.CharField(null=True, max_length=20)

    class Meta:
        db_table = 'ai_model'


class Expert(models.Model):
    rt_image = models.OneToOneField(RtImage, related_name='expert',on_delete=models.CASCADE)

    class Meta:
        db_table = 'expert'


class BaseDefect(models.Model):
    defect_type = models.CharField(max_length=20)
    xmin        = models.IntegerField()
    ymin        = models.IntegerField()
    xmax        = models.IntegerField()
    ymax        = models.IntegerField()

    class Meta:
        abstract = True


class ExpertDefect(BaseDefect):
    expert = models.ForeignKey(Expert, related_name='expert_defect_set',on_delete=models.CASCADE)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    modified_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'expert_defect'


class AiDefect(BaseDefect):
    ai_model = models.ForeignKey(AiModel, related_name='ai_defect_set',on_delete=models.CASCADE)
    score    = models.FloatField()

    class Meta:
        db_table = 'ai_defect'