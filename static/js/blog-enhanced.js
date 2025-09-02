// Enhanced Blog Features JavaScript

// Auto-save functionality
let autoSaveTimer;
const AUTOSAVE_INTERVAL = 30000; // 30 seconds

function initAutoSave(blogId) {
    if (!blogId) return;
    
    const form = document.querySelector('#blog-form');
    if (!form) return;
    
    const inputs = form.querySelectorAll('input, textarea, select');
    
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => autoSaveDraft(blogId), AUTOSAVE_INTERVAL);
        });
    });
}

function autoSaveDraft(blogId) {
    const form = document.querySelector('#blog-form');
    if (!form) return;
    
    const formData = new FormData(form);
    formData.append('blog_id', blogId);
    
    fetch('/blog/auto-save/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showAutoSaveStatus(`Auto-saved at ${data.last_saved}`);
        }
    })
    .catch(error => console.error('Auto-save failed:', error));
}

function showAutoSaveStatus(message) {
    let statusEl = document.querySelector('#autosave-status');
    if (!statusEl) {
        statusEl = document.createElement('div');
        statusEl.id = 'autosave-status';
        statusEl.className = 'text-sm text-gray-500 mt-2';
        document.querySelector('#blog-form').appendChild(statusEl);
    }
    statusEl.textContent = message;
}

// Comment reactions
function toggleCommentReaction(commentId, reactionType) {
    fetch(`/blog/comment-reaction/${commentId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `reaction=${reactionType}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
            return;
        }
        
        // Update reaction counts
        const likesEl = document.querySelector(`#comment-${commentId}-likes`);
        const dislikesEl = document.querySelector(`#comment-${commentId}-dislikes`);
        const likeBtn = document.querySelector(`#comment-${commentId}-like-btn`);
        const dislikeBtn = document.querySelector(`#comment-${commentId}-dislike-btn`);
        
        if (likesEl) likesEl.textContent = data.likes;
        if (dislikesEl) dislikesEl.textContent = data.dislikes;
        
        // Update button states
        if (likeBtn) {
            likeBtn.classList.toggle('active', data.reacted && data.reaction_type === 'like');
        }
        if (dislikeBtn) {
            dislikeBtn.classList.toggle('active', data.reacted && data.reaction_type === 'dislike');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Share tracking
function trackShare(slug, platform) {
    fetch(`/blog/share/${slug}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `platform=${platform}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const shareCountEl = document.querySelector('#share-count');
            if (shareCountEl) {
                shareCountEl.textContent = data.share_count;
            }
        }
    })
    .catch(error => console.error('Error:', error));
}

// Social sharing functions
function shareOnFacebook(url, title) {
    const shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
    window.open(shareUrl, 'facebook-share', 'width=580,height=296');
    trackShare(getSlugFromUrl(), 'facebook');
}

function shareOnTwitter(url, title) {
    const shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
    window.open(shareUrl, 'twitter-share', 'width=580,height=296');
    trackShare(getSlugFromUrl(), 'twitter');
}

function shareOnLinkedIn(url, title) {
    const shareUrl = `https://www.linkedin.com/sharing/share-offsite/?url=${encodeURIComponent(url)}`;
    window.open(shareUrl, 'linkedin-share', 'width=580,height=296');
    trackShare(getSlugFromUrl(), 'linkedin');
}

function shareOnWhatsApp(url, title) {
    const shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
    window.open(shareUrl, 'whatsapp-share');
    trackShare(getSlugFromUrl(), 'whatsapp');
}

function copyToClipboard(url) {
    navigator.clipboard.writeText(url).then(() => {
        alert('Link copied to clipboard!');
        trackShare(getSlugFromUrl(), 'copy_link');
    }).catch(err => {
        console.error('Failed to copy: ', err);
    });
}

// Push notifications
function initPushNotifications() {
    if ('serviceWorker' in navigator && 'PushManager' in window) {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('Service Worker registered');
                return registration.pushManager.getSubscription();
            })
            .then(subscription => {
                if (!subscription) {
                    return subscribeToPush();
                }
            })
            .catch(error => console.error('Service Worker registration failed:', error));
    }
}

function subscribeToPush() {
    return navigator.serviceWorker.ready
        .then(registration => {
            const vapidPublicKey = 'YOUR_VAPID_PUBLIC_KEY'; // Replace with actual key
            return registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
            });
        })
        .then(subscription => {
            return fetch('/blog/push/subscribe/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    endpoint: subscription.endpoint,
                    keys: {
                        p256dh: arrayBufferToBase64(subscription.getKey('p256dh')),
                        auth: arrayBufferToBase64(subscription.getKey('auth'))
                    }
                })
            });
        })
        .catch(error => console.error('Push subscription failed:', error));
}

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getSlugFromUrl() {
    const path = window.location.pathname;
    const segments = path.split('/').filter(segment => segment);
    return segments[segments.length - 1];
}

function urlBase64ToUint8Array(base64String) {
    const padding = '='.repeat((4 - base64String.length % 4) % 4);
    const base64 = (base64String + padding)
        .replace(/-/g, '+')
        .replace(/_/g, '/');
    
    const rawData = window.atob(base64);
    const outputArray = new Uint8Array(rawData.length);
    
    for (let i = 0; i < rawData.length; ++i) {
        outputArray[i] = rawData.charCodeAt(i);
    }
    return outputArray;
}

function arrayBufferToBase64(buffer) {
    const bytes = new Uint8Array(buffer);
    let binary = '';
    for (let i = 0; i < bytes.byteLength; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    // Initialize push notifications
    initPushNotifications();
    
    // Initialize auto-save if on blog edit page
    const blogIdEl = document.querySelector('#blog-id');
    if (blogIdEl) {
        initAutoSave(blogIdEl.value);
    }
});