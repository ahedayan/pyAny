from django.urls import path
from . import views

app_name = "Certificates"

urlpatterns = [
    path('',views.menu,name='menu'),
    path('login',views.userLogin,name='login'),
    path("signup",views.userSignup,name="signup"),
    path('logout',views.logout_view,name='logout'),
    path("add" , views.add , name="add"),
    path('view',views.view,name='view'),
    path('<int:courseid>/details',views.details , name="details"),
    path('<int:courseid>/add',views.detailsAdd , name="detailsadd"),
    path('deleteMyCertificate',views.deleteMyCertificate , name="deleteMyCertificate"),
    path('deleteFromMenu',views.deleteMenuCertificate , name="deleteMenuCertificate"),
    path('updateMyCertificate' , views.updateMyCertificate , name="updateMyCertificate"),
    path('updateMenuCertificate' , views.updateMenuCertificate , name="updateMenuCertificate"),
    path('<int:courseid>/updateMenuCertificate' , views.updateMenuCertificateForm , name="updateMenuCertificateForm") 
]
