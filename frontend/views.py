from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from home.views import get_client_collections, get_last_sorted_time, search_collections
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render 
from django.contrib import messages
import random
from datetime import datetime, timedelta
from datetime import datetime, date
from django.core.paginator import Paginator
from django.utils.timezone import localtime
import logging

from .forms import GlobalSettingsForm
from shopify_app.models import Client, Usage, Subscription, SortingPlan, ClientCollections, ClientAlgo, History, FAQS
from shopify_app.api import fetch_order_for_billing
from shopify_app.context_processors import subscription_required

logger = logging.getLogger(__name__)


def home_redirect():
    return redirect('/auth/login/')

def get_shopify_client(request):
    """Retrieve the Shopify client details from session data."""

    shop_data = request.session.get("shopify", {})
    shop_url = shop_data.get("shop_url")

    if not shop_url:
        return None, JsonResponse({"error": "User data missing"}, status=400)

    try:
        client = Client.objects.get(shop_url=shop_url)
        return client, None  # Return client and no error

    except Client.DoesNotExist:
        return None, JsonResponse({"error": "User not found in database"}, status=400)

@subscription_required
def dashboard(request):
    """Render the dashboard page with client and collection data."""

    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response  # Return error if client not found

    shop_id = client.shop_id
    shop_name = client.shop_name
    subscription_status = client.member

    try:
        # Fetch usage and subscription details
        usage = Usage.objects.get(shop_id=shop_id)
        subscription = Subscription.objects.get(subscription_id=usage.subscription_id)
        sorting_plan = SortingPlan.objects.get(plan_id=subscription.plan_id)

        sort_limit = sorting_plan.sort_limit + usage.addon_sorts_count
        available_sorts = sort_limit - usage.sorts_count

    except Usage.DoesNotExist:
        logger.warning(f"Usage data missing for client {client.shop_url}")
        available_sorts = None
    except Subscription.DoesNotExist:
        logger.warning(f"Subscription missing for client {client.shop_url}")
        available_sorts = None
    except SortingPlan.DoesNotExist:
        logger.warning(f"Sorting Plan missing for client {client.shop_url}")
        available_sorts = None
    except Exception as e:
        logger.exception("Unexpected error in fetching subscription data")
        return JsonResponse({"error": "Something went wrong while fetching data"}, status=500)

    try:
        # Fetch last active collections
        collections = (
            ClientCollections.objects.filter(shop_id=shop_id, status=True)
            .order_by("-sort_date")[:5]
            .select_related("algo")
        )

        collections_data = [
            {
                "collection_id": collection.collection_id,
                "collection_name": collection.collection_name,
                "product_count": collection.products_count,
                "sort_date": collection.sort_date,
                "algo_name": collection.algo.algo_name,
            }
            for collection in collections
        ]

    except Exception as e:
        logger.exception("Error fetching collections")
        collections_data = []

    return render(
        request,
        "dashboard.html",
        {
            "shop_name": shop_name,
            "shop_url": client.shop_url,
            "subscription_status": subscription_status,
            "available_sorts": available_sorts,
            "collections": collections_data,
        },
    )

@subscription_required
def collection_manager(request):
    """Render the collection manager page."""

    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response  # Return error if client not found

    shop_id = client.shop_id

    try:
        last_sorted_time = get_last_sorted_time(request, shop_id)
    except Exception as e:
        logger.exception(f"Error fetching last sorted time for shop_id {shop_id}")
        last_sorted_time = "N/A"

    try:
        client_collections = get_client_collections(request, shop_id) or []

        # Ensure it's a list
        if not isinstance(client_collections, list):
            logger.warning(f"client_collections is not a list, received: {type(client_collections)}")
            client_collections = []

    except Exception as e:
        logger.exception(f"Error fetching client collections for shop_id {shop_id}")
        client_collections = []

    collections_data = []
    for collection in client_collections:
        if isinstance(collection, dict):  
            collections_data.append({
                "name": collection.get("name", "Unnamed"),
                "last_sorted": collection.get("last_sorted", "N/A"),
                "product_count": collection.get("product_count", 0),
                "frequency": collection.get("frequency", "N/A"),
                "strategy": collection.get("strategy", "None"),
            })
        else:
            logger.warning(f"Unexpected collection format: {collection}")

    # If no collections exist, set a flag
    no_collections = len(collections_data) == 0

    context = {
        "last_sorted_time": last_sorted_time,
        "collections": collections_data,
        "no_collections": no_collections,  # Pass flag to template
    }

    return render(request, "collection-manager.html", context)

@subscription_required
def sorting_rules(request):
    # Get the Shopify client
    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response  # Return error if client not found

    shop_id = client.shop_id

    # Fetch sorting algorithms
    try:
        primary_algorithms = ClientAlgo.objects.filter(is_primary=True)
        client_algorithms = ClientAlgo.objects.filter(shop_id=client)
        default_algo = client.default_algo
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

    return render(request, "sorting-rule.html", {
        "default_algo": default_algo,
        "primary_algorithms": primary_algorithms,
        "client_algorithms": client_algorithms
    })

@subscription_required
def sorting_configuration(request):
    return render(request, 'sorting-configuration.html')

@subscription_required
def global_settings(request):
    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response  

    if request.method == 'POST':
        form = GlobalSettingsForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data

            # Update client fields
            client.schedule_frequency = data['schedule_frequency']
            client.stock_location = data['stock_location']
            client.lookback_period = data['lookback_period']

            if data['schedule_frequency'] == 'custom':
                client.custom_start_time = datetime.combine(date.today(), data['custom_start_time'])
                client.custom_stop_time = datetime.combine(date.today(), data['custom_stop_time'])
                client.custom_frequency_in_hours = data['custom_frequency_in_hours']
            else:
                client.custom_start_time = None
                client.custom_stop_time = None
                client.custom_frequency_in_hours = None

            client.save()
            messages.success(request, 'Settings updated successfully!')
            return redirect('global_settings')
    else:
        # Pre-fill form with existing values
        form = GlobalSettingsForm(initial={
            'schedule_frequency': client.schedule_frequency,
            'custom_start_time': client.custom_start_time.time() if client.custom_start_time else None,
            'custom_stop_time': client.custom_stop_time.time() if client.custom_stop_time else None,
            'custom_frequency_in_hours': client.custom_frequency_in_hours,
            'stock_location': client.stock_location,
            'lookback_period': client.lookback_period,
        })

    return render(request, 'global-settings.html', {'form': form})

@subscription_required
def billings(request):
    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response

    try:
        shop_url = client.shop_url
        shop_id = client.shop_id

        # Get last month range
        today = datetime.today()
        first_day_last_month = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - timedelta(days=1)

        # Fetch order count for last month
        order_count = fetch_order_for_billing(shop_url, first_day_last_month, last_day_last_month)
        logger.debug("order_count : ",order_count)
        # Get client
        client = Client.objects.get(shop_url=shop_url)

        # Get usage and subscription
        usage = Usage.objects.get(shop_id=client.shop_id)
        subscription = Subscription.objects.get(subscription_id=usage.subscription_id)
        sorting_plan = SortingPlan.objects.get(plan_id=subscription.plan_id)

        # Calculate sorts
        sort_limit = sorting_plan.sort_limit
        available_sorts = sort_limit - usage.sorts_count

        current_subscription = {
            'plan_name': subscription.plan.name,
            'billing_cycle': "Annual" if subscription.is_annual else "Monthly",
            'current_period_start': subscription.current_period_start,
            'next_billing_date': subscription.next_billing_date,
            'sort_remaining': available_sorts,
            'total_sorts': sort_limit,
            'extra_sort': usage.addon_sorts_count,
            'order_count': order_count,
        }

        # Fetch all sorting plans for this shop
        subscription_plans = SortingPlan.objects.all().order_by('plan_id')
        logger.debug("subscription_plan :",subscription_plans)
        return render(request, 'billing.html', {
            "current_subscription": current_subscription,
            "subscription_plans": subscription_plans
        })

    except Exception as e:
        return render(request, 'billing.html', {
            "error": str(e),
            "current_subscription": None,
            "subscription_plans": []
        })

@subscription_required
def history(request):
    client, error_response = get_shopify_client(request)
    
    if error_response:
        return error_response  
    
    shop_id = client.shop_id
    logs = History.objects.filter(shop_id=shop_id).order_by('-requested_at')
    
    paginator = Paginator(logs, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    for idx, log in enumerate(page_obj, start=1 + (page_obj.number - 1) * paginator.per_page):
        log.sr_no = idx
        log.request_at = localtime(log.requested_at).strftime("%Y-%m-%d %H:%M:%S")
        log.started_at = localtime(log.started_at).strftime("%Y-%m-%d %H:%M:%S") if log.started_at else "N/A"
        log.ended_at = localtime(log.ended_at).strftime("%Y-%m-%d %H:%M:%S") if log.ended_at else "N/A"
        log.product_sorted = log.product_count
        log.status = log.status.capitalize()

    return render(request, 'history.html', {"page_obj": page_obj})

@subscription_required
def faqs(request):
    faqs = FAQS.objects.all().order_by('id')
    return render(request, 'faqs.html', {"faqs": faqs})

def billing_page(request):
    client, error_response = get_shopify_client(request)
    if error_response:
        return error_response  # Return error if client not found

    if client.member:
        return redirect('dashboard')

    plans = SortingPlan.objects.all().order_by("plan_id")
    return render(request, "billing_plans.html", {"plans": plans})