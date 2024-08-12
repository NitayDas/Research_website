from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import DetailView
from django.http import Http404
from lab_app.forms import BannerImageForm,LoginForm, PeopleCategoryForm
from lab_app.models import About, BannerImage, CentralContact, Contact, Education, PeopleCategory, PeopleProfile, Project, Publication, Research, ResearchInterest

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



class PeopleProfileDetailView(DetailView):
    model = PeopleProfile
    template_name = 'lab_app/people_detail.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['research_interests'] = ResearchInterest.objects.filter(author=self.object)
        return context



def author_projects(request, author_id):
    try:
        author = PeopleProfile.objects.get(id=author_id)
    except PeopleProfile.DoesNotExist:
        raise Http404("Author does not exist")
    
    projects = Project.objects.filter(author=author)
    
    if not projects.exists():
        messages.warning(request, "This author has no associated projects.")

    return render(request, 'lab_app/author_projects.html', {'author': author, 'projects': projects})



def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    related_projects = Project.objects.filter(author=project.author).exclude(id=project.id)
    return render(request, 'lab_app/project_detail.html', {'project': project, 'related_projects': related_projects})



def publication_list(request):
    publications = Publication.objects.all()
    return render(request, 'lab_app/publication_list.html', {'publications': publications})




def author_publications(request, author_id):
    author = get_object_or_404(PeopleProfile, id=author_id)
    publications = Publication.objects.filter(author=author)
    return render(request, 'lab_app/author_publications.html', {'author': author, 'publications': publications})



def contact_info(request, author_id):
    author = get_object_or_404(PeopleProfile, id=author_id)
    try:
        contact = Contact.objects.get(author=author)
    except Contact.DoesNotExist:
        contact = None  # Set contact to None if it doesn't exist

    return render(request, 'lab_app/contact_info.html', {'author': author, 'contact': contact})


def research_interest_view(request, author_id):
    author = get_object_or_404(PeopleProfile, pk=author_id)
    research_interests = ResearchInterest.objects.filter(author=author)
    return render(request, 'lab_app/research_interest.html', {
        'author': author,
        'research_interests': research_interests,
    })



def author_education(request, author_id):
    author = get_object_or_404(PeopleProfile, id=author_id)
    education_records = Education.objects.filter(author=author)
    return render(request, 'lab_app/author_education.html', {
        'education_records': education_records,
        'author': author,
    })



def author_research(request, author_id):
    try:
        author = PeopleProfile.objects.get(id=author_id)
    except PeopleProfile.DoesNotExist:
        raise Http404("Author does not exist")
    
    research = Research.objects.filter(author=author)
    
    if not research.exists():
        messages.warning(request, "This author has no associated projects.")

    return render(request, 'lab_app/author_research.html', {'author': author, 'research': research})



def research_detail(request, research_id):
    research = get_object_or_404(Research, id=research_id)
    related_research = Research.objects.filter(author=research.author).exclude(id=research.id)
    return render(request, 'lab_app/research_detail.html', {'research': research, 'related_research': related_research})



def central_contact_view(request):
    contacts = CentralContact.objects.all()
    return render(request, 'lab_app/central_contact.html', {'contacts': contacts})



def about_view(request):
    about = About.objects.first()
    context = {
        'about': about,
    }
    return render(request, 'lab_app/about.html', context)

