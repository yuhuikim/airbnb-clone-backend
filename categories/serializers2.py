from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.Serializer):
    # serializer에게 read_only = True를 써줌으로써 user가 어떤 건 보내고 보내지 않는지를 알려준다.
    """
    {'pk': [ErrorDetail(string='이 필드는 필수 항목입니다.', code='required')], 'created_at': [ErrorDetail(string='이 필드는 필수 항목입니다.', code='required')]}
    {'name': 'Category from DRF', 'kind': 'rooms'}
    """
    pk = serializers.IntegerField(
        read_only=True,
    )
    name = serializers.CharField(
        required=True,
        max_length=50,
    )
    kind = serializers.ChoiceField(
        choices=Category.CategoryKindChoieces.choices,
    )
    created_at = serializers.DateTimeField(
        read_only=True,
    )


# serializer은 django python 객체를 json으로 변환해주는 것
# ++ user에게서 온 data를 받아서 우리의 데이터 베이스에 넣을 수 있는 django 객체로 변환해준다. 양방향인 것!!!!!!!!

# 우리가 serializer에게 데이터의 형태를 미리 설명해주면 유효한 값인지 아닌지 다시한번 검사할 필요가 없을 것이다.
# 제약조건을 적어주면 알아서 user가 보낸 값을 검증할 수 있다.


    def create(self, validated_data):
        # # 여러개를 가져오게 된다면 비효율적이다.
        # Category.objects.create(
        #     name=validated_data['name'],
        #     kind=validated_data['kind'],
        # )

        # **를 사용 : 딕셔너리를 가져오는 기호
        # """
        #  {'name': 'Category from DRF', 'kind': 'rooms'}를 가져와서

        #  name = 'Category'
        #  kind = 'rooms'로 바꿔준다.
        # """
        return Category.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        # default 값을 선언해줌으로서, 기존에 있는 값은 유지시키고, 새로운 값이 있으면 새로운 값으로 바꾸는 update 코드 완성
        instance.name = validated_data.get('name',instance.name)
        instance.kind = validated_data.get('kind',instance.kind)
        instance.save()
        return instance
