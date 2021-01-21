from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime 


class Person(models.Model):
    user         = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    birthDay     = models.DateField('Birthday',default=None,null=True)
    phoneNumber  = models.PositiveBigIntegerField(default=0)
    account_type = models.CharField(max_length=20)
    # Abstract Class

class Hospital(models.Model):
    hospital_manager = models.OneToOneField('HospitalManager',on_delete=models.CASCADE,null=True)
    hospital_name = models.CharField(max_length=50)
    def getAvailableRooms(self):
        available_rooms = self.room_set.filter(max_capacity__gt=models.F('current_capacity'))
        return available_rooms.all()




class Service(models.Model):
    hospital      = models.ForeignKey('Hospital',on_delete=models.CASCADE,null=True) 
    service_name  = models.CharField(max_length=50)
    service_price = models.IntegerField(default=0)

class Department(models.Model):
    department_name = models.CharField(max_length=50)
    hospital        = models.ForeignKey('Hospital',on_delete=models.CASCADE,null=True)

class Room(models.Model):
    hospital = models.ForeignKey('Hospital',on_delete=models.CASCADE,null=True)
    is_taken = models.BooleanField(default=False)
    current_capacity = models.IntegerField(default=0)
    max_capacity = models.IntegerField(default=1)

    
class Appointment(models.Model):
    schedule   = models.ForeignKey('Schedule',related_name='appointments',on_delete=models.CASCADE)
    service    = models.OneToOneField('Service',on_delete=models.CASCADE,null=True)
    patient    = models.ForeignKey('Patient',on_delete=models.CASCADE,null=True)
    date       = models.DateField('Appointment Date',default=None)
    staffmember= models.ForeignKey('StaffMember',on_delete=models.CASCADE,null=True)
    startTime  = models.TimeField('start time',default=datetime.time(8,0,0))
    is_booked  = models.BooleanField(default=False)
    is_payed   = models.BooleanField(default=False)
    def get_doctor(self):
        doctor = self.schedule.staffmember
        return doctor
    class Meta:
        ordering = ['startTime']




class MedicalRecord(models.Model):
    doctor_describtion = models.TextField(max_length=1000)
    medical_problems   = models.TextField(max_length=1000)
    patient            = models.ForeignKey('Patient',on_delete=models.CASCADE,null=True)


class Schedule(models.Model):
    last_modified = models.DateField("schedule day",auto_now=True)
    start_time    = models.TimeField('',default=datetime.time(8,0,0))
    end_time      = models.TimeField('',default=datetime.time(2,0,0))
    
    def get_appointments(self,date=timezone.now(),booked=True):
        if self.appointments.count() == 0:
            for i in range(8):
                self.appointments.create(date=date,startTime=datetime.time(self.start_time.hour+i,0,0),staffmember=self.staffmember)
                self.appointments.create(date=date,startTime=datetime.time(self.start_time.hour+i,30,0),staffmember=self.staffmember)
            self.save()
        appointments = self.appointments.filter(date=date,is_booked=booked)
        return appointments

class Patient(Person):
    height = models.IntegerField(default=0)
    weight = models.FloatField(default=0)







class StaffMember(Person):
    salary         = models.IntegerField(default=0)
    schedule       = models.OneToOneField('Schedule', on_delete=models.CASCADE,null=True)
    department     = models.ForeignKey('Department', on_delete=models.CASCADE,null=True)
    patients       = models.ManyToManyField(Patient)
    # Abstract class

class HospitalManager(StaffMember):
    pass


class Doctor(StaffMember):
    pass

class FinanceEmployee(StaffMember):
    pass


class EmergencyEmployee(StaffMember):
    pass


class FrontdeskEmployee(StaffMember):
    pass

class FeedBack(models.Model):
    feedback = models.TextField(max_length=1000)
    staff_member = models.ForeignKey('StaffMember',on_delete=models.CASCADE)
    patient = models.ForeignKey('Patient',on_delete=models.CASCADE)


class RadiologySpecialist(StaffMember):
    pass

class LabSpecialist(StaffMember):
    pass
