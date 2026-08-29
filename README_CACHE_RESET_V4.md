# Tablet Part 2 v4 — cache-safe development build

This build was created because an older Service Worker/cache could make the browser
show previous statistics even after the GeoJSON files were replaced.

Checks:
- Huanipaca source GeoPackages have UPDATE_DATE 2026-08-27 12:55.
- The generated WGS84 GeoJSON preserves those updated attributes.
- Statistics UI uses:
  - MEAN_DEM
  - MEAN_SLOPE
  - Plantaciones = LC06_HA + LC07_HA
  - Pajonal/Pastos = LC13_HA + LC14_HA
  - Bofedal = LC15_HA

During development, watershed GeoJSON is now network-first with no-store,
then falls back to the cached copy when offline.

The Statistics panel displays:
  Versión de datos: 2026-08-27 12:55 / Tablet Part 2 v4

If that line is not visible, the browser is still showing an older HTML version.
