# Horario — S-PLUS Workshop 2026

Formato diario: **9:00–10:00** y **10:00–11:00** clases teóricas · **14:00–15:30** hands-on.

---

## Lunes 20/07 — Bases de datos astronómicas

- **L1 (9:00)** — *Astronomy in the context of large-area sky surveys — The case of S-PLUS* — **Claudia Mendes de Oliveira**. Descripción general de S-PLUS.
- **L2 (10:00)** — *Spectroscopic properties of galaxies* — **Ricardo Demarco**. Espectros según tipo de galaxia; distribución espectral pancromática; rasgos espectrales prominentes; edad, metalicidad, masa y formación estelar.
- **Hands-on 1 (14:00)** — *Astronomical Databases* — **Gissel Montaguth**. SIMBAD, VizieR, Aladin, ds9, introducción a TOPCAT. Acceso a datos (cargar tablas, crossmatch local y con CDS), análisis (submuestras, gráficos), ejemplos.
- **Evaluación:** familiarizarse con varias bases de datos y con TOPCAT.

## Martes 21/07 — Análisis fotométrico

- **L3 (9:00)** — *Principles of photometric analysis* — **Claudia Mendes de Oliveira**.
- **L4 (10:00)** — *Source Extractor — building catalogs from astronomical images* — **Gissel Montaguth**. Introducción a Source Extractor y PSFEx; ejemplos prácticos.
- **Hands-on 2 (14:00)** — **Gissel Montaguth**. Correr los ejemplos de la L4.
- **Evaluación:** elegir una región del footprint de S-PLUS, obtener las imágenes en los 12 filtros vía splus.cloud y extraer la fotometría para construir un catálogo de esa región.

## Miércoles 22/07 — Datos S-PLUS en Python

- **L5 (9:00)** — *The S-PLUS iDR6* — **Gustavo Oliveira Schwarz**. Visión general de iDR6; observaciones y reducción; calibración astrométrica y fotométrica; productos de imagen, catálogos e información de calidad; acceso e interpretación.
- **L6 (10:00)** — *Astronomical Data and Data Retrieval* — **Gustavo Oliveira Schwarz**. NumPy, pandas, Matplotlib, Astropy Tables; lectura y manejo de catálogos; recuperar datos S-PLUS con `splusdata`; visualización y análisis exploratorio.
- **Hands-on 3 (14:00)** — **Gustavo Oliveira Schwarz + TBD**. Workflow completo con datos reales: consultar y recuperar un catálogo con `splusdata`; explorar columnas, medidas fotométricas y flags de calidad; elegir una galaxia y traer su imagen; visualizarla y hacer gráficos de color/diagnóstico; medir y graficar su perfil de brillo superficial; inspeccionar un cubo de datos.

## Jueves 23/07 — Poblaciones estelares

- **L7 (9:00)** — *Spectroscopy vs. Photometry* — **Julia Thainá Batista**. Conceptos y diferencias; ventajas y límites de cada técnica; imaging de banda ancha, espectroscopía integrada e IFU; qué permite una técnica y la otra no.
- **L8 (10:00) — CHARLA INVITADA** — *Paleontology of Galaxies* — **Prof. Roberto Cid Fernandes**. Poblaciones estelares simples (SSPs) y su evolución; métodos de síntesis (foto)espectral; aplicaciones.
- **Hands-on 4 (14:00)** — **Julia Thainá Batista**. Ejercicios con SSPs; efecto de la edad estelar sobre las SEDs; efecto de la metalicidad sobre colores y espectros; fotometría sintética (de espectros a magnitudes); flujos vs magnitudes; construir e interpretar CMDs.

## Viernes 24/07 — Evolución y simulaciones

- **L9 (9:00)** — *Topics of Galaxy Evolution: What We Know and What We Still Do Not Understand* — **Prof. Ricardo Demarco**.
- **L10 (10:00) — CHARLA INVITADA** — *Cosmological Simulations* — **Prof. Rubens Machado**. Simulaciones hidrodinámicas de N-cuerpos; datos de IllustrisTNG; conexión entre galaxias simuladas y observaciones.
- **Hands-on 5 (14:00)** — *SKIRT Mock Images of TNG50 Galaxies in S-PLUS Bands* — **Tutor invitado: Gustavo Gonçalves**. Visualizar datos crudos de simulación (HDF5); manejar la salida de SKIRT (cubo FITS); agregar ruido sintético y convolución con la PSF.
