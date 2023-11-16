from django.contrib import admin
from .models import (
    RtImage,
    AiModel,
    Defect,
)

# Register your models here.

@admin.register(RtImage)
class RtImageAdmin(admin.ModelAdmin):
    pass

@admin.register(AiModel)
class AiModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    pass