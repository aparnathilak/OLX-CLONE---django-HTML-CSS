from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, ListView, TemplateView, DetailView
from buyer.forms import LoginForm, RegistrationForm, UserCreationForm, ProductAddForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from buyer.models import Products, UserProfile
from django.contrib.auth.models import User
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

# Create your views here.

def signin_required(fn):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Invalid session")
            return redirect("signin")
        else:
            return fn(request, *args, **kwargs)
    return wrapper

decs = [signin_required, never_cache]  


@method_decorator(decs, name="dispatch")
class HomeView(ListView):
    template_name = "index.html"
    context_object_name = "products"
    model = Products

class SignUpView(CreateView):
    template_name = "signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("signin")

    def form_valid(self, form) :
        messages.success(self.request,"Account Created Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Account Creation failed")
        return super().form_invalid(form)



class SignInView(FormView):
    template_name = "login.html"
    form_class = LoginForm


    def post(self, request, *args, **kwargs) :
         form = LoginForm(request.POST)
         if form.is_valid():
            uname = form.cleaned_data.get("username")
            pwd = form.cleaned_data.get("password")
            usr = authenticate(request, username = uname, password = pwd)
            if usr:
                login(request, usr)
                messages.success(request, "Logined Successfully")
                return redirect("home")
            else:
                messages.error(request, "Invalid Credentials")
                return render(request, "login.html", {"form":form})


decs
def product_create(request):
    if request.method == 'POST':
        form = ProductAddForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            return redirect('home')
    else:
        form = ProductAddForm()
    return render(request, 'productadd_form.html', {'form': form})


@method_decorator(decs, name="dispatch")
class ProductDetailView(DetailView):
    template_name = "product_detail.html"
    context_object_name = "product"
    pk_url_kwarg = "id"
    model= Products

decs
def profile_create(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            mobile = form.cleaned_data['mobile']
            address = form.cleaned_data['address']
            return redirect('profile-view')
    else:
        form = UserCreationForm()
    return render(request, 'userprofile.html', {'form': form})


@method_decorator(decs, name="dispatch")
class ViewProfile(TemplateView):
    template_name="profile.html"

@method_decorator(decs, name="dispatch")
class MyProductView(ListView):
    model = Products
    template_name = "profile.html"
    context_object_name = "products"

    def get_queryset(self) :
        return Products.objects.filter(seller=self.request.user)


decs
def logout_view(request, *args, **kwargs):
    logout(request)
    messages.success(request,"Logged Out")
    return redirect("signin")

# @method_decorator(decs, name="dispatch")
# class ViewProfile(ListView):
#     model = UserProfile
#     template_name = "profile.html"
#     context_object_name = "todos"
#     def get_queryset(self):
#         return  UserProfile.objects.filter(user = self.request.user)
