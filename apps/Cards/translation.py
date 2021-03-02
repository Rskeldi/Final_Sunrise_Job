from modeltranslation.translator import register, TranslationOptions
from .models import Card, Category


@register(Card)
class CardTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


# @register(Category)
# class CustomerServiceTranslationOptions(TranslationOptions):
#     fields = ('title',)


