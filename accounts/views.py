from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import UpdateView, DetailView

from accounts.forms import SignUpForm, profile_edit_form_c
from posts.models import profile_c


def signup(request):
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request, user)
            return redirect('home')
    else:
        form=SignUpForm()
    return render(request, 'signup.html',{ 'form':form })


class profile_edit_view_c(UpdateView):
    model = profile_c
    form_class = profile_edit_form_c

    template_name = 'profile_edit.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        self.object = self.get_object()
        ctx = super().get_context_data(**kwargs)
        ctx['user']=self.object.user
        return ctx


class profile_view_c(DetailView):
    model = profile_c
    template_name = 'profile.html'

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('user_pk')
        user = get_object_or_404(User, pk=user_pk)
        profile = user.profile
        # profile = profile_c.objects.get(user__pk=user_pk)
        self.object = profile
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        # self.object = self.get_object()
        ctx = super().get_context_data(**kwargs)
        return ctx



