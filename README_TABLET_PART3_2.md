# Tablet/PWA Part 3-2 — Recursos hídricos (3 distritos)

Implementado:
- Huanipaca, Yanatile y San Juan del Oro
- Microcuenca 2 km² / 10 km²
- Selección de cuadrículas de 100 m
- Comparación entre raster hídrico actual y escenario de uso futuro
- Conversión de mm/mes a m³/mes usando el área real del píxel
- Trazado D8 aguas abajo
- Convergencia a cauce compartido (40 %, mínimo 3 trayectorias, mínimo 3 pasos)
- Expansión del corredor según Flow Accumulation (radio 1–3 píxeles)
- Área potencialmente afectada, disponibilidad hídrica actual e impacto relativo
- Visualización del área afectada en el mapa
- Ejecutar simulación se ubica encima de Borrar selección

La composición de cobertura terrestre por cuadrícula se mantiene para Huanipaca. Para Yanatile y San Juan del Oro se añadirán sus GeoPackage de cobertura terrestre en una actualización posterior.

Riesgo de incendio se implementará en Part 3-3.
