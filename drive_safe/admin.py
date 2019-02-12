from django.contrib import admin
from drive_safe.models import Advice, Tags, TestQuestions

# Register your models here.
# admin.site.register(Advice)
admin.site.register(Tags)
admin.site.register(TestQuestions)


class TestQuestionsInline(admin.StackedInline):
    model = TestQuestions


class AdviceAdmin(admin.ModelAdmin):
    inlines = [
        TestQuestionsInline,
    ]
    exclude = ('passed_by', 'likes')


admin.site.register(Advice, AdviceAdmin)
