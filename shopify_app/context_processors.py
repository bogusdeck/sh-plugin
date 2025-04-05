import shopify

def current_shop(request):
    if not shopify.ShopifyResource.site:
        return {'current_shop': None}
    return {'current_shop': shopify.Shop.current()}

def client_id_processor(request):
    return {"client_id": request.GET.get("client_id", "")}

from django.shortcuts import redirect, render
from .models import Subscription, Client

def subscription_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        shop_url = request.session.get("shopify", {}).get("shop_url")
        if not shop_url:
            return render(request, "shopify_login_required.html")  

        client = Client.objects.get(shop_url=shop_url)

        if not client.member:
            return redirect("billing_page")

        return view_func(request, *args, **kwargs)
    return _wrapped_view