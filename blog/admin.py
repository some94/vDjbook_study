from django.contrib import admin
from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display  = ('id', 'title', 'modify_dt', 'tag_list')
    list_filter   = ('modify_dt',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):  # Post 테이블과 Tag 테이블이 다대다 관계이므로, Tag 테이블 관련 레코들을 한 번의 쿼리로 미리 가져오기 위함
        return super().get_queryset(request).prefetch_related('tags')  # 다대다 관계에서 쿼리 횟수를 줄여 성능을 높이고자 할 때 prefetch_related() 메서드 사용

    def tag_list(self, obj):
        return ', '.join(o.name for o in obj.tags.all())
