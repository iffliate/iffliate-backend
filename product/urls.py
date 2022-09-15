from django.urls import path

from product.models import Order
from .views import ProductCreateView, ProductDetailView, OrderCreateView, OrderDetailView

urlpatterns = [
    path('product/', ProductCreateView.as_view()),
    path('product/<slug:slug>/', ProductDetailView.as_view()),
    path('order/', OrderCreateView.as_view()),
    path('order/<str:orderId>/', OrderDetailView.as_view())
]
