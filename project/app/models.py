import os

from django.db import models

class TaskState(models.Model):
    """
    Model for task state
    """
    TASK_STARTED = 'S'
    TASK_REVOKED = 'T'
    TASK_PAUSED = 'P'
    TASK_RESUMED = 'R'
    TASK_COMPLETED = 'C'

    STATE_OPTIONS = (
        (TASK_STARTED, 'STARTED'),
        (TASK_REVOKED, 'REVOKED'),
        (TASK_PAUSED, 'PAUSED'),
        (TASK_RESUMED, 'RESUMED'),
        (TASK_COMPLETED, 'COMPLETED')
    )

    task_id = models.UUIDField()
    task_status = models.CharField(
        max_length=1, choices=STATE_OPTIONS, default=STATE_OPTIONS[0][0]
    )

    def __str__(self):
        return f'Task {self.task_id} : {self.get_task_status_display()} '

    class Meta:
        verbose_name = 'Task state'
        verbose_name_plural = 'Task state'


class StudentDetail(models.Model):
    """
    Model for student details
    """
    name = models.CharField(max_length=70)
    address = models.TextField()
    discipline = models.CharField(max_length=100)
    cgpa = models.PositiveSmallIntegerField()
    date_recorded = models.DateField()
    task = models.ForeignKey(
        TaskState, on_delete=models.CASCADE, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Student detail'
        verbose_name_plural = 'Student details'

    