from django.urls import path
from .views import ProfileListView, ProfileDetailView

urlpatterns = [
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
    path(r'profile/<int:pk>', ProfileDetailView.as_view(), name="show_profile")
]