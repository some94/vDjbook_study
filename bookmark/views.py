from django.views.generic import ListView, DetailView
from bookmark.models import Bookmark

from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from vDjbook.views import OwnerOnlyMixin

class BookmarkLV(ListView):
    model = Bookmark

class BookmarkDV(DetailView):
    model = Bookmark

class BookmarkCreateView(LoginRequiredMixin, CreateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

    # 입력된 폼에 대해 유효성 검사 후 모델 객체를 생성하여 폼의 내용을 overwrite 함
    def form_valid(self, form):
        # 폼에 연결된 모델 객체의 owner 필드에 현재 로그인된 사용자의 User 객체 할당
        form.instance.owner = self.request.user
        return super().form_valid(form)

class BookmarkChangeLV(LoginRequiredMixin, ListView):
    template_name = 'bookmark/bookmark_change_list.html'

    # 화면에 출력할 레코드 리스트 반환. Bookmark 테이블의 레코드 중 owner 필드가 로그인한 사용자인 레코드 리스트 반환.
    def get_queryset(self):
        return Bookmark.objects.filter(owner=self.request.user)

class BookmarkUpdateView(OwnerOnlyMixin, UpdateView):
    model = Bookmark
    fields = ['title', 'url']
    success_url = reverse_lazy('bookmark:index')

class BookmarkDeleteView(OwnerOnlyMixin, DeleteView):
    model = Bookmark
    success_url = reverse_lazy('bookmark:index')