from django.contrib import admin
from sponsorsManager.models import UserProfile
from sponsorsManager.models import Event
from sponsorsManager.models import Needs
from sponsorsManager.models import Sponsors
from sponsorsManager.models import Sponsor_cat
from sponsorsManager.models import Benefit
from sponsorsManager.models import Concession
from sponsorsManager.models import Sponsorship

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Event)
admin.site.register(Needs)
admin.site.register(Sponsors)
admin.site.register(Sponsor_cat)
admin.site.register(Benefit)
admin.site.register(Concession)
admin.site.register(Sponsorship)
