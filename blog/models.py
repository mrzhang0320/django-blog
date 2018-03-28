import markdown
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.urls import reverse


@python_2_unicode_compatible
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    created_time = models.DateTimeField()
    #最后修改时间
    modified_time = models.DateTimeField()
    #文章摘要
    excerpt = models.CharField(max_length=200, blank=True)
    #分类
    category = models.ForeignKey(Category)
    #标签
    tags = models.ManyToManyField(Tag, blank=True)
    #作者
    author = models.ForeignKey(User)
    #阅读量
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extenstions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post, self).save(*args, **kwargs)

