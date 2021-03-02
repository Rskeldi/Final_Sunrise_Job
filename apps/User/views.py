import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.utils.translation import gettext as _
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.User.forms import UserEditForm, UserRegistrationForm
from apps.User.serializers import RegisterApiSerializer, LoginSerializer, UserEditSerializer, RefreshSerializer

User = get_user_model()


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'user/registration.html'

    def get_success_url(self, *args):
        messages.success(self.request,
                         (_(f"Ты успешно зарегистрировался! Тебе на {self.object.email} придет сообщение с активацией аккаунта. \nПОКА НЕ АКТИВИРУЕШЬ, ВОЙТИ НЕ СМОЖЕШЬ")))
        return reverse_lazy('account_edit')


class UserActivationView(TemplateView):

    def get(self, request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return render(request, 'user/activation_complete.html')

        except User.DoesNotExist:
            return render(request, 'user/off_link.html', {})


def update_profile(request):
    if request.user.is_authenticated:
        args = {}
        if request.method == 'POST':
            json_post = json.load(request)
            user = User.objects.get(pk=request.user.pk)
            user.first_name = json_post['first_name']
            user.last_name = json_post['last_name']
            user.save()
        form = UserEditForm()
        obj = User.objects.get(pk=request.user.pk)
        args['form'] = form
        args['object'] = obj
        return render(request, 'user/user_edit.html', args)
    else:
        return render(request, 'user/register_complete.html', {})


"""
API VIEWS STARTED
"""


class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterApiSerializer(
            data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                user.is_active = False
                user.save()
                user.email_user()
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )


class LoginApiView(TokenObtainPairView):
    LoginSerializer


class TokenRefresh(TokenRefreshView):
    serializer_class = RefreshSerializer


class EditUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserEditSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        obj = User.objects.get(pk=self.request.user.pk)
        return obj
