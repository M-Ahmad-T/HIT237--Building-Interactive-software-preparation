from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Book, Loan
from .forms import BookForm


class BookListView(ListView):
    model = Book
    template_name = 'catalogue/book_list.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.available().select_related('author')


class BookDetailView(DetailView):
    model = Book
    template_name = 'catalogue/book_detail.html'
    context_object_name = 'book'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['loan_history'] = Loan.objects.filter(
            book=self.object
        ).select_related('member__user').order_by('-date_borrowed')
        return context


class BookCreateView(CreateView):
    model = Book
    form_class = BookForm
    template_name = 'catalogue/book_form.html'
    success_url = reverse_lazy('catalogue:book_list')

    def form_valid(self, form):
        form.instance.is_available = True
        return super().form_valid(form)


class BookUpdateView(UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'catalogue/book_form.html'
    success_url = reverse_lazy('catalogue:book_list')

    def get_queryset(self):
        return Book.objects.filter(is_available=True)


class BookDeleteView(DeleteView):
    model = Book
    template_name = 'catalogue/book_confirm_delete.html'
    success_url = reverse_lazy('catalogue:book_list')

    def get_queryset(self):
        return Book.objects.available()
