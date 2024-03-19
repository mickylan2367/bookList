from django.contrib import admin

# Register your models here.
# サイトの管理画面を開いた時、データベースを認識させる
from .models import Book, Review
admin.site.register(Book)
admin.site.register(Review)