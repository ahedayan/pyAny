from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms
from .models import certificate,granted # New Added
from django.db import IntegrityError # New Added
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.cache import never_cache


class UserLogin(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'usernamefield','autofocus': True}),label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'passwordfield'}),label="")

class UserSignup(forms.Form):
    fname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'First Name','class': 'fname','autofocus': True}),label="")
    lname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Last Name','class': 'lname'}),label="")
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username','class': 'usernamefield'}),label="")
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email','class': 'emailfield'}),label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password','class': 'passwordfield'}),label="")
    
    

class addCerti(forms.Form):
    cname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Cetificate Name','class': 'certificateNameField' , 'id':'cname'}),label="")
    ccompany = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company','class': 'companyfield', 'id':'ccompany'}),label="")
    chours = forms.FloatField(widget=forms.NumberInput(attrs={'placeholder': 'Cetificate Hours','class': 'hoursfield', 'id':'chours'}),label="", min_value=0)
    cfield = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Certificate Field','class': 'coursefield', 'id':'cfield'}),label="")
    accredited = forms.ChoiceField(choices=(("",""),('Yes',"Yes"),('No',"No")),widget=forms.Select(attrs={'class': 'accreditedfield' , 'id':'accredited'}),label="")

    
    

class detailsAddCerti(forms.Form):
    cdate = forms.DateField(widget=forms.widgets.DateInput(attrs={'placeholder': 'Cetificate Date','class': 'detailsDateField' , 'type':'date'}),label="")
    cEndDate = forms.DateField(widget=forms.widgets.DateInput(attrs={'placeholder': 'Cetificate Date','class': 'detailsDateField' , 'type':'date'}),label="",required=False)






def userSignup(request):
    
    try:
        if request.method == "POST":
            formdata = UserSignup(request.POST)
            if formdata.is_valid():
                username = formdata.cleaned_data['username']
                fname = formdata.cleaned_data['fname']
                lname = formdata.cleaned_data['lname']
                email = formdata.cleaned_data['email']
                password = formdata.cleaned_data['password']
                
                myuser = User.objects.create_user(username=username , password=password , email=email,first_name = fname,last_name = lname)
                
                myuser.save()
                
                messages.success(request,"Your account has been successfully created.")
                return render(request , 'Certificates/Login.html',{"form":UserLogin()})

            else:
                messages.error(request,"Make sure you type all fields correctly!") # New Added
     
     # New Added           
    except IntegrityError:
        messages.error(request,"The username already exist, try to login!")
     # New Added
            
    
    return render(request,'Certificates/signup.html',{"form":UserSignup()})

@never_cache
def userLogin(request):
    
    if request.method == "POST":
        formdata = UserLogin(request.POST)
        if formdata.is_valid():
            userN = formdata.cleaned_data['username']
            passW = formdata.cleaned_data['password']
        
            user = authenticate(request , username = userN , password = passW)
            
            if user:
                login(request,user)
                cert = certificate.objects.exclude(users = request.user)
                render(request,'Certificates/Menu.html',{"name":userN.capitalize() , "certi":cert})
                return HttpResponseRedirect(reverse("Certificates:menu"))
            else:
                messages.error(request,"Username OR password is incorrect!") # New Added
        
        else:
            return render(request,'Certificates/Login.html')

    
    return render(request,'Certificates/Login.html',{"form":UserLogin()})




def menu(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    
    user = request.user
    cert = certificate.objects.exclude(users = user) # New Added
    
    if len(cert) != 0:
        return render(request,'Certificates/Menu.html' , {"certi":cert , "name":request.user.first_name.capitalize()})
    else:
        return render(request,'Certificates/Menu.html' , {"noCertificates":len(cert) == 0 , "name":request.user.first_name.capitalize()})





def add(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    # Added
    
    else:
        if request.method == "POST":
            formdata = addCerti(request.POST)
            if formdata.is_valid():
                cname = formdata.cleaned_data['cname']
                ccompany = formdata.cleaned_data['ccompany']
                chours = formdata.cleaned_data['chours']
                cfield = formdata.cleaned_data['cfield']
                accredited = formdata.cleaned_data['accredited']
                
                c = certificate(cname = cname,ccompany = ccompany , chours = chours , cfield = cfield , accredited = accredited) # New Added
                c.save()
                
                messages.success(request,f"The {ccompany}'s {cname} certificate has been Added successfuly")  
                return HttpResponseRedirect(reverse("Certificates:menu"))
                
                
                
                
    return render(request,'Certificates/AddCertificate.html',{"form":addCerti()})


def view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    # Added
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    if len(grantedCert) != 0:
        return render(request,"Certificates/ViewCertificate.html",{"certi":grantedCert})
    else:
        return render(request,"Certificates/ViewCertificate.html",{"noCertificates":len(grantedCert) == 0})
        
        


# New Added
def details(request,courseid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    else:
        user = request.user
        cert = certificate.objects.filter(users = user) 
        cert = certificate.objects.get(courseid = courseid)
                
        return render(request , 'Certificates/CertificateDetails.html' , {"certi":cert})
   
   
  
def detailsAdd(request,courseid):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    else:
        user = request.user
        cert = certificate.objects.filter(users = user) 
        cert = certificate.objects.get(courseid = courseid)
        
        try:
            grantedCert = granted.objects.get(user = user , course = cert)
            
            if grantedCert is not None:
                messages.error(request,"This certificate is already chosen!!")
                
                            
        except ObjectDoesNotExist:
            if request.method == "POST":
                    formdata = detailsAddCerti(request.POST)
                        
                    if formdata.is_valid():
                        cdate = formdata.cleaned_data['cdate']
                        cEndDate = formdata.cleaned_data['cEndDate']
                        g= granted(course = cert , user = user , grantedDate = cdate , cEndDate = cEndDate)
                        g.save()
                        
                        messages.success(request,f"The {cert.ccompany}'s {cert.cname} has been added to my certificate successfuly")  
                        return HttpResponseRedirect(reverse("Certificates:menu"))
        

            

    return render(request , 'Certificates/CertificateDetailsAdd.html' , {"certi":cert , "dateform":detailsAddCerti()})



def deleteMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    else:
        if request.method == "POST":
            courseid = int(request.POST["certificate"])
            course = certificate.objects.get(courseid = courseid)
            granted.objects.get(user = request.user,course = course).delete()
            
            messages.success(request,f"The {course.ccompany}'s {course.cname} certificate has been deleted successfuly")  
            return HttpResponseRedirect(reverse("Certificates:view"))
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Certificates/DeleteCertificate.html",{"certi":grantedCert})



def deleteMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    else:
        try:
            if request.method == "POST":
                courseid = int(request.POST["certificate"])
                deletedCourse =  certificate.objects.get(courseid = courseid)
                deletedCourse.delete()
                
                messages.success(request,f"The {deletedCourse.ccompany}'s {deletedCourse.cname} certificate has been deleted successfuly") 
                return HttpResponseRedirect(reverse("Certificates:menu"))
            
        except MultiValueDictKeyError:
            messages.error(request,"You must choose a certificate to delete!")
    
    publicCertificate = certificate.objects.all()# New Added
     
    return render(request,"Certificates/DeleteCertitficateMenu.html",{"certi":publicCertificate})
    


def updateMyCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    
    else:
        if request.method == "POST":
            formdata = detailsAddCerti(request.POST)
            if formdata.is_valid():
                courseid = int(request.POST["certificate"])
                course = certificate.objects.get(courseid = courseid)
                cc = granted.objects.get(user = request.user,course = course)
                cdate = formdata.cleaned_data['cdate']
                cEnddate = formdata.cleaned_data['cEndDate']
                cc.grantedDate = str(cdate)
                
                if str(cEnddate) != "":
                    cc.cEndDate = str(cEnddate)
                
                messages.success(request,f"The {course.ccompany}'s {course.cname} certificate has been updated successfuly")    
                cc.save()
                return HttpResponseRedirect(reverse("Certificates:view"))
            
            
                
    
    user = request.user
    grantedCert = granted.objects.filter(user = user) # New Added
     
    return render(request,"Certificates/UpdateCertificate.html",{"certi":grantedCert, "dateform":detailsAddCerti()})






def updateMenuCertificate(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    
    else:
        try:
            if request.method == "POST":
                courseid = int(request.POST["certificate"])
                c = certificate.objects.get(courseid = courseid)
                return render(request,"Certificates/UpdateCertificateMenuForm.html",{"certi":c , 'form':addCerti()})
            
            
            
        except MultiValueDictKeyError:
            messages.error(request,"You must choose a certificate to update!")
            
    
    cert = certificate.objects.all() # New Added
     
    return render(request,"Certificates/UpdateCertificateMenu.html",{"certi":cert})



def updateMenuCertificateForm(request,courseid):
    
    c = certificate.objects.get(courseid = courseid)

    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    
    else:
            if request.method == "POST":
                
                formdata = addCerti(request.POST)
                
                if formdata.is_valid():
                    
                    cname = formdata.cleaned_data['cname']
                    ccompany = formdata.cleaned_data['ccompany']
                    chours = formdata.cleaned_data['chours']
                    cfield = formdata.cleaned_data['cfield']
                    accredited = formdata.cleaned_data['accredited']
                    
                    c.cname = cname
                    c.ccompany = ccompany
                    c.chours = chours
                    c.cfield = cfield
                    c.accredited = accredited
                    
                    c.save()
                    messages.success(request,f"The {ccompany}'s {cname} certificate has been updated successfuly")
                    return HttpResponseRedirect(reverse("Certificates:menu"))
                
    return render(request,"Certificates/UpdateCertificateMenuForm.html",{"certi":c , 'form':addCerti()})
   


@never_cache
def logout_view(request):
    # Added
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("Certificates:login"))
    # Added
    
    logout(request)
    messages.success(request,"Logged Out Successfully")
    return render(request , 'Certificates/Login.html',{"form":UserLogin()})