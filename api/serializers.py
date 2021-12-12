from rest_framework import serializers
from api.models import Product


class ProductSerializer(serializers.ModelSerializer):
    """ 商品 """
    type_name = serializers.CharField()
    tags = serializers.SerializerMethodField()

    def get_tags(self, instance: Product):
        return [t.name for t in instance.tags.all()]

    class Meta:
        model = Product
        fields = ['name', 'type_name', 'price', 'tags']
