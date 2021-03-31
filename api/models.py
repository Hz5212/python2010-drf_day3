from django.db import models


# Create your models here.
# 抽象表  基表
class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Book(BaseModel):
    book_name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    pic = models.ImageField(upload_to="pic", default="pic/1.png")
    publish = models.ForeignKey(to="Press", on_delete=models.CASCADE, db_constraint=False, related_name="books")
    authors = models.ManyToManyField(to="Author", db_constraint=False, related_name="books")

    # 自定义序列化字段
    @property
    # 返回每本图书对应的出版社
    def publish_name(self):
        return self.publish.press_name

    @property
    # 返回当前图书出版社的地址
    def press_address(self):
        return self.publish.address

    @property
    # 返回当前图书对应作者信息
    def author_list(self):
        return self.authors.values("author_name", "age", "detail__phone")

    class Meta:
        db_table = "day3_book"
        verbose_name = "图书"
        verbose_name_plural = verbose_name

    # 格式化当前对象输出格式,查询时显示的对象的名字
    def __str__(self):
        return self.book_name


class Press(BaseModel):
    press_name = models.CharField(max_length=50)
    pic = models.ImageField(upload_to="pic", default="pic/1.png")
    address = models.CharField(max_length=256)

    class Meta:
        db_table = "day3_press"
        verbose_name = "出版社"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.press_name


class Author(BaseModel):
    author_name = models.CharField(max_length=128)
    age = models.IntegerField()

    class Meta:
        db_table = "day3_author"
        verbose_name = "作者"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.author_name


class AuthorDetail(BaseModel):
    phone = models.CharField(max_length=11)
    author = models.OneToOneField(to="Author", on_delete=models.CASCADE, related_name="detail")

    class Meta:
        db_table = "day3_author_detail"
        verbose_name = "作者详情"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s的详情" % self.author.author_name
