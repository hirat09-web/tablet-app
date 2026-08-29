# Forest Management Tablet/PWA – Part 2 (Huanipaca Statistics)

## Added in Part 2
- Huanipaca Statistics mode.
- Microcuenca 2 km² / 10 km² selection.
- Watershed GeoPackages converted from EPSG:32718 to EPSG:4326 for Leaflet display.
- Tap a watershed to display pre-calculated statistics.
- Basic indicators, land-cover areas, forest degradation, fire risk and water resources.
- WATER_MEAN null is displayed as “Sin datos”; zero remains zero.
- New statistics GeoJSON files are included in the offline Service Worker cache.

## Source of calculations
The statistical values are taken from the supplied UTM GeoPackages. Only geometries are transformed to WGS84 for web display; statistical attributes are not recalculated in the browser.


## Correcciones v2
- Plantaciones = LC06 (eucalipto) + LC07 (pino).
- Pajonal/Pastos = LC13 + LC14.
- Bofedal = LC15.
- Se corrigió la selección para poder cambiar de microcuenca después de seleccionar una.
