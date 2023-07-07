from django.urls import path
from . import views

urlpatterns = [
    path('email/activation/',views.RagistrationView.as_view(),name='ragistration'),
    path('email/activation/<str:uid>/<str:token>/',views.ActivationView.as_view(),name='activate')
    
]
