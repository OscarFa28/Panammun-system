from django.urls import path
from django.contrib.auth import views as auth_views
from .views import home_page, admin_panel_page, public_panel_page, create_account, CreateUserAPIView, UpdateUserStatusAPIView, AssignCountryView
from panammun_panel import views

app_name = 'panammun_panel'

urlpatterns = [
    path('',views.home_page, name="home"),
    path('adminPanel/',views.admin_panel_page, name="admin-panel"),
    path('panel/',views.public_panel_page, name="panel"),
    path('createAccount/', views.create_account, name="create-account"),
    path('meetUs/', views.meet_us, name="meet-us"),
    
    path('usersApi/', CreateUserAPIView.as_view(), name='users-api'),
    path('updateUserApi/', UpdateUserStatusAPIView.as_view(), name='update-user-api'),
    path('selectCountry/', AssignCountryView.as_view(), name='select-country'),
]