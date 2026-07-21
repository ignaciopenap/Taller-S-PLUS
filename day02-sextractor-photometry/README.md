# Día 2 — Análisis fotométrico: Source Extractor + PSFEx

**Martes 21/07** · Mendes de Oliveira · Montaguth

## Objetivos
- Entender los principios del análisis fotométrico.
- Correr Source Extractor y PSFEx sobre imágenes reales.
- **Evaluación:** elegir una región del footprint de S-PLUS, bajar las imágenes en los 12 filtros (splus.cloud) y extraer un catálogo fotométrico.

## Qué hice
<completar: región elegida (RA/Dec), config de SExtractor, catálogo resultante>

## Conceptos clave
Detección por umbral sobre el fondo, deblending, tipos de magnitud (AUTO/ISO/apertura),
modelado de PSF con PSFEx. Ver `../reference/glossary.md`.

## Cómo reproducir
1. Bajar las 12 imágenes de la región (ver `data/README.md`).
2. Correr SExtractor (config en `data/`) — o `sep` desde Python.
3. (Opcional) PSFEx para la PSF, y segunda pasada de SExtractor.

## Dudas / pendientes
<completar>

## Referencias
Bertin & Arnouts (1996) · Bertin (2011, PSFEx). Docs: https://www.astromatic.net/
