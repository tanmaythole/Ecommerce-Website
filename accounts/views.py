from mall.models import Order
from accounts.models import Address, User
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import auth
from random import randint
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

# Create your views here.
def send_otp(email, otp):
    if send_mail("OTP Verification", "Your OTP for TholeMall Account Verification is "+ str(otp), settings.EMAIL_HOST_USER, [email] ):
        return True
    return False
    
def signup(request):
    if request.method=='POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['countryCode']+request.POST['mobile']
        password = request.POST['password']
        repassword = request.POST['repassword']
        otp = randint(100000, 999999)

        if password!=repassword:
            messages.error(request, "Password Not Matched")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username Already Exists.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Exists")
        elif User.objects.filter(mobile=mobile).exists():
            messages.error(request, "Mobile number Already Exists")
        else:
            user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email, password=password, mobile=mobile, otp=otp)
            user.save()
            if send_otp(email, otp):
                messages.success(request, "OTP sent successfully on your registered E-mail.")
            auth.login(request, user)
            return redirect('/accounts/verifyaccount')

    return render(request, 'signup.html')


def login(request):
    if request.method=='POST':
        email = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # print("Login")
            if user.is_verified:
                return redirect("/")
            else:
                return redirect('/accounts/verifyaccount')
        else:
            return redirect("/accounts/signup")
    return render(request, 'login.html')

@login_required
def verifyaccount(request):
    if request.method=='POST':
        username = request.POST['userinfo']
        user = User.objects.get(email=username)
        if request.POST.get('verifyotp'):
            otp = request.POST['otp']
            if int(otp) == int(user.otp):
                user.is_verified = True
                user.save()
                messages.success(request, "Your Account Verified Successfully")
                print("verified")
                return redirect('/')
            else:
                messages.error(request, "Invalid OTP")
        
        elif request.POST.get('resendOtp'):
            otp = randint(100000, 999999)
            user.otp = otp
            user.save()
            if send_otp(user.email, otp):
                messages.success(request, "OTP sent successfully on your registered E-mail.")
    return render(request, 'verifyotp.html')

@login_required
def profile(request):
    user = User.objects.filter(id=request.user.id)
    if request.method=="POST":
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        email = request.POST['email']
        mobile = request.POST['mobile']

        if user.update(first_name=firstName, last_name=lastName, email=email, mobile=mobile):
            messages.success(request, "Personal Information Updated Successfully!")
            # user = User.objects.filter(id=request.user.id)
            print(user[0].last_name)
        else:
            messages.error(request, "Something Went Wrong")


    userInfo = {'userinfo': user[0]}
    return render(request, 'profile.html', userInfo)

@login_required
def change_password(request):
    if request.method=="POST":
        currPass = request.POST['curr_password']
        newPass = request.POST['new_password']
        reNewPass = request.POST['renew_password']
        user = request.user
        if newPass==reNewPass:
            if user.check_password(currPass):
                try:
                    user.set_password(newPass)
                    user.save()
                    messages.success(request, "Password Changed Successfully!")
                except Exception as e:
                    messages.error(request, "Something Went Wrong!")
            else:
                messages.error(request, "Enter Correct Password.")
        else:
            messages.error(request, "Password Not Matched!")

    return render(request, 'change_password.html')
    
@login_required
def addresses(request):
    if request.method=="POST":
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode']
        addressType = request.POST['address-type']

        if len(Address.objects.filter(address_user=request.user)) == 0:
            default = True
        else:
            default = False

        if Address.objects.create(full_name=name, address_user=request.user, mobile=mobile, address=address, city=city, district=district, state=state, pincode=pincode, address_type=addressType, default=default):
            messages.success(request, "Address Added Successfully!")
        else:
            messages.error(request, "Something Went Wrong!")
    
    user_addresses = {"addresses": Address.objects.filter(address_user=request.user)}

    return render(request, 'addresses.html', user_addresses)

@login_required
def edit_address(request, slug):
    address = Address.objects.filter(id=slug)[0]
    if request.method == 'POST':
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        district = request.POST['district']
        state = request.POST['state']
        pincode = request.POST['pincode']
        addressType = request.POST['address-type']
        if Address.objects.filter(id=slug).update(full_name=name, address_user=request.user, mobile=mobile, address=address, city=city, district=district, state=state, pincode=pincode, address_type=addressType):
            messages.success(request, "Address Edited Successfully!")
            return redirect('/accounts/addresses/')
    return render(request, "edit-address.html", {"address": address})

@login_required
def delete_address(request, slug):
    if Address.objects.filter(id=slug, address_user=request.user).delete():
        messages.success(request, "Address deleted successfully!")
        # return redirect('/accounts/addresses/')
    else:
        messages.error(request, "Something Went Wrong!")
    return redirect('/accounts/addresses/')

@login_required
def make_default_address(request, slug):
    if Address.objects.filter(address_user=request.user, default=True).update(default=False):
        if Address.objects.filter(id=slug, address_user=request.user).update(default=True):
            messages.success(request, "Changes Updated Successfully!!")
        else:
            messages.error(request, "Something Went Wrong!")
    else:
        messages.error(request, "Something Went Wrong!")
    return redirect('/accounts/addresses/')

@login_required
def orders(request):
    order = Order.objects.filter(order_user=request.user).order_by("-orderTime")
    params = {'orders':order}
    return render(request, 'orders.html', params)


def logout(request):
    auth.logout(request)
    return redirect("/")