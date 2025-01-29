from rest_framework import serializers
from blog.models import Post , Image , Category , Comment , CommentReply
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

class CommentModelSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post   = serializers.SlugRelatedField(slug_field='slug' , queryset=Post.objects.all())
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self , validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)
class CommentReplyModelSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comment = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all())
    class Meta:
        model = CommentReply
        fields = '__all__'
    def create(self , validated_data):
        validated_data['author'] = self.context['request'].user.profile
        return super().create(validated_data)