from django.db import models
from django.core.exceptions import ValidationError


SPORT = 'Спорт'
FOOD = 'Їжа'
ELECTRONIC = 'Електроніка'

SHOPS = [
        (SPORT, SPORT),
        (FOOD, FOOD),
        (ELECTRONIC, ELECTRONIC),
    ]


class Shop(models.Model):
    name = models.CharField('Назва', max_length=255)
    description = models.TextField('Опис', blank=True)
    type = models.CharField('Тип', max_length=20, choices=SHOPS)
    latitude = models.DecimalField('Широта', max_digits=9, decimal_places=6)
    longitude = models.DecimalField('Довгота', max_digits=9, decimal_places=6)
    sales_commission = models.DecimalField('Комісія з продажів', max_digits=5,
                                           decimal_places=2, default=0)

    def __str__(self):
        return self.name

    def clean(self):
        if self.sales_commission < 0 or self.sales_commission > 100:
            raise ValidationError('Комісія з продажів повинна бути у межах від 0 до 100.')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазини'


class Category(models.Model):
    allowed_categories = {
        SPORT: ('Зима', 'Літо', 'Футбол'),
        FOOD: ('Випічка', 'Солодощі', 'Алкоголь'),
        ELECTRONIC: ('Ноутбуки', 'Смартфони', 'Навушники'),
    }

    name = models.CharField('Категорія', max_length=255)
    shop = models.CharField('Тип магазину', max_length=20, choices=SHOPS)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()
        if self.shop:
            if self.name not in self.allowed_categories[self.shop]:
                raise ValidationError(f'Для магазину типу "{self.shop}" допустимі лише наступні категорії: '
                                      f'{", ".join(self.allowed_categories[self.shop])}.')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'
        unique_together = ('name', 'shop')


class Product(models.Model):
    name = models.CharField('Назва', max_length=255)
    description = models.TextField('Опис', blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='Магазин')
    categories = models.ManyToManyField(Category, verbose_name='Категорії', blank=True)
    price = models.DecimalField('Ціна (грн)', max_digits=10, decimal_places=2)
    weight = models.DecimalField('Вага', max_digits=10, decimal_places=2, blank=True)
    keywords = models.TextField('Ключові слова', blank=True)

    def __str__(self):
        return self.name

    def clean(self):
        super().clean()

        self.validate_weight()
        self.validate_price()

    def validate_price(self):
        if self.price < 0:
            raise ValidationError('Ціна не може бути від\'ємною.')

    def validate_weight(self):
        if self.weight is not None and self.weight < 0:
            raise ValidationError({'weight': ['Вага товару не може бути від\'ємною.']})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товари'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos')
    photos = models.ImageField(upload_to=f'product_photos/', verbose_name='Фото')

    class Meta:
        verbose_name = 'Фото продукта'
        verbose_name_plural = 'Фото продуктів'



