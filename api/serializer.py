from rest_framework.serializers import ModelSerializer
from rest_framework import serializers, exceptions

from api.models import Book, Press


class PressModeSerializer(ModelSerializer):
    #出版社序列化器
    class Meta:
        model = Press
        fields = ("press_name", "address", "pic")

    #图书的序列化器
class BookModelSerializer(ModelSerializer):
    #多表连表查询
    publish = PressModeSerializer()

    class Meta:
        # 指定当前要序列化器的模型
        model = Book
        # 指定你要序列化的字段
        fields = ("book_name", "price", "publish")

class BookDeModelSerializer(ModelSerializer):
    #反序列化器  用于数据入库
    class Meta:
        model = Book
        # 指定反序列化需要的字段
        fields = ("book_name", "price", "publish", "authors")
        # 添加DRF官方所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填
                "min_length": 1,  # 最小长度
                "error_messages": {
                    "required": "请填写图书名称",
                    "min_length": "图书名长度太短"
                }
            },
            "price": {
                "max_digits": 5,
            }
        }

    def validate_book_name(self, value):
        book = Book.objects.filter(book_name=value)
        if book:
            raise exceptions.ValidationError("图书名已存在")
        return value
    def validate(self, attrs):
        # 自定义校验规则
        return attrs

class BookModelSerializerV2(ModelSerializer):
    #序列化器与反序列化器整合

    class Meta:
        model = Book
        # 字段的填写项目
        fields = ("book_name", "price", "publish", "authors", "pic")

        # 添加DRF官方所提供的校验规则
        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 1,
                "error_messages": {
                    "required": "请填写图书名称V2",
                    "min_length": "图书名长度太短"
                }
            },
            # 指定该字段只参与反序列化  保存时提交
            "publish": {
                "write_only": True,
            },
            "authors": {
                "write_only": True,
            },
            # 指定该字段只参与序列化  查询时使用
            "pic": {
                "read_only": True
            }
        }

    def validate_book_name(self, value):
        book = Book.objects.filter(book_name=value)
        if book:
            raise exceptions.ValidationError("图书名已存在")
        return value

    def validate(self, attrs):
        price = attrs.get("price")
        if price > 1000:
            raise exceptions.ValidationError("太贵啦")
        return attrs

