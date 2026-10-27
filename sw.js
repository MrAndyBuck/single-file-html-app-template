const APP_ID = "cadnt";
const VERSION = "v00000-020";
const CACHE = APP_ID + "-" + VERSION;
const FILES = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon.svg",
  "./vendor/three.min.js",
  "./vendor/three-csg.js",
  "./vendor/three-exporters.js",
  "./vendor/three-loaders.js",
  "./assets/manifest.json",
  "./assets/Finger.jpg",
  "./assets/ChineseFlag.webp",
  "./assets/brand/CADNTLogo.png",
  "./assets/brand/favicon-32x32.png",
  "./assets/ads/AipacAppAd.jpeg",
  "./assets/ads/AmwayAppAd.jpeg",
  "./assets/ads/AppAds.jpeg",
  "./assets/ads/AppleAppAd.jpeg",
  "./assets/ads/AsbestosAppAd.webp",
  "./assets/ads/CnBAppAd.png",
  "./assets/ads/EnronAppAd.jpg",
  "./assets/ads/FushigiAppAd.jpg",
  "./assets/ads/GamblingAppAd.webp",
  "./assets/ads/GamblingAppAd2.png",
  "./assets/ads/MomsAppAd.jpg",
  "./assets/ads/MrCleanAppAd.png",
  "./assets/ads/PalantirAppAd.jpeg",
  "./assets/ads/TheranosAppAd.jpeg",
  "./assets/ads/TourismAppAd.jpeg",
  "./assets/ads/ViagraAppAd.webp",
  "./assets/ads/VirusAppAd.png",
  "./assets/ads/ZuneAppAd.webp",
  "./assets/audio/ChinaMusic.m4a",
  "./assets/audio/New%20Recording%2012.m4a"
];

self.addEventListener("install", (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then((c) =>
      c.addAll(FILES.map((f) => new Request(f, { cache: "reload" })))
    )
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys
          .filter((k) => k !== CACHE)
          .map((k) => caches.delete(k))
      )
    ).then(() => self.clients.claim())
  );
});

self.addEventListener("message", (e) => {
  if (e.data === "SKIP_WAITING") self.skipWaiting();
});

self.addEventListener("fetch", (e) => {
  if (e.request.method !== "GET") return;

  const url = new URL(e.request.url);
  const isHtml = e.request.mode === "navigate" || 
                 e.request.destination === "document" || 
                 url.pathname.endsWith(".html") || 
                 url.pathname.endsWith("/");

  if (isHtml) {
    // Network-First for HTML: always serve fresh code when connected
    e.respondWith(
      fetch(e.request)
        .then((resp) => {
          if (resp && resp.status === 200) {
            const clone = resp.clone();
            caches.open(CACHE).then((c) => c.put(e.request, clone));
          }
          return resp;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-First for static vendor assets
  e.respondWith(
    caches.match(e.request).then((hit) => hit || fetch(e.request))
  );
});
