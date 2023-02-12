from django.urls import path 
from django.contrib.auth import views as auth_views
from trackingapp import views

urlpatterns = [ 
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('login/', views.loginpage, name = 'loginuser'),
    path('logout/', views.logoutpage, name = 'logoutuser'),
    path('register/', views.registeruser, name = 'registeruser'),
    path('userform/', views.userform, name = 'user-form'),
    path('userprofile/', views.userprofile, name = 'userprofile'),
    path('update-profile', views.updateprofile, name = 'update-profile'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('dashboard/activity-tracker', views.dashboard_activitiytracker, name = 'dashboard-activitytracker'),
    path('dashboard/food-tracker', views.dashboard_foodtracker, name = 'dashboard-foodtracker'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'trackingapp/password_reset.html'), name = 'password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='trackingapp/password_reset_done.html'), name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'trackingapp/password_reset_confirm.html'), name = 'password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
            template_name = 'trackingapp/password_reset_complete.html'
         ),
         name = 'password_reset_complete'),
]