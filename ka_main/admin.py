from django.contrib import admin
from .models import *


@admin.register(RecordedCourse)
class RecordedCourseAdmin(admin.ModelAdmin):
    list_filter = ["for_index","offer",]
    search_fields = ["courseid","title"]

@admin.register(LiveCourse)
class LiveCourseAdmin(admin.ModelAdmin):
    list_filter = ["for_index","offer",]
    search_fields = ["courseid",]

@admin.register(RecordedClass)
class RecordedClassAdmin(admin.ModelAdmin):
    list_filter = ["courseid",]

@admin.register(LiveClass)
class RecordedClassAdmin(admin.ModelAdmin):
    list_filter = ["courseid",]

admin.site.register(Enrolled)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    search_fields = ["title",]

@admin.register(Faq)
class FaqAdmin(admin.ModelAdmin):
    list_filter = ["relatedid",]

admin.site.register(Purchased)
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_filter = ["totallikes","totalcomments","for_index","tag",]
    search_fields = ["tag","title",]

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_filter = ["blogid",]

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    search_fields = ["phone",]

@admin.register(MemberDetails)
class MemberDetailsAdmin(admin.ModelAdmin):
    search_fields = ["username","primary","email"]
    list_filter = ["allokay",]

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    search_fields = ["username","trxID","paymentID"]
    list_filter = ["status","username","relatedid"]

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    search_fields = ["username","courseid"]
    list_filter= ["courseid","username"]

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    search_fields = ["phone",]
    list_filter = ["phone",]