from django.db.models import (
    Case,
    CharField,
    Count,
    Exists,
    F,
    Func,
    IntegerField,
    OuterRef,
    Max,
    Prefetch,
    Q,
    Subquery,
    Sum,
    When,
    Value,
)
from django.db.models.functions import Coalesce
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from api.models import Product, Tag, PurchaseHistory
from api.serializers import ProductSerializer, TagSerializer


class PurchaseYearSummaryView(GenericAPIView):
    queryset = PurchaseHistory.objects

    def get(self, _: Request, product_id: int, year: int):
        data = self.get_queryset()

        return Response(data=data)

    def get_queryset(self):
        queryset = super(PurchaseYearSummaryView, self).get_queryset()

        return queryset.annotate(
            year=Func(
                F('purchase_date'),
                function='YEAR',
                template="%(function)s(%(expressions)s)",
                output_field=IntegerField(),
            ),
            year_month=Func(
                F('purchase_date'),
                function='DATE_FORMAT',
                template="%(function)s(%(expressions)s, '%%%%Y/%%%%m')",
                output_field=CharField(),
            ),
        ).filter(
            product_id=self.kwargs.get('product_id'),
            year=self.kwargs.get('year'),
        ).annotate(
            total=Sum('price'),
        ).order_by('year_month').values('year_month', 'total')


class PurchasePriceSummaryView(GenericAPIView):
    queryset = PurchaseHistory.objects

    def get(self, _: Request):
        data = self.get_queryset()

        return Response(data=data)

    def get_queryset(self):
        queryset = super(PurchasePriceSummaryView, self).get_queryset()

        return queryset.select_related('product').values('product_id', 'product__name').annotate(
            total=Coalesce(Sum('price'), 0),
        ).order_by('-total')


class ProductCountSummaryView(GenericAPIView):
    queryset = Product.objects

    def get(self, _: Request):
        data = self.get_queryset()

        return Response(data=data)

    def get_queryset(self):
        queryset = super(ProductCountSummaryView, self).get_queryset()

        # Subquery を使ったサブクエリを作成し count の結果を annotate で紐づける
        subquery = PurchaseHistory.objects.filter(
            product_id=OuterRef('pk'),
        ).annotate(
            purchage_count=Count('id')
        ).values('purchage_count')
        subquery.query.set_group_by('product_id')

        queryset = queryset.annotate(
            purchase_count=Coalesce(Subquery(
                subquery,
                output_field=IntegerField(),
            ), 0),
        )

        return queryset.filter(purchase_count__gt=0).values('id', 'name', 'purchase_count')


class ProductListAPIView(ListAPIView):
    queryset = Product.objects
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = super(ProductListAPIView, self).get_queryset()

        # Exists を使ったフィールドを annotate を使ってマッピングする
        queryset = queryset.prefetch_related(
            Prefetch('tags'),
        ).annotate(
            has_tag=Exists(
                Tag.objects.filter(
                    product_id=OuterRef('pk'),
                ).exclude(
                    code='test',
                ).values('id'),  # values は指定したフィールドのみを辞書型で取り出すが、ここでは select するフィールドとして使う
            ),
        ).filter(has_tag=True)

        # When 内に条件と表示する項目を定義する
        # カラムではなく値を利用する場合は Value を使う必要がある
        queryset = queryset.annotate(
            type_name=Case(
                When(
                    type=1,
                    then=Value('食品'),
                ),
                When(
                    type=2,
                    then=Value('衣類'),
                ),
                default=Value('その他'),
                output_field=CharField(),
            ),
        )

        return queryset.order_by('type')


class MaxPriceProductView(GenericAPIView):
    queryset = Product.objects

    def get(self, _: Request):
        data = self.get_queryset()

        return Response(data=data)

    def get_queryset(self):
        queryset = super(MaxPriceProductView, self).get_queryset()

        # 単純な集計なら aggregate が利用できる
        # この場合、戻り値は QuerySet オブジェクトではなくカラム名と値をもった辞書型になる
        # return queryset.aggregate(max_price=Max('price'))

        # カラムを指定した集計の場合 group by を指定する必要があるが、これは QuerySet 経由で行えない
        # QuerySet のプロパティ `query` で設定する必要がある
        queryset = queryset.annotate(max_price=Max('price')).annotate(
            type_name=Case(
                When(
                    type=1,
                    then=Value('食品'),
                ),
                When(
                    type=2,
                    then=Value('衣類'),
                ),
                default=Value('その他'),
                output_field=CharField(),
            ),
        )
        queryset.query.set_group_by('type')

        return queryset.values('type_name', 'max_price').all()


class TagListAPIView(ListAPIView):
    queryset = Tag.objects
    serializer_class = TagSerializer

    def get_queryset(self):
        queryset = super(TagListAPIView, self).get_queryset()

        code = self.request.query_params.get('code')

        if code:
            return queryset.select_related('product').filter(
                Q(code__contains=code) | Q(code__isnull=True),
            )

        return queryset
