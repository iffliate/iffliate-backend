from django.urls import path
from .views import ShopCreate, ShopUpdate
urlpatterns=[
    path('shop/', ShopCreate.as_view()),
    path('shop/<slug:slug>/', ShopUpdate.as_view())
]