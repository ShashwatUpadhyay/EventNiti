from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from .models import (Blog, BlogCategory, BlogTag, BlogComment, BlogLike, BlogView, BlogBookmark,
                    CommentReaction, BlogShare, NewsletterSubscription, WritingChallenge,
                    ChallengeSubmission, PushNotificationSubscription)
from .forms import BlogCommentForm
from .utils import track_blog_analytics, send_push_notification, generate_social_meta_tags
import json

def blog_list(request):
    blogs = Blog.objects.filter(status='published').select_related('user', 'category').prefetch_related('tags')
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(excerpt__icontains=search_query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        blogs = blogs.filter(category__slug=category_slug)
    
    # Tag filter
    tag_slug = request.GET.get('tag')
    if tag_slug:
        blogs = blogs.filter(tags__slug=tag_slug)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    if sort_by == 'popular':
        blogs = blogs.annotate(total_likes=Count('likes')).order_by('-total_likes', '-created_at')
    elif sort_by == 'views':
        blogs = blogs.order_by('-view_count', '-created_at')
    else:
        blogs = blogs.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for filters
    categories = BlogCategory.objects.annotate(blog_count=Count('blog')).filter(blog_count__gt=0)
    popular_tags = BlogTag.objects.annotate(blog_count=Count('blog')).filter(blog_count__gt=0)[:10]
    featured_blogs = Blog.objects.filter(status='published', is_featured=True)[:3]
    
    context = {
        'blogs': page_obj,
        'categories': categories,
        'popular_tags': popular_tags,
        'featured_blogs': featured_blogs,
        'search_query': search_query,
        'current_category': category_slug,
        'current_tag': tag_slug,
        'current_sort': sort_by,
    }
    
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    
    # Track view
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    view, created = BlogView.objects.get_or_create(
        blog=blog,
        ip_address=ip_address,
        defaults={'user': request.user if request.user.is_authenticated else None, 'user_agent': user_agent}
    )
    
    if created:
        blog.view_count += 1
        blog.save(update_fields=['view_count'])
    
    # Get comments with reactions
    comments = blog.comments.filter(is_approved=True, parent=None).select_related('user').prefetch_related('replies__user')
    
    # Check if user liked/bookmarked
    user_liked = False
    user_bookmarked = False
    user_comment_reactions = {}
    
    if request.user.is_authenticated:
        user_liked = blog.likes.filter(user=request.user).exists()
        user_bookmarked = blog.bookmarks.filter(user=request.user).exists()
        
        # Get user's comment reactions
        reactions = CommentReaction.objects.filter(
            comment__blog=blog, user=request.user
        ).values('comment_id', 'reaction')
        user_comment_reactions = {r['comment_id']: r['reaction'] for r in reactions}
    
    # Related blogs
    related_blogs = Blog.objects.filter(
        status='published'
    ).exclude(id=blog.id)
    
    if blog.category:
        related_blogs = related_blogs.filter(category=blog.category)
    elif blog.tags.exists():
        related_blogs = related_blogs.filter(tags__in=blog.tags.all()).distinct()
    
    related_blogs = related_blogs[:4]
    
    # Comment form
    comment_form = BlogCommentForm()
    
    # Generate social media meta tags
    social_meta = generate_social_meta_tags(blog)
    
    context = {
        'blog': blog,
        'comments': comments,
        'comment_form': comment_form,
        'user_liked': user_liked,
        'user_bookmarked': user_bookmarked,
        'user_comment_reactions': user_comment_reactions,
        'related_blogs': related_blogs,
        'social_meta': social_meta,
    }
    
    return render(request, 'blog/blog_detail.html', context)

@login_required
def add_comment(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug, status='published')
        form = BlogCommentForm(request.POST)
        
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = blog
            comment.user = request.user
            
            # Handle reply
            parent_id = request.POST.get('parent_id')
            if parent_id:
                comment.parent = get_object_or_404(BlogComment, id=parent_id)
            
            comment.save()
            track_blog_analytics(blog, request, 'comment')
            
            # Send notification to blog author
            if blog.user != request.user:
                send_push_notification(
                    blog.user,
                    'New Comment',
                    f'{request.user.username} commented on your blog: {blog.title}',
                    blog
                )
            
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'Error adding comment.')
    
    return redirect('blog_detail', slug=slug)

@require_POST
@login_required
def toggle_like(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    like, created = BlogLike.objects.get_or_create(blog=blog, user=request.user)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
        track_blog_analytics(blog, request, 'like')
        
        # Send notification to blog author
        if blog.user != request.user:
            send_push_notification(
                blog.user,
                'Blog Liked',
                f'{request.user.username} liked your blog: {blog.title}',
                blog
            )
    
    return JsonResponse({
        'liked': liked,
        'like_count': blog.like_count
    })

@login_required
def toggle_bookmark(request, slug):
    if request.method == 'POST':
        blog = get_object_or_404(Blog, slug=slug, status='published')
        bookmark, created = BlogBookmark.objects.get_or_create(blog=blog, user=request.user)
        
        if not created:
            bookmark.delete()
            bookmarked = False
        else:
            bookmarked = True
        
        return JsonResponse({
            'bookmarked': bookmarked,
            'message': 'Bookmarked!' if bookmarked else 'Bookmark removed!'
        })
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

def category_blogs(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    blogs = Blog.objects.filter(status='published', category=category).order_by('-created_at')
    
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,
        'category': category,
        'page_title': f'Blogs in {category.name}'
    }
    
    return render(request, 'blog/category_blogs.html', context)

def tag_blogs(request, slug):
    tag = get_object_or_404(BlogTag, slug=slug)
    blogs = Blog.objects.filter(status='published', tags=tag).order_by('-created_at')
    
    paginator = Paginator(blogs, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'blogs': page_obj,
        'tag': tag,
        'page_title': f'Blogs tagged with {tag.name}'
    }
    
    return render(request, 'blog/tag_blogs.html', context)

@login_required
def my_bookmarks(request):
    bookmarks = BlogBookmark.objects.filter(user=request.user).select_related('blog').order_by('-created_at')
    
    paginator = Paginator(bookmarks, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bookmarks': page_obj,
        'page_title': 'My Bookmarks'
    }
    
    return render(request, 'blog/my_bookmarks.html', context)

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@require_POST
@login_required
def comment_reaction(request, comment_id):
    comment = get_object_or_404(BlogComment, id=comment_id)
    reaction_type = request.POST.get('reaction')
    
    if reaction_type not in ['like', 'dislike']:
        return JsonResponse({'error': 'Invalid reaction'}, status=400)
    
    reaction, created = CommentReaction.objects.get_or_create(
        comment=comment, user=request.user,
        defaults={'reaction': reaction_type}
    )
    
    if not created:
        if reaction.reaction == reaction_type:
            reaction.delete()
            reacted = False
        else:
            reaction.reaction = reaction_type
            reaction.save()
            reacted = True
    else:
        reacted = True
    
    likes = comment.reactions.filter(reaction='like').count()
    dislikes = comment.reactions.filter(reaction='dislike').count()
    
    return JsonResponse({
        'reacted': reacted,
        'reaction_type': reaction_type,
        'likes': likes,
        'dislikes': dislikes
    })

@require_POST
def track_share(request, slug):
    blog = get_object_or_404(Blog, slug=slug, status='published')
    platform = request.POST.get('platform')
    
    if platform in ['facebook', 'twitter', 'linkedin', 'whatsapp', 'email', 'copy_link']:
        BlogShare.objects.create(
            blog=blog,
            user=request.user if request.user.is_authenticated else None,
            platform=platform,
            ip_address=get_client_ip(request)
        )
        
        blog.share_count += 1
        blog.save(update_fields=['share_count'])
        track_blog_analytics(blog, request, 'share')
    
    return JsonResponse({'success': True, 'share_count': blog.share_count})

@login_required
def newsletter_subscribe(request):
    if request.method == 'POST':
        frequency = request.POST.get('frequency', 'weekly')
        category_ids = request.POST.getlist('categories')
        
        subscription, created = NewsletterSubscription.objects.get_or_create(
            user=request.user,
            defaults={'frequency': frequency}
        )
        
        if not created:
            subscription.is_subscribed = True
            subscription.frequency = frequency
            subscription.save()
        
        if category_ids:
            categories = BlogCategory.objects.filter(id__in=category_ids)
            subscription.categories.set(categories)
        
        messages.success(request, 'Successfully subscribed to newsletter!')
        return redirect('blog_list')
    
    categories = BlogCategory.objects.all()
    return render(request, 'blog/newsletter_subscribe.html', {'categories': categories})

@csrf_exempt
@require_POST
def auto_save_draft(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    blog_id = request.POST.get('blog_id')
    content_data = {
        'title': request.POST.get('title', ''),
        'content': request.POST.get('content', ''),
        'excerpt': request.POST.get('excerpt', ''),
    }
    
    try:
        blog = Blog.objects.get(id=blog_id, user=request.user)
        blog.auto_save_data = content_data
        blog.last_auto_save = timezone.now()
        blog.save(update_fields=['auto_save_data', 'last_auto_save'])
        
        return JsonResponse({
            'success': True,
            'last_saved': blog.last_auto_save.strftime('%H:%M:%S')
        })
    except Blog.DoesNotExist:
        return JsonResponse({'error': 'Blog not found'}, status=404)

@login_required
def soft_delete_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, user=request.user)
    blog.status = 'deleted'
    blog.is_deleted = True
    blog.deleted_at = timezone.now()
    blog.save()
    
    messages.success(request, 'Blog post moved to trash.')
    return redirect('my_blogs')

@login_required
def restore_blog(request, slug):
    blog = get_object_or_404(Blog, slug=slug, user=request.user, is_deleted=True)
    blog.status = 'draft'
    blog.is_deleted = False
    blog.deleted_at = None
    blog.save()
    
    messages.success(request, 'Blog post restored successfully.')
    return redirect('my_blogs')

@login_required
def my_blogs(request):
    status_filter = request.GET.get('status', 'all')
    
    blogs = Blog.objects.filter(user=request.user)
    
    if status_filter == 'published':
        blogs = blogs.filter(status='published')
    elif status_filter == 'draft':
        blogs = blogs.filter(status='draft')
    elif status_filter == 'deleted':
        blogs = blogs.filter(is_deleted=True)
    elif status_filter == 'active':
        blogs = blogs.filter(is_deleted=False)
    
    blogs = blogs.order_by('-created_at')
    
    paginator = Paginator(blogs, 10)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    
    return render(request, 'blog/my_blogs.html', {
        'blogs': blogs,
        'status_filter': status_filter
    })

class ChallengeListView(ListView):
    model = WritingChallenge
    template_name = 'blog/challenge_list.html'
    context_object_name = 'challenges'
    paginate_by = 12
    
    def get_queryset(self):
        return WritingChallenge.objects.filter(
            status__in=['upcoming', 'active', 'judging']
        ).order_by('-created_at')

class ChallengeDetailView(DetailView):
    model = WritingChallenge
    template_name = 'blog/challenge_detail.html'
    context_object_name = 'challenge'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        challenge = self.object
        
        if self.request.user.is_authenticated:
            context['user_submission'] = ChallengeSubmission.objects.filter(
                challenge=challenge, participant=self.request.user
            ).first()
        
        context['submissions'] = challenge.submissions.filter(
            status__in=['submitted', 'winner', 'runner_up']
        ).select_related('blog', 'participant').order_by('-judge_score', '-public_votes')
        
        return context

@login_required
def submit_to_challenge(request, slug):
    challenge = get_object_or_404(WritingChallenge, slug=slug)
    
    if not challenge.is_active:
        messages.error(request, 'This challenge is not currently active.')
        return redirect('challenge_detail', slug=slug)
    
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id, user=request.user, status='published')
        
        ChallengeSubmission.objects.create(
            challenge=challenge,
            blog=blog,
            participant=request.user
        )
        
        messages.success(request, 'Successfully submitted to the challenge!')
        return redirect('challenge_detail', slug=slug)
    
    user_blogs = Blog.objects.filter(
        user=request.user,
        status='published',
        created_at__gte=challenge.start_date
    )
    
    return render(request, 'blog/submit_to_challenge.html', {
        'challenge': challenge,
        'user_blogs': user_blogs
    })

@csrf_exempt
@require_POST
def subscribe_push_notifications(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    data = json.loads(request.body)
    endpoint = data.get('endpoint')
    keys = data.get('keys', {})
    
    PushNotificationSubscription.objects.update_or_create(
        user=request.user,
        endpoint=endpoint,
        defaults={
            'p256dh_key': keys.get('p256dh', ''),
            'auth_key': keys.get('auth', ''),
            'is_active': True
        }
    )
    
    return JsonResponse({'success': True})

# Legacy views for backward compatibility
def blogs(request):
    return blog_list(request)

def blogpage(request, slug):
    return blog_detail(request, slug)