from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,request,HttpRequest,JsonResponse
from django.http.response import StreamingHttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User 
from user_agents import parse
from requests import request
import requests
import datetime
from django.http import FileResponse, Http404
import os
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import *
from .forms import *
from .bkash import grant_payment,create_payment,execute_payment
from .bn_nums import to_bn,to_num
import random,string,json,time
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
#from .camera import VideoCamera,IPWebCam,MaskDetect,LiveWebCam


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
            theclasses = LiveCourse.objects.get(id=enroll.courseid)
            liveclass.append(theclasses)
        except:
            theclasses = RecordedCourse.objects.get(id=enroll.courseid)
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
    for enroll in enrolls:
        try:
            course = LiveCourse.objects.get(id=enroll.courseid)
            modules = LiveCourseModule.objects.filter(course=course)
            for module in modules:
                classes.append(LiveCourseModuleClass.objects.filter(module=module,class_ongoing=True))
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
        'yes':yes,
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


def live_courses(request):
    courses = LiveCourse.objects.all()
    context={
        'courses': courses,
    }
    return render(request,"ka_main/live/list.html",context)

def recorded_courses(request):
    courses = RecordedCourse.objects.all()
    context={
        'courses': courses,
    }
    return render(request,"ka_main/recorded/list.html",context)

def livecourse(request,pk):
    course = LiveCourse.objects.get(id=pk)
    modules = LiveCourseModule.objects.filter(course=course)
    enrolled_check = Enrolled.objects.filter(username=get_username(request),courseid=pk)
    if len(enrolled_check) == 0:
        enrolled = False
    else:
        enrolled = True

    context={
        'enrolled':enrolled,
        'course':course,
        'modules':modules,
    }
    return render(request,"ka_main/live/course.html",context)

def recordedcourse(request,pk):
    course = RecordedCourse.objects.get(id=pk)
    modules = RecordedCourseModule.objects.filter(course=course)
    rcpt = []
    enrolled_check = Enrolled.objects.filter(username=get_username(request),courseid=pk)
    if len(enrolled_check) == 0:
        enrolled = False
    else:
        enrolled = True
        rcpt = RecordedCourseProgressTracking.objects.filter(username=get_username(request),course=course)
    context = {
        'course':course,
        'enrolled':enrolled,
        'modules':modules,
        'rcpt':rcpt,
    }
    return render(request,"ka_main/recorded/course.html",context)

@require_POST
def recordedcoursenoti(request,pk):
    course = RecordedCourse.objects.get(id=pk)
    rcn_instance = RecordedCourseNotification.objects.get_or_create(username=get_username(request),course=course)
    rcn_instance.alert = True
    rcn_instance.save()

def recordedcoursenotif(request,pk,pk2):
    course = RecordedCourse.objects.get(id=pk)
    rcn_instance = RecordedCourseNotification.objects.get_or_create(username=get_username(request),course=course)
    rcn_instance.frequency = int(pk2)
    rcn_instance.save()
    return redirect('rclass',pk=pk,pk2="১")

def recordedclass(request,pk,pk2):
    course = RecordedCourse.objects.get(id=pk)
    modules = RecordedCourseModule.objects.filter(course=course)
    pk2 = int(to_num(pk2))
    prev_pk2 = pk2-1
    if prev_pk2<0:
        prev_pk2 = "১"
    else:
        prev_pk2 = to_bn(str(prev_pk2))
    if pk2+1 == len(modules):
        next_pk2 = to_bn(str(pk2))
    else:
        next_pk2 = to_bn(str(pk2+1))
    module = modules[pk2]
    context = {
        'course':course,
        'modules':modules,
        'module':module,
        'next_pk2':next_pk2,
        'this_pk2':to_bn(str(pk2)),
        'prev_pk2':prev_pk2,
    }
    return render(request,"ka_main/recorded/class.html",context)

def liveclass(request):
    
    context = {
        
    }
    return render(request,"ka_main/live/class.html",context)

def livestream(request):
    if request.method == "POST":
        moduleid = request.POST.get("module")
        class_serial = request.POST.get("serial")
        done = True if request.POST.get("done") == 'on' else False
        ongoing = True if request.POST.get("ongoing") == 'on' else False
        link = request.POST.get("link")
        date_time = request.POST.get("datetime")
        module = LiveCourseModule(id=moduleid)
        instance = LiveCourseModuleClass.objects.get_or_create(module=module,class_serial=class_serial)
        instance.class_done = done
        instance.class_link = link
        instance.class_date = date_time
        instance.class_ongoing = ongoing
        instance.save()
        return redirect("lstream")
    context = {
        
    }
    return render(request,"ka_main/live/stream.html",context)

'''
@csrf_exempt
def upload_capture(request):
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        with open(f'media/captures/{uploaded_file.name}', 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        return JsonResponse({'message': 'File uploaded successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request'}, status=400)
'''
@csrf_exempt
def upload_capture(request):
    if request.method == 'POST':
        file = request.FILES['file']
        file_name = default_storage.save('recordings/' + file.name, file)
        return JsonResponse({'message': 'File uploaded successfully', 'file_name': file_name})
    return JsonResponse({'message': 'Only POST method is allowed'}, status=405)


def stream_video_chunk(request, chunk_name):
    file_path = os.path.join(settings.MEDIA_ROOT, 'video_chunks', chunk_name)

    if not os.path.exists(file_path):
        raise Http404("Chunk not found")

    return FileResponse(open(file_path, 'rb'), content_type='video/webm')

def recordedassignment(request,pk,pk2):
    if request.method == "POST":
        ass = request.FILES["ass"]
        course = RecordedCourse.objects.get(id=pk)
        modules = RecordedCourseModule.objects.filter(course=course)
        pk2 = int(to_num(pk2))
        module = modules[pk2]
        assignment = RecordedCourseAssignmentSubmission.objects.get_or_create(course=course,module=module,username=get_username(request),file=ass)
        assignment.save()
        return redirect("rquiz",pk=course.id,pk2=to_bn(str(pk2)))
    course = RecordedCourse.objects.get(id=pk)
    modules = RecordedCourseModule.objects.filter(course=course)
    pk2 = int(to_num(pk2))
    prev_pk2 = pk2-1
    if prev_pk2<0:
        prev_pk2 = "১"
    else:
        prev_pk2 = to_bn(str(prev_pk2))
    next_pk2 = to_bn(str(pk2+1))
    module = modules[pk2]
    context = {
        'course':course,
        'modules':modules,
        'module':module,
        'next_pk2':next_pk2,
        'this_pk2':to_bn(str(pk2)),
        'prev_pk2':prev_pk2,
    }
    return render(request,"ka_main/recorded/assignment.html",context)

def recordedquiz(request,pk,pk2):
    if request.method == "POST":
        course = RecordedCourse.objects.get(id=pk)
        modules = RecordedCourseModule.objects.filter(course=course)
        pk2 = int(to_num(pk2))
        module = modules[pk2]
        questions = Question.objects.filter(course=course,module=module)
        score = 0
        for ques in questions:
            ans = request.POST.get(str(ques.serial))
            if ans == ques.answer5:
                score += 1
            else:
                score = score
        score = (score/len(questions))*100
        score = to_bn(str(score))+"%"
        quiz_result = QuizResult.objects.get_or_create(course=course,module=module,username=get_username(request),score=score)
        quiz_result.save()
        prev_pk2 = pk2-1
        if prev_pk2<0:
            prev_pk2 = "১"
        else:
            prev_pk2 = to_bn(str(prev_pk2))
        next_pk2 = to_bn(str(pk2+1))
        context = {
            'course':course,
            'modules':modules,
            'module':module,
            'next_pk2':next_pk2,
            'this_pk2':to_bn(str(pk2)),
            'prev_pk2':prev_pk2,
            'questions':questions,
        }
        return redirect("rquiz",pk=course.id,pk2=to_bn(str(pk2)))

    course = RecordedCourse.objects.get(id=pk)
    modules = RecordedCourseModule.objects.filter(course=course)
    pk2 = int(to_num(pk2))
    prev_pk2 = pk2-1
    if prev_pk2<0:
        prev_pk2 = "১"
    else:
        prev_pk2 = to_bn(str(prev_pk2))
    next_pk2 = to_bn(str(pk2+1))
    module = modules[pk2]
    questions = Question.objects.filter(course=course,module=module)
    try:
        quiz_result = QuizResult.objects.filter(course=course,module=module,username=get_username(request))
        score = quiz_result[0].score
    except:
        score = "০%"
    context = {
        'course':course,
        'modules':modules,
        'module':module,
        'next_pk2':next_pk2,
        'this_pk2':to_bn(str(pk2)),
        'prev_pk2':prev_pk2,
        'questions':questions,
        'score':score,
    }
    return render(request,"ka_main/recorded/quiz.html",context)

def books(request):
    books = Book.objects.all()
    context={
        'books':books,
        }
    return render(request,"ka_main/books.html",context)

def book(request,pk):
    book = Book.objects.get(bookid=pk)
    try:
        purchased = Purchased.objects.get(bookid=pk,userid=get_username(request)).status
    except:
        purchased = False
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


@login_required(login_url="/sign-up/")
def checkout(request,pk):
    try:
        try:
            instance = RecordedCourse.objects.get(id=pk)
            bookinstance = False
        except:
            instance = LiveCourse.objects.get(id=pk)
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
                    
                    if bookinstance:
                        bookpurchase = Purchased.objects.create(purchaseid=invoice_no,bookid=id,userid=get_username(request))
                    else:
                        coursepurchase = Enrolled.objects.create(username=get_username(request),courseid=id,way=payment_type,amount=amount)

                except:
                    
                    if bookinstance:
                        bookpurchase = Purchased.objects.create(purchaseid=invoice_no,bookid=id,userid=get_username(request))
                    else:
                        coursepurchase = Enrolled.objects.create(username=get_username(request),courseid=id,way=payment_type,amount=amount)
                

                id_token = grant_payment()
                invoice_no = "INV"+generate_otp()
                invoice = Invoice.objects.create(invoice=invoice_no,username=get_username(request),relatedid=id,id_token=id_token)
                invoice.save()
                
                return create_payment(amount,id_token,invoice_no)
            except:
                
                return render(request,"ka_main/checkout.html",context)

        else:
            return render(request,"ka_main/payment.html")

    return render(request,"ka_main/checkout.html",context)

# ----------------------- admin panel ------------------------ #
def admin_login(request):
    context = {}
    return render(request,"ka_main/admin/admin-login.html",context)

def admin_join(request):
    context = {}
    return render(request,"ka_main/admin/admin-join.html",context)

def hr_dashboard(request):
    context = {}
    return render(request,"ka_main/admin/hr-dashboard.html",context)



# ----------------------------------- camera stream ----------- #
'''
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n'+ frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),content_type='multipart/x-mixed-replace; boundary=frame')

def webcam_feed(request):
    return StreamingHttpResponse(gen(IPWebCam()),content_type='multipart/x-mixed-replace; boundary=frame')

def mask_feed(request):
    return StreamingHttpResponse(gen(MaskDetect()),content_type='multipart/x-mixed-replace; boundary=frame')

def livecam_feed(request):
    return StreamingHttpResponse(gen(LiveWebCam()),content_type='multipart/x-mixed-replace; boundary=frame')

    '''