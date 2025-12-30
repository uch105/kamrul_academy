from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from .models import (
    ReviewModel, ReviewSubModel
)
from .forms import (
    ReviewModelForm, ReviewSubModelForm, RadioQuestionForm, 
    CheckboxQuestionForm, TextQuestionForm
)
from django.contrib import messages

@login_required(login_url="/behind-the-desk/login/")
def admin_home(request):
    review_models = ReviewModel.objects.all().order_by('-created_at')
    
    # Calculate statistics
    total_forms = review_models.count()
    active_forms = review_models.filter(is_active=True).count()
    
    total_submodels = 0
    total_questions = 0
    
    for review_model in review_models:
        total_submodels += review_model.sub_models.count()
        for sub_model in review_model.sub_models.all():
            total_questions += (sub_model.radio_questions.count() + 
                              sub_model.checkbox_questions.count() + 
                              sub_model.text_questions.count())
    
    context = {
        'review_models': review_models,
        'total_forms': total_forms,
        'active_forms': active_forms,
        'total_submodels': total_submodels,
        'total_questions': total_questions,
    }
    return render(request, 'review/admin_home.html', context)

@login_required(login_url="/behind-the-desk/login/")
def create_review_form(request):
    # Forms
    review_model_form = ReviewModelForm(request.POST or None)
    review_sub_model_form = ReviewSubModelForm(request.POST or None, initial={'review_model': None})
    
    # Get all review models for sub-model form
    all_review_models = ReviewModel.objects.all()
    review_sub_model_form.fields['review_model'].queryset = all_review_models
    
    # Question forms
    radio_form = RadioQuestionForm(request.POST or None)
    checkbox_form = CheckboxQuestionForm(request.POST or None)
    text_form = TextQuestionForm(request.POST or None)
    
    # Get all sub-models for question forms
    all_review_sub_models = ReviewSubModel.objects.all()
    radio_form.fields['review_sub_model'].queryset = all_review_sub_models
    checkbox_form.fields['review_sub_model'].queryset = all_review_sub_models
    text_form.fields['review_sub_model'].queryset = all_review_sub_models
    
    # Handle form submissions
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'review_model':
            if review_model_form.is_valid():
                review_model = review_model_form.save()
                messages.success(request, f'Review form "{review_model.name}" created successfully!')
                return redirect('review:create_review_form')
        
        elif form_type == 'review_sub_model':
            if review_sub_model_form.is_valid():
                review_sub_model = review_sub_model_form.save()
                messages.success(request, f'Sub-category "{review_sub_model.name}" created successfully!')
                return redirect('review:create_review_form')
        
        elif form_type == 'radio_question':
            if radio_form.is_valid():
                radio_question = radio_form.save(commit=False)
                
                # Parse options
                options_text = request.POST.get('options', '')
                options_list = []
                for i, line in enumerate(options_text.strip().split('\n')):
                    if ':' in line:
                        text, value = line.strip().split(':', 1)
                        options_list.append({
                            'text': text.strip(),
                            'value': int(value.strip()) if value.strip().isdigit() else i + 1
                        })
                    else:
                        options_list.append({
                            'text': line.strip(),
                            'value': i + 1
                        })
                
                radio_question.answer_options = options_list
                radio_question.save()
                messages.success(request, f'Radio question created successfully!')
                return redirect('review:create_review_form')
        
        elif form_type == 'checkbox_question':
            if checkbox_form.is_valid():
                checkbox_question = checkbox_form.save(commit=False)
                
                # Parse options
                options_text = request.POST.get('options', '')
                options_list = []
                for line in options_text.strip().split('\n'):
                    if line.strip():
                        options_list.append({
                            'text': line.strip(),
                            'value': 1
                        })
                
                checkbox_question.answer_options = options_list
                checkbox_question.save()
                messages.success(request, f'Checkbox question created successfully!')
                return redirect('review:create_review_form')
        
        elif form_type == 'text_question':
            if text_form.is_valid():
                text_form.save()
                messages.success(request, f'Text question created successfully!')
                return redirect('review:create_review_form')
    
    context = {
        'review_model_form': review_model_form,
        'review_sub_model_form': review_sub_model_form,
        'radio_form': radio_form,
        'checkbox_form': checkbox_form,
        'text_form': text_form,
        'all_review_models': all_review_models,
        'all_review_sub_models': all_review_sub_models,
    }
    
    return render(request, 'review/create_review_form.html', context)

@login_required(login_url="/behind-the-desk/login/")
def delete_review_model(request, pk):
    review_model = get_object_or_404(ReviewModel, pk=pk)
    
    if request.method == 'POST':
        review_model.delete()
        messages.success(request, f'Review form "{review_model.name}" deleted successfully!')
        return redirect('review:admin_home')
    
    return render(request, 'review/delete_review_model.html', {'review_model': review_model})

@login_required(login_url="/behind-the-desk/login/")
def view_stats(request, pk):
    review_model = get_object_or_404(ReviewModel, pk=pk)
    
    # Calculate overall rating
    sub_models = review_model.sub_models.all()
    
    # Get stats for each sub-model
    sub_model_stats = []
    for sub_model in sub_models:
        # Prepare radio questions with calculated values
        radio_questions_data = []
        for radio_q in sub_model.radio_questions.all():
            # Calculate max value for radio question
            max_value = 1
            if radio_q.answer_options:
                for option in radio_q.answer_options:
                    if option.get('value', 1) > max_value:
                        max_value = option.get('value', 1)
            
            percentage = (radio_q.avg_score / max_value * 100) if max_value > 0 else 0
            
            radio_questions_data.append({
                'question': radio_q,
                'max_value': max_value,
                'percentage': round(percentage, 1)
            })
        
        # Prepare checkbox questions with calculated values
        checkbox_questions_data = []
        for checkbox_q in sub_model.checkbox_questions.all():
            # Calculate max options for checkbox question
            max_options = len(checkbox_q.answer_options) if checkbox_q.answer_options else 5
            
            percentage = (checkbox_q.avg_score / max_options * 100) if max_options > 0 else 0
            
            checkbox_questions_data.append({
                'question': checkbox_q,
                'max_options': max_options,
                'percentage': round(percentage, 1)
            })
        
        # Get text responses for display
        text_responses = []
        for text_question in sub_model.text_questions.all():
            if text_question.answer_text:
                # Parse the stored text responses
                responses = text_question.answer_text.strip().split('\n\n')
                for response in responses:
                    if response.strip():
                        lines = response.strip().split('\n', 1)
                        if len(lines) == 2:
                            name, text = lines
                            text_responses.append({
                                'name': name.strip(),
                                'text': text.strip(),
                                'question': text_question.question_text[:50] + '...' if len(text_question.question_text) > 50 else text_question.question_text
                            })
        
        sub_model_stats.append({
            'sub_model': sub_model,
            'rating_percentage': 0,  # We'll calculate this below
            'radio_questions_data': radio_questions_data,
            'checkbox_questions_data': checkbox_questions_data,
            'text_questions': sub_model.text_questions.all(),
            'text_responses': text_responses[:10],
        })
    
    # Calculate percentages for each sub-model
    for stat in sub_model_stats:
        total_percentage = 0
        count = 0
        
        for radio_data in stat['radio_questions_data']:
            total_percentage += radio_data['percentage']
            count += 1
        
        for checkbox_data in stat['checkbox_questions_data']:
            total_percentage += checkbox_data['percentage']
            count += 1
        
        stat['rating_percentage'] = round(total_percentage / count, 1) if count > 0 else 0
    
    # Calculate overall percentage
    if sub_model_stats:
        overall_percentage = sum(stat['rating_percentage'] for stat in sub_model_stats) / len(sub_model_stats)
    else:
        overall_percentage = 0
    
    context = {
        'review_model': review_model,
        'sub_model_stats': sub_model_stats,
        'overall_percentage': round(overall_percentage, 1),
    }
    
    return render(request, 'review/view_stats.html', context)

def submit_review(request, shareable_link):
    review_model = get_object_or_404(ReviewModel, shareable_link=shareable_link, is_active=True)
    
    if request.method == 'POST':
        # Get respondent name or use "Anonymous"
        respondent_name = request.POST.get('respondent_name', '').strip()
        if not respondent_name:
            respondent_name = 'Anonymous'
            
        # Process each sub-model
        for sub_model in review_model.sub_models.filter(is_active=True):
            # Process radio questions
            for radio_q in sub_model.radio_questions.all():
                field_name = f"radio_{radio_q.id}"
                if field_name in request.POST:
                    selected_value = int(request.POST[field_name])
                    
                    # Update question stats
                    radio_q.answer_instances += 1
                    total_score = (radio_q.avg_score * (radio_q.answer_instances - 1)) + selected_value
                    radio_q.avg_score = total_score / radio_q.answer_instances
                    radio_q.save()
            
            # Process checkbox questions
            for checkbox_q in sub_model.checkbox_questions.all():
                field_name = f"checkbox_{checkbox_q.id}"
                selected_indices = request.POST.getlist(field_name)
                
                if selected_indices:
                    # Update question stats
                    checkbox_q.answer_instances += 1
                    score = len(selected_indices)  # Each checkbox = 1 point
                    total_score = (checkbox_q.avg_score * (checkbox_q.answer_instances - 1)) + score
                    checkbox_q.avg_score = total_score / checkbox_q.answer_instances
                    checkbox_q.save()
            
            # Process text questions
            for text_q in sub_model.text_questions.all():
                field_name = f"text_{text_q.id}"
                if field_name in request.POST and request.POST[field_name].strip():
                    answer_text = request.POST[field_name]
                    
                    # Update question stats and store text response
                    text_q.answer_instances += 1
                    
                    respondent_id = request.POST.get('respondent_name', 'Anonymous')
                    
                    if text_q.answer_text:
                        text_q.answer_text += f"\n\n{respondent_name}\n{answer_text}"
                    else:
                        text_q.answer_text = f"{respondent_name}\n{answer_text}"
                    
                    text_q.save()
        
        # Update overall ratings
        for sub_model in review_model.sub_models.all():
            radio_avg = sub_model.radio_questions.aggregate(Avg('avg_score'))['avg_score__avg'] or 0
            checkbox_avg = sub_model.checkbox_questions.aggregate(Avg('avg_score'))['avg_score__avg'] or 0
            
            total_questions = sub_model.radio_questions.count() + sub_model.checkbox_questions.count()
            if total_questions > 0:
                sub_model.overall_rating = (radio_avg + checkbox_avg) / total_questions
                sub_model.save()
        
        # Update review model rating
        sub_model_ratings = [sm.overall_rating for sm in review_model.sub_models.all()]
        if sub_model_ratings:
            review_model.overall_rating = sum(sub_model_ratings) / len(sub_model_ratings)
            review_model.save()
        
        return render(request, 'review/review_thankyou.html', {'review_model': review_model})
    
    # GET request - show the form
    context = {
        'review_model': review_model,
        'sub_models': review_model.sub_models.filter(is_active=True),
    }
    return render(request, 'review/review_form.html', context)