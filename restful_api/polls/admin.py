from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    # StackedInline, TabularInline
    model = Choice
    extra = 2  # 默认提供的明细框个数


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

# 注册才会在admin网站显示并管理
admin.site.register(Question, QuestionAdmin)
