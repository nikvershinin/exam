from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Автор')

    def get_absolute_url(self):
        return f'/posts/{self.pk}'

    def __str__(self):
        return self.authorUser.username

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'

class Category(models.Model):
    CATEGORY_CHOISES = (
        ('tanks', 'Танки'),
        ('heals', 'Хилы'),
        ('dd', 'ДД'),
        ('traders', 'Торговцы'),
        ('guildMasters', 'Гилдмастеры'),
        ('smiths', 'Кузнецы'),
        ('skinmakers', 'Кожевники'),
        ('poisonmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    )
    categoryType = models.CharField(max_length=32, choices=CATEGORY_CHOISES, default='tanks', verbose_name='Категория')
    subscribers = models.ManyToManyField(User, related_name='categories')

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = RichTextUploadingField()
    postCategory = models.ManyToManyField(Category, verbose_name='Категория')

    class Meta:
        verbose_name = 'Объясвление'
        verbose_name_plural = 'Объявления'

    # def __str__(self):
    #     return self.title()

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/post/{self.pk}'

    def preview(self):
        return self.text[0:123] + '...'

class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.pk} {self.commentUser.username} {self.commentPost.title[:200]}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'