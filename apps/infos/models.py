from django.db import models


class BaseModel(models.Model):
    is_delete = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)

    # 设置 abstract = True 来声明基表，作为基表的Model不能在数据库中形成对应的表
    class Meta:
        abstract = True


class Author(BaseModel):
    id = models.AutoField(primary_key=True)
    author_name = models.CharField(max_length=50, verbose_name='作者名字')
    author_uid = models.BigIntegerField(verbose_name='作者uid')
    author_sec_uid = models.CharField(max_length=100, verbose_name='作者sec_uid')
    author_short_id = models.CharField(max_length=30, verbose_name='作者抖音id')
    author_gender = models.CharField(max_length=30, verbose_name='作者性别')
    author_sign = models.CharField(max_length=500, verbose_name='作者简介')
    author_fans_num = models.IntegerField(verbose_name='作者粉丝数')
    author_favorited = models.BigIntegerField(verbose_name='作者获赞数')
    author_aweme_count = models.BigIntegerField(verbose_name='作者作品数')
    author_unique_id = models.CharField(max_length=30, verbose_name='作者抖音号')

    class Meta:
        db_table = 'Author'  # 设置数据库名
        verbose_name = '抖音作者'  # 设置中文名
        verbose_name_plural = verbose_name  # 需要设置这个不然verbose_name会变成书籍s
        indexes = [models.Index(fields=['author_name']), ]

    def __str__(self):
        return '%s' % self.author_name


class Fans(BaseModel):
    fan_name = models.CharField(max_length=200, verbose_name='粉丝名字')
    fan_uid = models.BigIntegerField(verbose_name='粉丝uid')
    fan_sec_uid = models.CharField(max_length=200, verbose_name='粉丝sec_uid')
    fan_gender = models.IntegerField(default=3, verbose_name='粉丝性别 1：男， 2：女')
    department = models.ForeignKey("Author", on_delete=models.CASCADE,
                                   related_name='employee')
    fan_is_follow = models.IntegerField(default=0, verbose_name='是否已经关注 0：未关注， 1：正在关注, 2: 已经关注')

    class Meta:
        db_table = 'Fans'  # 设置数据库名
        verbose_name = '粉丝'  # 设置中文名
        verbose_name_plural = verbose_name  # 需要设置这个不然verbose_name会变成书籍s

    def __str__(self):
        return '%s' % self.fan_name


# class AuthorFans(BaseModel):
#     author = models.ForeignKey(Author, on_delete=models.CASCADE)
#     fans = models.ForeignKey(Fans, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'AuthorFans'  # 设置数据库名
#         verbose_name = '作者粉丝中间表'  # 设置中文名
#         verbose_name_plural = verbose_name  # 需要设置这个不然verbose_name会变成书籍s
