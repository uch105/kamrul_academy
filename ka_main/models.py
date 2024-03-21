from django.db import models
from django.db.models import Model
from tinymce.models import HTMLField

class RecordedCourse(models.Model):
    courseid = models.CharField(max_length=50,unique=True,primary_key=True)
    title = models.TextField()
    banner = models.ImageField(upload_to="media/images/recorded/",blank=True,null=True)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    isitlive = models.BooleanField(default=False)
    for_index = models.BooleanField(default=False)
    #for_top = models.BooleanField(default=False)
    total_duration = models.IntegerField(default=0)
    total_class = models.IntegerField(default=0)
    total_exam = models.IntegerField(default=0)
    total_enrolled = models.IntegerField(default=0)
    offer = models.BooleanField(default=False)
    promocode = models.CharField(max_length=10,blank=True,null=True)
    saving = models.IntegerField(default=0)
    savingfrom = models.IntegerField(default=0)
    expiry_date = models.CharField(max_length=100)
    fee = models.IntegerField(default=0)
    firstclass = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.title

class RecordedClass(models.Model):
    classid = models.CharField(max_length=100,blank=True,null=True)
    courseid = models.CharField(max_length=100,blank=True,null=True)
    title = models.TextField()
    notes = models.FileField(upload_to="media/notes/recorded/",blank=True,null=True)
    video = models.FileField(upload_to="media/videos/recorded/",blank=True,null=True)

    def __str__(self):
        return self.title

class LiveCourse(models.Model):
    courseid = models.CharField(max_length=50,unique=True,primary_key=True)
    title = models.TextField()
    utubelink = models.CharField(max_length=100,blank=True,null=True)
    banner = models.ImageField(upload_to="media/images/live/",blank=True,null=True)
    showlink = models.BooleanField(default=False)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    total_enrolled = models.IntegerField(default=0)
    isitlive = models.BooleanField(default=True)
    for_index = models.BooleanField(default=False)
    #for_top = models.BooleanField(default=False)
    offer = models.BooleanField(default=False)
    promocode = models.CharField(max_length=10,blank=True,null=True)
    saving = models.IntegerField(default=0)
    savingfrom = models.IntegerField(default=0)
    expiry_date = models.CharField(max_length=100,blank=True,null=True)
    fee = models.IntegerField(default=0)
    startdate = models.CharField(max_length=100,blank=True,null=True)
    classtime = models.CharField(max_length=100,blank=True,null=True)
    classday = models.CharField(max_length=100,blank=True,null=True)
    batchno = models.CharField(max_length=20,blank=True,null=True)
    seatremaining = models.IntegerField(default=50)
    daysremaining =models.IntegerField(default=50)

    def __str__(self):
        return self.title
    
class LiveClass(models.Model):
    classid = models.CharField(max_length=100,blank=True,null=True)
    courseid = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    startdate = models.CharField(max_length=100,blank=True,null=True)
    link = models.CharField(max_length=100,blank=True,null=True)
    date = models.CharField(max_length=100,blank=True,null=True)
    schedule = models.CharField(max_length=100,blank=True,null=True)
    
class Enrolled(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    courseid = models.CharField(max_length=100,blank=True,null=True)
    #islive = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    way = models.CharField(max_length=100,blank=True,null=True)
    issuetime = models.DateTimeField(auto_now=True)
    amount = models.IntegerField(default=0)
    
class Book(models.Model):
    bookid = models.CharField(max_length=100,unique=True,primary_key=True)
    title = models.CharField(max_length=200,blank=True,null=True)
    bookimage = models.ImageField(upload_to="media/images/book/",blank=True,null=True)
    bookauthor = models.CharField(max_length=100,blank=True,null=True)
    bookpdf = models.FileField(upload_to="media/pdfs/books/",blank=True,null=True)
    bookdescription = models.TextField()
    fee = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Faq(models.Model):
    faqid = models.CharField(max_length=100,unique=True,primary_key=True)
    relatedid = models.CharField(max_length=100,blank=True,null=True)
    question = models.TextField()
    answer = models.TextField()

    def __str__(self):
        return self.question

class Purchased(models.Model):
    purchaseid = models.CharField(max_length=100,unique=True,primary_key=True)
    bookid = models.CharField(max_length=100,blank=True,null=True)
    userid = models.CharField(max_length=100,blank=True,null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.purchaseid
    
class Blog(models.Model):
    blogid = models.CharField(max_length=100,unique=True,primary_key=True)
    tag = models.CharField(max_length=100,blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    author = models.CharField(max_length=100,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    minutecount = models.IntegerField(default=0)
    banner = models.ImageField(upload_to="media/images/blogs/",blank=True,null=True)
    preface = models.CharField(max_length=100,blank=True,null=True)
    body = models.TextField()
    for_index = models.BooleanField(default=True)
    totallikes = models.IntegerField(default=0)
    totalcomments = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    #commentid = models.CharField(max_length=100,unique=True,primary_key=True)
    blogid = models.CharField(max_length=100,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    comment = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.blogid

class Member(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    password = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,unique=True,primary_key=True)

    def __str__(self):
        return self.phone

class MemberDetails(models.Model):
    username = models.CharField(max_length=100,unique=True,primary_key=True)
    fullname = models.CharField(max_length=100,blank=True,null=True)
    dp = models.ImageField(upload_to="media/user/",blank=True,null=True)
    primary = models.CharField(max_length=100,blank=True,null=True)
    alternative = models.CharField(max_length=100,blank=True,null=True)
    email = models.CharField(max_length=100,blank=True,null=True)
    allokay = models.BooleanField(default=False)


class Invoice(models.Model):
    invoice = models.CharField(max_length=255,unique=True,primary_key=True)
    status = models.BooleanField(default=False)
    relatedid = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    id_token = models.CharField(max_length=255,blank=True,null=True)
    paymentID = models.CharField(max_length=255,blank=True,null=True,unique=True)
    trxID = models.CharField(max_length=100,blank=True,null=True)
    refresh_token = models.CharField(max_length=255,blank=True,null=True)


    def __str__(self):
        return self.invoice
    
class Certificate(models.Model):
    certificateid = models.CharField(max_length=100,unique=True,primary_key=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    courseid = models.CharField(max_length=100,blank=True,null=True)
    banner = models.ImageField(upload_to="media/images/certificates/",blank=True,null=True)
    title = models.CharField(max_length=100,blank=True,null=True)
    certificate = models.FileField(upload_to="media/certificates/",blank=True,null=True)
    zippednotes = models.FileField(upload_to="media/certificates/",blank=True,null=True)
    issuedate = models.DateField(auto_now_add=True)

    def __str__(self):
        return  self.username

class Inquiry(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    msg = models.TextField()

    def __str__(self):
        return self.phone