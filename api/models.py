from django.db import models
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=50)
    type = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'products'
        verbose_name = '商品'
        verbose_name_plural = '商品'


class Tag(models.Model):
    parent = models.ForeignKey('self', models.PROTECT, blank=True, null=True, related_name='children')
    product = models.ForeignKey('Product', models.PROTECT, related_name='tags')
    code = models.CharField(max_length=30, blank=True, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.code}: {self.name}'

    class Meta:
        db_table = 'tags'
        verbose_name = '商品タグ'
        verbose_name_plural = '商品タグ'


class PurchaseHistory(models.Model):
    product = models.ForeignKey('Product', models.PROTECT, related_name='purchase_histories')
    count = models.IntegerField(default=1)
    price = models.IntegerField()
    purchase_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f'{self.product.name}: {self.count}個'

    class Meta:
        db_table = 'purchase_histories'
        verbose_name = '購入履歴'
        verbose_name_plural = '購入履歴'
