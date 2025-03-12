from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    # path('login/', views.LoginView.as_view(), name="login")
    
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', views.CustomRefreshTokenView.as_view(), name='token_refresh'),
    path('logout/', views.logout, name='logout'),
    path('authenticated/', views.is_authenticated, name='isauthenticated'),
]