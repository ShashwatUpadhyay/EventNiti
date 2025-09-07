// Service Worker for Event Niti PWA
const CACHE_NAME = 'eventniti-v2';
const urlsToCache = [
  '/',
  '/static/css/styles.css',
  '/static/images/en2.png',
  '/static/images/logo/icon-192.png',
  '/static/images/logo/icon-512.png',
  '/static/manifest.json',
  'https://cdn.tailwindcss.com',
  'https://unpkg.com/aos@2.3.1/dist/aos.css',
  'https://unpkg.com/swiper/swiper-bundle.min.css'
];

const OFFLINE_URL = '/offline/';

// Install event
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(function(cache) {
        return cache.addAll(urlsToCache);
      })
  );
});

// Fetch event with offline support
self.addEventListener('fetch', function(event) {
  if (event.request.mode === 'navigate') {
    event.respondWith(
      fetch(event.request)
        .catch(() => caches.match(OFFLINE_URL))
    );
    return;
  }
  
  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        return response || fetch(event.request)
          .then(function(fetchResponse) {
            // Cache successful responses
            if (fetchResponse.status === 200) {
              const responseClone = fetchResponse.clone();
              caches.open(CACHE_NAME)
                .then(cache => cache.put(event.request, responseClone));
            }
            return fetchResponse;
          })
          .catch(() => {
            // Return offline page for navigation requests
            if (event.request.destination === 'document') {
              return caches.match(OFFLINE_URL);
            }
          });
      })
  );
});

// Push notification event
self.addEventListener('push', function(event) {
  const options = {
    body: event.data ? event.data.text() : 'New event notification',
    icon: '/static/images/logo/android/android-launchericon-192-192.png',
    badge: '/static/images/logo/android/android-launchericon-192-192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '1'
    },
    actions: [
      {
        action: 'explore',
        title: 'View Event',
        icon: '/static/images/logo/android/android-launchericon-192-192.png'
      },
      {
        action: 'close',
        title: 'Close',
        icon: '/static/images/logo/android/android-launchericon-192-192.png'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('Event Niti', options)
  );
});

// Notification click event
self.addEventListener('notificationclick', function(event) {
  event.notification.close();

  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/events/')
    );
  } else if (event.action === 'close') {
    event.notification.close();
  } else {
    event.waitUntil(
      clients.openWindow('/')
    );
  }
});

// Activate event
self.addEventListener('activate', function(event) {
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});