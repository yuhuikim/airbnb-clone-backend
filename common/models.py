from django.db import models

# Create your models here.
# DB에 CommonModel이라고 사용하지 않음
class CommonModel(models.Model):

  """Common Model Definition"""
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    # Django가 이 model을 봐도 이걸 DB에 저장하지 않는다. 이 코드를 우리의 다른 어플리케이션에서 사용할 수 있다. 
    abstract = True
    
