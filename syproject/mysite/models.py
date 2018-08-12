from django.db import models


class ShopUser(models.Model):
    user_name = models.CharField(max_length=64, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256)
    real_name = models.CharField(max_length=64, verbose_name="姓名")
    company = models.CharField(max_length=64, unique=True, verbose_name="公司名")
    email = models.EmailField(max_length=64)
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company

    class Meta:
        ordering = ['-create_date']
        verbose_name = "商家"
        verbose_name_plural = "商家"


class AuditorUser(models.Model):
    user_name = models.CharField(max_length=64, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=256)
    real_name = models.CharField(max_length=64, verbose_name="姓名")
    wk_id = models.CharField(max_length=32, unique=True, verbose_name="工号")
    email = models.EmailField(max_length=64)
    phone_num = models.CharField(max_length=24, verbose_name="手机号")

    def __str__(self):
        return self.real_name

    class Meta:
        ordering = ['id']
        verbose_name = "审核员"
        verbose_name_plural = "审核员"


class Product(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name="产品名称")
    synopsis = models.TextField("简介")
    origin = models.CharField(max_length=64, verbose_name="产地")
    classify = models.CharField(max_length=16, verbose_name="分类")
    producers = models.ForeignKey('ShopUser', on_delete=models.CASCADE, verbose_name="商家")
    is_audit = models.BooleanField(default=False, verbose_name="审核情况")
    create_date = models.DateTimeField("生产日期")
    add_date = models.DateTimeField(auto_now_add=True, verbose_name="创建日期")
    auditor = models.ForeignKey('AuditorUser', on_delete=models.CASCADE, verbose_name="审核员")
    Audit_date = models.DateTimeField("审核日期")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-add_date']
        verbose_name = "产品"
        verbose_name_plural = "产品"
