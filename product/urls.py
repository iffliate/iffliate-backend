from django.urls import path

from product.models import Order
from .views import( ProductCreateView, ProductDetailView, OrderCreateView, OrderDetailView,
UserOrderManagemnt,ShopOrderManagement
)
from rest_framework.routers import DefaultRouter



route = DefaultRouter()
route.register('order-user-management',UserOrderManagemnt)
route.register('order-shop-management',ShopOrderManagement)
urlpatterns = [
    path('product/', ProductCreateView.as_view()),
    path('product/<slug:slug>/', ProductDetailView.as_view()),
    path('order/', OrderCreateView.as_view()),
    path('order/<str:orderId>/', OrderDetailView.as_view())
]
urlpatterns += route.urls