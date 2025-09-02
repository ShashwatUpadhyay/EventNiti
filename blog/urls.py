from django.urls import path
from . import views

urlpatterns = [
    # Blog listing and detail
    path('', views.blog_list, name='blog_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    
    # Category and tag views
    path('category/<slug:slug>/', views.category_blogs, name='category_blogs'),
    path('tag/<slug:slug>/', views.tag_blogs, name='tag_blogs'),
    
    # User interactions
    path('like/<slug:slug>/', views.toggle_like, name='toggle_like'),
    path('bookmark/<slug:slug>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('comment/<slug:slug>/', views.add_comment, name='add_comment'),
    path('comment-reaction/<int:comment_id>/', views.comment_reaction, name='comment_reaction'),
    path('share/<slug:slug>/', views.track_share, name='track_share'),
    
    # User dashboard
    path('my/bookmarks/', views.my_bookmarks, name='my_bookmarks'),
    path('my/blogs/', views.my_blogs, name='my_blogs'),
    
    # Content management
    path('delete/<slug:slug>/', views.soft_delete_blog, name='soft_delete_blog'),
    path('restore/<slug:slug>/', views.restore_blog, name='restore_blog'),
    path('auto-save/', views.auto_save_draft, name='auto_save_draft'),
    
    # Newsletter
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # Writing challenges
    path('challenges/', views.ChallengeListView.as_view(), name='challenge_list'),
    path('challenges/<slug:slug>/', views.ChallengeDetailView.as_view(), name='challenge_detail'),
    path('challenges/<slug:slug>/submit/', views.submit_to_challenge, name='submit_to_challenge'),
    
    # Push notifications
    path('push/subscribe/', views.subscribe_push_notifications, name='subscribe_push_notifications'),
    
    # Legacy URLs
    path('blogs/', views.blogs, name='blogs'),
    path('blogpage/<slug:slug>/', views.blogpage, name='blogpage'),
]