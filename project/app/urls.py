from django.urls import path

from app.views import (
    csv_export, FileUploadView, pause, resume, revoke
)

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='file-upload'),
    path('revoke/<str:task_id>/', revoke, name='revoke'),
    path('pause/<str:task_id>/', pause, name='pause'),
    path('resume/<str:task_id>/', resume, name='resume'),
    path('export/', csv_export, name='export')
]
