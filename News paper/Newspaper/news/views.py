from django.views.generic import ListView, DetailView
from .models import Post
from  datetime import  datetime

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-date_posted']
    template_name = 'news.html'

    def get_context_data(self, **kwargs):
        # Получаем базовый контекст
        context = super().get_context_data(**kwargs)
        # Добавляем текущее время
        context['time_now'] = datetime.utcnow()
        # Добавляем количество всех новостей
        context['news_count'] = self.get_queryset().count()
        return context

class PostDetailView(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'news_detail.html'

