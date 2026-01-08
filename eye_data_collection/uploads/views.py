from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import SubmissionForm


def upload_form(request):
    """
    Display the upload form and handle form submissions.
    """
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the submission with IP address
            submission = form.save(commit=False)
            submission.ip_address = get_client_ip(request)
            submission.save()
            
            messages.success(
                request,
                'Your images have been successfully uploaded! Thank you for your contribution.'
            )
            return redirect('uploads:upload_success')
    else:
        form = SubmissionForm()
    
    return render(request, 'uploads/upload_form.html', {'form': form})


def upload_success(request):
    """
    Display success page after successful upload.
    """
    return render(request, 'uploads/success.html')


def get_client_ip(request):
    """
    Get the client's IP address from the request.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
