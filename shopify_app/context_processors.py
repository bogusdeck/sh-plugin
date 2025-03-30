import shopify

def current_shop(request):
    if not shopify.ShopifyResource.site:
        return {'current_shop': None}
    return {'current_shop': shopify.Shop.current()}

def client_id_processor(request):
    return {"client_id": request.GET.get("client_id", "")}
