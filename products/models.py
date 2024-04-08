from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    # Sử dụng AutoField để tạo ra một trường int tự tăng
    # primary_key=True để chỉ định khóa chính cho bảng
    id = models.AutoField(primary_key=True)
    # Sử dụng CharField để tạo ra một trường kiểu varchar, max_length là attribute bắt buộc
    name = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)
    # Cho phép một trường varchar có thể nhận giá trị null
    icon_url = models.CharField(max_length=128, null=True)
    # Sử dụng DateTimeField để tạo ra một trường kiểu String dạng Datetime
    # default=timezone.now sẽ gán giá trị mặc định là thời điểm tạo record
    created_at = models.DateTimeField(default=timezone.now)
    # auto_now sẽ tự động gán giá trị datetime mới mỗi khi record được update
    updated_at = models.DateTimeField(auto_now=True)
    # delete_at dùng để soft delete
    deleted_at = models.DateTimeField(null=True)


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=3)
    # Sử dụng FloatField, IntegerField để tạo trường kiểu số
    price = models.FloatField()
    discount = models.IntegerField()
    amount = models.IntegerField()
    rating = models.FloatField(default=0)
    favorite = models.IntegerField(default=0)
    mix = models.CharField(max_length=128)
    weight = models.FloatField()
    is_public = models.BooleanField(null=True, blank=True)
    thumbnail = models.CharField(max_length=128)
    review = models.IntegerField(default=0)
    description = models.TextField(verbose_name='Description')
    # sử dụng ForeignKey để khai báo một field là khóa ngoại từ một bảng khác
    # on_delete=models.CASCADE để mô tả khi bảng category bị xóa một record...
    # thì tất cả record product có id tương ứng sẽ bị xóa theo
    # related_name thể hiện khi query ở bảng category...
    # tất cả các record product con sẽ được hiển thị trong một mảng có tên là products
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,
                                    related_name='products', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


@receiver(post_save, sender=Product)
def update_product_rating(sender, instance, **kwargs):
    if kwargs.get('created', False):
        return

    total_favorite = Product.objects.filter(category_id=instance.category_id).aggregate(
        total_favorite=models.Sum('favorite'))['total_favorite'] or 0
    new_rating = total_favorite / \
        Product.objects.filter(category_id=instance.category_id).count()
    instance.category_id.rating = min(5, max(0, new_rating))
    instance.category_id.save()


class Meta:
    # Sắp xếp mặc định khi query là giảm dần theo ngày tạo
    ordering = ['-created_at']
    indexes = [
        # Chỉ mục index sẽ đánh theo field created_at
        models.Index(fields=['created_at'])
    ]


class ProductImage(models.Model):
    id = models.AutoField(primary_key=True)
    image_url = models.CharField(max_length=128)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_images', null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)


class ProductComment(models.Model):
    id = models.AutoField(primary_key=True)
    rating = models.IntegerField()
    comment = models.CharField(max_length=512)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   related_name='product_comments', null=False)
    # user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    # ForeignKey('self',...) diễn tả mối quan hệ cha - con trong cùng một bảng
    # Một comment có nhiều người rep lại, thì comment gốc sẽ không có parent_id...
    # còn các comment rep lại sẽ có parent_id là id của comment gốc
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                null=False)
