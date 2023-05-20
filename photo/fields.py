import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile


class ThumbnailImageFieldFile(ImageFieldFile):
    def _add_thumb(self, s):  # 이미지 파일명을 기준으로 썸네일 이미지 파일명 만들기.
        parts = s.split('.')
        parts.insert(-1, 'thumb')  # abc.jpg -> abc.thumb.jpg
        if parts[-1].lower() not in ['jpeg', 'jpg']:  # 확장자가 jpeg, jpg가 아닐 경우 jpg로 변경
            parts[-1] = 'jpg'
        return '.'.join(parts)

    @property  # 메서드를 멤버 변수처럼 사용하기 위함
    def thumb_path(self):  # 원본 파일 경로인 path 속성에 추가해, 썸네일 경로인 thumb_path 속성 추가
        return self._add_thumb(self.path)

    @property
    def thumb_url(self):  # 원본 파일의 URL인 url 속성에 추가해, 썸네일의 URL인 thumb_url 속성을 만듦
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):  # 파일 시스템에 파일을 저장하고 생성하는 메서드
        super().save(name, content, save)  # 부모 ImageFieldFile 클래스의 save() 메서드를 호출해 원본 이미지 저장

        img = Image.open(self.path)
        size = (self.field.thumb_width, self.field.thumb_height)  # 원본 파일로부터 디폴트 128*128px 크기의 썸네일 이미지 생성
        img.thumbnail(size)  # PIL 라이브러리의 Image.thumbnail() 함수로 썸네일 이미지를 만듦. 썸네일을 만들 때 가로*세로 비율 유지
        background = Image.new('RGB', size, (255, 255, 255))
        box = (int((size[0]-img.size[0])/2), int((size[1]-img.size[1])/2))  # 썸네일과 배경 이미지를 합쳐서 정사각형 모양의 썸네일 이미지를 만듦. 배경은 흰색
        background.paste(img, box)
        background.save(self.thumb_path, 'JPEG')

    def delete(self, save=True):  # delete 메서드 호출 시 원본 이미지와 썸네일 이미지 함께 삭제
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)


class ThumbnailImageField(ImageField):
    attr_class = ThumbnailImageFieldFile

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)

