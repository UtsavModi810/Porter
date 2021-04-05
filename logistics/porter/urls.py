from django.urls import path
from . import views
# from .views import Pdf

urlpatterns = [
    #Admin main
    path('home/', views.home, name='home'),
	path('admin_login/', views.admin_login, name='admin_login'),
    path('admin_logout/', views.logout_admin, name='admin_logout'),
    path('editprofile/', views.editprofile_admin, name='admin_editprofile'),
    path('admin_forget/', views.admin_forget, name='admin_forget'),
    path('resetpassword/', views.resetpassword, name='resetpassword'),
    path('managecustomer/', views.managecustomer, name='managecustomer'),
    path('manageenterprise/', views.manageenterprise, name='manageenterprise'),
    path('managecity/', views.managecity, name='managecity'),
    path('insertcity/', views.insertcity, name='insertcity'),
    path('updatecity/', views.updatecity, name='updatecity'),
    path('managecategory/', views.managecategory, name='managecategory'),
    path('insertcategory/', views.insertcategory, name='insertcategory'),
    path('updatecategory/', views.updatecategory, name='updatecategory'),
    path('managevehicle/', views.managevehicle, name='managevehicle'),
    path('insertvehicle/', views.insertvehicle, name='insertvehicle'),
    path('updatevehicle/', views.updatevehicle, name='updatevehicle'),
    path('managedriver/', views.managedriver, name='managedriver'),  
    path('managebooking/', views.managebooking, name='managebooking'),  
    path('trackorderadmin/', views.trackorderadmin, name='trackorderadmin'), 
    path('manageenterprisebooking/', views.manageenterprisebooking, name='manageenterprisebooking'),  
    path('enterprisetrackorderadmin/', views.enterprisetrackorderadmin, name='enterprisetrackorderadmin'), 
  

    # Driver URLS
    path('driver_login/', views.driver_login, name='driver_login'),  
    path('driverhome/', views.driverhome, name='driverhome'),
    path('driver_logout/', views.driver_logout, name='driver_logout'),
    path('driver_register/', views.driver_register, name='driver_register'),
    path('driver_forget/', views.driver_forget, name='driver_forget'),
    path('resetpassworddriver/', views.resetpassworddriver, name='resetpassworddriver'),
    path('managetrackorder/', views.managetrackorder, name='managetrackorder'),
    path('enterprisetrackorder/', views.enterprisetrackorder, name='enterprisetrackorder'),


     # Client URLS
    path('client_home/', views.client_home, name='client_home'),
    path('client_login/', views.client_login, name='client_login'),
    path('client_register/', views.client_register, name='client_register'), 
    path('client_forget/', views.client_forget, name='client_forget'),
    path('resetpasswordcustomer/', views.resetpasswordcustomer, name='resetpasswordcustomer'),
    path('client_logout/', views.client_logout, name='client_logout'),
    path('editprofile_client/', views.editprofile_client, name='editprofile_client'),
    path('categoryclient/', views.categoryclient, name='categoryclient'),
    path('vehicleclient/', views.vehicleclient, name='vehicleclient'),
    path('bookingclient/', views.bookingclient, name='bookingclient'),
    path('bookingclient1/', views.bookingclient1, name='bookingclient1'),
    path('bookingdetail/', views.bookingdetail, name='bookingdetail'),
    path('trackorder/', views.trackorder, name='trackorder'),
    path('payment/', views.payment, name='payment'),


    #Enterprise Urls
    path('enterpriselogin/', views.enterpriselogin, name='enterpriselogin'), 
    path('enterpriseregister/', views.enterpriseregister, name='enterpriseregister'),    
    path('enterpriselogout/', views.enterpriselogout, name='enterpriselogout'),
    path('editprofile_enterprise/', views.editprofile_enterprise, name='editprofile_enterprise'),   
    path('bookingenterprise/', views.bookingenterprise, name='bookingenterprise'),  
    path('bookingenterprise1/', views.bookingenterprise1, name='bookingenterprise1'),   
    path('bookingdetailenterprise/', views.bookingdetailenterprise, name='bookingdetailenterprise'),   
    path('enterprisetrackorder1/', views.enterprisetrackorder1, name='enterprisetrackorder1'),
    path('enterprise_forget/', views.enterprise_forget, name='enterprise_forget'),
    path('resetpasswordenterprise/', views.resetpasswordenterprise, name='resetpasswordenterprise'),




    # #PayPal
    # path('admin/', admin.site.urls),
    # path('', include('cart.urls')),
    # path('paypal/', include('paypal.standard.ipn.urls')),

    
]

