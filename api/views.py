from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Book
from api.serializer import BookModelSerializer, BookDeModelSerializer, BookModelSerializerV2


# Create your views here.

class BookAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # 查询单个
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            book_serializer = BookModelSerializer(book_obj).data

            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_serializer
            })
        else:
            book_set = Book.objects.all()
            book_set_serializer = BookModelSerializer(book_set, many=True).data

            return Response({
                "status": 200,
                "message": "set succeed",
                "results": book_set_serializer
            })

    def post(self, request, *args, **kwargs):
        # 新增
        request_data = request.dara
        # 将参数交给反序列化进行校验
        serializer = BookDeModelSerializer(data=request_data)
        # 校验数据，失败则抛出异常
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 201,
            "message": "put succeed",
            "results": BookModelSerializer(book_obj).data
        })

    def delete(self, request, *args, **kwargs):
        # 删除对象（单个&多个）
        book_id = kwargs.get("id")
        if book_id:
            # 如果id存在，则删除单个
            ids = [book_id]
        else:
            # 要删除多个
            ids = request.data.get("ids")
        print(ids)
        # 判断是否存在且未删除
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 202,
                "message": "delete succeed"
            })

        return Response({
            "status": 400,
            "message": "删除失败或删除的图书不存在"
        })

    def put(self, request, *args, **kwargs):
        # 修改单个对象的全部字段
        # 要修改的值
        request_data = request.data
        # 获取图书id
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 401,
                "message": "图书不存在"
            })
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj)
        book_serializer.is_valid(raise_exception=True)
        # 经过序列化器校验后，保存修改后的值
        book = book_serializer.save()

        return Response({
            "status": 203,
            "message": "put succeed",
            "results": BookModelSerializerV2(book).data
        })

    def patch(self, request, *args, **kwargs):
        #完成修改的单个对象的字段
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 401,
                "message": "图书不存在"
            })
        # 如果要修改部分字段，只需要将partial=True
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_serializer.is_valid(raise_exception=True)

        book = book_serializer.save()

        return Response({
            "status": 204,
            "message": "patch succeed",
            "results": BookModelSerializerV2(book).data
        })


class BookAPIViewV2(APIView):
    def get(self, request, *args, **kwargs):
        # 查询单个
        book_id = kwargs.get("id")
        if book_id:
            book_obj = Book.objects.get(pk=book_id)
            book_serializer = BookModelSerializer(book_obj).data

            return Response({
                "status": 200,
                "message": "查询成功",
                "results": book_serializer
            })
        else:
            book_set = Book.objects.all()
            book_set_serializer = BookModelSerializer(book_set, many=True).data

            return Response({
                "status": 200,
                "message": "set succeed",
                "results": book_set_serializer
            })

    def post(self, request, *args, **kwargs):
        # 新增
        request_data = request.dara
        serializer = BookModelSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        book_obj = serializer.save()

        return Response({
            "status": 201,
            "message": "put succeed",
            "results": BookModelSerializer(book_obj).data
        })

    def delete(self, request, *args, **kwargs):
        # 删除对象（单个&多个）
        book_id = kwargs.get("id")
        if book_id:
            ids = [book_id]
        else:
            ids = request.data.get("ids")
        print(ids)
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 202,
                "message": "delete succeed"
            })

        return Response({
            "status": 400,
            "message": "删除失败或删除的图书不存在"
        })

    def put(self, request, *args, **kwargs):
        # 修改单个对象的全部字段
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 401,
                "message": "图书不存在"
            })
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()

        return Response({
            "status": 203,
            "message": "put succeed",
            "results": BookModelSerializerV2(book).data
        })

    def patch(self, request, *args, **kwargs):
        # 完成修改的单个对象的字段
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            book_obj = Book.objects.get(pk=book_id)
        except Book.DoesNotExist:
            return Response({
                "status": 401,
                "message": "图书不存在"
            })
        book_serializer = BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        book_serializer.is_valid(raise_exception=True)
        book = book_serializer.save()

        return Response({
            "status": 204,
            "message": "patch succeed",
            "results": BookModelSerializerV2(book).data
        })