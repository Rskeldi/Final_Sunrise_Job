from django.db.models import Q
from django.views.generic import ListView, DetailView, TemplateView

from apps.Cards.models import Card
from apps.Cards.models import Category


class CustomFilter:
    def custom_filter(self, cards):
        try:
            price_from = self.request.GET['from']
            price_to = self.request.GET['to']
            if price_from:
                cards = cards.filter(price__gte=price_from)
            if price_to:
                cards = cards.filter(price__lte=price_to)
            print(price_to, price_to)
            return cards
        except:
            return cards


class IndexView(TemplateView):
    template_name = 'content/index.html'


class CardListView(ListView, CustomFilter):
    model = Card
    template_name = 'content/cards.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = {}
        cards = Card.objects.all()
        context['categories'] = Category.objects.filter(parent=None)
        cards = self.custom_filter(cards)
        context['object_list'] = cards
        return context


class CardDetailView(DetailView):
    model = Card
    template_name = 'content/card_detail.html'


class CategoryListView(ListView):
    model = Category
    template_name = 'content/categories.html'

    def get_queryset(self):
        queryset = Category.objects.filter(parent=None)
        return queryset


class CategoryDetailView(DetailView, CustomFilter):
    model = Category
    template_name = 'content/cards.html'

    def get_context_data(self, **kwargs):
        context = {}
        cards = Card.objects.filter(category=self.object.pk)
        context['categories'] = Category.objects.filter(parent=None)
        context['category_title'] = self.object
        if self.object.children:
            category_list = [self.object.pk]
            for child in Category.objects.filter(parent=self.object.pk):
                category_list.append(child.pk)
                if child.children:
                    for super_child in Category.objects.filter(parent=child.pk):
                        category_list.append(super_child.pk)
            cards = Card.objects.filter(category__in=category_list)
        cards = self.custom_filter(cards)
        context['object_list'] = cards
        return context


class SearchView(ListView, CustomFilter):
    model = Card
    template_name = 'content/cards.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        search = self.request.GET.getlist('search')
        context = {}
        cards = Card.objects.all()
        context['categories'] = Category.objects.filter(parent=None)
        if search and search[0] != '':
            cards = Card.objects.filter(Q(title__icontains=search[0]) |
                                                           Q(description__icontains=search[0]))
        context['filter_not'] = 1
        context['object_list'] = cards
        return context
