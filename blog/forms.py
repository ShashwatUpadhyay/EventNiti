from django import forms
from .models import BlogComment, Blog, BlogCategory, BlogTag

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': 'Write your comment...'
            })
        }

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'title', 'excerpt', 'content', 'featured_image', 
            'category', 'tags', 'related_event', 'meta_description', 
            'meta_keywords', 'status', 'is_featured', 'allow_comments'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'Enter blog title'
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 3,
                'placeholder': 'Brief description of your blog'
            }),
            'meta_description': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'SEO meta description (160 characters max)'
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'SEO keywords (comma separated)'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'tags': forms.CheckboxSelectMultiple(),
            'related_event': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            }),
            'featured_image': forms.FileInput(attrs={
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
            })
        }

class BlogSearchForm(forms.Form):
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Search blogs...'
        })
    )
    category = forms.ModelChoiceField(
        queryset=BlogCategory.objects.all(),
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )
    sort_by = forms.ChoiceField(
        choices=[
            ('-created_at', 'Latest'),
            ('created_at', 'Oldest'),
            ('popular', 'Most Popular'),
            ('views', 'Most Viewed'),
            ('title', 'A-Z'),
            ('-title', 'Z-A'),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500'
        })
    )