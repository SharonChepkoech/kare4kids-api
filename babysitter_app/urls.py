
from django.urls import path
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import SitterList, ProfileView, mark_job_completed, ProfilePictureUploadView, UpdateParentProfileView, UpdateSitterProfileView, RequestSitterView, UserProfileView, SitterBookingsView, ParentBookingsView,CancelBookingView,  UpdateBookingStatusView ,CurrentUserView, JobListView, SitterDetail, RegisterAPIView, LoginAPIView, UserListView, CreateSitterView, UpdateSitterView, ParentCreateView, ParentUpdateView, ParentDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path("api/register/", RegisterAPIView.as_view(), name="register"),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('sitters/', views.sitter_list, name='sitter_list'),
    path('sitters/create/', CreateSitterView.as_view(), name='create_sitter'),
    path('sitters/update/<int:pk>/', UpdateSitterView.as_view(), name='update_sitter'),
    path('sitters/delete/<int:pk>/', views.delete_sitter, name='delete_sitter'),
    path('api/request-sitter/<int:sitter_id>/', RequestSitterView.as_view(), name='request_sitter'),
    path("api/current-user/", CurrentUserView.as_view(), name="current-user"),
    path('api/sitters/<int:pk>/', SitterDetail.as_view(), name='sitter_detail'),
    path('sitters/search/', views.search_sitters, name='search_sitters'), 
    path('api/sitters/', SitterList.as_view(), name='sitter_list_api'), 
    path('parents/', views.parent_list, name='parent_list'), 
    path('parents/create/', ParentCreateView.as_view(), name='create_parent'),
    path('parents/update/<int:pk>/', ParentUpdateView.as_view(), name='update_parent'),
    path('parents/delete/<int:pk>/', ParentDeleteView.as_view(), name='delete_parent'),
    path('jobs/request/', RequestSitterView.as_view(), name='request_sitter'),  # POST
    path('api/sitter/bookings/', SitterBookingsView.as_view(), name='sitter-bookings'),
    path('jobs/', JobListView.as_view(), name='job_list'),  # GET
    path("api/bookings/<int:id>/", UpdateBookingStatusView.as_view(), name="update-booking"),
    path("api/bookings/parent/", ParentBookingsView.as_view(), name="parent-bookings"),
    path("api/bookings/<int:id>/cancel/", CancelBookingView.as_view(), name="cancel-booking"),
    path("profile/", UserProfileView.as_view(), name="user-profile"),
    path("profile/sitter/", UpdateSitterProfileView.as_view(), name="update_sitter_profile"),
    path("profile/parent/", UpdateParentProfileView.as_view(), name="update_parent_profile"),
    path("api/profile/upload-picture/", ProfilePictureUploadView.as_view(), name="upload-profile-picture"),
    path("api/profile/", ProfileView.as_view(), name="user-profile"),
    path('api/jobs/<int:id>/complete/', mark_job_completed, name='mark_job_completed'),
]
