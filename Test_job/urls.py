from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from Test_job import settings
from apps.Cards.views import CardListView, CardDetailView, IndexView, CategoryDetailView, CategoryListView, SearchView
from apps.User.views import update_profile, UserRegistrationView, UserActivationView, RegisterApiView, LoginApiView, \
    EditUserView, TokenRefresh

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/register/', RegisterApiView.as_view(), name='api_register'),
    path('api/v1/login/', LoginApiView.as_view()),
    path('api/v1/edit/', EditUserView.as_view()),
    path('api/v1/token-refresh/', TokenRefresh.as_view()),
    path('rosetta/', include('rosetta.urls')),
    path('social-auth/', include('social_django.urls'), name='social'),
]


urlpatterns += i18n_patterns(
    path('', IndexView.as_view(), name='index'),
    path('account/', update_profile, name='account_edit'),
    path('account/register/', UserRegistrationView.as_view(), name='signup'),
    path('account/login/', LoginView.as_view(), name='login'),
    path('account/logout/', LogoutView.as_view(), name='logout'),
    path('account/activate/<uuid:activation_code>/', UserActivationView.as_view(), name='activate_account'),
    path('cards/', CardListView.as_view(), name='index_cards'),
    path('cards/<int:pk>/', CardDetailView.as_view(), name='card_detail'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category'),

    path('search/', SearchView.as_view(), name='search'),
)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
