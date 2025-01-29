from rest_framework import serializers
from blog.models import Post , Image , Category
class PostModelSerializer(serializers.ModelSerializer):
    images   = serializers.PrimaryKeyRelatedField(queryset=Image.objects.all() , many=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    author   = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['slug']
    def create(self , validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)

class ImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'

class CategoryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'