from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import uuid

class ReviewModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    overall_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    shareable_link = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ReviewModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        
        if not self.shareable_link:
            self.shareable_link = f"review_{uuid.uuid4().hex[:10]}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ReviewSubModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    review_model = models.ForeignKey(ReviewModel, on_delete=models.CASCADE, related_name='sub_models')
    name = models.TextField()
    slug = models.SlugField(unique=True, blank=True) 
    description = models.TextField(blank=True)
    overall_rating = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while ReviewSubModel.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.review_model.name} - {self.name}"

class RadioQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    review_sub_model = models.ForeignKey(ReviewSubModel, on_delete=models.CASCADE, related_name='radio_questions')
    question_text = models.TextField()
    answer_options = models.JSONField()
    answer_instances = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    required = models.BooleanField(default=True)
    index = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"Radio: {self.question_text[:50]}..."

class CheckboxQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    review_sub_model = models.ForeignKey(ReviewSubModel, on_delete=models.CASCADE, related_name='checkbox_questions')
    question_text = models.TextField()
    answer_options = models.JSONField()
    answer_instances = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0.0)
    required = models.BooleanField(default=True)
    index = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"Checkbox: {self.question_text[:50]}..."

class TextQuestion(models.Model):
    id = models.BigAutoField(primary_key=True)
    review_sub_model = models.ForeignKey(ReviewSubModel, on_delete=models.CASCADE, related_name='text_questions')
    question_text = models.TextField()
    answer_instances = models.IntegerField(default=0)
    answer_text = models.TextField(default="")
    required = models.BooleanField(default=True)
    index = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['index']

    def __str__(self):
        return f"Text: {self.question_text[:50]}..."