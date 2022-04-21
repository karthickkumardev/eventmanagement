from django.urls import path
from . import views
urlpatterns = [
path('',views.admin_login,name="admin_login"),
path('admin_logout/',views.admin_logout,name="admin_logout"),
path('dashboard/',views.dashboard,name="dashboard"),
path('add_event/',views.add_event,name="add_event"),
path('events/',views.events,name="events"),
path('add_customer/',views.add_customer,name="add_customer"),
path('customers/',views.customers,name="customers"),
path('delete_customer/<int:pk>/',views.delete_customer,name="delete_customer"),
path('booked_event/',views.booked_event,name="booked_event"),
path('event_details/<str:pk>/',views.event_details,name="event_details"),
path('workers/<str:pk>/<int:cus_id>/',views.workers,name="workers"),
path('add_worker/<str:pk>/<int:cus_id>/',views.add_worker,name="add_worker"),
path('update/<int:pk>/',views.update,name="update"),
path('customer_detail/',views.customer_detail,name="customer_detail"),
path('event_status/<str:pk>/',views.event_status,name="event_status"),
path('report/',views.report,name="report"),
path('single_profit/<str:pk>/',views.single_profit,name="single_profit"),
path('search/',views.search,name="search"),
]