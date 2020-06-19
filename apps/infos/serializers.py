from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from . import models


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = models.Author
        fields = ('author_name', 'author_uid', 'author_sec_uid', 'author_short_id', 'author_gender',
                  'author_sign', 'author_fans_num', 'author_favorited', 'author_aweme_count', 'author_unique_id')

        extra_kwargs = {
            # write_only：只反序列化
            # read_only：只序列化
            'author_sign': {
                'read_only': True
            },
            'author_sec_uid': {
                'write_only': True
            },
            'author_uid': {
                'write_only': True
            },
            'author_short_id': {
                'write_only': True
            },

        }

    def validate(self, attrs):
        """
        检验作者是否存在
        :param attrs:  post 请求对象
        :return:
        """
        author_uid = attrs.get('author_uid')
        if models.Author.objects.filter(author_uid=author_uid):
            raise ValidationError({'message': '作者已经存在'})
        return attrs


class FansSerializer(ModelSerializer):
    class Meta:
        model = models.Fans
        fields = ('fan_name', 'fan_uid', 'fan_sec_uid', 'fan_gender', 'department')

        extra_kwargs = {
            # write_only：只反序列化
            # read_only：只序列化
            'fan_gender': {
                'read_only': True
            },
            'department': {
                'write_only': True
            },

        }
