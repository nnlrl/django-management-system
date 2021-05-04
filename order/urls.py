from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_view),
    path('add-order/', views.add_order_view),
    path('<int:order_id>/', views.edit_order_view),
    path('order-management/<int:order_id>/', views.order_check_view),
    path('delete/<int:order_id>/', views.order_delete_view),
    path('statistics/', views.order_statistics_view),
    path('statistics/ajax/<str:userid>', views.order_statistics_ajax),
    path('statistics/ajax1/<str:userid>', views.order_statistics_admin_ajax),
]
