from django import forms
from .models import ReviewModel, ReviewSubModel, RadioQuestion, CheckboxQuestion, TextQuestion

class ReviewModelForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ['name', 'description', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter review form name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class ReviewSubModelForm(forms.ModelForm):
    class Meta:
        model = ReviewSubModel
        fields = ['review_model', 'name', 'description', 'is_active']
        widgets = {
            'review_model': forms.Select(attrs={
                'class': 'form-control'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter sub-category name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description (optional)'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }

class RadioQuestionForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter one option per line\nFormat: Option Text:Value (e.g., Poor:1, Excellent:5)'
        }),
        help_text="One option per line. Format: Option Text:Value"
    )
    
    class Meta:
        model = RadioQuestion
        fields = ['review_sub_model', 'question_text', 'required', 'index']
        widgets = {
            'review_sub_model': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter question text'
            }),
            'required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'index': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order'
            }),
        }

class CheckboxQuestionForm(forms.ModelForm):
    options = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Enter one option per line'
        }),
        help_text="One option per line"
    )
    
    class Meta:
        model = CheckboxQuestion
        fields = ['review_sub_model', 'question_text', 'required', 'index']
        widgets = {
            'review_sub_model': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter question text'
            }),
            'required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'index': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order'
            }),
        }

class TextQuestionForm(forms.ModelForm):
    class Meta:
        model = TextQuestion
        fields = ['review_sub_model', 'question_text', 'required', 'index']
        widgets = {
            'review_sub_model': forms.Select(attrs={'class': 'form-control'}),
            'question_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter question text'
            }),
            'required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'index': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Display order'
            }),
        }