# Tablet/PWA Part 3-3f — Fire Risk loading fix

Problem observed:
- Python HTTP server returned HTTP 200 for fire_risk.bin in all districts.
- Browser still showed "No se pudo cargar fire_risk".

Fix:
- Fire Risk rasters are now embedded as Base64 in:
  data/simulation/fire_risk_embedded.js
- Huanipaca, Yanatile and San Juan del Oro Fire Risk arrays are decoded directly
  to Uint8Array in the browser.
- The array length is checked against width x height before simulation.
- Water Resources loading and calculation logic are unchanged.
- The validated QGIS grid-origin / pixel-mask logic from Part 3-3d is retained.

This is a focused Fire Risk loading fix.
