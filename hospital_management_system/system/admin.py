from django.contrib import admin
from system.models import *

admin.site.register(Doctor)
admin.site.register(LabSpecialist)
admin.site.register(RadiologySpecialist)
admin.site.register(Schedule)
admin.site.register(Appointment)

admin.site.register(Hospital)
admin.site.register(Service)
admin.site.register(Department)
admin.site.register(Room)
admin.site.register(HospitalManager)
admin.site.register(Patient)


