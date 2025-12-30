from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'review'

urlpatterns = [
    path('admin/', views.admin_home, name='admin_home'),
    path('admin/create/', views.create_review_form, name='create_review_form'),
    path('admin/delete/<int:pk>/', views.delete_review_model, name='delete_review_model'),
    path('admin/stats/<int:pk>/', views.view_stats, name='view_stats'),
    path('submit/<str:shareable_link>/', views.submit_review, name='submit_review'),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)