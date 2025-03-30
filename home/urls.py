from django.urls import path
from . import views
from .billing import create_billing_plan, confirm_billing, purchase_additional_sorts, extra_sort_confirm, handle_app_uninstall


urlpatterns = [
    # header 
    path('', views.index, name='root_path'),
    
    # dashboard 
    path('get-client-info/', views.get_client_info, name="get_client_info"), #
    path('get-graph/', views.get_graph, name='get-graph'),
    path('available-sorts/', views.available_sorts, name='available_sorts'), #
    path('last-active-collections/', views.last_active_collections, name='last_active_collections'), #
    
    # # collection manager
    path('client-last-sorted-time/<int:client_id>/', views.get_last_sorted_time, name='get_last_sorted_time'),#
    path('search-collections/<int:client_id>/', views.search_collections, name='search_collections'),#
    path('client-collections/<int:client_id>/', views.get_client_collections, name='client_collections'), #
    path('sort-now/', views.sort_now, name="sort_now"), #
    path('update-collections/<str:collection_id>/', views.update_collection, name='update_collection'), #
    path('update-collection-settings/', views.update_collection_settings, name='update-collection-settings'), #
    path('fetch-sort-date/', views.fetch_last_sort_date, name='fetch-sort-date'), #
    path('get-products/<str:collection_id>/', views.get_products, name='get-products'), #
    path('update-pinned-products/', views.update_pinned_products, name='update-pinned-products'), # 
    path('update-default-algo/', views.update_default_algo, name='update-default-algo'), # 
    path('collections/<int:collection_id>/tags/', views.get_collection_tags, name='collection-tags'),

    # # global settings
    path('update-global-settings/', views.update_global_settings, name='update-global-settings'), # 
    path('get-and-update-collections/', views.get_and_update_collections, name='get-and-update-collections'), # 
    
    # # Billing urls 
    path('current_subscription_plan/', views.current_subscription_plan, name='current_subscription_plan'),
    path('order-count/', views.fetch_last_month_order_count, name='fetch_last_month_order_count'),
    path('billing/create/', create_billing_plan, name='create_billing_plan'),
    path('billing/confirm/', confirm_billing, name='confirm_billing'),
    path('billing/addon-sorts/', purchase_additional_sorts, name='additional_sorts'),
    path('billing/extra-sort-confirm/', extra_sort_confirm, name='extra_sorts_confirm'),
    path('webhook/app_uninstall/', handle_app_uninstall, name='handle_app_uninstall'), # working in postman not tested yet

    # new apis
    path('preview-products/', views.preview_products, name='preview-products'),
    path('post-quick-config/', views.post_quick_config, name='post-quick-config'),
    path('get-sorting-algorithms/', views.get_sorting_algorithms, name='get-sorting-algorithms'), 
    path('save-client-algorithm/', views.save_client_algorithm, name='save-client-algorithm'),
    path('get-active-collections/', views.get_active_collections, name="get-active-collections"), # post man 
    path('search-products/<str:collection_id>/', views.search_products, name='search-collections'), # no use yet
    path('update-all-algo/<int:algo_id>/', views.update_all_algo, name='update-all-algo'), # 
    path('applied-on-active-collection/', views.applied_on_active_collection, name='applied-on-active-collection'),
    path('sorting-rule/<int:algo_id>/', views.sorting_rule, name='sorting-rule'),
    path('advance-config/', views.advance_config, name='advance-config'),
    path('get-collection-analytics/<int:collection_id>/', views.get_collection_analytics, name='get-collection-analytics'),
]
