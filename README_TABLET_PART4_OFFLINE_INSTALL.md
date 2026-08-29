# Tablet/PWA Part 4 — Offline installation

## Windows / Android development test
1. Extract the ZIP into a new folder.
2. Open Command Prompt in that folder.
3. Run:
   py -m http.server 8000
4. Open:
   http://127.0.0.1:8000/
5. Keep the page open for a while the Service Worker caches local files.
6. Use the app's "Comprobar offline" status box.
7. After the cache is ready, disconnect the network and reload the app.

## Android tablet
When deployed on HTTPS (GitHub Pages or another HTTPS host), open the app in Chrome/Edge.
Use "Instalar aplicación" or the browser menu → Install app / Add to Home screen.
After the first complete online load, the local PWA cache contains the operational files.

## iPad
Open the HTTPS version in Safari.
Use Share → Add to Home Screen.
iPadOS does not show the same install prompt as Android, but the Home Screen web app works as a PWA.
Open the app online once before field use so Safari can cache the application data.

## Important
- localhost/127.0.0.1 is valid for PC development.
- For tablets, installation requires an HTTPS origin for normal PWA use.
- The app itself contains offline OSM-independent data, DEM relief, offline satellite images, statistics data, Water Resources simulation data and Fire Risk simulation data.
- Online OSM and Online Satellite naturally require internet. Use Offline Satellite or DEM Relief in the field.
