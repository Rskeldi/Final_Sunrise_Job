from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin

from .models import Card, Category


@admin.register(Card)
class CardAdmin(TabbedTranslationAdmin):
    pass


admin.site.register(Category)
