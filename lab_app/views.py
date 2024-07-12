from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lab_app.forms import BannerImageForm,LoginForm
from lab_app.models import BannerImage

# Create your views here.
def home_page_view(request):
    banner_images = BannerImage.objects.order_by('-uploaded_at')[:3]
    context = {
        'banner_images': banner_images
    }
    return render(request, 'lab_app/home.html', context)



@login_required
@permission_required('lab_app.add_bannerimage')
def upload_banner_image(request):
    if request.method == 'POST':
        form = BannerImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Banner image uploaded successfully!')
            return redirect('lab_app:home_page_view')
    else:
        form = BannerImageForm()
    return render(request, 'lab_app/banner_image_upload_form.html', {'form': form})


def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully logged in!')
                return redirect('lab_app:home_page_view')
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()
    return render(request, 'lab_app/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully!')
    return redirect('lab_app:login')