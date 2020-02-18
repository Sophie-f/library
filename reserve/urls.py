from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'reserve'
urlpatterns = [
    path('', views.HomePageView.as_view(), name='homepage'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signup_done/', views.SignUpDoneView.as_view(), name='signup_done'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('details/<int:pk>/', views.DetailsView.as_view(), name='details'),
    path('accounts/login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('edit/', views.EditView.as_view(), name='edit'),

]


# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']
