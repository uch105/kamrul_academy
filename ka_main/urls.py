from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.home,name="home"),
    #path("<str:pk>",views.callbackhome,name="callbackhome"),
    #path("parentcourses/",views.parentcourses,name="courses"),
    path("parentcourses/all-live",views.live_parentcourses,name="livecourses"),
    path("parentcourses/all-recorded",views.recorded_parentcourses,name="recordedcourses"),
    path("books/",views.books,name="books"),
    path("blogs/",views.blogs,name="blogs"),
    #path("course/<str:pk>/",views.course,name="course"),
    path("book/<str:pk>/",views.book,name="book"),
    path("blog/<str:pk>/",views.blog,name="blog"),
    path("like/<str:pk>/",views.like,name="like"),
    path("class/<str:pk>/<str:pk2>/",views.course_class,name="class"),
    #path("dislike/<str:pk>/",views.blog_dislike_count,name="dislike"),
    #path("courselike/<str:pk>/",views.course_like_count,name="courselike"),
    #path("coursedislike/<str:pk>/",views.course_dislike_count,name="coursedislike"),
    path("about/",views.about,name="about"),
    #path("sign-in/",views.sign_in,name="sign-in"),
    path("sign-out/",views.sign_out,name="sign-out"),
    path("sign-up/",views.sign_up,name="sign-up"),
    path("verify/<str:pk>/",views.verify_otp,name="otp"),
    path("dashboard/my-courses/",views.dashboard_my_courses,name="dashboard"),
    path("dashboard/live-courses/",views.dashboard_live_courses,name="dashboard-live-courses"),
    path("dashboard/certificate/",views.dashboard_certificate,name="dashboard-certificate"),
    path("dashboard/profile/",views.dashboard_profile,name="dashboard-profile"),
    path("dashboard/transaction/",views.dashboard_transaction,name="dashboard-transaction"),
    #path("dashboard/edit/<str:pk>/",views.dashboard_edit_info,name="dashboard-edit-info"),
    #path("dashboard/courses/<str:pk>/",views.dashboard_course_list,name="course-list"),
    #path("dashboard/live-courses/<str:pk>/",views.dashboard_live_course_list,name="live-course-list"),
    #path("mentor-join/",views.mentor_join,name="mentor-join"),
    #path("mentor/<str:pk>/",views.mentor,name="mentor"),
    path("privacy/",views.policy,name="privacy"),
    path("refund-policy/",views.refund,name="refund"),
    path("terms-and-conditions/",views.terms,name="terms"),
    path("checkout/<str:pk>",views.checkout,name="checkout"),
    path("parentcourse/<str:pk>/",views.parentcourse,name="parentcourse"),
    #path("enroll/<str:pk>/",views.enrolling,name="enroll")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)