from statistics import mode
import markdown
from django.utils.html import strip_tags
from audioop import reverse
from multiprocessing import set_forkserver_preload
from time import time
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField
from django.utils import timezone
from django.urls import reverse
# Create your models here.

class Category(models.Model):
    name = CharField(max_length=200)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name

class Tag(models.Model):
    name = CharField(max_length=200)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return self.name

class Post(models.Model):
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    modified_time = models.DateTimeField('修改时间')
    excerpt = models.CharField('摘要', max_length=200, blank=True)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0, editable=False)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def save(self, *args, **kwargs):
        self.modified_time = timezone.now()
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:54]

        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.title
    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])