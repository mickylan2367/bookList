from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .models import Book, Review
from django.urls import reverse_lazy, reverse
from django.db.models import Avg
from django.core.paginator import Paginator
from .consts import ITEM_PER_PAGE
# from django.contrib.auth import logout

# Create your views here.
class ListBookView(LoginRequiredMixin, ListView):
    template_name = 'book/book_list.html'
    model = Book
    paginate_by = ITEM_PER_PAGE


class DetailBookView(LoginRequiredMixin, DetailView):
    template_name = 'book/book_detail.html'
    model = Book

class CreateBookView(LoginRequiredMixin, CreateView):
    template_name = 'book/book_create.html'
    model = Book
    fields = ("title", "text", "category", "thumbnail")
    success_url = reverse_lazy('list-book')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = 'book/book_confirm_delete.html'
    model = Book
    success_url = reverse_lazy('list-book')

class UpdateBookView(LoginRequiredMixin, UpdateView):
    template_name = 'book/book_update.html'
    fields = ('title', 'text', 'category', 'thumbnail')
    model = Book
    success_url = reverse_lazy('list-book')

    def get_object(self, queryset = None):
        # データベースのデータを取得
        obj = super().get_object(queryset)
        # データを作ったUserが現在のログインユーザーとは異なる場合、編集できないエラーを出す
        # Permission ForbiddenはDjangoがデフォルトで用意したエラー。
        if obj.user != self.request.user:
            raise PermissionDenied
        return obj

    # データを更新した後に飛ぶページを作成
    def get_success_url(self):
        return reverse('detail-book', kwargs = {'pk':self.object.id})



def index_view(request):
    # print('index_view is called')
    object_list = Book.objects.order_by("-id")

    # オブジェクト順に並べ替える
    ranking_list = Book.objects.annotate(avg_rating=Avg('review__rate')).order_by('-avg_rating')
    
    
    # ページネーションの実装
    pagenator = Paginator(ranking_list, ITEM_PER_PAGE)
    page_number = request.GET.get('page', 1)
    page_obj = pagenator.page(page_number)
    
    return render(
        request, 
        'book/index.html', 
        {'object_list':object_list, 'ranking_list':ranking_list, 'page_obj':page_obj}
    )



# def logout_view(request):
#     logout(request)
#     return redirect('index')


class CreateReviewView(LoginRequiredMixin, CreateView):
    model = Review
    fields=('book', 'title', 'text', 'rate')
    template_name = 'book/review_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = Book.objects.get(pk=self.kwargs['book_id'])
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail-book', kwargs={'pk':self.object.book.id})


