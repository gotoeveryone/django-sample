from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('products', views.ProductListAPIView.as_view()),
    path('products/summary', views.ProductCountSummaryView.as_view()),
    path('products/max_price', views.MaxPriceProductView.as_view()),
    path('tags', views.TagListAPIView.as_view()),
    path('purchases/summary', views.PurchasePriceSummaryView.as_view()),
    path('purchases/summary/<int:product_id>/<int:year>', views.PurchaseYearSummaryView.as_view()),
]
