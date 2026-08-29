# Tablet/PWA Part 2 — Statistics for all districts

This version extends the Statistics mode to:
- Huanipaca
- Yanatile
- San Juan del Oro

The supplied UTM GeoPackages remain the master analysis data.
For Leaflet display, watershed geometries were converted to EPSG:4326 GeoJSON.
Precomputed statistical attributes are preserved.

Land-cover display rules:
- Plantaciones = LC06_HA + LC07_HA
- Pajonal/Pastos = LC13_HA + LC14_HA
- Bofedal = LC15_HA

Statistics can be switched between Microcuenca 2 km² and 10 km².
The selected watershed can be changed by tapping another watershed.

Run locally with:
    py -m http.server 8000

Then open:
    http://127.0.0.1:8000/
