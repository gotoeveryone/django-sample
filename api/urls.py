from django.urls import path
from api import views

app_name = 'api'

urlpatterns = [
    path('products', views.ProductListAPIView.as_view()),
    path('summary', views.PurchaseSummaryView.as_view()),
    path('products/max_price', views.MaxPriceProductView.as_view()),
]
