from django.shortcuts import render

def dashboard(request):
    return render(request, 'frontend/dashboard.html')

def collection_manager(request):
    return render(request, 'frontend/collection-manager.html')
