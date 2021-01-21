from django.urls import path
from . import views

# including the app_name to make it easier to namespace the routes
app_name = 'system'

urlpatterns = [
	path('', views.home_view),
    # Patient
    path('API/doctors/<str:dep>',views.doctor_list),

    path('API/patient/register', views.register_view),

    
    path('API/patient/reports', views.reports_view),
    path('API/patient/reports/add', views.add_report_view),
    path('API/patient/reports/edit', views.edit_report_view),
    path('API/patient/reports/delete', views.delete_report_view),
    path('API/patient/reports/deletebyid/<int:pk>', views.deleteByID_report_view),
    path('API/patient/write/feedback', views.write_staff_feedback_view),
    path('API/patient/doctors', views.get_patient_doctors_views),
    


    path('API/patient/appointments', views.appointments_view),
    path('API/patient/appointments/book', views.book_appointment_view),
    path('API/patient/appointments/edit', views.edit_appointment_view),
    path('API/patient/appointments/delete', views.delete_appointment_view),

    

    path('API/hospital', views.Hospital_view),
    # Hospital Manage
    path('API/employees', views.show_employees_view),
    path('API/employees/feedback', views.show_all_feedback_view),
    path('API/employee/feedback', views.show_staff_feedback_view),

    # Employees
    path('API/employee/schedule', views.schedule_view),
    path('API/user/information/view', views.show_user_information_view),
    path('API/user/information/edit', views.edit_user_information_view),
    path('API/patient/add_report', views.add_report_view),
    path('API/hospital/available_rooms', views.show_available_rooms_view),
    path('API/hospital/rooms/allocate', views.allocate_room_view),
    path('API/employee/finance/salary', views.get_employees_salary),
    path('API/employee/emergency/register', views.emergency_patient_register_view),
    path('API/employee/patients', views.get_doctor_patients_views),
    path('API/employee/statistics', views.get_doctor_statistics),
    

]
