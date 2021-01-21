from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import RequestsClient
from system.models import *
from random import random
from math import floor
from rest_framework.test import APIRequestFactory
from system.views import *
from rest_framework.test import APIClient
# Create your tests here.
class API_TEST(TestCase):
	def setUp(self):
		user = User.objects.create_user(username="HospitalManager",password="password")
		manager = HospitalManager.objects.create(account_type="HospitalManager",user=user)
		hospital = Hospital.objects.create(hospital_manager=manager,hospital_name="masr")

		dep =[ Department.objects.create(hospital=hospital,department_name="Cardiology"),
			Department.objects.create(hospital=hospital,department_name="Diagnostic imaging"),
			Department.objects.create(hospital=hospital,department_name="Ear nose and throat"),
			Department.objects.create(hospital=hospital,department_name="General surgery"),
			Department.objects.create(hospital=hospital,department_name="Microbiology"),
			Department.objects.create(hospital=hospital,department_name="Neurology")]

		ser1 = Service.objects.create(hospital=hospital,service_name="book doctor appointment",service_price=100)
		ser2 = Service.objects.create(hospital=hospital,service_name="book lab test",service_price=100)
		ser3 = Service.objects.create(hospital=hospital,service_name="book radiology test",service_price=100)

		for i in range(5):
			Room.objects.create(hospital=hospital)

		user = User.objects.create_user(username="FinanceEmployee",password="password")
		FinanceEmployee.objects.create(user=user,account_type="FinanceEmployee")

		user = User.objects.create_user(username="EmergencyEmployee",password="password")
		EmergencyEmployee.objects.create(user=user,account_type="EmergencyEmployee")

		user = User.objects.create_user(username="FrontdeskEmployee",password="password")
		FrontdeskEmployee.objects.create(user=user,account_type="FrontdeskEmployee")

		for i in range(2):
			username='DOC'+str(i)+'_TEST'+str(i)
			user = User.objects.create_user(username=username,password=username+'password')
			user.first_name='First'+str(i)
			user.last_name='last'+str(i)
			user.email = 'example@gmail.com'
			sch = Schedule()
			sch.save()
			doc = Doctor(department=dep[i],user=user,
							  birthDay=timezone.now(),phoneNumber=00,schedule=sch,salary=1000,account_type="Doctor")
			doc.save()
			doc.schedule.get_appointments(booked=False)
			doc.save()
			user.save()

		username=['TEST1','TEST122','TEST11','TEST22','TEST44']
		for i in range(2):
			user = User.objects.create_user(username=username[i],password=username[i])
			patient = Patient(height=160,weight=70,user=user,
							  birthDay=timezone.now(),phoneNumber=00,account_type="Patient")
			patient.save()
			patient.staffmember_set.add(Doctor.objects.get(user__username__startswith="DOC"+str(i)))
			FeedBack(staff_member=Doctor.objects.get(user__username__startswith="DOC"+str(i)),feedback ="ffffeeeeddddback")
			med=MedicalRecord(patient=patient,doctor_describtion="describtion",medical_problems="problems")
			med.save()
			user.save()
			patient.save()

		for i in range(2):
			username='LAB'+str(i)+'_TEST'+str(i)
			user = User.objects.create_user(username=username,password=username+'password')
			user.first_name='First'+str(i)
			user.last_name='last'+str(i)
			user.email = 'example@gmail.com'
			sch = Schedule()
			sch.save()
			lab = LabSpecialist(user=user,
							  birthDay=timezone.now(),phoneNumber=00,schedule=sch,salary=1000,account_type="LabSpecialist")
			lab.save()
			lab.schedule.get_appointments(booked=False)
			lab.save()
		for i in range(2):
			username='Radio'+str(i)+'_TEST'+str(i)
			user = User.objects.create_user(username=username,password=username+'password')
			user.first_name='First'+str(i)
			user.last_name='last'+str(i)
			user.email = 'example@gmail.com'
			sch = Schedule()
			sch.save()
			radio = RadiologySpecialist(user=user,
							  birthDay=timezone.now(),phoneNumber=00,schedule=sch,salary=1000,account_type="RadiologySpecialist")
			radio.save()
			radio.schedule.get_appointments(booked=False)
			radio.save()

	#'API/doctors/<str:dep>'
	def test_doctor_list(self):
		factory = APIRequestFactory(enforce_csrf_checks=True)
		request = factory.get('API/doctors/')
		dep = Department.objects.all().first()
		response = doctor_list(request,dep)
		self.assertEqual(response.status_code,200)

	#'API/patient/register'
	def test_register_view(self):
		factory = APIRequestFactory(enforce_csrf_checks=True)
		data = {
				 "username":"TEST33444" ,
				 "password1":"TEST33" ,
				 "password2":"TEST33" ,
				 "weight":80 ,
				 "height":175 , 
				 "birthday":None,
				 "phoneNumber":65 ,
				 "first_name":"test" ,
				 "last_name":"test"
				}
		request = factory.post('/API/patient/register/', data,format='json')
		response = register_view(request)
		self.assertEqual(response.status_code,201)
		user = User.objects.get(username="TEST33444")
		request = factory.post('/API/patient/register/', data,format='json')
		response = register_view(request)
		self.assertEqual(response.status_code,406)
		data = {
				 "username":"TEST1111" ,
				 "password1":"4" ,
				 "password2":"TEST33" ,
				 "weight":80 ,
				 "height":175 , 
				 "phoneNumber":65 ,
				 "first_name":"test" ,
				 "last_name":"test"
				}
		request = factory.post('/API/patient/register/', data,format='json')
		response = register_view(request)
		self.assertEqual(response.status_code,406)

   # 'API/patient/reports'

	def test_reports_view(self):
		user = Patient.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/patient/reports')
		self.assertEqual(response.status_code,200)






		
	# #'/API/patient/reports/add'
	def test_add_report_view(self):
		user = Patient.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.post('/API/patient/reports/add')
		self.assertEqual(response.status_code,406)

		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = Patient.objects.all().first().id
		data = {
				"patient":pk,
				"doctor_describtion":"test","medical_problems":"test"}

		response = client.post('/API/patient/reports/add',data=data,format="json")
		self.assertEqual(response.status_code,201)
		
	# #'API/patient/reports/edit'
	def test_edit_report_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = Patient.objects.all().first().id
		iD = MedicalRecord.objects.all().first().pk 
		data = {
				"id":iD,
				"patient":pk,
				"doctor_describtion":"test",
				"medical_problems":"test"
				}

		response = client.post('/API/patient/reports/edit',data=data,format="json")
		self.assertEqual(response.status_code,201)
		data = {
				"id":iD,
				"patient":pk,
				"medical_problems":"test"
				}

		response = client.post('/API/patient/reports/edit',data=data,format="json")
		self.assertEqual(response.status_code,201)

		
	# #'API/patient/reports/delete'
	def test_delete_report_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		iD = MedicalRecord.objects.all().first().pk 
		data = {
				"id":iD,
				}
		response = client.post('/API/patient/reports/delete',data=data,format="json")
		self.assertEqual(response.status_code,200)

	#'API/patient/appointments'
	def test_appointments_view(self):
		patient = Patient.objects.all().first()
		user = patient.user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/patient/appointments',format="json")
		self.assertEqual(response.status_code,200)
		


	#'API/patient/appointments/book'
	def test_book_appointment_view(self):
		patient = Patient.objects.all().first()
		user = patient.user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = Appointment.objects.all().first().pk
		data = {"id":pk}
		response = client.post('/API/patient/appointments/book',data=data,format="json")
		self.assertEqual(response.status_code,200)





	# #'API/patient/appointments/edit'
	def test_edit_appointment_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = Appointment.objects.all().first().pk
		data = {
			   "id": pk,
			   "is_booked": True,
			   "is_payed": True
			   }
		response = client.post('/API/patient/appointments/edit',data=data,format="json")
		self.assertEqual(response.status_code,201)



	# #'API/patient/appointments/delete'
	def test_delete_appointment_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = Appointment.objects.all().first().pk
		data = {
			   "id": pk,
			   }
		response = client.post('/API/patient/appointments/delete',data=data,format="json")
		self.assertEqual(response.status_code,200)

		

	

	#'API/hospital'
	def test_Hospital_view(self):
		client = APIClient()
		response = client.get('/API/hospital',format="json")
		self.assertEqual(response.status_code,200)
		

	# #'API/employees'
	def test_show_employees_view(self):
		user = HospitalManager.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employees',format="json")
		self.assertEqual(response.status_code,201)


	#'API/employee/schedule'
	def test_schedule_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		pk = user.pk
		data = {
			   "id": pk,
			   }
		response = client.post('/API/employee/schedule',data=data,format="json")
		self.assertEqual(response.status_code,200)

		




	#'API/user/information/view'
	def test_show_user_information_view(self):

		user = Patient.objects.all().first().user
		print(user.person.account_type)
		client = APIClient()
	
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = Doctor.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = RadiologySpecialist.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)
		

		user = LabSpecialist.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = FinanceEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = EmergencyEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = FrontdeskEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)

		user = HospitalManager.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.get('/API/user/information/view')
		self.assertEqual(response.status_code,200)


		



	#'/API/user/information/edit'
	def test_edit_user_information_view(self):
		user = Patient.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		data ={"phoneNumber":12}

		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = Doctor.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = RadiologySpecialist.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)
		
		user = LabSpecialist.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = FinanceEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = EmergencyEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = FrontdeskEmployee.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)

		user = HospitalManager.objects.all().first().user
		client.force_authenticate(user=user)
		response = client.post('/API/user/information/edit',data,format='json')
		self.assertEqual(response.status_code,201)
	


	'API/hospital/available_rooms'
	def test_show_available_rooms_view(self):
		user = FrontdeskEmployee.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/hospital/available_rooms',format='json')
		self.assertEqual(response.status_code,200)
		


		


	# #'API/hospital/rooms.allocate'
	def test_allocate_room_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)

		data ={"id":Room.objects.all().first().pk}

		response = client.post('/API/hospital/rooms/allocate',data,format='json')
		self.assertEqual(response.status_code,200)


	# #'API/employee/finance/salary'
	def test_get_employees_salary(self):
		user = FinanceEmployee.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employee/finance/salary',format='json')
		self.assertEqual(response.status_code,200)

		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employee/finance/salary',format='json')
		self.assertEqual(response.status_code,401)

	'API/employee/emergency/register'

	def test_emergency_patient_register_view(self):

		data = {
				 "phoneNumber":65 ,
				  "first_name":"TEST" ,
 				  "last_name":"TEST"
				}
		user = EmergencyEmployee.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.post('/API/employee/emergency/register',data,format='json')
		self.assertEqual(response.status_code,200)

		


	#'API/employee/patients'
	def test_get_doctor_patients_views(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employee/patients',format='json')
		self.assertEqual(response.status_code,200)

	#'API/patient/doctors'
	def test_get_patient_doctors_views(self):
		user = Patient.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/patient/doctors',format='json')
		self.assertEqual(response.status_code,200)

		

		#'API/employees/feedback'
	def test_show_all_feedback_view(self):
		user = HospitalManager.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employees/feedback',format='json')
		self.assertEqual(response.status_code,200)

		
	#'API/employee/feedback'
	def test_show_staff_feedback_view(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employees/feedback',format='json')
		self.assertEqual(response.status_code,200)


		
		#'API/patient/write/feedback'

	def test_write_staff_feedback_view(self):
		user = Patient.objects.all().first().user
		pk = Doctor.objects.all().first().pk
		data = {
				"id":pk,
				"feedback":"TEST FEEDBACK"
			   }
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.post('/API/patient/write/feedback',data,format='json')
		self.assertEqual(response.status_code,200)

	def test_get_doctor_statistics(self):
		user = Doctor.objects.all().first().user
		client = APIClient()
		client.force_authenticate(user=user)
		response = client.get('/API/employee/statistics',format='json')
		self.assertEqual(response.status_code,200)

class SanityCheck(TestCase):
	def setUp(self):
		pass
	def test(self):
		self.assertEqual(5, 5)

class PatientTEST(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "TESTUSERNAME",first_name="Mamdouh", last_name="Waleed")
		Patient.objects.create(user=user,account_type="Patient")
	def testPatientCreated(self):
		patient = Patient.objects.get(user__first_name="Mamdouh")
		self.assertEqual(patient.user.last_name, "Waleed")

class HospitalCreationTEST(TestCase):
	def setUp(self):
		Hospital.objects.create(hospital_name="Amal Hospital")
	def testHospitalCreated(self):
		hosp_count = Hospital.objects.filter(hospital_name="Amal Hospital").count()
		self.assertEqual(hosp_count, 1)
		

class DepartmentTEST(TestCase):
	def setUp(self):
		Department.objects.create(department_name="Neurology")
	def testDepartmentCreated(self):
		dep_count = Department.objects.get(department_name="Neurology")
	def testDepartmentGetDoctors(self):
		department = Department.objects.get(department_name="Neurology")
		rn = floor(random()*10) + 3
		for i in range(0, rn):
			user = User.objects.create_user(username = "TESTUSERNAME"+str(i),first_name=f"a{i}", last_name="b{i}",)
			Doctor.objects.create(user=user,department=department)
		doctor_count = department.staffmember_set.count()
		self.assertEqual(doctor_count, rn)
	

class DoctorTEST(TestCase):
	def setUp(self):
		user = User.objects.create_user(username = "TESTUSERNAME515151",first_name="Mariam", last_name="Adel")
		Doctor.objects.create(user=user)
	def testDoctorCreated(self):
		doc = Doctor.objects.get(user__first_name="Mariam")
		self.assertEqual(doc.user.last_name, "Adel")
	def testAttachDoctorToPatient(self):
		user = User.objects.create_user(username = "TESTUSERNAME515151545454",first_name="A", last_name="B")
		patient = Patient.objects.create(user=user)
		doctor = Doctor.objects.get(user__first_name="Mariam", user__last_name="Adel")
		patient.staffmember_set.add(doctor)
		self.assertEqual((patient.staffmember_set.get(pk=doctor.pk).pk) == doctor.pk,True)