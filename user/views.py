from django.shortcuts import render,redirect,get_object_or_404
from .models import User
from .forms import UserForm,UpdateUserForm
# from . import utils
import cv2
import numpy as np
from pyzbar.pyzbar import decode


# Create your views here.

def home(request,*args,**kwargs):
    search_here = ''
    if request.GET.get('q'):
        search_here = request.GET.get('q')

    users = User.objects.filter(name__icontains=search_here )
    users = User.objects.filter(cnic__icontains=search_here )
    users = User.objects.filter(rc_id__icontains=search_here )
    context = {
        'users' : users,
    }
    return render(request,'user/home.html',context)

def details(request,pk):
    user = User.objects.get(id=pk)
    context = {
        'user' : user,
    }
    return render(request,'user/details.html',context)

def upload(request):
    form = UserForm()
    if request.method == 'POST':
        form =UserForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {
        'form' : form,
    }
    return render(request,'user/upload.html',context)

def update(request,pk):
    user =User.objects.get(id=pk)
    form = UpdateUserForm()
    if request.method == 'POST':
        form =UserForm(request.POST,request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UpdateUserForm(instance=user)
    context = {
        'form' : form,
    }
    return render(request,'user/update.html',context)

def backside(request,pk):
    user = User.objects.get(id=pk)
    
    context = {
        'user' : user,
    }
    return render(request,'user/backside.html',context)


def check(request):
    
    scan = User.objects.all()
    return render(request,'user/check.html',{'scan':scan})

def identify(request):
    
    try:
        #img = cv2.imread('1.png')
        cap = cv2.VideoCapture(0)
        cap.set(3,640)
        cap.set(4,480)
        
        with open('rc_id.text') as f:
            myDataList = f.read().splitlines()
        
        while True:
#         now this is the part I think I'd advice you adjust.
# There are two things you could possibly do here: 1. if you had a separate database table for the rc_ids instead of a text file, you would be able to have a complete separation of concerns
# and would be able to filter out the table with the rc_ids gotten from the user_scan.
# 2. It's no problem though; since you have the rc_id column in your User table(user model), you can can do something like:
            success, img = cap.read()
            for barcode in decode(img):
                myData = barcode.data.decode('utf-8')
                print(myData)
#        a.  Around here where you are checking if the myData exists in your textfile (myDataList), do something like:
#                 try:
#                   user_exists= User.objects.get(rc_id=myData).exists()
#                 except User.DoesNotExist:
#                       return redirect("signup_page")
#                 if user_exists:
#                         return render(request, "your_template.html", context)

# the code above should validate for you for each iteration, whether the rc_id exists in the user table or not.
                if myData in myDataList:
                    myOutput = 'Authorized'
                    myColor = (0,255,0)
                else:
                    myOutput = 'Un-Authorized'
                    myColor = (0, 0, 255)
        
                pts = np.array([barcode.polygon],np.int32)
                pts = pts.reshape((-1,1,2))
                cv2.polylines(img,[pts],True,myColor,5)
                pts2 = barcode.rect
                cv2.putText(img,myOutput,(pts2[0],pts2[1]),cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,myColor,2)
        
            cv2.imshow('Result',img)
            cv2.waitKey(1)
    
    except:
        return render(request,'user/auth.html')
