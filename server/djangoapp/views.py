import json
from json import JSONDecodeError

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

DEALERS = [
    {
        "id": 1,
        "city": "El Paso",
        "state": "Texas",
        "address": "384 Lambert Parkway",
        "zip": "79901",
        "short_name": "Classic Motors",
        "full_name": "Classic Motors Dealership Inc",
    },
    {
        "id": 2,
        "city": "Austin",
        "state": "Texas",
        "address": "129 Capital Way",
        "zip": "78701",
        "short_name": "Lone Star Auto",
        "full_name": "Lone Star Auto Group",
    },
    {
        "id": 3,
        "city": "Wichita",
        "state": "Kansas",
        "address": "456 Sunflower St",
        "zip": "67202",
        "short_name": "Jayhawk Motors",
        "full_name": "Jayhawk Car Dealership",
    },
]


def home(request):
    states = sorted({dealer["state"] for dealer in DEALERS})
    selected_state = request.GET.get("state", "")
    dealers = DEALERS

    if selected_state:
        filtered_dealers = [
            dealer for dealer in DEALERS if dealer["state"] == selected_state
        ]
        if filtered_dealers:
            dealers = filtered_dealers
        else:
            selected_state = ""

    return render(
        request,
        "djangoapp/home.html",
        {
            "dealers": dealers,
            "states": states,
            "selected_state": selected_state,
        },
    )


@require_GET
@ensure_csrf_cookie
def csrf_token(request):
    return JsonResponse({"csrfToken": get_token(request)})


@require_POST
def login_user(request):
    try:
        credentials = json.loads(request.body)
    except (JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "Request body must be valid JSON."}, status=400)

    if not isinstance(credentials, dict):
        return JsonResponse({"error": "Request body must be a JSON object."}, status=400)

    username = credentials.get("userName")
    password = credentials.get("password")
    if not isinstance(username, str) or not isinstance(password, str):
        return JsonResponse(
            {"error": "Both userName and password are required."}, status=400
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse({"error": "Invalid username or password."}, status=401)

    login(request, user)
    return JsonResponse(
        {
            "userName": user.get_username(),
            "status": "Authenticated",
            "csrfToken": get_token(request),
        }
    )


@require_POST
def logout_user(request):
    logout(request)
    return JsonResponse({"userName": ""})
