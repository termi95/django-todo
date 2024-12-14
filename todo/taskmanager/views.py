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
    todos = TodoItem.objects.filter(is_completed=False).order_by('priority')
    return render(request, "todolist.html", {"todos":todos})

def getTask(request, task_id):
    try:
        todo = TodoItem.objects.get(id=task_id)
    except TodoItem.DoesNotExist:
        return JsonResponse({"error": "TodoItem not found."}, status=404)    
    return JsonResponse({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "priority": todo.priority,
        "is_completed": todo.is_completed
    }, status=200)

@csrf_exempt
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

@csrf_exempt    
def delete(request, task_id):
    if request.method == "DELETE":
        task = get_object_or_404(TodoItem, id=task_id)
        task.delete()
        return JsonResponse({'message': 'Task deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@csrf_exempt
def edit(request, task_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            try:
                todo = TodoItem.objects.get(id=task_id)
            except TodoItem.DoesNotExist:
                return JsonResponse({"error": "TodoItem not found."}, status=404)

            title = data.get("title")
            description = data.get("description")
            priority = data.get("priority", "low")
            is_completed = data.get("is_completed")

            if title:
                todo.title = title
            if description is not None:
                todo.description = description
            if priority in ["low", "medium", "high"]:
                todo.priority = {"low": 3, "medium": 2, "high": 1}.get(priority)                
            if is_completed:
                todo.is_completed = is_completed

            todo.save()
            return JsonResponse({
                "id": todo.id,
                "title": todo.title,
                "description": todo.description,
                "priority": priority,
                "updated_at": todo.updated_at.isoformat(),
                "is_completed": todo.is_completed
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data."}, status=400)
    else:
        return JsonResponse({"error": "Only PUT method is allowed."}, status=405)

@csrf_exempt    
def done(request, task_id):
    if request.method == 'POST':
            try:
                task = TodoItem.objects.get(id=task_id)
                task.is_completed = True
                task.save()

                return JsonResponse({
                    "message": "Task marked as completed",
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_completed": task.is_completed
                    }
                }, status=200)

            except TodoItem.DoesNotExist:
                return JsonResponse({"error": "Task not found"}, status=404)

    return JsonResponse({"error": "Only POST method is allowed"}, status=405)