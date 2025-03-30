from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from home.views import get_client_collections, get_last_sorted_time, search_collections

def home_redirect():
    return redirect('/auth/login/')

def dashboard(request):
    client_id = request.GET.get("client_id")

    if not client_id:
        return JsonResponse({"error": "Client ID is missing"}, status=400)

    return render(request, 'dashboard.html',  {"client_id": client_id})

def collection_manager(request):
    client_id = request.GET.get("client_id")

    # Debugging: Ensure client_id is present
    if not client_id:
        return HttpResponse("Client ID is missing", status=400)
    
    # Get last sorted time
    last_sorted_time = get_last_sorted_time(request, client_id)

    # Get client collections safely
    client_collections = get_client_collections(request, client_id)

    # Ensure collections is a list, otherwise default to an empty list
    if not isinstance(client_collections, list):
        client_collections = []

    # Convert data into a format suitable for the template
    collections_data = [
        {
            "name": collection.get("name", "Unnamed"),
            "last_sorted": collection.get("last_sorted", "N/A"),
            "product_count": collection.get("product_count", 0),
            "frequency": collection.get("frequency", "N/A"),
            "strategy": collection.get("strategy", "None"),
        }
        for collection in client_collections
    ]

    context = {
        "last_sorted_time": last_sorted_time,
        "collections": collections_data,
    }

    return render(request, "collection-manager.html", context)

def sorting_rules(request):
    client_id = request.GET.get("client_id")

    # Debugging: Ensure client_id is present
    if not client_id:
        return HttpResponse("Client ID is missing", status=400)
    return render(request, 'sorting-rule.html')

def sorting_configuration(request):
    return render(request, 'sorting-configuration.html')

def global_settings(request):
    return render(request, 'global-settings.html')

def billings(request):
    return render(request, 'history.html')

def history(request):
    return render(request, 'history.html')

def faqs(request):
    return render(request, 'faqs.html')
