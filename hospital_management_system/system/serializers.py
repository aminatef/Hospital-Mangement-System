from rest_framework import serializers
from system.models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','first_name', 'last_name', 'email']
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'department_name']  

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'hospital', 'service_name', 'service_price']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        depth=2
        fields = ['id','last_modified','appointments','start_time', 'end_time']    

class AppointmentSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    class Meta:
        model = Appointment
        fields = ['id', 'service', 'staffmember','patient','date','startTime','is_booked','is_payed']

class PatientSerializer(serializers.ModelSerializer):
    user  = UserSerializer()
    class Meta:
        model = Patient
        read_only_fields = ['user']
        fields = ['id', 'user', 'weight', 'height','account_type','birthDay','phoneNumber']  

 

class DoctorSerializer(serializers.ModelSerializer):
    #schedule = ScheduleSerializer()
    user     = UserSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = Doctor
        read_only_fields = ['user','department']
        fields = ['id', 'user', 'salary', 'account_type','department','birthDay','phoneNumber']  

class MedicalRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalRecord
        fields = ['id', 'doctor_describtion', 'medical_problems','patient']  


class RadiologySpecialistSerializer(serializers.ModelSerializer):
    #schedule = ScheduleSerializer()
    user     = UserSerializer()
    class Meta:
        model = RadiologySpecialist
        read_only_fields = ['user','department']
        fields = ['id', 'user', 'salary', 'account_type','department','birthDay','phoneNumber']  


class LabSpecialistSerializer(serializers.ModelSerializer):
    #schedule = ScheduleSerializer()
    user     = UserSerializer()
    class Meta:
        model = LabSpecialist
        read_only_fields = ['user','department']
        fields = ['id', 'user', 'salary','account_type','department','birthDay','phoneNumber']  

class EmergencyEmployeeSerializer(serializers.ModelSerializer):
    user     = UserSerializer()
    class Meta:
        model = EmergencyEmployee
        read_only_fields = ['user']
        fields = ['id', 'user', 'salary','account_type','birthDay','phoneNumber']  

class FinanceEmployeeSerializer(serializers.ModelSerializer):
    user     = UserSerializer()
    class Meta:
        model = FinanceEmployee
        read_only_fields = ['user']
        fields = ['id', 'user', 'account_type','salary','birthDay','phoneNumber']  

class FrontdeskEmployeeSerializer(serializers.ModelSerializer):
    user     = UserSerializer()
    class Meta:
        model = FrontdeskEmployee
        read_only_fields = ['user']
        fields = ['id', 'user', 'account_type','salary','birthDay','phoneNumber']  

class HospitalManagerSerializer(serializers.ModelSerializer):
    user     = UserSerializer()
    class Meta:
        model = HospitalManager
        read_only_fields = ['user']
        fields = ['id', 'user', 'account_type','salary','birthDay','phoneNumber']  

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        depth = 1
        fields = ['id', 'hospital_name', 'service_set','department_set']  


class StaffMemberSerializer(serializers.ModelSerializer):
    schedule = ScheduleSerializer()
    class Meta:
        model = StaffMember
        depth = 2
        fields = ['id','schedule'] 
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model=Room
        fields = ['hospital', 'is_taken', 'current_capacity', 'max_capacity']

class salarySerializer(serializers.ModelSerializer):
    user       = UserSerializer()
    department = DepartmentSerializer()
    class Meta:
        model = StaffMember
        depth = 1
        fields = ['id','salary','user','department'] 

class FeedBackSerializer(serializers.ModelSerializer):
    staff_member = StaffMemberSerializer()
    class Meta:
        model = FeedBack
        fields = ['id','feedback','staff_member','patient']
class statisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id','height','weight']


        







