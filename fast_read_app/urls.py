from django.urls import path
from .views import HomePageView
from .read_request_handler import get_text_and_quetions
urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('get_text_and_questions/', get_text_and_quetions, name='get_text_and_quetions'), 
]
