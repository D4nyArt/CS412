from django.urls import path
from .views import ProfileListView

urlpatterns = [
    path(r'', ProfileListView.as_view(), name='show_all_profiles'),
]