from django.contrib.auth import login
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetView, PasswordChangeDoneView, PasswordChangeView, LoginView
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse
from django.views.generic import UpdateView, DetailView

from accounts.forms import sign_up_form_c, profile_edit_form_c
from posts.models import profile_c
from posts.views import base_view_c


def signup(request):
    if request.method == 'POST':
        form = sign_up_form_c(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = sign_up_form_c()
    return render(request, 'signup.html', {'form': form})


class profile_edit_view_c(base_view_c, UpdateView):
    model = profile_c
    form_class = profile_edit_form_c
    context_object_name = 'profile'
    template_name = 'profile_edit.html'
    pk_url_kwarg = 'profile_pk'

    def get_success_url(self):
        return reverse('profile', kwargs=dict(user_pk=self.object.user.pk))
        # return super().get_success_url()

    # def get_object(self, queryset=None):
    #     if self.request.user.is_authenticated:
    #         obj, created = profile_c.objects.get_or_create(defaults={'user': self.request.user})
    #     return super().get_object(queryset)


    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, *, object_list=None, **kwargs):
        return super().get_context_data(object_list=object_list, **kwargs)

    # def form_valid(self, form):
    #     handle_uploaded_file(self.request.FILES['file'])

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     self.object = self.get_object()
    #     ctx = super().get_context_data(**kwargs)
    #     ctx['user']=self.object.user
    #     return ctx


class profile_view_c(base_view_c, DetailView):
    model = profile_c
    template_name = 'profile.html'
    context_object_name = 'profile'

    # def get_object(self, queryset=None):
    #     if self.request.user.is_authenticated:
    #         obj, created = profile_c.objects.get_or_create(defaults={'user': self.request.user})
    #     return super().get_object(queryset)

    def get(self, request, *args, **kwargs):
        user_pk = self.kwargs.get('user_pk')
        # user = get_object_or_404(User, pk=user_pk)
        # profile = user.profile
        profile =  profile_c.objects.filter(user__pk=user_pk).first()
        if (not profile):
            profile = profile_c.objects.create(user=self.request.user)
        self.object = profile
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, *, object_list=None, **kwargs):
        # self.object = self.get_object()
        ctx = super().get_context_data(**kwargs)
        return ctx


class login_view_c(base_view_c, LoginView):
    pass


class password_change_view_c(base_view_c, PasswordChangeView):
    def get_success_url(self):
        return reverse('accounts:pass_changed')


class password_change_view_done_c(base_view_c, PasswordChangeDoneView):
    pass


class password_reset_view_c(base_view_c, PasswordResetView):
    email_template_name = 'pass_reset_email.html'
    subject_template_name = 'pass_reset_subject.txt'

    def get_success_url(self):
        return reverse('accounts:pass_reset_done')

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class password_reset_done_view_c(base_view_c, PasswordResetDoneView):
    def get_success_url(self):
        return reverse('accounts:pass_reset_confirm')


class password_reset_confirm_view_c(base_view_c, PasswordResetConfirmView):
    def get_success_url(self):
        return reverse('accounts:pass_reset_complete')


class password_reset_complete_view_c(base_view_c, PasswordResetCompleteView):
    pass
