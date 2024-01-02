from django.db import models
from django.db.models import Model
from tinymce.models import HTMLField

# Create your models here.

class Random_user(models.Model):
    user_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    user_ip = models.GenericIPAddressField(null=True)
    user_device = models.TextField(null=True)
    search_history = models.FileField(upload_to='media/random_data_collection/',null=True)

    def __str__(self):
        return self.user_ip

class Signed_user(models.Model):
    user_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200,null=True)
    mother_name = models.CharField(max_length=200,null=True)
    nationality = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=50,null=True)
    blood_group = models.CharField(max_length=50,null=True)
    dob = models.DateField(null=True)
    s_class = models.CharField(max_length=100,null=True)
    s_group = models.CharField(max_length=100,null=True)
    sex = models.BooleanField(default=True)
    pp = models.ImageField(upload_to='media/images/user_iamges/',null=True)
    phone_number = models.CharField(max_length=100,unique=True)
    alter_phone_number = models.CharField(max_length=100,null=True)
    date_joined = models.DateTimeField(auto_now_add = True)
    password = models.CharField(max_length= 200)
    institution = models.CharField(max_length=50,null=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    book_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    name = models.CharField(max_length = 200)
    price = models.FloatField(default=0.0)
    book_image = models.ImageField(upload_to='media/images/book_iamges/',null=True)
    book_file = models.FileField(upload_to='media/docs/books/',null=True)
    downloads = models.BigIntegerField(default=0)
    uploaded = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return self.name

class Moderator(models.Model):
    user_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    name = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length=100,unique=True)
    pp = models.ImageField(upload_to='media/images/moderator_images/',null=True)
    email = models.EmailField()
    password = models.CharField(max_length= 200)
    nid = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

class Mentor(models.Model):
    user_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    name = models.CharField(max_length = 200)
    phone_number = models.CharField(max_length=100,unique=True)
    pp = models.ImageField(upload_to='media/images/mentor_images/',null=True)
    password = models.CharField(max_length= 200)
    nid = models.BigIntegerField(default=0)
    institution = models.TextField()
    expertise = models.TextField()
    payment_details = models.TextField()
    email = models.EmailField(null=True)

    def __str__(self):
        return self.name

class Blog(models.Model):
    blog_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    title = models.CharField(max_length = 200)
    thumbnail = models.ImageField(upload_to='media/images/blog_images/',null=True)
    preface = HTMLField()
    desc = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    mod_name = models.ForeignKey(Moderator,on_delete=models.SET_NULL,null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    read_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Course(models.Model):
    course_id = models.CharField(max_length= 100,unique=True,primary_key=True)
    title = models.CharField(max_length = 200)
    thumbnail = models.ImageField(upload_to='media/images/course_images/',null=True)
    preface = models.TextField()
    desc = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    mod_name = models.ForeignKey(Moderator,on_delete=models.SET_NULL,null=True)
    mentor_name = models.ForeignKey(Mentor,on_delete=models.SET_NULL,null=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    enrolled = models.IntegerField(default=0)
    course_promo_video = models.FileField(upload_to='media/videos/course/',null=True)
    course_video = models.FileField(upload_to='media/videos/course/',null=True)
    course_notes = models.FileField(upload_to='media/docs/notes/',null=True)
    for_index = models.BooleanField(default=False)
    for_top = models.BooleanField(default=False)
    duration_in_minutes = models.IntegerField(default=0)
    course_fee = models.IntegerField(default=1000)

    def __str__(self):
        return self.title
    
class Comments(models.Model):
    related_id = models.CharField(max_length=100)
    body = models.TextField()
    user_id =models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            cmnt = Blog.objects.get(blog_id = self.related_id)
        except:
            cmnt = Course.objects.get(course_id = self.related_id)
        return cmnt.title

class Course_hub(models.Model):
    c_hub_id = models.CharField(max_length=100,primary_key=True)
    title = models.CharField(max_length = 200)
    thumbnail = models.ImageField(upload_to='media/images/course_images/')
    preface = HTMLField()
    desc = HTMLField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now = True)
    mod_name = models.ForeignKey(Moderator,on_delete=models.SET_NULL,null=True)
    mentor_name = models.ForeignKey(Mentor,on_delete=models.SET_NULL,null=True)
    no_of_course = models.IntegerField(default=0)
    enrolled = models.IntegerField(default=0)
    course_list = models.FileField(upload_to='media/docs/course_list/',null=True)

    def __str__(self):
        return self.title
    
class RegularExam(models.Model):
    exam_id = models.CharField(max_length=100,primary_key=True)
    name = models.CharField(max_length=100)
    question_count = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)
    total_time = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Question(models.Model):
    exam_id = models.CharField(max_length=100,primary_key=True)
    question_text = HTMLField()
    option1 = HTMLField()
    option2 = HTMLField()
    option3 = HTMLField(null=True)
    option4 = HTMLField(null=True)
    r_option = HTMLField()

    def __str__(self):
        return self.exam_id

class Result(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    exam_id = models.CharField(max_length=100)
    gained_marks = models.IntegerField(default=0)
    total_marks = models.IntegerField(default=0)

    def __str__(self):
        return Signed_user.objects.get(user_id=self.username)
    
class LiveClass(models.Model):
    classname = models.CharField(max_length=200)
    id = models.CharField(max_length=100,primary_key=True)
    thumbnail = models.ImageField(upload_to='media/images/live_class/',null=True)
    mentor_id = models.CharField(max_length=100)
    scheduled_time = models.DateTimeField()
    participant_list = models.FileField(upload_to='media/docs/live_class/',null=True)
    shared_notes = models.FileField(upload_to='media/docs/live_class/',null=True)

    def __str__(self):
        return self.classname

class LiveClassComments(models.Model):
    id = models.CharField(max_length=100,primary_key=True)
    user = models.CharField(max_length=100)
    body = models.TextField()
    cmnt_images = models.ImageField(upload_to='media/images/live_class/',null=True)
    time = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return LiveClass.objects.get(id=self.id).classname
    
class IndexPromo(models.Model):
    titleBold = models.CharField(max_length=300)
    text = HTMLField()
    image = models.ImageField(upload_to="media/images/index")

    def __str__(self):
        return self.titleBold

class Faq(models.Model):
    title = models.CharField(max_length=300)
    answer = HTMLField()
    for_index = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Inquiry(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone = models.CharField(max_length=15)
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Terms_Conditions(models.Model):
    text = HTMLField()

class Refund_Policy(models.Model):
    text = HTMLField()

class Privacy(models.Model):
    text = HTMLField()

class UserConnectProduct(models.Model):
    piduid = models.CharField(max_length=200)
    pid = models.CharField(max_length=200)
    uid = models.CharField(max_length=200)

    def __str__(self):
        return self.piduid

class UserLikeBlog(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    blog_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserDislikeBlog(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    blog_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserLikeCourse(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    blog_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class UserDislikeCourse(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    blog_id = models.CharField(max_length=100)

    def __str__(self):
        return self.username