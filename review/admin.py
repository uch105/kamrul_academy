from django.contrib import admin
from .models import *

admin.site.register(ReviewModel)
admin.site.register(ReviewSubModel)
admin.site.register(RadioQuestion)
admin.site.register(CheckboxQuestion)
admin.site.register(TextQuestion)