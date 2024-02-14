from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",views.index,name="index"),
    path("courses/",views.courses,name="courses"),
    path("books/",views.books,name="books"),
    path("blogs/",views.blogs,name="blogs"),
    path("course/<str:pk>/",views.course,name="course"),
    path("book/<str:pk>/",views.book,name="book"),
    path("blog/<str:pk>/",views.blog,name="blog"),
    path("like/<str:pk>/",views.blog_like_count,name="like"),
    path("dislike/<str:pk>/",views.blog_dislike_count,name="dislike"),
    path("courselike/<str:pk>/",views.course_like_count,name="courselike"),
    path("coursedislike/<str:pk>/",views.course_dislike_count,name="coursedislike"),
    path("about/",views.about,name="about"),
    path("log-in/",views.login_view,name="log-in"),
    path("log-out/",views.logout_view,name="log-out"),
    path("sign-in/",views.signin,name="sign-in"),
    path("dashboard/<str:pk>/",views.dashboard,name="dashboard"),
    path("dashboard/edit/<str:pk>/",views.dashboard_edit_info,name="dashboard-edit-info"),
    path("dashboard/courses/<str:pk>/",views.dashboard_edit_info,name="liked-course-list"),
    path("dashboard/blogs/<str:pk>/",views.dashboard_edit_info,name="liked-blog-list"),
    path("career/",views.career,name="career"),
    path("offers/",views.offers,name="offers"),
    path("mentor-join/",views.mentor_join,name="mentor-join"),
    path("mentor/<str:pk>/",views.mentor,name="mentor"),
    path("affiliate-join/",views.affiliate_join,name="affiliate-join"),
    path("privacy/",views.privacy,name="privacy"),
    path("refund-policy/",views.refund_policy,name="refund-policy"),
    path("terms-and-conditions/",views.terms_and_conditions,name="terms-and-conditions"),
    path("certificates/",views.certificates,name="certificates"),
    path("checkout/<str:pk>",views.checkout,name="checkout"),
    path("parentcourse/<str:pk>/",views.parentcourse,name="parentcourse"),
    path("enroll/<str:pk>/",views.enrolling,name="enroll")
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)