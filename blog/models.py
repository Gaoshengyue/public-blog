from django.db import models
from django.contrib import auth
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):
    """
    用户信息
    """
    nid = models.AutoField(primary_key=True)
    nickname = models.CharField(verbose_name='昵称', max_length=32)
    telephone = models.CharField(max_length=11, null=True, unique=True)
    avatar = models.FileField(upload_to = 'avatar/',default="avatar/default.jpg")
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.OneToOneField(to='Blog', to_field='nid',null=True)

    def __str__(self):
        return self.username

class Blog(models.Model):

    """
    博客信息
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='个人博客标题', max_length=64)
    site = models.CharField(verbose_name='个人博客后缀', max_length=32, unique=True)
    theme = models.CharField(verbose_name='博客主题', max_length=32)

    def __str__(self):
        return self.title

class HomeCategory(models.Model):
    """
    博主个人文章分类表
    """
    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='分类标题', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

    def __str__(self):
        return self.title
class Tag(models.Model):

    nid = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blog = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='nid')

class Article(models.Model):

    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')

    comment_count= models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)

    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    homeCategory = models.ForeignKey(to='HomeCategory', to_field='nid', null=True)
    siteDetaiCategory = models.ForeignKey(to='SiteDetaiCategory', to_field='id', null=True)
    user = models.ForeignKey(verbose_name='作者', to='UserInfo', to_field='nid')
    tags = models.ManyToManyField(
        to="Tag",
        through='Article2Tag',
        through_fields=('article', 'tag'),
    )


    def __str__(self):
        return self.title

class ArticleDetail(models.Model):
    """
    文章详细表
    """
    nid = models.AutoField(primary_key=True)
    content = models.TextField()

    article = models.OneToOneField(to='Article', to_field='nid')

class Comment(models.Model):
    """
    评论表
    """
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='nid')
    user = models.ForeignKey(verbose_name='评论者', to='UserInfo', to_field='nid')
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    parent_comment = models.ForeignKey('self', null=True)


    def __str__(self):
        return self.content

class ArticleUpDown(models.Model):
    """
    点赞表
    """
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('UserInfo', null=True)
    article = models.ForeignKey("Article", null=True)
    is_up=models.BooleanField(default=True)
    is_down = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]

class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='文章', to="Article", to_field='nid')
    tag = models.ForeignKey(verbose_name='标签', to="Tag", to_field='nid')

    class Meta:
        unique_together = [
            ('article', 'tag'),
        ]

class SiteCategory(models.Model):
    name=models.CharField(max_length=32)

    def __str__(self):
        return  self.name
class SiteDetaiCategory(models.Model):
    name=models.CharField(max_length=32)
    siteCategory=models.ForeignKey("SiteCategory")

    def __str__(self):
        return self.name