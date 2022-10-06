from django.shortcuts import redirect, render
from django.views import View
from django.urls import reverse
from django.views.generic.base import TemplateView
from .models import Parks, Site, Favoritelist
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# after our other imports 
from django.views.generic import DetailView
# Create your views here.
# at top of file with other imports
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Here we will be creating a class called Home and extending it from the View class
class Home(TemplateView):
    template_name = "home.html"

    # adding playlist context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favoritelists'] = Favoritelist.objects.all()
        print(context)
        return context


class About(TemplateView):
    template_name = "about.html"

@method_decorator(login_required, name='dispatch')
class ParksList(TemplateView):
    template_name = "parks_list.html"
#     In here, I want to check if there has been a query made
# I know the queries will have a key of name

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mySearchName = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if mySearchName != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["parks"] = Parks.objects.filter(name__icontains=mySearchName)
            context["stuff_at_top"] = f"Searching through Parks list for {mySearchName}"
        else:
            context["parks"] = Parks.objects.filter(user=self.request.user)
            context["stuff_at_top"] = "Trending Parks"
        return context



@method_decorator(login_required, name='dispatch')
class ParkCreate(CreateView):
    model = Parks
    fields = ['name', 'img', 'bio']
    template_name = "park_create.html"
    # success_url = "/parks/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ParkCreate, self).form_valid(form)

    def get_success_url(self):
        print(self.kwargs)
        return reverse('park_detail', kwargs={'pk': self.object.pk})

class ParkDetail(DetailView):
    model = Parks
    template_name = "park_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favoritelists'] = Favoritelist.objects.all()
        return context

@method_decorator(login_required, name='dispatch')
class ParkUpdate(UpdateView):
    model = Parks
    fields = ['name', 'img', 'bio', 'verified_park']
    template_name = "park_update.html"
    success_url = "/parks/"

    def get_success_url(self):
        return reverse('park_detail', kwargs={'pk': self.object.pk})

@method_decorator(login_required, name='dispatch')
class ParkDelete(DeleteView):
    model = Parks
    template_name = "park_delete_confirmation.html"
    success_url = "/parks/"


@method_decorator(login_required, name='dispatch')
class SiteCreate(View):

    def post(self, request, pk):
        formTitle = request.POST.get("title")
        theParks = Parks.objects.get(pk=pk)
        Site.objects.create(title=formTitle, parks = theParks)
        return redirect('park_detail', pk=pk)

class FavoritelistSiteAssoc(View):

    def get(self, request, pk, site_pk):
        # get the query parameter from the 
        assoc = request.GET.get("assoc")

        if assoc == "remove":
            # get the playlist by the pk, remove the song (row) with the song_pk
            Favoritelist.objects.get(pk=pk).sites.remove(site_pk)
        
        if assoc == "add":

            # get the playlist by the pk, add the song (row) with the song_pk
            Favoritelist.objects.get(pk=pk).sites.add(site_pk)
        
        return redirect('home')


class Signup(View):
    # show a form to fill out
    def get(self, request):
        form = UserCreationForm()
        context = {"form": form}
        return render(request, "registration/signup.html", context)
    # on form submit, validate the form and login the user.
    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("parks_list")
        else:
            return redirect("signup")