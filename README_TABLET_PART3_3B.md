# Part 3-3b — Huanipaca QGIS pixel-mask validation

The latest QGIS simulation_grid.py confirms that the grid is a temporary in-memory layer: full 100 m x 100 m cells are retained when their centres fall inside/on the watershed. No persistent grid_*.gpkg is required.

This build therefore restores/keeps the original full-cell grid (so 9 selected cells = 9.00 ha), and changes the raster extraction logic instead:
- water raster pixels: include only pixel centres inside the union of selected 100 m cells
- hydrology starting cells: include only flow-direction pixel centres inside the selected geometry

This mirrors the QGIS centre-point mask logic and is the key test for matching current water volume and affected area.
