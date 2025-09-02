from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Blog, BlogCategory, BlogTag, BlogComment, BlogLike, BlogView, BlogBookmark

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'blog_count', 'color_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    
    def blog_count(self, obj):
        return obj.blog_set.count()
    blog_count.short_description = 'Blogs'
    
    def color_display(self, obj):
        return format_html(
            '<span style="background-color: {}; padding: 5px 10px; border-radius: 3px; color: white;">{}</span>',
            obj.color,
            obj.color
        )
    color_display.short_description = 'Color'

@admin.register(BlogTag)
class BlogTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'blog_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def blog_count(self, obj):
        return obj.blog_set.count()
    blog_count.short_description = 'Blogs'

class BlogCommentInline(admin.TabularInline):
    model = BlogComment
    extra = 0
    fields = ['user', 'content', 'is_approved', 'created_at']
    readonly_fields = ['created_at']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'category', 'status', 'is_featured', 
        'view_count', 'like_count', 'comment_count', 'created_at'
    ]
    list_filter = [
        'status', 'is_featured', 'category', 'tags', 
        'created_at', 'allow_comments'
    ]
    search_fields = ['title', 'content', 'excerpt']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    inlines = [BlogCommentInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'user', 'excerpt', 'content', 'featured_image')
        }),
        ('Categorization', {
            'fields': ('category', 'tags', 'related_event')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Publishing', {
            'fields': ('status', 'is_featured', 'allow_comments', 'published_at')
        }),
        ('Analytics', {
            'fields': ('view_count', 'read_time'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['view_count', 'read_time']
    
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Likes'
    
    def comment_count(self, obj):
        return obj.comments.filter(is_approved=True).count()
    comment_count.short_description = 'Comments'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'category').prefetch_related('tags')

@admin.register(BlogComment)
class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'content_preview', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'blog__title', 'user__username']
    actions = ['approve_comments', 'disapprove_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content'
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} comments approved.')
    approve_comments.short_description = 'Approve selected comments'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, f'{queryset.count()} comments disapproved.')
    disapprove_comments.short_description = 'Disapprove selected comments'

@admin.register(BlogLike)
class BlogLikeAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blog__title', 'user__username']

@admin.register(BlogView)
class BlogViewAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blog__title', 'user__username', 'ip_address']
    readonly_fields = ['user_agent']

@admin.register(BlogBookmark)
class BlogBookmarkAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['blog__title', 'user__username']