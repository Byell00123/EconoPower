##################################################################################
# from __future__ import absolute_import
##################################################################################


#from django import forms
from django.db import models


##################################################################################
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from django.contrib.auth import login, password_validation
# from requests import post
# from importlib import import_module
# from django import forms
# from django.contrib.auth import password_validation
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.contrib.sites.shortcuts import get_current_site
# from django.core import exceptions, validators
# from django.urls import reverse
# from django.utils.translation import gettext, gettext_lazy as _, pgettext
# from allauth.utils import (
#     build_absolute_uri,
#     get_username_max_length,
#     set_form_field_order,
# )
# from allauth import app_settings
# from allauth.account.adapter import get_adapter
# from allauth.app_settings import AuthenticationMethod
# from .models import EmailAddress
# from allauth.utils import (
#     assess_unique_email,
#     filter_users_by_email,
#     get_user_model,
#     perform_login,
#     setup_user_email,
#     sync_user_email_addresses,
#     url_str_to_user_pk,
#     user_email,
#     user_pk_to_url_str,
#     user_username,
# )
# from allauth.account import (PasswordField,loginform,BaseSignupForm)
#  ##################################################################################
# class LoginFormatado(forms.Form,PasswordField,loginform):
#     password = PasswordField(label=_("Nada"), autocomplete="current-password")
#     remember = forms.BooleanField(label=_("Nadinha"), required=False)

#     user = None
#     error_messages = {
#         "account_inactive": _("This account is currently inactive."),
#         "email_password_mismatch": _(
#             "The email address and/or password you specified are not correct."
#         ),
#         "username_password_mismatch": _(
#             "The username and/or password you specified are not correct."
#         ),
#     }

#     def __init__(self, *args, **kwargs):
#         self.request = kwargs.pop("request", None)
#         super(LoginFormatado, self).__init__(*args, **kwargs)
#         if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
#             login_widget = forms.TextInput(
#                 attrs={
#                     "type": "email",
#                     "placeholder": _("Email address"),
#                     "autocomplete": "email",
#                 }
#             )
#             login_field = forms.EmailField(label=_("Email"), widget=login_widget)
#         elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
#             login_widget = forms.TextInput(
#                 attrs={"placeholder": _("Username"), "autocomplete": "username"}
#             )
#             login_field = forms.CharField(
#                 label=_("Username"),
#                 widget=login_widget,
#                 max_length=get_username_max_length(),
#             )
#         else:
#             assert (app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME_EMAIL)
#             login_widget = forms.TextInput(
#                 attrs={"placeholder": _("Username or email"), "autocomplete": "email"}
#             )
#             login_field = forms.CharField(
#                 label=pgettext("field label", "Login"), widget=login_widget
#             )
#         self.fields["login"] = login_field
#         set_form_field_order(self, ["login", "password", "remember"])
#         if app_settings.SESSION_REMEMBER is not None:
#             del self.fields["remember"]

#     def user_credentials(self):
#         """
#         Provides the credentials required to authenticate the user for
#         login.
#         """
#         credentials = {}
#         login = self.cleaned_data["login"]
#         if app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.EMAIL:
#             credentials["email"] = login
#         elif app_settings.AUTHENTICATION_METHOD == AuthenticationMethod.USERNAME:
#             credentials["username"] = login
#         else:
#             if self._is_login_email(login):
#                 credentials["email"] = login
#             credentials["username"] = login
#         credentials["password"] = self.cleaned_data["password"]
#         return credentials

#     def clean_login(self):
#         login = self.cleaned_data["login"]
#         return login.strip()

#     def _is_login_email(self, login):
#         try:
#             validators.validate_email(login)
#             ret = True
#         except exceptions.ValidationError:
#             ret = False
#         return ret

#     def clean(self):
#         super(LoginFormatado, self).clean()
#         if self._errors:
#             return
#         credentials = self.user_credentials()
#         user = get_adapter(self.request).authenticate(self.request, **credentials)
#         if user:
#             self.user = user
#         else:
#             auth_method = app_settings.AUTHENTICATION_METHOD
#             if auth_method == app_settings.AuthenticationMethod.USERNAME_EMAIL:
#                 login = self.cleaned_data["login"]
#                 if self._is_login_email(login):
#                     auth_method = app_settings.AuthenticationMethod.EMAIL
#                 else:
#                     auth_method = app_settings.AuthenticationMethod.USERNAME
#             raise forms.ValidationError(
#                 self.error_messages["%s_password_mismatch" % auth_method]
#             )
#         return self.cleaned_data

#     def login(self, request, redirect_url=None):
#         email = self.user_credentials().get("email")
#         ret = perform_login(
#             request,
#             self.user,
#             email_verification=app_settings.EMAIL_VERIFICATION,
#             redirect_url=redirect_url,
#             email=email,
#         )
#         remember = app_settings.SESSION_REMEMBER
#         if remember is None:
#             remember = self.cleaned_data["remember"]
#         if remember:
#             request.session.set_expiry(app_settings.SESSION_COOKIE_AGE)
#         else:
#             request.session.set_expiry(0)
#         return ret

# class SignupForm(BaseSignupForm):
#     def __init__(self, *args, **kwargs):
#         super(SignupForm, self).__init__(*args, **kwargs)
#         self.fields["password1"] = PasswordField(
#             label=_("Password"),
#             autocomplete="new-password",
#             help_text=password_validation.password_validators_help_text_html(),
#         )
#         if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
#             self.fields["password2"] = PasswordField(
#                 label=_("Password (again)"), autocomplete="new-password"
#             )

#         if hasattr(self, "field_order"):
#             set_form_field_order(self, self.field_order)

#     def clean(self):
#         super(SignupForm, self).clean()

#         # `password` cannot be of type `SetPasswordField`, as we don't
#         # have a `User` yet. So, let's populate a dummy user to be used
#         # for password validation.
#         User = get_user_model()
#         dummy_user = User()
#         user_username(dummy_user, self.cleaned_data.get("username"))
#         user_email(dummy_user, self.cleaned_data.get("email"))
#         password = self.cleaned_data.get("password1")
#         if password:
#             try:
#                 get_adapter().clean_password(password, user=dummy_user)
#             except forms.ValidationError as e:
#                 self.add_error("password1", e)

#         if (
#             app_settings.SIGNUP_PASSWORD_ENTER_TWICE
#             and "password1" in self.cleaned_data
#             and "password2" in self.cleaned_data
#         ):
#             if self.cleaned_data["password1"] != self.cleaned_data["password2"]:
#                 self.add_error(
#                     "password2",
#                     _("You must type the same password each time."),
#                 )
#         return self.cleaned_data

#     def save(self, request):
#         if self.account_already_exists:
#             raise ValueError(self.cleaned_data.get("email"))
#         adapter = get_adapter()
#         user = adapter.new_user(request)
#         adapter.save_user(request, user, self)
#         self.custom_signup(request, user)
#         # TODO: Move into adapter `save_user` ?
#         setup_user_email(request, user, [])
#         return user
##################################################################################

#  class CadastroFormatado(UserCreationForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["username"].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"username",
#         })
#         self.fields["password1"].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"password1",
            
#         })
#         self.fields["password2"].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"password2",
#         })
#         self.fields["email"].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"email",
#         })
#     class Meta:
#         model = post
#         fields = ['username','email','password1','password2']

# class LoginFormatado(UserCreationForm,password_validation):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields[login].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"login",
#         })
#         self.fields[password_validation].widget.attrs.update({
#             "class":"input100",
#             "type":"text",
#             "name":"password_validation",
#         })
           
#     class Meta:
#         model = User
#         fields = ['login','password_validation']
    