from django.shortcuts import render

# Create your views here.

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer


class TaskDetail(APIView):
    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.title = request.data.get('title', task.title)
            task.description = request.data.get('description', task.description)
            task.completed = request.data.get('completed', task.completed)
            task.save()
            return Response({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            })
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)



class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            task = serializer.save()
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
