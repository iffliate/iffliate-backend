from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


route = DefaultRouter()

route.register('handle_shop_payment',views.HandleShopPaymentView,basename='handle_shop_payment')

urlpatterns = [
 path('process_order_payment/<int:order_id>/', views.InitOrderTran.as_view(),name='process_order_payment'),
 path('webhook/',views.payment_webhook,name='webhook'),
#  path('banks/', views.List_Banks.as_view()),
#  path('bank-list/', views.View_Banks.as_view())
] + route.urls