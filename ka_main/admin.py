from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Random_user)
class Random_userAdmin(admin.ModelAdmin):
    list_filter = ("user_ip",)

@admin.register(Signed_user)
class Signed_userAdmin(admin.ModelAdmin):
    search_fields = ("user_id","email","phone_number",)

@admin.register(User_Details)
class User_DetailsAdmin(admin.ModelAdmin):
    search_fields = ("user_id",)
    list_filter = ("blood_group","sex","s_class","s_group","date_joined","institution",)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ("downloads",)
    search_fields = ("book_id",)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    search_fields = ("course_id",)
    list_filter = ("created","likes","dislikes","for_index","for_top",)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    search_fields = ("blog_id",)
    list_filter = ("created","likes","dislikes","read_count",)

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    search_fields = ("related_id","user_id",)
    list_filter = ("related_id","user_id","created",)


@admin.register(Course_hub)
class Course_hubAdmin(admin.ModelAdmin):
    search_fields = ("c_hub_id",)
    list_filter = ("created","enrolled",)

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    search_fields = ("user_id",)

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    search_fields = ("user_id",)
    list_filter = ("phone_number","institution","phone_number",)

admin.site.register(IndexPromo)

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    search_fields = ("email","phone","name",)
    list_filter = ("date","email","phone","name",)

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_filter = ("for_index",)

admin.site.register(Terms_Conditions)


admin.site.register(Privacy)


admin.site.register(Refund_Policy)


@admin.register(UserConnectProduct)
class UserConnectProductAdmin(admin.ModelAdmin):
    search_fields = ("piduid",)
    list_filter = ("pid","uid",)

@admin.register(UserLikeBlog)
class UserLikeBlog(admin.ModelAdmin):
    list_filter = ("blog_id",)

@admin.register(UserDislikeBlog)
class UserDislikeBlog(admin.ModelAdmin):
    list_filter = ("blog_id",)

@admin.register(UserLikeCourse)
class UserLikeCourse(admin.ModelAdmin):
    list_filter = ("blog_id",)

@admin.register(UserDislikeCourse)
class UserDislikeCourse(admin.ModelAdmin):
    list_filter = ("blog_id",)