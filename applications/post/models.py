from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    name = models.SlugField(primary_key=True)
    parent = models.ForeignKey('Category', on_delete=models.CASCADE,blank=True, null=True,related_query_name='children')
    
    def __str__(self):
        return self.name
    
    
class Post(models.Model):
    title = models.CharField(max_length=80)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Post')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Post')
    # image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['id']

    # def save(self):
    #     pass


class Image(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')

    
    
class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='comment', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.owner.username} {self.post.title}"


class Like(models.Model):
    """
    likes model
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes') # Post.objects.likes
    like = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} -> {self.like}'


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='ratings')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ], blank=True, null=True
    )

    def __str__(self):
        return f'{self.owner} -> {self.rating}'