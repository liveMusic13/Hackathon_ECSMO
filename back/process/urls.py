from django.urls import path
from process import views


urlpatterns = [
    path('questions/', views.question),
    path('answers/<str:answer_id>/', views.answer_text),
]
