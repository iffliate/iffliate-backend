from django.urls import path

from . import views


urlpatterns = [
 path('process_order_payment/<int:order_id>/', views.InitOrderTran.as_view(),name='process_order_payment'),
 path('webhook/',views.payment_webhook,name='webhook'),
#  path('banks/', views.List_Banks.as_view()),
#  path('bank-list/', views.View_Banks.as_view())
]