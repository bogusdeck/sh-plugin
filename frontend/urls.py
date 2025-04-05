from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('collections/', views.collection_manager, name='collection_manager'),
    path('sorting/', views.sorting_configuration, name="sorting_config"),
    path('rules/', views.sorting_rules, name='sorting_rules'),
    path('settings/', views.global_settings, name="global_settings"),
    path('billing/', views.billings, name="billing"),
    path('history/', views.history, name="history"),
    path('faqs', views.faqs,  name="faqs"),
    path('billing_page', views.billing_page, name="billing_page"),
]
