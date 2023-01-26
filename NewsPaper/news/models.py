from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        posts_rating = sum([post.rating for post in Post.objects.filter(author=self)]) * 3
        comments_rating = sum([comment.rating for comment in Comment.objects.filter(user=self.user)])

        posts_comments_list = []

        for _post_ in Post.objects.filter(author=self):
            for comment in Comment.objects.filter(post=_post_):
                posts_comments_list.append(comment.rating)

        posts_comments_rating = sum(posts_comments_list)

        self.rating = sum([posts_rating, comments_rating, posts_comments_rating])
        self.save()


class Category(models.Model):
    theme = models.CharField(unique=True, max_length=150)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=(
        ("article", "Article"),
        ("news", "News")))
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through="PostCategory")
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def prewiew(self):
        return self.text[:124] + "..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
