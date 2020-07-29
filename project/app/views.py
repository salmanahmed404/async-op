from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from celery.app.task import Task

from app.models import TaskState
from app.serializers import FileSerializer
from app.tasks import handle_csv_export, handle_file_upload


import pdb

@api_view(http_method_names=['GET'])
def revoke(request, task_id):
    """
    View for revoking file upload
    """
    try:
        task = TaskState.objects.get(task_id=task_id)
        task.task_status = TaskState.TASK_REVOKED
        task.save()
        response_dict = {
            'task_id': task_id,
            'state': task.get_task_status_display(),
            'message': 'Task stopped'
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    except TaskState.DoesNotExist:
        response_dict = {
            'message': 'Task not found'
        }
        return Response(response_dict, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=['GET'])
def pause(request, task_id):
    """
    View for pausing file upload
    """
    try:
        task = TaskState.objects.get(task_id=task_id)
        task.task_status = TaskState.TASK_PAUSED
        task.save()
        response_dict = {
            'task_id': task_id,
            'state': task.get_task_status_display(),
            'message': 'Task paused'
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    except TaskState.DoesNotExist:
        response_dict = {
            'message': 'Task not found'
        }
        return Response(response_dict, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=['GET'])
def resume(request, task_id):
    """
    View for resuming a paused file upload
    """
    try:
        task = TaskState.objects.get(task_id=task_id)
        task.task_status = TaskState.TASK_RESUMED
        task.save()
        response_dict = {
            'task_id': task_id,
            'state': task.get_task_status_display(),
            'message': 'Task resumed'
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    except TaskState.DoesNotExist:
        response_dict = {
            'message': 'Task not found'
        }
        return Response(response_dict, status=status.HTTP_404_NOT_FOUND)

@api_view(http_method_names=['GET'])
def csv_export(request):
    """
    View for csv export
    """
    from_date = request.GET.get('from_date', None)
    to_date = request.GET.get('to_date', None)
    if (from_date and to_date):
        task = handle_csv_export.delay(from_date=from_date, to_date=to_date)
        response_dict = {
            'task_id': task.task_id,
            'message': 'File export started'
        }
        return Response(response_dict, status=status.HTTP_200_OK)
    else:
        response_dict = {
            'message': 'Enter from_date and to_date query params for filtering'
        }
        return Response(response_dict, status=status.HTTP_400_BAD_REQUEST)

class FileUploadView(GenericAPIView):
    """
    View for csv file upload
    """
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        serializer = FileSerializer(data=request.FILES)
        if serializer.is_valid():
            data = JSONRenderer().render(serializer._validated_data)
            task = handle_file_upload.delay(dump=data.decode('utf-8'))
            response_dict = {
                'task_id': task.task_id,
                'message': 'Uploaded file being processed'
            }
            return Response(response_dict, status=status.HTTP_200_OK)
        else:
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
 