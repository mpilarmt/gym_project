from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('admin/', admin.site.urls),
    path('profile/edit/', views.profile_edit, name='profile_edit'),


    #path('test-create/', views.test_create_user, name='test-create'),

]


# nomes index.html
# from django.urls import path
# from . import views
# Create your views here.

# urlpatterns = [
#     path('', views.index, name='index'),
# ]
