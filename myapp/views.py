from django.shortcuts import render
import json
from django.http import JsonResponse, HttpResponse
from django.views import View
from .models import Book
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Disable CSRF for the API (for simplicity)
@method_decorator(csrf_exempt, name='dispatch')

# Create your views here. In Django, you handle HTTP requests and responses via views.
class BookListCreateView(View):
    def get(self, request):
        """Handle get request to handle all books"""
        books = Book.objects.all().values('id', 'title', 'author','published_date')
        return JsonResponse(list(books), safe=False)
    
    def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        book = Book.objects.create(
            title = data['title'],
            author = data['author'],
            published_date = data['published_date']
        )
        return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date}, status=201)
    
@method_decorator(csrf_exempt, name='dispatch')

class BookDetailView(View):
        def get(self, request, pk):
            """Handle GET requests to retrieve a single book by ID."""
            try:
                book = Book.objects.get(pk=pk)
                return JsonResponse({
                    'id': book.id,
                    'title': book.title,
                    'author': book.author,
                    'published_date': book.published_date
                })
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=404)
        
        def put(self, request, pk):
            """Handle PUT requests to update a book."""
            try:
                book = Book.objects.get(pk=pk)
                data = json.loads(request.body.decode('utf-8'))
                book.title = data['title']
                book.author = data['author']
                book.published_date = data['published_date']
                book.save()
                return JsonResponse({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date})
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=404)
            
        def delete(self, request, pk):
            """Handle DELETE requests to delete a book."""
            try:
                book = Book.objects.get(pk=pk)
                book.delete()
                return JsonResponse({'message': 'Book deleted successfully'}, status=204)
            except Book.DoesNotExist:
                return JsonResponse({'error': 'Book not found'}, status=404)
        


