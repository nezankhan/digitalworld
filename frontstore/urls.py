from django.urls import path


from . import views
from . views import OrderListView, CustomerCreateView, InventoryListView,EmployeeListView

urlpatterns = [
    path('', views.home,name='home'),

    path('contactsales/',EmployeeListView.as_view(),name='contactsales'),
    path('staff/orders/', OrderListView.as_view(),name='orders'),
    path('staff/inventory/', InventoryListView.as_view(),name='inventory'),
    #path('staff/customerorders/', CustomerOrdersView.as_view(),name='customerorders'),
    path('staff/customerorders/', views.orders_date,name='customerorders'),
    path('staff/customerquery/', views.querycustomer,name='customerquery'),
    path('staff/customer/new', CustomerCreateView.as_view(),name='create-customer'),
    path('staff/home',views.about,name='staffhome'),
    path('staff/stocklevels/', views.stock_level,name='stocklevels'),
    
]


