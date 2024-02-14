from django.shortcuts import render,redirect
from django.http import HttpResponse,request,HttpRequest,JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate,logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User 
from user_agents import parse
from requests import request
import requests
import datetime
from django.core.mail import send_mail
from django.http.request import HttpRequest
from .models import *
from .forms import *

# Create your views here.

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

@require_POST
def blog_like_count(request,pk):
    try:
        instance = Blog.objects.get(blog_id=pk)
        instance.likes +=1
        instance.save()
        instance2 = UserLikeBlog.objects.create(username=get_username(request),blog_id=pk)
        instance2.save()
        return redirect('blog',pk=pk)
    except:
        return redirect('blog',pk=pk)

@require_POST
def blog_dislike_count(request,pk):
    try:
        instance = Blog.objects.get(blog_id=pk)
        instance.dislikes +=1
        instance.save()
        instance2 = UserDislikeBlog.objects.create(username=get_username(request),blog_id=pk)
        instance2.save()
        return redirect('blog',pk=pk)
    except:
        return redirect('blog',pk=pk)

@require_POST
def course_like_count(request,pk):
    try:
        instance = Course.objects.get(course_id=pk)
        instance.likes +=1
        instance.save()
        instance2 = UserLikeCourse.objects.create(username=get_username(request),blog_id=pk)
        instance2.save()
        return redirect('course',pk=pk)
    except:
        return redirect('course',pk=pk)

@require_POST
def course_dislike_count(request,pk):
    try:
        instance = Course.objects.get(course_id=pk)
        instance.dislikes +=1
        instance.save()
        instance2 = UserDislikeCourse.objects.create(username=get_username(request),blog_id=pk)
        instance2.save()
        return redirect('course',pk=pk)
    except:
        return redirect('course',pk=pk)

def get_user_id(request):
    return request.user.id

def get_username(request):
    return User.objects.get(id=get_user_id(request)).username

def logged_in(request):
    return request.user.is_authenticated

# webpage rendering

def index(request):
    if request.method == 'POST':
        form = request.POST
        name = form.get("name")
        email = form.get("email")
        phone = form.get("phone")
        text = form.get("message")

        device = identify_device(request)
        if device == "Desktop":
            template_name = 'ka_main/web/index.html'
        else:
            template_name = 'ka_main/mobile/index.html'

        Inquiry.objects.create(name=name,email=email,phone=phone,text=text)

        promos = IndexPromo.objects.all()
        courses = Course.objects.filter(for_index=True)
        faqs = Faq.objects.filter(for_index=True)
        context = {
            'promos': promos,
            'courses': courses,
            'faqs' : faqs,
        }

        return render(request, template_name , context=context)
    device = identify_device(request)
    promos = IndexPromo.objects.all()
    courses = Course.objects.filter(for_index=True)
    faqs = Faq.objects.filter(for_index=True)
    context = {
        'promos': promos,
        'courses': courses,
        'faqs' : faqs,
    }

    if device == "Desktop":
        template_name = 'ka_main/web/index.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    return render(request, template_name , context=context)

def courses(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/courses.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    top_courses = Course.objects.filter(for_top = True)
    courses = Course.objects.all()
    context = {
        'top_courses':top_courses,
        'courses':courses,
    }
    return render(request,template_name,context)

def course(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/course.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    if request.method == 'POST':
        body = request.POST.get("body")
        uid = get_username(request)
        piduid = uid + pk
        if UserConnectProduct.objects.filter(piduid=piduid).exists():
            purchased = True
        else:
            purchased = False

        comment = Comments.objects.create(related_id=pk,user_id=uid,body=body)
        comment.save()
        course = Course.objects.get(course_id=pk)
        comments = Comments.objects.filter(related_id=pk)
        try:
            liked = UserLikeCourse.objects.filter(username=get_username(request),blog_id=pk).exists()
            disliked = UserDislikeCourse.objects.filter(username=get_username(request),blog_id=pk).exists()
        except:
            liked = False
            disliked = False
        context = {
            'course':course,
            'purchased':purchased,
            'comments':comments,
            'liked':liked,
            'disliked':disliked,
        }

        return render(request,template_name,context)
    
    course = Course.objects.get(course_id=pk)
    comments = Comments.objects.filter(related_id=pk)
    if logged_in(request):
        uid = get_username(request)
        piduid = uid + pk
        if UserConnectProduct.objects.filter(piduid=piduid).exists():
            purchased = True
        else:
            purchased = False
    else:
        purchased = False
    
    try:
        liked = UserLikeCourse.objects.filter(username=get_username(request),blog_id=pk).exists()
        disliked = UserDislikeCourse.objects.filter(username=get_username(request),blog_id=pk).exists()
    except:
        liked = False
        disliked = False
    context = {
        'course':course,
        'purchased':purchased,
        'comments':comments,
        'liked':liked,
        'disliked':disliked,
    }
    
    return render(request,template_name,context)

def books(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/books.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    books = Book.objects.all()
    context = {
        'books':books,
    }

    return render(request,template_name,context)

def book(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/book.html'
    else:
        template_name = 'ka_main/mobile/index.html'

    book = Book.objects.get(book_id=pk)
    if logged_in(request):
        uid = get_username(request)
        piduid = uid + pk
        if UserConnectProduct.objects.filter(piduid=piduid).exists():
            purchased = True
        else:
            purchased = False
    else:
        purchased = False
    context = {
        'book':book,
        'purchased':purchased,
    }

    return render(request, template_name,context)

def blogs(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/blogs.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    blogs = Blog.objects.all()

    context = {
        'blogs':blogs,
    }

    return render(request,template_name,context)

def blog(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/blog.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    if request.method == 'POST':
        body = request.POST.get("body")
        uid = get_username(request)
        comment = Comments.objects.create(related_id=pk,user_id=uid,body=body)
        comment.save()
        blog = Blog.objects.get(blog_id=pk)
        comments = Comments.objects.filter(related_id=pk)
        try:
            liked = UserLikeBlog.objects.filter(username=get_username(request),blog_id=pk).exists()
            disliked = UserDislikeBlog.objects.filter(username=get_username(request),blog_id=pk).exists()
        except:
            liked = False
            disliked = False
        context = {
            'blog':blog,
            'comments':comments,
            'liked':liked,
            'disliked':disliked,
        }

        return render(request,template_name,context)
    
    try:
        liked = UserLikeBlog.objects.filter(username=get_username(request),blog_id=pk).exists()
        disliked = UserDislikeBlog.objects.filter(username=get_username(request),blog_id=pk).exists()
    except:
        liked = False
        disliked = False
    blog = Blog.objects.get(blog_id=pk)
    comments = Comments.objects.filter(related_id=pk)

    context = {
        'blog':blog,
        'comments':comments,
        'liked':liked,
        'disliked':disliked,
    }

    return render(request,template_name,context)

def about(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/about.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def login_view(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/login.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    if request.method == 'POST':
        instance_username = request.POST.get("username")
        try:
            try:
                username = Signed_user.objects.get(email = instance_username).user_id
            except:
                username = Signed_user.objects.get(phone_number = instance_username).user_id
        except:
            return render(request, template_name,{'error':'Invalid credentials!'})

        password = request.POST.get("password")

        user = authenticate(request, username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect('dashboard',pk=username)
        else:
            return render(request, template_name,{'error':'Invalid credentials!'})
    
    return render(request,template_name)

def dashboard(request,pk):
    signed_user = Signed_user.objects.get(user_id=pk)
    user_details = User_Details.objects.get(user_id=pk)
    liked_courses = len(UserLikeCourse.objects.filter(username=pk))
    liked_blogs = len(UserLikeBlog.objects.filter(username=pk))
    context = {
        'signed_user':signed_user,
        'user_details':user_details,
        'liked_courses':liked_courses,
        'liked_blogs':liked_blogs,
    }

    return render(request,'ka_main/web/dashboard.html',context)

def dashboard_edit_info(request,pk):
    if request.method == 'POST':
        instance = User_Details.objects.get(user_id=pk)
        instance.nationality = request.POST.get("nationality")
        instance.address = request.POST.get("address")
        instance.institution = request.POST.get("institution")
        instance.s_class = request.POST.get("s_class")
        instance.s_group = request.POST.get("s_group")
        sexstr = request.POST.get("sex")
        if sexstr == "Male":
            instance.sex = True
        else:
            instance.sex = False
        
        instance.save()
        return redirect('dashboard',pk)
        
    signed_user = Signed_user.objects.get(user_id=pk)
    user_details = User_Details.objects.get(user_id=pk)
    liked_courses = len(UserLikeCourse.objects.filter(username=pk))
    liked_blogs = len(UserLikeBlog.objects.filter(username=pk))
    context = {
        'signed_user':signed_user,
        'user_details':user_details,
        'liked_courses':liked_courses,
        'liked_blogs':liked_blogs,
    }
    return render(request,'ka_main/web/edit-info.html',context)

def liked_course_list(request,pk):
    pass

def liked_blog_list(request,pk):
    pass


def signin(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/signin.html'
    else:
        template_name = 'ka_main/mobile/index.html'

    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        try:
            query = Signed_user.objects.filter(phone_number=phone)
            if not query.exists():
                if password1 == password2 :
                    username = 'u'+datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    password = password1
                    try:
                        user = User.objects.create_user(username=username,email=email,password=password)
                        user.save()
                        signed_user = Signed_user.objects.create(user_id=username,name=fullname,email=email,phone_number=phone)
                        signed_user.save()
                        user_details = User_Details.objects.create(user_id = username)
                        user_details.save()
                        auth_login(request,user)
                        return redirect('dashboard',pk=username)
                    except:
                        return render(request,template_name,{'error':"Some error occured!",})
                else:
                    return render(request,template_name,{'error':"Password Does Not Match!",})
            else:
                return render(request,template_name,{'error':"Phone Number Already Exists!",})
        except:
            return render(request,template_name,{'error':"Some error occured! Please Try Again!",})
    
    return render(request, template_name)

def send_mail():
    subject= 'subject'
    message = 'Mesage body'
    from_email = 'example@example.com'
    recipient_list = ['example@example.com',]

    send_mail(subject,message,from_email,recipient_list)

def logout_view(request):
    logout(request)
    return redirect("log-in")

def career(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/career.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def offers(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/offers.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def mentor_join(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/mentorjoin.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def mentor(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/mentor.html'
    else:
        template_name = 'ka_main/mobile/mentor.html'
    
    mentor = Mentor.objects.get(user_id=pk)
    context = {
        'mentor':mentor,
    }
    
    #return render(request,template_name)
    return render(request,template_name,context)

def affiliate_join(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/affiliate.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def privacy(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/privacy.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    text = Privacy.objects.all()
    context = {'text': text,}
    
    return render(request,template_name,context)

def refund_policy(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/refund.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    text = Refund_Policy.objects.all()
    context = {'text': text,}
    
    return render(request,template_name,context)

def terms_and_conditions(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/terms.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    text = Terms_Conditions.objects.all()
    context = {'text': text,}
    
    return render(request,template_name,context)

def certificates(request):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/about.html'
    else:
        template_name = 'ka_main/mobile/index.html'
    
    return render(request,template_name)

def parentcourse(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/parentcourse.html'
    else:
        template_name = 'ka_main/mobile/parentcourse.html'
    
    instance = ParentcourseTypeOne.objects.get(courseId=pk)
    mentor = Mentor.objects.get(user_id=instance.mentorId)
    curriculums = Curriculum.objects.filter(courseId=pk)

    context = {
        'instance':instance,
        'mentor':mentor,
        'çurriculums':curriculums,
    }
    
    return render(request,template_name,context)

def checkout(request,pk):
    try:
        instance = Course.objects.get(course_id=pk)
        name = instance.title
        instance_price = instance.course_fee
    except:
        instance = Book.objects.get(book_id=pk)
        instance_price = instance.price
        name = instance.name
    
    pk=pk
    context = {
        'name': name,
        'instance_price': instance_price,
        'pk':pk,
    }

    if request.method == "POST":
        payment = request.POST.get("payment")
        if payment == "bkash":

            #grant token
            
            url = "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant"

            payload = {
                "app_key": "4f6o0cjiki2rfm34kfdadl1eqq",
                "app_secret": "2is7hdktrekvrbljjh44ll3d9l1dtjo4pasmjvs5vl5qr3fug4b"
            }
            headers = {
                "accept": "application/json",
                "username": "sandboxTokenizedUser02",
                "password": "sandboxTokenizedUser02",
                "content-type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

    return render(request,'ka_main/web/checkout.html',context)

def enrolling(request,pk):
    device = identify_device(request)
    if device == "Desktop":
        template_name = 'ka_main/web/enroll.html'
    else:
        template_name = 'ka_main/mobile/enroll.html'
    
    if request.method == 'POST':
        email = request.POST.get('email')
        phone = request.POST.get('phone')

        instance = Enrollment.objects.create(courseId=pk,user=email,phone=phone,enrolled=True)
        return redirect("parentcourse",pk)
    
    instance = ParentcourseTypeOne.objects.get(courseId=pk)
    context = {
        'instance':instance,
    }

    return render(request,template_name,context)



# ==========================mobile application json responses=======================