from django_cron import cronScheduler, CronJob
from dateutil.relativedelta import relativedelta
from datetime import date
from models import Status
from django.db.models import Q

class UpdateHiring(CronJob):
    "Cron Job that goes through every twenve hours and changes all statuses that are older than 30 days"

    # run every (12 hours)
    run_every = 30 #43200
            
    def job(self):
        cutoff_date = date.today() + relativedelta(days=-10)                    #the date of 30 days ago
        
        hiring_old = Status.objects.filter(
            Q(last_modified__lte=cutoff_date) & (Q(assign_bases__isnull=False) | Q(choice_bases__isnull=False))
        )
        
        if hiring_old:
            logfile = open(PROJECT_DIR + 'status_cron.log', 'a')
            logfile.write(date.today() + " -------------\n")
        
            for status in hirig_old:
                logfile.write(status + "\n")
            
            hiring_old.update(assign_bases=None, choice_bases=None)
            
            logfile.close()
        else:
            logfile = open(PROJECT_DIR + 'status_cron.log', 'a')
            logfile.write(date.today() + " nothing\n")

cronScheduler.register(UpdateHiring)
