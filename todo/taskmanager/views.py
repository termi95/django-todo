from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import TodoItem
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
def main(request):
    return render(request, "home.html")

def redirect_to_home(request, exception):
    return redirect('/todos/home')


def todomanager(request):
    return render(request, "todomanager.html")

def getTaskList(request):
    todos = TodoItem.objects.all()
    return render(request, "todolist.html", {"todos":todos})

def add(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            title = data.get("title")
            description = data.get("description", "")
            priority = data.get("priority", "low")

            if not title:
                return JsonResponse({"error": "Title is required."}, status=400)

            todo = TodoItem.objects.create(
                title=title,
                description=description,
                priority={"low": 3, "medium": 2, "high": 1}.get(priority, 3)
            )
            
            return JsonResponse({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "priority": priority,
                "created_at": todo.created_at.isoformat()
            }, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"error": "Only POST method is allowed."}, status=405)
    
def delete(request, task_id):
    if request.method == "DELETE":
        task = get_object_or_404(TodoItem, id=task_id)
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)