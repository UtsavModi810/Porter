from django.shortcuts import render
from .models import Admindetail,Customer,Enterprise,City,Category,Vehicle,Driver,Booking
from django.shortcuts import render,redirect,reverse
from json import dumps
from django.utils.encoding import smart_bytes
from django.core.signing import Signer
from django.core import signing
from django.core.mail import send_mail
from django.conf import settings
import json
import datetime
from django.contrib import messages
from django.core import serializers


# Create your views here.
def home(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        customers=Customer.objects.all().count()
        categories=Category.objects.all().count()
        bookings=Booking.objects.all().count()
        driver=Driver.objects.filter(status=0)

        confirm_driver = request.GET.get('confirm')
        if confirm_driver:
            driver_obj = Driver.objects.get(id= confirm_driver)
            driver_obj.status = True
            driver_obj.save(update_fields=['status'])
            email = driver_obj.email
            mail_subject = "Porter - Confirm Driver Registration"
            message = "THANK YOU FOR REGISTRATION.\nYou are successfully registered in Porter system."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(mail_subject, message, email_from, recipient_list)
        reject_driver = request.GET.get('reject')
        if reject_driver:
            driver_obj = Driver.objects.get(id= reject_driver)
            email = driver_obj.email
            mail_subject = "Porter - Rejected Driver Registration"
            message = "Your registration details are not convenient. Therefore, your registration is rejected by the administartion.\nPlease register again with valid details and valid RC book image, License image and Vehicle number.\nThank You "
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(mail_subject, message, email_from, recipient_list)
            driver_obj.delete()
        return render(request , 'admin/index.html',{'admin': admin,'customers':customers,'categories':categories,'bookings':bookings,'driver':driver})
    else:
        return redirect('admin_login')

def admin_login(request):
    if request.method == 'GET':
       return render(request, 'admin/admin_login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = Admindetail.get_user_by_email(email)
        error_msg = None
        
        if admin:
           # flag = check_password(password , user.password)
            if password == admin.password:
                request.session['admin_id'] = admin.id
                request.session['admin_name'] = admin.first_name+" "+admin.last_name
                return redirect('home')
            else:
                error_msg = 'Email or Password invalid !!'
        else:
            error_msg = 'Email or Password invalid !!'
            
        return render(request , 'admin/admin_login.html', {'error' : error_msg} )
    
def logout_admin(request):
    if request.session['admin_id']:
        del request.session['admin_id']
    if request.session['admin_name']:
        del request.session['admin_name']   
    return redirect('admin_login')

def editprofile_admin(request): 
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        
        if request.method == 'GET':
            msg = None
            return render(request , 'admin/editprofile.html',{'admin':admin,'msg':msg})
        else:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address = request.POST.get('address')
           
            contact_no = request.POST.get('contact_no')

            admin.first_name = first_name
            admin.last_name  = last_name 
            admin.address = address
            
            admin.contact_no = contact_no
            admin.save(update_fields=['first_name','last_name','address','contact_no'])
            msg = "Your profile is upldated successfully..." 
            request.session['admin_name']=admin.first_name+" "+admin.last_name

            return render(request,'admin/editprofile.html',{'admin':admin,'msg':msg})
        
def admin_forget(request):
    if request.method == 'GET':
        return render(request,'admin/admin_forget.html')
    else:
        forget_email = request.POST.get('forget_email')
        admin = Admindetail.get_user_by_email(forget_email)
        msg = None
        if admin:
            encoded_mail = signing.dumps(str(admin.email))
            mail_subject = "Porter - Forgot Password"
            message = "open link for reset pasword : \n http://127.0.0.1:8000/resetpassword?e="+ encoded_mail
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ str(admin.email)]
            send_mail(mail_subject, message, email_from, recipient_list)

            msg = 'You will receive an email for reset your password on your registered email ID...'
        else:
            msg = 'Please enter registered email...'
        
        return render(request,'admin/admin_forget.html', {'msg':msg})

def resetpassword(request):
    msg = None
    if request.method == 'GET':
        email = request.GET.get('e')
        decoded_email = signing.loads(email)
        request.session['decoded_email'] = decoded_email
        return render(request,'admin/resetpasswordadmin.html',{'msg':msg})
    else:
        new_pass = request.POST.get('password')
        admin = Admindetail.objects.get(email = request.session.get('decoded_email'))
        admin.password = new_pass
        admin.save(update_fields=['password'])
        msg = "Password reseted successfully..."
        return redirect('admin_login')  

def managecustomer(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        customers=Customer.objects.all()
        block=request.GET.get('block')
        if block:
            customer = Customer.objects.get(id=block)
            customer.block_status = 1
            customer.save(update_fields=['block_status'])
            if request.session['customer_id']:
                del request.session['customer_id']  
        unblock=request.GET.get('unblock')
        if unblock:
            customer = Customer.objects.get(id=unblock)
            customer.block_status = 0
            customer.save(update_fields=['block_status'])

        return render(request,'admin/managecustomer.html',{ 'customers':customers })
    else:
        return redirect('admin_login')

def manageenterprise(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        enterprises=Enterprise.objects.all()
        block=request.GET.get('block')
        if block:
            enterprise = Enterprise.objects.get(id=block)
            enterprise.block_status = 1
            enterprise.save(update_fields=['block_status'])
            if request.session['enterprise_id']:
                del request.session['enterprise_id']  
        unblock=request.GET.get('unblock')
        if unblock:
            enterprise = Enterprise.objects.get(id=unblock)
            enterprise.block_status = 0
            enterprise.save(update_fields=['block_status'])
        
        return render(request,'admin/manageenterprise.html',{ 'enterprises':enterprises })
    else:
        return redirect('admin_login')

def managecity(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        citys=City.objects.all()
        if request.method == 'GET':
            city_id = request.GET.get('del_city_id')
            if city_id:
                City.objects.filter(id = city_id).delete()
                return redirect(reverse('managecity'))
        return render(request,'admin/managecity.html',{ 'citys':citys })
    else:
        return redirect('admin_login')
    
def insertcity(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        citys=City.objects.all()
        if request.method == 'GET':
          
            return render(request,'admin/insertcity.html')
        else:
            postData = request.POST
            cityname = postData.get('city_name')
            city = City(city_name = cityname)
            city.save()
            return redirect('managecity')
    else:
        
        return redirect('admin_login')

def updatecity(request):
   
    if request.method == 'GET':
        city_id = request.GET.get('update_city_id')
        if city_id:
            city = City.objects.get(id = city_id)
        msg = None
        return render(request,'admin/updatecity.html',{'msg':msg,'city':city})
    else:
        city_name = request.POST.get('cityname')
        city_id = request.POST.get('cityid')
        city = City.objects.get(id = city_id)
        city.city_name = city_name
        city.save(update_fields=['city_name'])
        msg = "Your profile is upldated successfully..."

        return redirect('managecity')

def managecategory(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        categorys=Category.objects.all()
        if request.method == 'GET':
            category_id = request.GET.get('del_category_id')
            if category_id:
                Category.objects.get(id = category_id).delete()
                return redirect(reverse('managecategory'))
        return render(request,'admin/managecategory.html',{ 'categorys':categorys })
    else:
        return redirect('admin_login')

def updatecategory(request):
   
    if request.method == 'GET':
        category_id = request.GET.get('update_category_id')
        if category_id:
            category = Category.objects.get(id = category_id)
        msg = None
        return render(request,'admin/updatecategory.html',{'msg':msg,'category':category})
    else:
        category_name = request.POST.get('categoryname')
        category_description = request.POST.get('categorydescription')
        category_image = request.FILES['categoryimage']
        category_id = request.POST.get('categoryid')
        category = Category.objects.get(id = category_id)
        category.category_name = category_name
        category.category_description = category_description
        category.image = category_image
        category.save(update_fields=['category_name','category_description','image'])
        msg = "Your profile is upldated successfully..."

        return redirect('managecategory')

def insertcategory(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        categorys=Category.objects.all()
        if request.method == 'GET':
          
            return render(request,'admin/insertcategory.html',{'categorys': categorys})
        else:
            postData = request.POST
            categoryname = postData.get('category_name')
            categorydescription = postData.get('category_description')
            categoryimage = request.FILES['category_image']
            category = Category(category_name = categoryname,category_description = categorydescription,image = categoryimage)
            
            category.save()
            return redirect('managecategory')
    else:
        
        return redirect('admin_login')

def managevehicle(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        vehicles=Vehicle.objects.all()
        if request.method == 'GET':
            vehicle_id = request.GET.get('del_vehicle_id')
            if vehicle_id:
                Vehicle.objects.get(id = vehicle_id).delete()
                return redirect(reverse('managevehicle'))
        return render(request,'admin/managevehicle.html',{ 'vehicles':vehicles })
    else:
        return redirect('admin_login')

def insertvehicle(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        vehicles=Vehicle.objects.all()
        if request.method == 'GET':
          
            return render(request,'admin/insertvehicle.html',{'vehicles': vehicles})
        else:
            postData = request.POST
            vehiclename = postData.get('vehicle_name')
            vehicleimage = request.FILES['vehicle_image']
            vehiclecapacity = postData.get('vehicle_capacity')
            vehiclesize = postData.get('vehicle_size')
            vehicleprice = postData.get('vehicle_price')
            vehicle = Vehicle(vehicle_name = vehiclename,image = vehicleimage,capacity = vehiclecapacity,size = vehiclesize,price = vehicleprice)
            
            vehicle.save()
            return redirect('managevehicle')
    else:
        
        return redirect('admin_login')

def updatevehicle(request):
   
    if request.method == 'GET':
        vehicle_id = request.GET.get('update_vehicle_id')
        if vehicle_id:
            vehicle = Vehicle.objects.get(id = vehicle_id)
        msg = None
        return render(request,'admin/updatevehicle.html',{'msg':msg,'vehicle':vehicle})
    else:
        vehicle_id = request.POST.get('vehicleid')
        vehicle_name = request.POST.get('vehiclename')
        vehicle_image = request.FILES['vehicleimage']
        vehicle_capacity = request.POST.get('vehiclecapacity')
        vehicle_size = request.POST.get('vehiclesize')
        vehicle_price = request.POST.get('vehicleprice')

        vehicle = Vehicle.objects.get(id = vehicle_id)
        vehicle.vehicle_name = vehicle_name
        vehicle.image = vehicle_image
        vehicle.capacity = vehicle_capacity
        vehicle.size = vehicle_size
        vehicle.price = vehicle_price
        
        vehicle.save(update_fields=['vehicle_name','image','capacity','size','price'])
        msg = "Your profile is upldated successfully..."

        return redirect('managevehicle')

def managebooking(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        cbookings=Booking.objects.exclude(customer_id = None)

        return render(request,'admin/managebooking.html',{ 'cbookings':cbookings })
    else:
        return redirect('admin_login')

def manageenterprisebooking(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        ebookings=Booking.objects.exclude(enterprise_id = None)

        return render(request,'admin/manageenterprisebooking.html',{ 'ebookings':ebookings })
    else:
        return redirect('admin_login')

def trackorderadmin(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        cbookings=Booking.objects.exclude(customer_id = None)

        return render(request,'admin/trackorder.html',{ 'cbookings':cbookings })
    else:
        return redirect('admin_login')
    
def enterprisetrackorderadmin(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        ebookings=Booking.objects.exclude(enterprise_id = None)

        return render(request,'admin/enterprisetrackorder.html',{ 'ebookings':ebookings })
    else:
        return redirect('admin_login')


def managedriver(request):
    admin_id = request.session.get('admin_id')
    if admin_id:
        admin = Admindetail.objects.get(id = admin_id)
        drivers=Driver.objects.all()
        block=request.GET.get('block')
        if block:
            driver = Driver.objects.get(id=block)
            driver.block_status = 1
            driver.save(update_fields=['block_status'])
            if 'driver_id' in request.session:
                del request.session['driver_id']  
        unblock=request.GET.get('unblock')
        if unblock:
            driver = Driver.objects.get(id=unblock)
            driver.block_status = 0
            driver.save(update_fields=['block_status'])

        return render(request,'admin/managedriver.html',{ 'drivers':drivers })
    else:
        return redirect('admin_login')


def driverhome(request):
    driver_id = request.session.get('driver_id')
    if driver_id:
        driver = Driver.objects.get(id = driver_id)
        cbookings=Booking.objects.exclude(customer_id = None)
        ebookings=Booking.objects.exclude(enterprise_id = None)
        status=['pending','accepted','rejected']
        b_id=request.GET.get('b_id')
        if b_id:
            booking=Booking.objects.get(id=b_id)
            booking.status=status[1]
            booking.driver_id = driver
            booking.save(update_fields=['status','driver_id'])



            email=booking.customer_id.email
            mail_subject = "Porter - Booking Accepted"
            message = "Our Driver Will Come Within Few Minutes \nDriver Name : "+driver.driver_name + "\nDriver Contact No : "+driver.contact_no + "\nVehicle Name : " + driver.vehicle_id.vehicle_name + "\nVehicle Number : " + driver.vehicle_no
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(mail_subject, message, email_from, recipient_list)

            messages.success(request, 'Your Booking is Accepted By Driver Check Mail For More Information')

        be_id=request.GET.get('be_id')
        if be_id:
            booking=Booking.objects.get(id=be_id)
            booking.status=status[1]
            booking.driver_id = driver
            booking.save(update_fields=['status','driver_id'])



            email=booking.enterprise_id.email
            mail_subject = "Porter - Booking Accepted"
            message = "Our Driver Will Come Within Few Minutes \nDriver Name : "+driver.driver_name + "\nDriver Contact No : "+driver.contact_no + "\nVehicle Name : " + driver.vehicle_id.vehicle_name + "\nVehicle Number : " + driver.vehicle_no
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(mail_subject, message, email_from, recipient_list)

            messages.success(request, 'Your Booking is Accepted By Driver Check Mail For More Information')


        return render(request , 'driver/index.html',{'driver': driver,'cbookings':cbookings,'ebookings':ebookings,'status':status})

    else:
        return redirect('driver_login')

def driver_login(request):
    if request.method == 'GET':
        return render(request, 'driver/driver_login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_msg = None
        driver = None
        try:
            driver = Driver.objects.get(email = email)
        except:
            error_msg = "Email or Password invalid !!"
        
        if driver:
           # flag = check_password(password , user.password)
            if password == driver.password:
                if driver.status == False:
                    error_msg = "Your registration is under process. You will get the mail of confirmation from the porter system."
                else:
                    if driver.block_status==1:
                        error_msg="your are blocked by administrater "
                    else:
                        
                        request.session['driver_id'] = driver.id
                        request.session['driver_name'] = driver.driver_name
                        return redirect('driverhome')
            else:
                error_msg = 'Email or Password invalid !!'
        else:
            error_msg = 'Email or Password invalid !!'
            
        return render(request , 'driver/driver_login.html', {'error' : error_msg} )
    
def driver_logout(request):
    if request.session['driver_id']:
        del request.session['driver_id']
    if request.session['driver_name']:
        del request.session['driver_name']   
    return redirect('driver_login')


def driver_register(request):
    citys = City.objects.all()
    vehicles = Vehicle.objects.all()
    if request.method == 'GET':
        return render(request, 'driver/driver_register.html',{ 'citys':citys,'vehicles':vehicles })
    else:
        driver_name = request.POST.get('driver_name')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_no = request.POST.get('contact_no')
        city_id = request.POST.get('citys')
        vno = request.POST.get('vno') 
        limage = request.FILES['limage']
        rimage = request.FILES['rimage']
        vehicle_id = request.POST.get('vehicles')
        

        city_id = City.objects.get(pk = city_id)
        vehicle_id = Vehicle.objects.get(pk = vehicle_id)

        mail_subject = "Porter - Validate Driver Registration"
        message = "THANK YOU FOR REGISTRATION.\nWe have successfully received your details. Registration will be confirmed by administrator based on vehicle number, RC and Driving licence."
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(mail_subject, message, email_from, recipient_list)

        driver = Driver(driver_name = driver_name, address = address, email = email, password = password, contact_no = contact_no,city_id = city_id,vehicle_id=vehicle_id,license_image = limage,rc_image=rimage,vehicle_no=vno)
        driver.save()

        
        return redirect('driver_login')
      
def driver_forget(request):
    if request.method == 'GET':
        return render(request,'driver/driver_forget.html')
    else:
        forget_email = request.POST.get('forget_email')
        driver = Driver.get_user_by_email(forget_email)
        msg = None
        if driver:
            encoded_mail = signing.dumps(str(driver.email))
            mail_subject = "Porter - Forgot Password"
            message = "open link for reset pasword : \n http://127.0.0.1:8000/resetpassworddriver?e="+ encoded_mail
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ str(driver.email)]
            send_mail(mail_subject, message, email_from, recipient_list)

            msg = 'You will receive an email for reset your password on your registered email ID...'
        else:
            msg = 'Please enter registered email...'
        
        return render(request,'driver/driver_forget.html', {'msg':msg})

def resetpassworddriver(request):
    msg = None
    if request.method == 'GET':
        email = request.GET.get('e')
        decoded_email = signing.loads(email)
        request.session['decoded_email'] = decoded_email
        return render(request,'driver/resetpassworddriver.html',{'msg':msg})
    else:
        new_pass = request.POST.get('password')
        driver = Driver.objects.get(email = request.session.get('decoded_email'))
        driver.password = new_pass
        driver.save(update_fields=['password'])
        msg = "Password reseted successfully..."
        return redirect('driver_login')        


def client_home(request):
    category=Category.objects.all()
    vehicle=Vehicle.objects.all()
    if request.method=='GET':
        tmpJson = serializers.serialize("json",vehicle)
        tmpObj = json.loads(tmpJson)
        return render(request,"client/home.html",{'category':category,'vehicle':vehicle, 'js_vehicles':json.dumps(tmpObj)})
    else:
        email=request.POST.get('email')
        mail_subject = "Porter - SUBSCRIBE"
        message = "THANK YOU FOR SUBSCRIPTION"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(mail_subject, message, email_from, recipient_list)
        return redirect('client_home')
    

def client_login(request):
    if request.method == 'GET':
       return render(request, 'client/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_msg = None
        customer = None
        try:
            customer = Customer.objects.get(email = email)
        except:
            error_msg = 'Email or Password invalid !!'  

        if customer:
           # flag = check_password(password , user.password)
            if password == customer.password:
                if customer.block_status==1:
                    error_msg="your are block by administrater "
                else:
                    request.session['customer_id'] = customer.id
                    return redirect('client_home')
                
            else:
                error_msg = 'Email or Password invalid !!'
        else:
            error_msg = 'Email or Password invalid !!'
            
        return render(request , 'client/login.html', {'error' : error_msg} )
    
def client_register(request):
    citys = City.objects.all()
    if request.method == 'GET':
        return render(request, 'client/register.html',{ 'citys':citys })
    else:
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_no = request.POST.get('contact')
        birth_date = request.POST.get('birth')
        city_id = request.POST.get('citys')
      

        city_id = City.objects.get(pk = city_id)
        customer = Customer(first_name = first_name, last_name = last_name,address = address, email = email, password = password, contact_no = contact_no,birth_date = birth_date ,city_id = city_id)
        customer.save()
        return redirect('client_login')

    return render(request,"client/register.html")

def client_forget(request):
    if request.method == 'GET':
        return render(request,'client/client_forget.html')
    else:
        forget_email = request.POST.get('forget_email')
        customer = Customer.get_user_by_email(forget_email)
        msg = None
        if customer:
            encoded_mail = signing.dumps(str(customer.email))
            mail_subject = "Porter - Forgot Password"
            message = "open link for reset pasword : \n http://127.0.0.1:8000/resetpasswordcustomer?e="+ encoded_mail
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ str(customer.email)]
            send_mail(mail_subject, message, email_from, recipient_list)

            msg = 'You will receive an email for reset your password on your registered email ID...'
        else:
            msg = 'Please enter registered email...'
        
        return render(request,'client/client_forget.html', {'msg':msg})

def resetpasswordcustomer(request):
    msg = None
    if request.method == 'GET':
        email = request.GET.get('e')
        decoded_email = signing.loads(email)
        request.session['decoded_email'] = decoded_email
        return render(request,'client/resetpasswordcustomer.html',{'msg':msg})
    else:
        new_pass = request.POST.get('password')
        customer = Customer.objects.get(email = request.session.get('decoded_email'))
        customer.password = new_pass
        customer.save(update_fields=['password'])
        msg = "Password reseted successfully..."
        return redirect('client_login')   

def client_logout(request):
    if request.session['customer_id']:
        del request.session['customer_id']  
    return redirect('client_login')

def editprofile_client(request): 
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id = customer_id)
        citys=City.objects.all()

        if request.method == 'GET':
            msg = None
            return render(request , 'client/editprofile.html',{'customer':customer,'citys':citys,'msg':msg})
        else:
            first_name = request.POST.get('fname')
            last_name = request.POST.get('lname')
            address = request.POST.get('address')
            contact_no = request.POST.get('contact')
            city=request.POST.get('citys')


            customer.first_name = first_name
            customer.last_name  = last_name 
            customer.address = address
            customer.contact_no = contact_no
            customer.city_id = City.objects.get(id=city)
           
            customer.save(update_fields=['first_name','last_name','address','contact_no','city_id'])
            msg = "Your profile is upldated successfully..." 
            

            return render(request,'client/editprofile.html',{'customer':customer,'citys':citys,'msg':msg})

def categoryclient(request):
    category=Category.objects.all()
    return render(request,'client/category.html',{'category':category})

def vehicleclient(request):
    vehicle=Vehicle.objects.all()
    cat_id=request.GET.get('cat_id')
    if cat_id:

        return render(request,'client/vehicle.html',{'vehicle':vehicle,'cat_id':cat_id})
        
    return render(request,'client/vehicle.html',{'vehicle':vehicle})
    

def bookingclient(request):
    
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id = customer_id)

        if request.method=='GET':
            print("Entered-----------------")
            vehicle_id=request.GET.get('ve_id')
            global vehicle
            vehicle = Vehicle.objects.get(id=vehicle_id)
            cat_id=request.GET.get('cat_id')
            global category
            category=Category.objects.get(id=cat_id)
            

            return render(request,'client/booking.html',{'vehicle_price':json.dumps(vehicle.price),'vehicle':vehicle,'category':category})
    else:
        return redirect('client_login')

def bookingclient1(request):
    customer_id = request.session.get('customer_id')
    if customer_id:
        customer = Customer.objects.get(id = customer_id)
    record=""

    for i in dict(request.GET).keys():
        record=i
    listdata = record.split(":")

    origin = listdata[1].split('",')[0][1:]
    destination = listdata[2].split('",')[0][1:]
    category_id = listdata[3].split('",')[0][1:]
    vehicle_id = listdata[4].split('",')[0][1:]
    total = listdata[5].split('"')[1]
    items = listdata[6].split('"')[1]
    date = datetime.datetime.now()

    vehicle = Vehicle.objects.get(id=vehicle_id)
    category=Category.objects.get(id=category_id)
    
    booking=Booking(pick_address = origin, drop_address = destination,category_id = category, vehicle_id = vehicle, date = date, customer_id = customer,total_amount=float(total), items = items)
    booking.save() 

    return render(request,'client/home.html')


def bookingdetail(request):
    customer_id = request.session.get('customer_id')
    if customer_id:

        bookings=Booking.objects.filter(customer_id=customer_id)
        return render(request,'client/bookingdetail.html',{'bookings':bookings})
    else:
        return redirect('client_login')


def trackorder(request):
    booking_id=request.GET.get('b_id')
    if booking_id:
        booking=Booking.objects.get(id=booking_id)

    return render(request,'client/trackorder.html',{'track_status':booking.track_status,'booking':booking})




def managetrackorder(request):
    driver_id = request.session.get('driver_id')
    if driver_id:
        bookings=Booking.objects.filter(driver_id=driver_id).filter(enterprise_id = None)
        # all_status = []
        # for b in bookings:
        #     try:
        #         status = TrackDetails.objects.get(booking_id=b.id)
        #     except:
        #         pass  
        #     if status.track_status == 1:
        #         all_status.append('shipped')
        #     elif status..track_status == 2:
        #         all_status.append('out for delivery')
        #     elif status.track_status == 3:
        #         all_status.append('Delivery Successfully')
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            if booking_id:

                trackvalue = request.POST.get('trackvalue')
                booking = Booking.objects.get(id = booking_id)
                if booking.track_status == 0:
                    email = booking.customer_id.email
                    mail_subject = "Porter - Order Dispatched"
                    message = "Your order is dispatched. Please make payment ready of amount ₹ "+ str(booking.total_amount) + "\nOur driver will receive payment from you.\nDelivery will start only after payment received"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(mail_subject, message, email_from, recipient_list)
                booking.track_status += int(trackvalue)
                booking.save(update_fields=['track_status'])
            
            b_id = request.POST.get('payment')
            if b_id:
                booking = Booking.objects.get(id = b_id)
                booking.payment_status = True
                booking.save(update_fields=['payment_status'])

        return render(request,'driver/managetrackorder.html',{'bookings':bookings})

def enterprisetrackorder(request):
    driver_id = request.session.get('driver_id')
    if driver_id:
        bookings=Booking.objects.filter(driver_id=driver_id).filter(customer_id = None)
        # all_status = []
        # for b in bookings:
        #     try:
        #         status = TrackDetails.objects.get(booking_id=b.id)
        #     except:
        #         pass  
        #     if status.track_status == 1:
        #         all_status.append('shipped')
        #     elif status..track_status == 2:
        #         all_status.append('out for delivery')
        #     elif status.track_status == 3:
        #         all_status.append('Delivery Successfully')
        if request.method == 'POST':
            booking_id = request.POST.get('booking_id')
            if booking_id:

                trackvalue = request.POST.get('trackvalue')
                booking = Booking.objects.get(id = booking_id)
                if booking.track_status == 0:
                    email = booking.enterprise_id.email
                    mail_subject = "Porter - Order Dispatched"
                    message = "Your order is dispatched. Please make payment ready of amount ₹ "+ str(booking.total_amount) + "\nOur driver will receive payment from you.\nDelivery will start only after payment received"
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [email]
                    send_mail(mail_subject, message, email_from, recipient_list)
                booking.track_status += int(trackvalue)
                booking.save(update_fields=['track_status'])
        
        b_id = request.POST.get('payment')
        if b_id:
            booking = Booking.objects.get(id = b_id)
            booking.payment_status = True
            booking.save(update_fields=['payment_status'])
        

        return render(request,'driver/managetrackorder.html',{'bookings':bookings})


def payment(request):
    return render(request,'client/payment.html')




def enterpriselogin(request):
    if request.method == 'GET':
       return render(request, 'enterprise/enterpriselogin.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        error_msg = None
        enterprise = None
        try:
            enterprise = Enterprise.objects.get(email = email)
        except:
            error_msg = 'Email or Password invalid !!'  

        if enterprise:
           # flag = check_password(password , user.password)
            if password == enterprise.password:
                if enterprise.block_status==1:
                    error_msg="your are block by administrater "
                else:
                    request.session['enterprise_id'] = enterprise.id
                    return redirect('client_home')
                
            else:
                error_msg = 'Email or Password invalid !!'
        else:
            error_msg = 'Email or Password invalid !!'
            
        return render(request , 'enterprise/enterpriselogin.html', {'error' : error_msg} )


def enterpriseregister(request):
    citys = City.objects.all()
    if request.method == 'GET':
        return render(request, 'enterprise/enterpriseregister.html',{ 'citys':citys })
    else:
        person_name = request.POST.get('pname')
        company_name = request.POST.get('cname')
        address = request.POST.get('address')
        email = request.POST.get('email')
        password = request.POST.get('password')
        contact_no = request.POST.get('contact')
        city_id = request.POST.get('citys')
      

        city_id = City.objects.get(pk = city_id)
        enterprise = Enterprise(person_name = person_name, company_name = company_name,address = address, email = email, password = password, contact_no = contact_no,city_id = city_id)
        enterprise.save()
        return redirect('enterpriselogin')

    return render(request,"enterprise/enterpriseregister.html")

def enterpriselogout(request):
    if request.session['enterprise_id']:
        del request.session['enterprise_id']  
    return redirect('enterpriselogin')


def editprofile_enterprise(request): 
    enterprise_id = request.session.get('enterprise_id')
    if enterprise_id:
        enterprise = Enterprise.objects.get(id = enterprise_id)
        citys=City.objects.all()

        if request.method == 'GET':
            msg = None
            return render(request , 'enterprise/editprofile_enterprise.html',{'enterprise':enterprise,'citys':citys,'msg':msg})
        else:
            person_name = request.POST.get('pname')
            company_name = request.POST.get('cname')
            address = request.POST.get('address')
            contact_no = request.POST.get('contact')
            city=request.POST.get('citys')


            enterprise.person_name = person_name
            enterprise.company_name  = company_name 
            enterprise.address = address
            enterprise.contact_no = contact_no
            enterprise.city_id = City.objects.get(id=city)
           
            enterprise.save(update_fields=['person_name','company_name','address','contact_no','city_id'])
            msg = "Your profile is upldated successfully..." 
            

            return render(request,'enterprise/editprofile_enterprise.html',{'enterprise':enterprise,'citys':citys,'msg':msg})

def bookingenterprise(request):
    enterprise_id = request.session.get('enterprise_id')
    if enterprise_id:
        enterprise = Enterprise.objects.get(id = enterprise_id)

        if request.method=='GET':
            print("Entered-----------------")
            vehicle_id=request.GET.get('ve_id')
            global vehicle
            vehicle = Vehicle.objects.get(id=vehicle_id)

            return render(request,'enterprise/bookingenterprise.html',{'vehicle_price':json.dumps(vehicle.price),'vehicle':vehicle})
    else:
        return redirect('enterpriselogin')

def bookingenterprise1(request):
    enterprise_id = request.session.get('enterprise_id')
    if enterprise_id:
        enterprise = Enterprise.objects.get(id = enterprise_id)
    record=""

    for i in dict(request.GET).keys():
        record=i
    listdata = record.split(":")

    origin = listdata[1].split('",')[0][1:]
    destination = listdata[2].split('",')[0][1:]
    vehicle_id = listdata[3].split('",')[0][1:]
    total = listdata[4].split('"')[1]
    items = listdata[5].split('"')[1]
    date = datetime.datetime.now()

    vehicle = Vehicle.objects.get(id=vehicle_id)
    
    booking=Booking(pick_address = origin, drop_address = destination, vehicle_id = vehicle, date = date, enterprise_id = enterprise,total_amount=float(total), items = items)
    booking.save() 

    return render(request,'client/home.html')


def bookingdetailenterprise(request):
    enterprise_id = request.session.get('enterprise_id')
    if enterprise_id:

        bookings=Booking.objects.filter(enterprise_id=enterprise_id)
        return render(request,'enterprise/bookingdetailenterprise.html',{'bookings':bookings})
    else:
        return redirect('enterpriselogin')


def enterprisetrackorder1(request):
    booking_id=request.GET.get('b_id')
    if booking_id:
        booking=Booking.objects.get(id=booking_id)

    return render(request,'client/trackorder.html',{'track_status':booking.track_status,'booking':booking})


def enterprise_forget(request):
    if request.method == 'GET':
        return render(request,'enterprise/enterprise_forget.html')
    else:
        forget_email = request.POST.get('forget_email')
        enterprise = Enterprise.get_user_by_email(forget_email)
        msg = None
        if enterprise:
            encoded_mail = signing.dumps(str(enterprise.email))
            mail_subject = "Porter - Forgot Password"
            message = "open link for reset pasword : \n http://127.0.0.1:8000/resetpasswordenterprise?e="+ encoded_mail
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ str(enterprise.email)]
            send_mail(mail_subject, message, email_from, recipient_list)

            msg = 'You will receive an email for reset your password on your registered email ID...'
        else:
            msg = 'Please enter registered email...'
        
        return render(request,'enterprise/enterprise_forget.html', {'msg':msg})


def resetpasswordenterprise(request):
    msg = None
    if request.method == 'GET':
        email = request.GET.get('e')
        decoded_email = signing.loads(email)
        request.session['decoded_email'] = decoded_email
        return render(request,'enterprise/resetpasswordenterprise.html',{'msg':msg})
    else:
        new_pass = request.POST.get('password')
        enterprise = Enterprise.objects.get(email = request.session.get('decoded_email'))
        enterprise.password = new_pass
        enterprise.save(update_fields=['password'])
        msg = "Password reseted successfully..."
        return redirect('enterpriselogin')   