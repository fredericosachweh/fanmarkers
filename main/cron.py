from django_cron import cronScheduler, CronJob
from dateutil.relativedelta import relativedelta
from datetime import date
from models import Status
from django.db.models import Q
from settings import PROJECT_PATH

class UpdateHiring(CronJob):
    "Cron Job that goes through every twenve hours and changes all statuses that are older than 30 days"

    # run every (12 hours)
    run_every = 43200
            
    def job(self):
        logfile = open(PROJECT_PATH + 'status_cron.log', 'a')
        
        cutoff_date = date.today() + relativedelta(days=-30)                    #the date of 30 days ago
        
        hiring_old = Status.objects.filter(Q(last_modified__lte=cutoff_date) & (Q(assign_bases__isnull=False) | Q(choice_bases__isnull=False)))
        
        if hiring_old:
            logfile.write(str(date.today()) + " -------------\n")
        
            for status in hiring_old:
                logfile.write(str(status) + "\n")
                status.assign_bases.clear()
                status.choice_bases.clear()
            
            logfile.close()
        else:
            logfile.write(str(date.today()) + " nothing\n")

cronScheduler.register(UpdateHiring)
