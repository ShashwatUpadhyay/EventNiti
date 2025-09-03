from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from events.models import Event, EventSubmission
from blog.models import Blog, BlogCategory, BlogAnalytics
from account.models import User
from .models import DashboardMetrics, ActivityLog
import json

@staff_member_required
def dashboard_home(request):
    # Get current metrics
    today = timezone.now().date()
    
    # Basic counts
    total_events = Event.objects.count()
    total_blogs = Blog.objects.count()
    total_users = User.objects.count()
    total_registrations = EventSubmission.objects.count()
    
    # Recent activity
    recent_events = Event.objects.order_by('-upload_time')[:5]
    recent_blogs = Blog.objects.order_by('-created_at')[:5]
    recent_registrations = EventSubmission.objects.select_related('event', 'user').order_by('-id')[:10]
    
    # Analytics data for charts
    last_30_days = [today - timedelta(days=i) for i in range(30)]
    
    daily_registrations = []
    daily_events = []
    
    for day in reversed(last_30_days):
        start = timezone.make_aware(datetime.combine(day, datetime.min.time()))
        end = timezone.make_aware(datetime.combine(day, datetime.max.time()))
        reg_count = EventSubmission.objects.filter(created_at__range=(start, end)).count()  # Simplified for now
        event_count = Event.objects.filter(upload_time__date=day).count()
        daily_registrations.append(reg_count if reg_count else 0)
        daily_events.append(event_count if event_count else 0)
    
    # Top performing events
    top_events = Event.objects.annotate(
        reg_count=Count('participant')
    ).order_by('-reg_count')[:5]
    
    # Blog analytics
    blog_stats = BlogAnalytics.objects.filter(
        date__gte=today - timedelta(days=30)
    ).aggregate(
        total_views=Sum('views'),
        total_likes=Sum('likes'),
        total_shares=Sum('shares')
    )
    print(json.dumps(daily_registrations))
    context = {
        'total_events': total_events,
        'total_blogs': total_blogs,
        'total_users': total_users,
        'total_registrations': total_registrations,
        'recent_events': recent_events,
        'recent_blogs': recent_blogs,
        'recent_registrations': recent_registrations,
        'daily_registrations': json.dumps(daily_registrations),
        'daily_events': json.dumps(daily_events),
        'top_events': top_events,
        'blog_stats': blog_stats,
    }
    
    return render(request, 'dashboard/home.html', context)

@staff_member_required
def events_management(request):
    events = Event.objects.select_related('organized_by').annotate(
        reg_count=Count('participant')
    ).order_by('-upload_time')
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter:
        if status_filter == 'active':
            events = events.filter(event_open=True, event_over=False)
        elif status_filter == 'completed':
            events = events.filter(event_over=True)
        elif status_filter == 'closed':
            events = events.filter(event_open=False)
    
    search = request.GET.get('search')
    if search:
        events = events.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    paginator = Paginator(events, 20)
    page = request.GET.get('page')
    events = paginator.get_page(page)
    
    return render(request, 'dashboard/events_management.html', {
        'events': events,
        'status_filter': status_filter,
        'search': search
    })

@staff_member_required
def blogs_management(request):
    blogs = Blog.objects.select_related('user', 'category').order_by('-created_at')
    
    # Filters
    status_filter = request.GET.get('status')
    if status_filter:
        blogs = blogs.filter(status=status_filter)
    
    category_filter = request.GET.get('category')
    if category_filter:
        blogs = blogs.filter(category_id=category_filter)
    
    search = request.GET.get('search')
    if search:
        blogs = blogs.filter(
            Q(title__icontains=search) | Q(content__icontains=search)
        )
    
    paginator = Paginator(blogs, 20)
    page = request.GET.get('page')
    blogs = paginator.get_page(page)
    
    categories = BlogCategory.objects.all()
    
    return render(request, 'dashboard/blogs_management.html', {
        'blogs': blogs,
        'categories': categories,
        'status_filter': status_filter,
        'category_filter': category_filter,
        'search': search
    })

@staff_member_required
def registrations_view(request):
    registrations = EventSubmission.objects.select_related(
        'event', 'user'
    ).order_by('-id')
    
    # Filters
    event_filter = request.GET.get('event')
    if event_filter:
        registrations = registrations.filter(event_id=event_filter)
    
    status_filter = request.GET.get('status')
    if status_filter == 'approved':
        registrations = registrations.filter(allowed=True)
    elif status_filter == 'pending':
        registrations = registrations.filter(allowed=False)
    
    search = request.GET.get('search')
    if search:
        registrations = registrations.filter(
            Q(user__username__icontains=search) |
            Q(user__email__icontains=search) |
            Q(event__title__icontains=search)
        )
    
    paginator = Paginator(registrations, 25)
    page = request.GET.get('page')
    registrations = paginator.get_page(page)
    
    events = Event.objects.all()
    
    return render(request, 'dashboard/registrations.html', {
        'registrations': registrations,
        'events': events,
        'event_filter': event_filter,
        'status_filter': status_filter,
        'search': search
    })

@staff_member_required
def analytics_view(request):
    # Date range
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    # Event analytics
    event_analytics = Event.objects.filter(
        upload_time__date__range=[start_date, end_date]
    ).values('upload_time__date').annotate(
        count=Count('id')
    ).order_by('upload_time__date')
    
    # Registration analytics - simplified since EventSubmission doesn't have created_at
    reg_analytics = []
    for i in range(30):
        reg_analytics.append({'date': start_date + timedelta(days=i), 'count': 0})
    
    # Blog analytics
    blog_analytics = BlogAnalytics.objects.filter(
        date__range=[start_date, end_date]
    ).values('date').annotate(
        total_views=Sum('views'),
        total_likes=Sum('likes')
    ).order_by('date')
    
    # Popular events
    popular_events = Event.objects.annotate(
        reg_count=Count('participant')
    ).order_by('-reg_count')[:10]
    
    # User growth
    user_growth = User.objects.filter(
        date_joined__date__range=[start_date, end_date]
    ).values('date_joined__date').annotate(
        count=Count('id')
    ).order_by('date_joined__date')
    
    context = {
        'event_analytics': list(event_analytics),
        'reg_analytics': list(reg_analytics),
        'blog_analytics': list(blog_analytics),
        'popular_events': popular_events,
        'user_growth': list(user_growth),
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'dashboard/analytics.html', context)

@staff_member_required
def users_management(request):
    users = User.objects.annotate(
        event_count=Count('host'),
        blog_count=Count('blogs'),
        reg_count=Count('eventsubmission')
    ).order_by('-date_joined')
    
    search = request.GET.get('search')
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    role_filter = request.GET.get('role')
    if role_filter == 'staff':
        users = users.filter(is_staff=True)
    elif role_filter == 'active':
        users = users.filter(is_active=True)
    
    paginator = Paginator(users, 25)
    page = request.GET.get('page')
    users = paginator.get_page(page)
    
    return render(request, 'dashboard/users_management.html', {
        'users': users,
        'search': search,
        'role_filter': role_filter
    })

@staff_member_required
def quick_stats_api(request):
    today = timezone.now().date()
    
    stats = {
        'today_registrations': EventSubmission.objects.count(),  # Simplified
        'today_events': Event.objects.filter(upload_time__date=today).count(),
        'today_blogs': Blog.objects.filter(created_at__date=today).count(),
        'active_events': Event.objects.filter(event_open=True).count(),
        'pending_registrations': EventSubmission.objects.filter(allowed=False).count(),
    }
    
    return JsonResponse(stats)