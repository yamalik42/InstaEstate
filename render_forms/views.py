from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ProfileForm, UserForm, PropertyForm, EnquiryForm
from rest_api.models import Property, Inquiry
from rest_api.serializers import UserSerializer, ProfileSerializer
import requests as Req
from InstaEstate.settings import SERVER_URL
from django.contrib.auth.models import User
from controller.views import prop_mod_auth, enq_auth, paginate_filter_props


# Create your views here.
class HomeView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        api_loc = 'api/property/recent/'
        props = Req.get(url=SERVER_URL+api_loc).json()['props']
        context.update({'is_home': True, 'props': props})
        return context


class LoginView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'is_login': True, 'user_form': UserForm()})
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if request.session.get('login_fail', False):
            context['login_fail'] = True
            del request.session['login_fail']
        return self.render_to_response(context)


class PropertyDetailView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            prop = Property.objects.get(pk=kwargs['pk'])
            prop.images = prop.propertyimage_set.all()
            context.update({'prop': prop, 'single_prop': True})
            is_anon = self.request.user.is_anonymous
            if not is_anon and not enq_auth(self.request.user, prop.pk):
                context['buyer_already_enquired'] = True
        except Property.DoesNotExist:
            return redirect('/')

        return context


class PropertyFormView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if kwargs.get('pk', False):
            prop = Property.objects.get(pk=kwargs['pk'])
            context['upd_prop_form'] = PropertyForm(property=prop)
            context['has_auth'] = prop_mod_auth(self.request.user, prop)
        else:
            context['new_prop_form'] = PropertyForm()
            context['has_auth'] = prop_mod_auth(self.request.user)
            
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['has_auth']:
            return redirect('/')
        return self.render_to_response(context)


class UserProfileFormView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        is_update = kwargs.get('pk', False)

        context.update({
            'user_form': UserForm(), 
            'prof_form': ProfileForm(),
            'user_edit': True,
            'user': self.request.user,
            'upd_forms': dict(),
            'has_auth': not is_update and user.is_anonymous
        })

        if is_update and not user.is_anonymous:
            context['upd_forms']['user'] = UserForm(user=user)
            context['upd_forms']['prof'] = ProfileForm(profile=user.profile)
            try:
                context['has_auth'] = user == User.objects.get(pk=is_update)
            except User.DoesNotExist:
                context['home_redirect'] = True
        
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if not context['has_auth'] or context.get('home_redirect', False):
            return redirect('/')
        return self.render_to_response(context)
        

class UserDetailView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['user_detail'] = User.objects.get(pk=kwargs['pk'])
        except User.DoesNotExist:
            context['home_redirect'] = True

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if context.get('home_redirect', False):
            return redirect('/')
        return self.render_to_response(context)


class EnquiryFormView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['enq_form'] = EnquiryForm()
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous or not enq_auth(user, kwargs['pk']):
            return redirect(f"/property/detail/{kwargs['pk']}/")

        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class EnquiryList(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if context.get('pk', False):
            try:
                context['prop'] = Property.objects.get(pk=context['pk'])
                enqs = context['prop'].inquiry_set.all().order_by('-sent_date')
                context['enqs'] = enqs
            except Property.DoesNotExist:
                context['home_redirect'] = True
            return context

        user = self.request.user
        enqs = Inquiry.objects.all().order_by('-sent_date')
        context['enqs'] = [enq for enq in enqs if enq.property.seller == user]
        return context

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_anonymous or not enq_auth(user, kwargs.get('pk', False)):
            return redirect(f"/property/detail/{kwargs['pk']}/")

        context = self.get_context_data(**kwargs)
        context['is_enq'] = True
        return self.render_to_response(context)


class SearchFormView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        props = Property.objects.all().values
        context['is_search'] = True
        context['states'] = props('state').distinct().order_by('state')
        context['beds'] = props('bedroom').distinct().order_by('bedroom')
        context['baths'] = props('bathroom').distinct().order_by('bathroom')
        context['garages'] = props('garage').distinct().order_by('garage')
        return context


class PropertyListView(TemplateView):
    template_name = 'all.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        props = paginate_filter_props(self.request.GET)
        page = kwargs.get('page', 1)

        try:
            props = props.page(page)
        except EmptyPage:
            props = props.page(paginator.num_pages)

        context['paged_props'] = props
        return context
    