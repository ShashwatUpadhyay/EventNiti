from django.contrib import admin
from .models import *
# Register your models here.

class PollOptionAdmin(admin.StackedInline):
    model = PollOption

class PollQuestionAdmin(admin.ModelAdmin):
    list_display = ['question']
    inlines = [PollOptionAdmin]

admin.site.register(PollQuestion,PollQuestionAdmin)
admin.site.register(PollOption)
admin.site.register(QnaQuestion)
admin.site.register(QnaAnswer)