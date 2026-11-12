import json
from json import JSONDecodeError

from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import redirect, render
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

DEALER_REVIEWS = {
    1: [
        {
            "name": "Upkar Singh",
            "review": "Great customer service and very smooth buying experience. Highly recommend!",
            "car_make": "Audi",
            "car_model": "A4",
            "car_year": 2023,
            "sentiment": "positive",
        }
    ]
}


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


def web_login(request):
    error = ""
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        error = "Username or password is incorrect."

    return render(request, "djangoapp/login.html", {"error": error})


@require_POST
def web_logout(request):
    logout(request)
    return redirect("home")


def dealer_detail(request, dealer_id):
    dealer = next((dealer for dealer in DEALERS if dealer["id"] == dealer_id), None)
    if dealer is None:
        raise Http404("Dealer not found.")
    return render(
        request,
        "djangoapp/dealer_detail.html",
        {"dealer": dealer, "reviews": DEALER_REVIEWS.get(dealer_id, [])},
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
