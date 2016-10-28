from celery.task.schedules import crontab
from  celery.decorators import periodic_task
from  . import scrapers
from celery.utils.log import get_task_logger
from datetime import datetime

logger = get_task_logger(__name__)

@periodic_task(run_every=(crontab(hour="*", minute="*", day_of_week="*")))
def loan():
	logger.info("Start task")
	now = datetime.now()
	result = scrapers.scraper_example(now.day, now.minute)
	logger.info("Task finished: result = %i" % result)