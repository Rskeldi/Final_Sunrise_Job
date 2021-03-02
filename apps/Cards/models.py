from django.db import models


class Category(models.Model):
    title = models.CharField('Название категории', max_length=150, unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True,
                               related_name='children', verbose_name='Надкатегория')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        if self.parent:
            return f'{self.parent} ➔ {self.title}'
        return self.title


class Card(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField("Описание", max_length=350)
    price = models.IntegerField("Цена")
    image = models.ImageField('Изображение', upload_to='card_images/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = 'Карточка'
        verbose_name_plural = 'Карточки'

    def __str__(self):
        return self.title



