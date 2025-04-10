from django.contrib.auth.models import User
from django.db import models
from datetime import datetime
from django.db.models import Sum
from django.urls import reverse

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    def uptade_rating(self):
        # 1. Сумма рейтингов всех статей автора × 3
        post_rating = Post.objects.filter(author=self).aggregate(
            total=Sum('rating')
        )['total'] or 0
        post_rating *= 3

        # 2. Сумма рейтингов всех комментариев автора
        comment_rating = Comment.objects.filter(user=self.user).aggregate(
            total=Sum('rating')
        )['total'] or 0

        # 3. Сумма рейтингов всех комментариев к статьям автора
        post_comments_rating = Comment.objects.filter(
            post__author=self
        ).aggregate(
            total=Sum('rating')
        )['total'] or 0

    def __str__(self):
        return self.user.username

class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPES = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость'),
    ]
    post_type = models.CharField(max_length=2, choices=POST_TYPES, default=ARTICLE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=datetime.now)
    category = models.ManyToManyField(Category, through='PostCategory', related_name='posts')
    title = models.CharField(
        max_length=200)
    content = models.TextField()
    rating = models.IntegerField(default=0)
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts_list', args=[str(self.id)])

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(default=datetime.now)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
