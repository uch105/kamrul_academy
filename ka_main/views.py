from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,request,HttpRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from user_agents import parse
from requests import request
import requests
import datetime
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import *
from .forms import *
import random,string,json,time


ALPHA_NET_SMS_API_KEY = "qoIgUE6G3h395x1Ud6Swa6Y2Y9hgTqj41DAr2lje"
# global trackers and monitoring

def identify_browser(request):
    user_agent_str = request.META.get('HTTP_USER_AGENT','')
    user_agent = parse(user_agent_str)

    browser_info = user_agent.browser.family

    return browser_info

def identify_device(request):
    user_agent_str = request.META.get('HTTP_USER_AGENT','')
    user_agent = parse(user_agent_str)

    device_info = "Mobile" if user_agent.is_mobile else "Desktop"

    return device_info

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    return ip

def get_user_id(request):
    return request.user.id

def get_username(request):
    if logged_in(request):
        username = User.objects.get(id=get_user_id(request)).username
    else:
        username = "None"
    return username

def logged_in(request):
    return request.user.is_authenticated

def generate_otp():
    return str(random.randint(10000,99999))


def generate_password():
    uppercase_letters = string.ascii_uppercase
    lowercase_letters = string.ascii_lowercase
    special_characters = '!@#$%^&*()'
    password=[]
    password.append(random.choice(uppercase_letters))
    password.append(random.choice(lowercase_letters))
    password.append(random.choice(special_characters))
    for _ in range(9):
        password.append(random.choice(string.ascii_letters+string.digits+special_characters))
    random.shuffle(password)
    return ''.join(password)

# _______________________ functionalities ______________________

def home(request):

    if request.method == "POST":
        inquiry = Inquiry.objects.create(name=request.POST.get('name'),phone=request.POST.get('phone'),msg=request.POST.get('msg'))
        inquiry.save()

    lcourses = LiveCourse.objects.filter(for_index=True)
    rcourses = RecordedCourse.objects.filter(for_index=True)
    blogs = Blog.objects.filter(for_index=True)
    try:
        paymentID = request.GET.get("paymentID")
        status = request.GET.get("status")
        if status == "success":
            execute_payment(paymentID)
            url = "https://api.sms.net.bd/sendsms"
            phone = Member.objects.get(username=get_username(request)).phone
            payload = {'api_key': ALPHA_NET_SMS_API_KEY,
                'msg': 'Your purchase is successfull. Thank you for being a member!',
                'to': '88'+phone,
            }
            requests.request("POST", url, data=payload)
            context = {
                'lcourses':lcourses,
                'rcourses':rcourses,
                'blogs':blogs,
            }
            return render(request,"ka_main/index.html",context)
        else:
            context = {
                'lcourses':lcourses,
                'rcourses':rcourses,
                'blogs':blogs,
                }
            return render(request,"ka_main/index.html",context)

    except:
        context = {
            'lcourses':lcourses,
            'rcourses':rcourses,
            'blogs':blogs,
            }
    return render(request,"ka_main/index.html",context)

def about(request):
    return render(request,"ka_main/about.html")

def policy(request):
    return render(request,"ka_main/privacy.html")

def refund(request):
    return render(request,"ka_main/refund.html")

def terms(request):
    return render(request,"ka_main/terms.html")

def verify_otp(request,pk):
    
    if request.method == 'POST':
        entered_otp = str(request.POST.get("1"))+str(request.POST.get("2"))+str(request.POST.get("3"))+str(request.POST.get("4"))+str(request.POST.get("5"))
        
        stored_otp = request.session.get("otp")
        
        if entered_otp == stored_otp:
            if not Member.objects.filter(phone=pk).exists():
                username = "u"+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                password = generate_password()
                try:
                    member = Member.objects.create(username=username,password=password,phone=pk)
                    member.save()
                    print("member")
                    user = User.objects.create_user(username=username,password=password)
                    user.save()
                    print("user")
                    
                    auth_login(request,user)
                    return redirect("dashboard")
                except:
                    print("first except")
                    return render(request,"ka_main/signin.html",{'error': 'Failed! Try again!'})
            else:
                print("Existing user login")
                username = Member.objects.get(phone=pk).username
                user = User.objects.get(username=username)
                auth_login(request,user)
                return redirect("dashboard")
                #return render(request,"ka_main/signin.html",{'error':'Facing some internal error! Please contact authority!'})
        else:
            print("otp not match")
            return render(request,"ka_main/signin.html",{'error':'Facing some internal error! Please contact authority!'})
    return render(request,"ka_main/otp.html",{"phone":pk})

def sign_up(request):

    if request.method == 'POST':
        phone = request.POST.get("phone")
        url = "https://api.sms.net.bd/sendsms"
        otp = generate_otp()
        request.session['otp'] = otp
        payload = {'api_key': ALPHA_NET_SMS_API_KEY,
            'msg': 'Your OTP Code is '+ otp,
            'to': '88'+phone,
        }
        requests.request("POST", url, data=payload)
        return redirect("otp",pk=phone)
    
    return render(request,"ka_main/signin.html")

'''
def sign_in(request):
    context={}
    return render(request,"ka_main/login.html",context)
'''

def sign_out(request):
    logout(request)
    return redirect("home")

@login_required(login_url="/sign-up/")
def dashboard_my_courses(request):
    enrolls = Enrolled.objects.filter(username=get_username(request))
    recordedclass = []
    liveclass =[]
    for enroll in enrolls:
        try:
            theclasses = LiveCourse.objects.get(courseid=enroll.courseid)
            liveclass.append(theclasses)
        except:
            theclasses = RecordedCourse.objects.get(courseid=enroll.courseid)
            recordedclass.append(theclasses)

    yes = True if (len(recordedclass)+len(liveclass))!=0 else False

    context={
        'recordedclass': recordedclass,
        'liveclass': liveclass,
        'yes': yes,
    }
    return render(request,"ka_main/dashboard-my-courses.html",context)

@login_required(login_url="/sign-up/")
def dashboard_live_courses(request):
    enrolls = Enrolled.objects.filter(username=get_username(request))
    classes = []
    for enroll in enrolls :
        try:
            theclasses = LiveClass.objects.get(courseid=enroll.courseid)
            classes.append(theclasses)
        except:
            pass
    
    yes = False if len(classes)==0 else True
    context={
        'classes':classes,
        'yes': yes,
    }
    return render(request,"ka_main/dashboard-live-courses.html",context)

@login_required(login_url="/sign-up/")
def dashboard_certificate(request):
    certificates = Certificate.objects.filter(username=get_username(request))
    yes = True if len(certificates)!=0 else False
    context={
        'certificates': certificates,
    }
    return render(request,"ka_main/dashboard-certificate.html",context)

@login_required(login_url="/sign-up/")
def dashboard_profile(request):
    instance = MemberDetails.objects.get_or_create(username=get_username(request))
    if request.method == 'POST':
        instance = MemberDetails.objects.get(username=get_username(request))
        instance.dp = request.FILES['dp']
        instance.fullname = request.POST.get('fullname')
        instance.primary = request.POST.get('primary')
        instance.alternative = request.POST.get('alternative')
        instance.email = request.POST.get('email')
        instance.allokay = True
        instance.save()
    context={
        'instance':instance,
    }
    return render(request,"ka_main/dashboard-profile.html",context)

@login_required(login_url="/sign-up/")
def dashboard_transaction(request):
    alltrans = Enrolled.objects.filter(username=get_username(request))
    context={
        'alltrans': alltrans,
    }
    return render(request,"ka_main/dashboard-transaction.html",context)


def live_parentcourses(request):
    courses = LiveCourse.objects.all()
    context={
        'courses': courses,
    }
    return render(request,"ka_main/livecourses.html",context)

def recorded_parentcourses(request):
    courses = RecordedCourse.objects.all()
    context={
        'courses': courses,
    }
    return render(request,"ka_main/recordedcourses.html",context)

def parentcourse(request,pk):

    if pk[:4]=="live":
        course = LiveCourse.objects.get(courseid=pk)
        islive = True
        enrolleds = Enrolled.objects.filter(username=get_username(request),courseid=pk)
        enrolled = False if len(enrolleds)==0 else True
        faqs = Faq.objects.filter(relatedid = pk)
        
    else:
        course = RecordedCourse.objects.get(courseid=pk)
        islive = False
        enrolleds = Enrolled.objects.filter(username=get_username(request),courseid=pk)
        enrolled = True if len(enrolleds)==0 else False
        faqs = Faq.objects.filter(relatedid = pk)
        

    context={
        'course': course,
        'islive': islive,
        'enrolled': enrolled,
        'faqs': faqs,
    }
    return render(request,"ka_main/course.html",context)


def course_class(request,pk,pk2):

    classes = RecordedClass.objects.filter(courseid=pk)
    theclass = RecordedClass.objects.get(classid=pk2)
    courseid = pk
    context = {
        'classes': classes,
        'theclass': theclass,
        'courseid': courseid,
    }
    return render(request,"ka_main/class.html",context)

def books(request):
    books = Book.objects.all()
    context={
        'books':books,
        }
    return render(request,"ka_main/books.html",context)

def book(request,pk):
    book = Book.objects.get(bookid=pk)
    purchased = Purchased.objects.get(bookid=pk,userid=get_username(request)).status
    faqs = Faq.objects.filter(relatedid=pk)
    context={
        'book':book,
        'purchased':purchased,
        'faqs': faqs,
    }
    return render(request,"ka_main/book.html",context)

def blogs(request):
    blogs = Blog.objects.all().order_by('-created')
    context={
        'blogs':blogs,
    }
    return render(request,"ka_main/blogs.html",context)

def blog(request,pk):

    if request.method=="POST":
        comment=request.POST.get('comment')
        instance = BlogComment.objects.create(username=get_username(request),blogid=pk,comment=comment)
        instance.save()
        ainstance = Blog.objects.get(blogid=pk)
        ainstance.totalcomments+=1
        ainstance.save()
        pk=pk
        return redirect("blog",pk)

    blog = Blog.objects.get(blogid=pk)
    comments = BlogComment.objects.filter(blogid=pk)
    context={
        'blog':blog,
        'comments':comments,
    }
    return render(request,"ka_main/blog.html",context)

@require_POST
@login_required(login_url="/sign-up/")
def like(request,pk):
    instance = Blog.objects.get(blogid=pk)
    instance.totallikes+=1
    instance.save()
    pk=pk
    return redirect("blog",pk)


@login_required(login_url="/sign-up/")
@require_POST
def blog_comment(request,pk):
    instance = Blog.objects.get(blogid=pk)
    if request.method == 'POST':
        username = get_username(request)
        comment = request.POST.get("body")
        instance2 = BlogComment.objects.create(blogid=pk,username=username,comment=comment)
        instance2.save()
        instance.totalcomments+=1
        instance.save()
        return redirect("blog",pk)
    return redirect("blog",pk)





# checkout process & payment section ............

SANDBOX_APP_KEY = '8o2NKRBt9DM3n0e6OXkO8eKftc'

SANDBOX_APP_SECRET_KEY = 'xYQO1NscWgNXL52P2pNRDvVFXtcm5IMi8Gx2BCJvFm2wLeV3LnFK'

SANDBOX_USERNAME = '01323314826'

SANDBOX_PASSWORD = '5<I|PK:xdWq'

GRANT_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant'

REFRESH_TOKEN_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/token/refresh'

CREATE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create'

EXECUTE_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/execute'

QUERY_PAYMENT_URL = 'https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/payment/status'

CALL_BACK_URL = 'kamrulacademy.com'


@login_required(login_url="/sign-up/")
def checkout(request,pk):
    try:
        try:
            instance = RecordedCourse.objects.get(courseid=pk)
            bookinstance = False
        except:
            instance = LiveCourse.objects.get(courseid=pk)
            bookinstance = False
    except:
        instance = Book.objects.get(bookid=pk)
        bookinstance = True
    
    amount = instance.fee
    #invoice_no = "INV"+generate_otp()
    title = instance.title
    id=pk

    context={
        'amount': amount,
        #'invoice_no': invoice_no,
        'title': title,
        'id': id,
    }

    if request.method=='POST':
        payment_type = request.POST.get("payment")
        if payment_type == "bkash":
            try:
                try:
                    invoice_no = "INV"+generate_otp()
                    invoice = Invoice.objects.create(invoice=invoice_no,username=get_username(request),relatedid=id)
                    if bookinstance:
                        bookpurchase = Purchased.objects.create(purchaseid=invoice_no,bookid=id,userid=get_username(request))
                    else:
                        coursepurchase = Enrolled.objects.create(username=get_username(request),courseid=id,way=payment_type,amount=amount)

                except:
                    invoice_no = "INV"+generate_otp()
                    invoice = Invoice.objects.create(invoice=invoice_no,username=get_username(request),relatedid=id)
                    if bookinstance:
                        bookpurchase = Purchased.objects.create(purchaseid=invoice_no,bookid=id,userid=get_username(request))
                    else:
                        coursepurchase = Enrolled.objects.create(username=get_username(request),courseid=id,way=payment_type,amount=amount)
                
                id_token = grant_payment(invoice_no)
                return create_payment(amount,id_token,invoice_no)
            except:
                return render(request,"ka_main/checkout.html",context)

        else:
            return render(request,"ka_main/payment.html")

    return render(request,"ka_main/checkout.html",context)

def grant_payment(invoice_no):

    grant_payload = {
        "app_key": SANDBOX_APP_KEY,
        "app_secret": SANDBOX_APP_SECRET_KEY
        }
    grant_headers = {
        "accept": "application/json",
        "username": SANDBOX_USERNAME,
        "password": SANDBOX_PASSWORD,
        "content-type": "application/json"
        }
    grant_response = requests.post(GRANT_TOKEN_URL , json=grant_payload, headers=grant_headers)

    grant_json = grant_response.text
    grant_json_data = json.loads(grant_json)

    id_token = grant_json_data['id_token']
    refresh_token = grant_json_data['refresh_token']

    invoice = Invoice.objects.get(invoice=invoice_no)
    invoice.id_token = id_token
    invoice.refresh_token = refresh_token
    invoice.save()

    return id_token

def create_payment(amount,id_token,invoice_no):
                
    create_payload = {
        "mode": "0011",
        "payerReference": "KamrulAcademy",
        "callbackURL": 'https://kamrulacademy.com/',
        "amount": str(amount),
        "intent": "sale",
        "currency": "BDT",
        "merchantInvoiceNumber": invoice_no,
    }
    create_headers = {
        "accept": "application/json",
        "Authorization": id_token,
        "X-APP-Key": SANDBOX_APP_KEY,
        "content-type": "application/json"
    }
    create_response = requests.post(CREATE_PAYMENT_URL , json=create_payload, headers=create_headers)

    create_json = create_response.text
    create_json_data = json.loads(create_json)
    paymentID = create_json_data["paymentID"]
    bkash_url = create_json_data["bkashURL"]

    invoice = Invoice.objects.get(invoice=invoice_no)
    invoice.paymentID = paymentID
    invoice.save()

    return redirect(bkash_url)

def execute_payment(paymentID):

    invoice = Invoice.objects.get(paymentID=paymentID)
        
    execute_payload = {
        "paymentID" : invoice.paymentID,#paymentID
    }
    execute_headers = {
        "accept": "application/json",
        "Authorization": invoice.id_token,#id_token
        "X-APP-Key": SANDBOX_APP_KEY,
        "content-type": "application/json"
    }

    execute_response = requests.post(EXECUTE_PAYMENT_URL , json=execute_payload, headers=execute_headers)

    execute_json = execute_response.text
    print(execute_json)
    if invoice.relatedid[:4]=="book":
        bookpurchase = Purchased.objects.get(purchaseid=invoice.invoice)
        bookpurchase.status = True
        bookpurchase.save()
    else:
        coursepurchase = Enrolled.objects.get(courseid=invoice.relatedid,username=invoice.username)
        coursepurchase.status = True
        coursepurchase.save()
        if invoice.relatedid[:4]=="live":
            course = LiveCourse.objects.get(courseid=invoice.relatedid)
            course.total_enrolled = course.total_enrolled + 1
            course.save()
        else:
            course = RecordedCourse.objects.get(courseid=invoice.relatedid)
            course.total_enrolled = course.total_enrolled + 1
            course.save()
    execute_json_data = json.loads(execute_json)
    invoice.trxID = execute_json_data["trxID"]
    invoice.save()
    return True