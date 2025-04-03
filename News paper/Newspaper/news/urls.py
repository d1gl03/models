from django.urls import path
# Импортируем созданные нами представления
from .views import PostListView, PostDetailView

urlpatterns = [

   path('', PostListView.as_view()),
   path('<int:pk>', PostDetailView.as_view()),
    ]