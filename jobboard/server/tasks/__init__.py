from celery.schedules import crontab
from server.utils.celery import celery


# Ensure Celery auto-discovers tasks
celery.autodiscover_tasks()

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Aggregates all cron jobs for the Celery worker.

    Args:
        sender (_type_): Celery object manager.
    """
    # # Add periodic task to run `pull_data_into_elastic` every day at 00:00 UTC
    # sender.add_periodic_task(
    #     crontab(hour=0, minute=0),  # This sets the schedule to run at 00:00 UTC every day
    #     pull_data_into_elastic.s(),  # Task to be scheduled
    #     name='Pull data into Elastic at midnight'
    # )

