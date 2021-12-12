from rest_framework import serializers
from api.models import Product, Tag


class ProductSerializer(serializers.ModelSerializer):
    """ 商品 """
    type_name = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, instance: Product):
        return [t.name for t in instance.tags.all()]

    def get_type_name(self, instance: Product):
        return instance.type_name if hasattr(instance, 'type_name') else None

    class Meta:
        model = Product
        fields = ['name', 'type_name', 'price', 'tags']


class TagSerializer(serializers.ModelSerializer):
    """ 商品タグ """
    product_name = serializers.SerializerMethodField()

    def get_product_name(self, instance: Tag):
        return instance.product.name

    class Meta:
        model = Tag
        fields = ['code', 'name', 'product_name']
