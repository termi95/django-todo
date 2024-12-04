from django.http import JsonResponse
from django.shortcuts import render
from .models import TodoItem
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def main(request):
    return render(request, "home.html")


def todomanager(request):
    todos = TodoItem.objects.all()
    return render(request, "todomanager.html", {"todos":todos})

@csrf_exempt
def add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title")
            description = data.get("description", "")
            priority = data.get("priority", "low")
            category = data.get("category", "")

            if not title:
                return JsonResponse({"error": "Title is required."}, status=400)

            todo = TodoItem.objects.create(
                title=title,
                description=description,
                priority={"low": 3, "medium": 2, "high": 1}.get(priority, 3),
                category=category
            )
            
            return JsonResponse({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "priority": priority,
                "category": todo.category,
                "created_at": todo.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)