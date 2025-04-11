code structure

```
.
└── pearchace/
    ├── home/
    │   ├── __init__.py
    │   ├── apps.py
    │   ├── billing.py 
    │   ├── strategies.py
    │   ├── urls.py
    │   └── views.py
    ├── shopify_app/
    │   ├── __init__.py
    │   ├── api.py
    │   ├── apps.py
    │   ├── context_processors.py
    │   ├── decorators.py
    │   ├── middleware.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── shopify_django_app/
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── mongodb.py
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    ├── nginx/
    │   └── nginx.conf
    ├── .gitignore
    ├── .env
    ├── dockerfile
    ├── manage.py 
    └── pearch.toml

```

code file structure
```
.
├── devpearch/
│   ├── home/
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── billing.py 
│   │   ├── strategies.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── shopify_app/
│   │   ├── __init__.py
│   │   ├── api.py
│   │   ├── apps.py
│   │   ├── context_processors.py
│   │   ├── decorators.py
│   │   ├── middleware.py
│   │   ├── models.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── shopify_django_app/
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── mongodb.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── nginx/
│   │   └── nginx.conf
│   ├── .gitignore
│   ├── .env
│   ├── dockerfile
│   ├── manage.py 
│   └── pearch.toml
└── docker-compose.yml

```



## Things to resolve in the future
- admin api usage  - > sorting order setup before updating products of a collection
<!-- - login/authentication -> To get the access token for a store -->  // DONE
<!-- - Frontend views ready with billing auth logic  --> // Done
- UI FIXUP (HIGH Priority) // needs to be done before 19 april
- logo and color theme (garima)
- Celery server setup // needs to be done before 19 april
- Billing api testing
- elastic search setup if possible for faster fetching and updation
- sentry for issues
- email setup