from django.contrib import admin
from .models import (
    RtImage,
    AiModel,
    Expert,
    ExpertDefect,
    AiDefect,
)

# Register your models here.

@admin.register(RtImage)
class RtImageAdmin(admin.ModelAdmin):
    pass

@admin.register(AiModel)
class AiModelAdmin(admin.ModelAdmin):
    pass

@admin.register(Expert)
class DefectAdmin(admin.ModelAdmin):
    pass

@admin.register(ExpertDefect)
class DefectAdmin(admin.ModelAdmin):
    pass

@admin.register(AiDefect)
class DefectAdmin(admin.ModelAdmin):
    pass