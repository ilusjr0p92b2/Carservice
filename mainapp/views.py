from django.http import HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404, render
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from .forms import CommentForm, EditArticleForm
from .models import Article, Comment


class ArticleListView(ListView):
    model = Article
    template_name = 'mainapp/index.html'
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self):
        return super().get_queryset()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class EditArticleView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        form = EditArticleForm(instance=article)
        return render(request, 'mainapp/edit_article.html', {'article': article, 'form': form})

    def post(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.title = request.POST['title']
        article.content = request.POST['content']
        article.save()
        return redirect(article.get_absolute_url())


class DeleteArticleView(View):
    def get(self, request, pk):
        article = get_object_or_404(Article, id=pk)
        article.delete()
        return redirect('home')


class AboutView(ListView):
    model = Article
    template_name = 'mainapp/about.html'
    context_object_name = 'articles'
    paginate_by = 5


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'mainapp/article.html'
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['comments'] = Comment.objects.filter(article=self.get_object()).order_by('-created_at')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = self.object
            comment.author = request.user
            comment.save()
            return redirect('article', pk=self.object.pk)
        return self.render_to_response(self.get_context_data(comment_form=form))


class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])
        if request.user == comment.author or request.user.is_superuser:
            comment.delete()
            return redirect('article', pk=comment.article.pk)
        return HttpResponseForbidden()


class NotFoundView(TemplateView):
    template_name = '404_template.html'
