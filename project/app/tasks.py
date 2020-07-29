from datetime import datetime
import csv
import json
import os
import time

from django.forms.models import model_to_dict

from celery.result import AsyncResult
from celery.exceptions import Ignore

from app.models import StudentDetail, TaskState
from taskmanager import celery_app

@celery_app.task(bind=True)
def handle_file_upload(self, dump):
    """
    Function for handling the file upload in the background
    """
    data_dict = json.loads(dump)
    data_items = data_dict['uploaded_file']
    task = TaskState.objects.create(task_id=self.request.id)

    for i in range(1, len(data_items), 1):
        item = data_items[i].split(',')
        task = TaskState.objects.get(task_id=self.request.id)
        
        if (task.task_status == TaskState.TASK_REVOKED):
            task.delete()
            raise Ignore

        if (task.task_status == TaskState.TASK_STARTED or task.task_status == TaskState.TASK_RESUMED):
            StudentDetail.objects.create(
                name=item[0], address=item[1], discipline=item[2],
                cgpa=item[3], date_recorded=datetime.strptime(item[4][:-2], '%Y-%m-%d').date(),
                task=task
            )
        
        elif (task.task_status == TaskState.TASK_PAUSED):
            counter = 0
            while (task.task_status == TaskState.TASK_PAUSED and counter < 5):
                counter = counter + 1
                time.sleep(60)

            # Revoke the task if user pauses the task
            # for more than 300 seconds
            if (counter == 5):
                task.task_status = TaskState.TASK_REVOKED
                task.save()
            elif (task.task_status == TaskState.TASK_RESUMED):
                StudentDetail.objects.create(
                    name=item[0], address=item[1], discipline=item[2],
                    cgpa=item[3], date_recorded=datetime.strptime(item[4][:-2], '%Y-%m-%d').date(),
                    task=task
                )

    
    #Task completed successfully
    task.task_status = TaskState.TASK_COMPLETED
    task.save()
    return 'File processing complete'

@celery_app.task(bind=True)
def handle_csv_export(self, from_date, to_date):
    """
    Function for handling csv export
    """
    from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date, '%Y-%m-%d').date()

    qs = StudentDetail.objects.filter(
        date_recorded__gte=from_date, date_recorded__lte=to_date
    )
    task = TaskState.objects.create(task_id=self.request.id)
    csvfile = open('../exports/exported_{}.csv'.format(task.task_id), 'w', newline='')
    fieldnames = [field.name for field in StudentDetail._meta.get_fields()]
    
    #Removing the id field which is not required
    fieldnames = fieldnames[1:]
    csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
    csvwriter.writeheader()
    
    for instance in qs:
        task = TaskState.objects.get(task_id=self.request.id)

        if (task.task_status == TaskState.TASK_STARTED or task.task_status == TaskState.TASK_RESUMED):
            instance_dict = model_to_dict(instance)
            del instance_dict['task']
            del instance_dict['id']
            csvwriter.writerow(instance_dict)

        if (task.task_status == TaskState.TASK_REVOKED):
            csvfile.close()
            os.remove('../exports/exported{}.csv'.format(task.task_id))
            raise Ignore
        
        elif (task.task_status == TaskState.TASK_PAUSED):
            counter = 0
            while (task.task_status == TaskState.TASK_PAUSED and counter < 5):
                counter = counter + 1
                time.sleep(60)

            # Revoke the task if user pauses the task
            # for more than 300 seconds
            if (counter == 5):
                task.task_status = TaskState.TASK_REVOKED
                task.save()
            elif (task.task_status == TaskState.TASK_RESUMED):
                instance_dict = model_to_dict(instance)
                del instance_dict['task']
                del instance_dict['id']
                csvwriter.writerow(instance_dict)

    
    csvfile.close()
    return 'File successfully exported'