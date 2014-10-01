import hashlib
import random
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.shortcuts import redirect,render_to_response
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.contrib.sites.models import RequestSite, Site
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.template import RequestContext, loader
from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



from registration import signals
from forms import RegistrationForm
from trendzmania.models import User

class Home(TemplateView):
    template_name = 'tm/home.html'

class ShoppingBag(TemplateView):
    template_name = 'tm/shopping-bag.html'





class _RequestPassingFormView(FormView):
    """
    A version of FormView which passes extra arguments to certain
    methods, notably passing the HTTP request nearly everywhere, to
    enable finer-grained processing.

    """
    def get(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        # Pass request to get_form_class and get_form for per-request
        # form control.
        form_class = self.get_form_class(request)
        form = self.get_form(form_class)
        if form.is_valid():
            # Pass request to form_valid.
            return self.form_valid(request, form)
        else:
            return self.form_invalid(form)

    def get_form_class(self, request=None):
        return super(_RequestPassingFormView, self).get_form_class()

    def get_form_kwargs(self, request=None, form_class=None):
        return super(_RequestPassingFormView, self).get_form_kwargs()

    def get_initial(self, request=None):
        return super(_RequestPassingFormView, self).get_initial()

    def get_success_url(self, request=None, user=None):
        # We need to be able to use the request and the new user when
        # constructing success_url.
        return super(_RequestPassingFormView, self).get_success_url()

    def form_valid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_valid(form)

    def form_invalid(self, form, request=None):
        return super(_RequestPassingFormView, self).form_invalid(form)


class RegistrationView(_RequestPassingFormView):
    """
    Base class for user registration views.

    """
    disallowed_url = 'registration_disallowed'
    form_class = RegistrationForm
    http_method_names = ['get', 'post', 'head', 'options', 'trace']
    success_url = None
    template_name = 'registration/registration_form.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        if not self.registration_allowed(request):
            return redirect(self.disallowed_url)
        return super(RegistrationView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, request, form):
        new_user = self.register(request, **form.cleaned_data)
        #success_url = self.get_success_url(request, new_user)
        # success_url may be a simple string, or a tuple providing the
        # full argument set for redirect(). Attempting to unpack it
        # tells us which one it is.
        try:
            to, args, kwargs = '/register/complete/'
            return redirect(to, *args, **kwargs)
        except ValueError:
            return redirect(reverse('registration_complete'))

    def registration_allowed(self, request):
        """
        Override this to enable/disable user registration, either
        globally or on a per-request basis.

        """
        return True

    def register(self, request, **cleaned_data):
        """
        Implement user-registration logic here. Access to both the
        request and the full cleaned_data of the registration form is
        available here.

        """
        first_name = cleaned_data['first_name']
        last_name = cleaned_data['last_name']
        email=cleaned_data['email']
        username = '%s %s' %(first_name, last_name)
        new_user = User.objects.create(email=cleaned_data['email'],phone=cleaned_data['phone'],address1=cleaned_data['address1'],\
                                       address2 = cleaned_data['address2'],city = cleaned_data['city'],\
                                       country = cleaned_data['country'],state = cleaned_data['state'],\
                                        zipcode = cleaned_data['zipcode'])
        new_user.set_password(cleaned_data['password1'])
        new_user.last_name = last_name
        new_user.first_name = first_name
        new_user.username = username
        new_user.is_active = False
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        if isinstance(email, unicode):
            email = email.encode('utf-8')
        new_user.activation_key = hashlib.sha1(salt+email).hexdigest() 
        #new_user.phone = cleaned_data['phone']
        #new_user.address1 = cleaned_data['address1']
        #new_user.address2 = cleaned_data['address2']
        #new_user.city = cleaned_data['city']
        #new_user.country = cleaned_data['country']
        #new_user.state = cleaned_data['state']
        #new_user.zipcode = cleaned_data['zipcode']
        new_user.save()
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
            
        send_activation_email(new_user, site)    
                
        
        signals.user_registered.send(sender=User,
                                     user=new_user,
                                     request=request)
        
        
        return HttpResponseRedirect(reverse('registration_complete'))
    
    
def send_activation_email(user, site):
        '''
        Send an activation email to the user associated with this User object.          
        '''

        ctx_dict = {'activation_key': user.activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'static_url': settings.STATIC_URL,}

        subject = render_to_string('registration/activation_email_subject.txt',
                                   ctx_dict)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        
        message_text = render_to_string('registration/activation_email.txt', ctx_dict)
        message_html = render_to_string('registration/activation_email.html', ctx_dict)

        msg = EmailMultiAlternatives(subject, message_text, settings.DEFAULT_FROM_EMAIL, [user.email])
        print settings.DEFAULT_FROM_EMAIL,[user.email]
        msg.attach_alternative(message_html, "text/html")
        msg.send()
        
        
def activate(request, activation_key, template_name='registration/activate.html',
             success_url=None, extra_context=None, **kwargs):
    """
    Activate a user's account.
    """ 
    #activated = User.objects.activate_user(activation_key)
    #print activated,"activated activated"
    try:
        user = User.objects.get(activation_key=activation_key)
    except User.DoesNotExist:
        raise 
    user.is_active = True
    #user.activation_key = u"ALREADY_ACTIVATED"    
    user.save()
    if user:
        signals.user_activated.send(sender=User,
                                    user=user,
                                    request=request)

        if settings.AUTHENTICATE_WHEN_ACTIVATE:
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)

        if success_url is None:
            return redirect('registration_activation_complete', **kwargs)
        else:
            return redirect(success_url)

    if extra_context is None:
        extra_context = {}
    context = RequestContext(request)
    for key, value in extra_context.items():
        context[key] = callable(value) and value() or value
    print kwargs,context    

    return render_to_response(template_name,
                              kwargs,
                              context_instance=context)



def category(request):
    return render_to_response('category.html',
                          {},
                          context_instance=RequestContext(request))
    
    
    
    