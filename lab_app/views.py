from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from lab_app.forms import BannerImageForm,LoginForm, PeopleCategoryForm
from lab_app.models import BannerImage, PeopleCategory, PeopleProfile, Project

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




@login_required
@permission_required('lab_app.add_peoplecategory')
def add_category(request):
    if request.method == 'POST':
        form = PeopleCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New category added successfully!')
            return redirect('lab_app:home_page_view')
    else:
        form = PeopleCategoryForm()
    return render(request, 'lab_app/add_category.html', {'form': form})




def people_list(request):
    categories = PeopleCategory.objects.all()
    profiles = PeopleProfile.objects.all()
    return render(request, 'lab_app/people_list.html', {'categories': categories, 'profiles': profiles})


def category_people_list(request, category_name):
    category = get_object_or_404(PeopleCategory, category=category_name)
    profiles = PeopleProfile.objects.filter(category=category)
    return render(request, 'lab_app/category_people_list.html', {'category': category, 'profiles': profiles})

from django.views.generic import DetailView

class PeopleProfileDetailView(DetailView):
    model = PeopleProfile
    template_name = 'lab_app/people_detail.html'  # Use the provided template
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.object.category  # Assuming 'category' is the author
        return context




def author_projects(request, author_id):
    author = get_object_or_404(PeopleProfile, id=author_id)
    projects = Project.objects.filter(author=author)
    return render(request, 'lab_app/author_projects.html', {'author': author, 'projects': projects})

