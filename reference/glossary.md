# Glosario

Documento vivo. Cada entrada intenta ir de la **intuición** al **detalle técnico**. Agregá
términos a medida que aparezcan.

---

## Bases de datos y Observatorio Virtual (día 1)

**Observatorio Virtual (VO)** — No es un sitio ni un servidor: es un conjunto de *estándares*
(los define la IVOA) para que todos los archivos astronómicos "hablen el mismo idioma". La
idea: usar todos los archivos del mundo como si fueran una sola base de datos. Análogo a HTTP.

**TAP** (*Table Access Protocol*) — El protocolo para pedirle tablas a un servidor. Lo que hay
detrás del menú `VO → TAP Query` de TOPCAT.

**ADQL** (*Astronomical Data Query Language*) — SQL extendido con geometría esférica (conos,
polígonos en el cielo). El lenguaje en el que escribís la consulta dentro de TAP. Ojo: **no
distingue mayúsculas**, así que hay que encomillar identificadores ambiguos (`"uPmag"`).

**VOTable** — El formato de tabla estándar del VO. Trae los datos *y* sus metadatos (unidades,
descripciones, UCDs). Extensión `.vot`.

**UCD** (*Unified Content Descriptor*) — Etiqueta estándar que dice qué *significa* una columna,
independientemente de cómo se llame. `zsp` y `Z_SPEC` pueden ser el mismo `src.redshift`. El
software confía en el UCD, no en el nombre.

**Cone search** — "Dame todo lo que hay dentro de este círculo del cielo." Consulta posicional.

**Crossmatch** — Cruzar dos catálogos por posición. Clave: no devuelve la *unión* sino la
**intersección de dos funciones de selección**, y lo que se pierde rara vez es aleatorio.

**Registry** — La "guía telefónica" del VO: quién ofrece qué tabla y en qué dirección.

**SAMP** — Protocolo para que los programas de tu máquina se hablen entre sí (Aladin le manda
una tabla a TOPCAT, etc.).

---

## Fotometría y catálogos (días 2–3)

**S-PLUS** — *Southern Photometric Local Universe Survey*. Survey del hemisferio sur con **12
filtros**: 5 anchos (tipo SDSS: u, g, r, i, z) + 7 angostos centrados en rasgos estelares
clave ([OII], CaHK, Hδ, G-band, Mgb, Hα, CaT). La SED de baja resolución que dan esos 12
puntos es la marca del survey.

**Source Extractor (SExtractor)** — Software que detecta fuentes en una imagen y mide su
fotometría, construyendo un catálogo. Detección por umbral sobre el fondo, deblending,
distintos tipos de magnitud (AUTO, ISO, apertura).

**PSFEx** (*PSF Extractor*) — Modela la PSF variable a lo largo del campo a partir de las
estrellas, para hacer fotometría de PSF consistente. Se usa junto con SExtractor.

**PSF vs Petrosian vs model** — Tres formas de medir el brillo. **PSF** ajusta la fuente
puntual: perfecto para estrellas, **malo para galaxias** (tira disco y halo). **Petrosian**
define la apertura por el perfil de luz, independiente del redshift: el estándar para galaxias.
**Model** ajusta un perfil (de Vaucouleurs o exponencial). *Nunca mezclar sistemas* en un mismo
color o magnitud.

**splusdata** — Librería de Python para consultar catálogos y traer imágenes de S-PLUS desde
splus.cloud. Requiere cuenta.

**iDR6** — *internal Data Release 6* de S-PLUS. Incluye imágenes, catálogos, calibración y
flags de calidad.

**Flags de calidad** — Columnas que marcan objetos problemáticos. Necesarias pero **no
suficientes**: aun con los flags "buenos" puede colarse basura. Siempre mirar los datos.

---

## Poblaciones estelares y CMDs (día 4)

**SED** (*Spectral Energy Distribution*) — Cómo se reparte el flujo de un objeto en función de
la longitud de onda. La fotometría de 12 filtros de S-PLUS es una SED de baja resolución.

**SSP** (*Simple Stellar Population*) — Población de estrellas de la misma edad y metalicidad,
nacida a la vez. Ladrillo básico: cualquier galaxia se modela como suma de SSPs.

**Síntesis espectral de poblaciones** — Reconstruir la historia de formación estelar de una
galaxia ajustando su espectro/SED como combinación de SSPs. El código clásico es **STARLIGHT**
(Cid Fernandes). De ahí el nombre "paleontología de galaxias".

**Fotometría sintética** — Integrar un espectro contra la curva de transmisión de un filtro
para obtener la magnitud que *mediría* ese filtro. Puente entre espectros y fotometría.

**Corrección K** — Corrige el desplazamiento del espectro por redshift dentro de la banda del
filtro. Depende del color, así que omitirla **sesga** (no solo degrada) los colores.
Referencia usada por TOPCAT: Chilingarian et al. (2010).

**Módulo de distancia / distancia de luminosidad** — Para pasar de magnitud aparente a
absoluta. En ΛCDM (H₀=70, Ωm=0.3, ΩΛ=0.7). Referencia canónica: Hogg (2000).

**CMD** (*Colour–Magnitude Diagram*) — Color vs magnitud absoluta. En galaxias revela la
**bimodalidad**: secuencia roja (apagadas, elípticas), nube azul (formando estrellas, discos)
y el **green valley** poco poblado entre ambas → la transición (*quenching*) es rápida.
Referencias fundacionales: Strateva et al. (2001), Baldry et al. (2004).

---

## Simulaciones (día 5)

**IllustrisTNG / TNG50** — Suite de simulaciones cosmológicas magnetohidrodinámicas. TNG50 es
la de mayor resolución (caja de 50 Mpc). Los datos vienen en **HDF5**.

**SKIRT** — Código de transporte radiativo Monte Carlo. Genera imágenes/espectros "mock" de
galaxias simuladas, incluyendo el efecto del polvo, en las bandas que quieras (acá, los 12
filtros de S-PLUS). Su salida es un **cubo FITS**.

**HDF5** — Formato jerárquico para datos científicos grandes. Se lee con `h5py`.

**Cubo de datos (data cube)** — Arreglo 3D: dos ejes espaciales + un tercer eje (longitud de
onda o filtro). Cada "rebanada" es una imagen en una banda.

**PSF convolution / ruido sintético** — Para que una imagen mock parezca observada: se la
convoluciona con la PSF del instrumento y se le suma ruido realista. Convierte una imagen
"perfecta" de simulación en algo comparable con datos reales.

**Perfil de brillo superficial** — Cómo cae el brillo desde el centro de la galaxia hacia
afuera. Diagnóstico estructural clave (bulbo vs disco). Se mide con `photutils`.
