# Tablet/PWA Part 2 v5

This build refreshes the Statistics data for all 3 districts using the latest
updated watershed GeoPackages supplied on 2026-08-27.

Districts / analysis units:
- Huanipaca: 2 km² / 10 km²
- Yanatile: 2 km² / 10 km²
- San Juan del Oro: 2 km² / 10 km²

Important corrections already incorporated in the source GeoPackages:
- DEM / slope statistics aligned with the QGIS Statistics polygon-mask logic
- Plantations handled as eucalyptus + pine (codes 6 + 7)
- Carbon total aligned with QGIS Statistics
- Updated raster-derived statistics after the common extraction fix

Tablet land-cover display rules remain:
- Plantaciones = LC06_HA + LC07_HA
- Pajonal/Pastos = LC13_HA + LC14_HA
- Bofedal = LC15_HA

The UTM GeoPackages remain the master analysis data.
Only the web display geometry is converted to EPSG:4326 GeoJSON.

During development, Statistics GeoJSON is network-first with offline cache fallback.
The Statistics panel should show:
  Versión de datos: 2026-08-27 / Tablet Part 2 v5
