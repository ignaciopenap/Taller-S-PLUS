# S-PLUS Workshop 2026 — mi experiencia

Apuntes, ejercicios y código de mi paso por el **S-PLUS Workshop** (IAG / Universidad de
São Paulo), del 20 al 24 de julio de 2026. El taller recorre el ciclo completo del dato
astronómico moderno: desde las bases de datos y los surveys de área grande, pasando por la
construcción de catálogos fotométricos, hasta el análisis en Python, las poblaciones
estelares y las simulaciones cosmológicas.

> **S-PLUS** = *Southern Photometric Local Universe Survey*: un survey fotométrico del
> hemisferio sur con **12 filtros** (5 anchos tipo SDSS + 7 angostos), liderado desde el
> IAG-USP. Es el hilo conductor de todo el taller.

## Objetivo de este repositorio

Aprender de verdad —no solo apretar botones— y dejar registrada la experiencia de forma
**reproducible** para poder mostrarla. Cada día es una unidad autocontenida: apuntes de las
clases, el hands-on, la proveniencia de los datos y las figuras que valen la pena.

## Los cinco días

| Día | Carpeta | Tema | Docentes |
|-----|---------|------|----------|
| Lun 20/07 | [`day01-databases-topcat/`](day01-databases-topcat/) | Bases de datos astronómicas · SIMBAD, VizieR, Aladin, ds9, TOPCAT | Mendes de Oliveira · Demarco · Montaguth |
| Mar 21/07 | [`day02-sextractor-photometry/`](day02-sextractor-photometry/) | Análisis fotométrico · Source Extractor + PSFEx · catálogos | Mendes de Oliveira · Montaguth |
| Mié 22/07 | [`day03-splus-python-workflow/`](day03-splus-python-workflow/) | Datos S-PLUS iDR6 en Python · `splusdata`, Astropy, perfiles | Oliveira Schwarz |
| Jue 23/07 | [`day04-stellar-populations-cmd/`](day04-stellar-populations-cmd/) | Espectro vs fotometría · poblaciones estelares · fotometría sintética · CMDs | Batista · Cid Fernandes |
| Vie 24/07 | [`day05-tng-simulations-skirt/`](day05-tng-simulations-skirt/) | Evolución de galaxias · IllustrisTNG · imágenes mock SKIRT (TNG50) | Demarco · Machado · Gonçalves |

Horario, docentes y criterios de evaluación completos en
[`reference/schedule.md`](reference/schedule.md).

## Cómo montar el entorno

```bash
# 1. Clonar
git clone <url-de-tu-repo> && cd splus-workshop-2026

# 2. Crear el entorno conda (incluye lo de los 5 días)
conda env create -f environment.yml
conda activate splus-workshop

# 3. Registrar el kernel para los notebooks
python -m ipykernel install --user --name splus-workshop
```

Para acceder a los datos de S-PLUS necesitás una cuenta gratuita en
[splus.cloud](https://splus.cloud/) (la usa `splusdata` desde el día 3).

## Una nota sobre los datos

Las imágenes FITS (12 filtros), los cubos de datos y los archivos HDF5 de simulación **no
se versionan** — son binarios grandes y GitHub no es su lugar. En su lugar, cada
`dayNN/data/README.md` documenta **cómo regenerar el dato**: la consulta, el comando o el
enlace. Es la misma lección del día 1: *guardá la pregunta, no solo la respuesta.*

## Herramientas de IA

Usé un asistente de IA para ordenar apuntes, explicar conceptos y depurar código (ver
[`prompts/`](prompts/)). La ciencia —las decisiones, las consultas, la interpretación— es
mía, y la verifiqué. Un output plausible no es un output correcto.

## Licencia

Código bajo licencia MIT (ver [`LICENSE`](LICENSE)). Los apuntes son personales; citá las
fuentes originales listadas en [`papers/`](papers/) y [`reference/resources.md`](reference/resources.md).
