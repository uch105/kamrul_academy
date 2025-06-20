from django.db import models
from django.db.models import Model
#from tinymce.models import HTMLField



class Mentor(models.Model):
    id = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=100,blank=True,null=True)
    designation = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.name
class RecordedCourse(models.Model):
    id = models.CharField(max_length=30,primary_key=True,default="0")
    title = models.CharField(max_length=50,null=True,blank=True)
    preface = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    banner = models.ImageField(upload_to="media/images/recorded/",null=True,blank=True)
    total_modules = models.CharField(max_length=4,null=True,blank=True)
    total_exams = models.CharField(max_length=4,null=True,blank=True)
    total_hours = models.CharField(max_length=4,null=True,blank=True)
    total_pdfs = models.CharField(max_length=4,null=True,blank=True)
    days_remain = models.CharField(max_length=4,null=True,blank=True)
    total_student = models.CharField(max_length=10,null=True,blank=True)
    mentor = models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True)
    for_index = models.BooleanField(default=False)
    softwares = models.TextField(null=True,blank=True)
    learningoutcome1 = models.TextField(null=True,blank=True)
    learningoutcome2 = models.TextField(null=True,blank=True)
    forwhom1 = models.TextField(null=True,blank=True)
    forwhom2 = models.TextField(null=True,blank=True)
    opportunities = models.TextField(null=True,blank=True)
    fee = models.FloatField(default=0.0)
    feebangla = models.CharField(max_length=10,null=True,blank=True)

    def __str__(self):
        return self.title


class RecordedCourseModule(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    module_name = models.CharField(max_length=150,blank=True,null=True)
    class_one_valid = models.BooleanField(default=False)
    class_one_name = models.CharField(max_length=150,blank=True,null=True)
    class_one_video = models.FileField(upload_to="media/recorded/videos/",null=True,blank=True)
    class_two_valid = models.BooleanField(default=False)
    class_two_name = models.CharField(max_length=150,blank=True,null=True)
    class_two_video = models.FileField(upload_to="media/recorded/videos/",null=True,blank=True)
    class_three_valid = models.BooleanField(default=False)
    class_three_name = models.CharField(max_length=150,blank=True,null=True)
    class_three_video = models.FileField(upload_to="media/recorded/videos/",null=True,blank=True)
    class_four_valid = models.BooleanField(default=False)
    class_four_name = models.CharField(max_length=150,blank=True,null=True)
    class_four_video = models.FileField(upload_to="media/recorded/videos/",null=True,blank=True)
    class_five_valid = models.BooleanField(default=False)
    class_five_name = models.CharField(max_length=150,blank=True,null=True)
    class_five_video = models.FileField(upload_to="media/recorded/videos/",null=True,blank=True)
    note = models.FileField(upload_to="media/recorded/notes/",null=True,blank=True)
    assignment_desc = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.module_name


class RecordedCourseAssignmentSubmission(models.Model):
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(RecordedCourseModule,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    file = models.FileField(upload_to="media/recorded/assignments/",blank=True,null=True)


class Question(models.Model):
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(RecordedCourseModule,on_delete=models.CASCADE,null=True)
    serial = models.CharField(max_length=15,null=True,blank=True)
    serial_text = models.CharField(max_length=15,null=True,blank=True)
    text = models.TextField(null=True,blank=True)
    answer1 = models.CharField(max_length=100,null=True,blank=True)
    answer2 = models.CharField(max_length=100,null=True,blank=True)
    answer3 = models.CharField(max_length=100,null=True,blank=True)
    answer4 = models.CharField(max_length=100,null=True,blank=True)
    answer5 = models.CharField(max_length=10,null=True,blank=True)


class QuizResult(models.Model):
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(RecordedCourseModule,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=100,null=True,blank=True)
    score = models.CharField(max_length=100,null=True,blank=True)

class RecordedCourseProgressTracking(models.Model):
    username = models.CharField(max_length=100,null=True,blank=True)
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    done = models.CharField(max_length=10,null=True,blank=True)
    total = models.CharField(max_length=10,null=True,blank=True)
    calc = models.FloatField(default=0.0)

class ClassPermissionTracking(models.Model):
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    module = models.ForeignKey(RecordedCourseModule,on_delete=models.CASCADE,null=True)
    username = models.CharField(max_length=100,blank=True,null=True)
    quiz_marks = models.FloatField(default=0.0)
    allow_next = models.BooleanField(default=False)

class RecordedCourseNotification(models.Model):
    username = models.CharField(max_length=100,blank=True,null=True)
    course = models.ForeignKey(RecordedCourse,on_delete=models.CASCADE,null=True)
    frequency = models.IntegerField(default=0)
    alert = models.BooleanField(default=False)


class LiveCourse(models.Model):
    id = models.CharField(max_length=30,primary_key=True,default="001")
    title = models.CharField(max_length=50,null=True,blank=True)
    preface = models.CharField(max_length=100,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    banner = models.ImageField(upload_to="media/images/recorded/",null=True,blank=True)
    batch_no = models.CharField(max_length=4,null=True,blank=True)
    seats_remain = models.CharField(max_length=4,null=True,blank=True)
    days_remain = models.CharField(max_length=4,null=True,blank=True)
    total_student = models.CharField(max_length=10,null=True,blank=True)
    total_modules = models.CharField(max_length=4,null=True,blank=True)
    total_classes = models.CharField(max_length=4,null=True,blank=True)
    total_hours = models.CharField(max_length=4,null=True,blank=True)
    total_pdfs = models.CharField(max_length=4,null=True,blank=True)
    total_quizes = models.CharField(max_length=4,null=True,blank=True)
    mentor = models.ForeignKey(Mentor,on_delete=models.CASCADE,null=True)
    for_index = models.BooleanField(default=False)
    softwares = models.TextField(null=True,blank=True)
    learningoutcome1 = models.TextField(null=True,blank=True)
    learningoutcome2 = models.TextField(null=True,blank=True)
    forwhom1 = models.TextField(null=True,blank=True)
    forwhom2 = models.TextField(null=True,blank=True)
    opportunities = models.TextField(null=True,blank=True)
    fee = models.FloatField(default=0.0)
    fee_per_month = models.FloatField(default=0.0)
    fee_bangla = models.CharField(max_length=20,null=True,blank=True)
    fee_per_month_bangla = models.CharField(max_length=20,null=True,blank=True)



class LiveCourseModule(models.Model):
    id = models.CharField(primary_key=True,max_length=50)
    course = models.ForeignKey(LiveCourse,on_delete=models.CASCADE,null=True)
    module_name = models.CharField(max_length=150,blank=True,null=True)

class LiveCourseModuleClass(models.Model):
    module = models.ForeignKey(LiveCourseModule,on_delete=models.CASCADE,null=True,related_name="classes")
    class_serial = models.CharField(max_length=200,null=True,blank=True)
    class_done = models.BooleanField(default=False)
    class_ongoing = models.BooleanField(default=False)
    class_link = models.CharField(max_length=200,null=True,blank=True)
    class_date = models.CharField(max_length=200,null=True,blank=True)
    class_name = models.CharField(max_length=150,blank=True,null=True)



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

class ManualEnrollment(models.Model):
    rid = models.CharField(max_length=255,blank=True,null=True)
    username = models.CharField(max_length=255,blank=True,null=True)
    phone = models.CharField(max_length=255,blank=True,null=True)
    title = models.CharField(max_length=255,blank=True,null=True)
    way = models.CharField(max_length=255,blank=True,null=True)
    trxID = models.CharField(max_length=255,blank=True,null=True)
    issuetime = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    
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

class Cert(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    d = models.CharField(max_length=100,blank=True,null=True)
    course_name = models.CharField(max_length=255,null=True,blank=True)
    image = models.ImageField(upload_to="certificate/")

    def __str__(self):
        return self.id

class Inquiry(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    phone = models.CharField(max_length=100,blank=True,null=True)
    msg = models.TextField()

    def __str__(self):
        return self.phone
