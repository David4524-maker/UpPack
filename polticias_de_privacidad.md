# UpPack · Política de privacidad

> Última actualización: 30 de octubre de 2026

UpPack es una app de almacenamiento "en la nube" para guardar y proteger archivos. Existe en dos versiones: **`uppack.py`** (Python/Tkinter) y **`uppack.html`** (simulación en el navegador). Este documento explica, en lenguaje claro, qué hace y qué no hace cada una con tus datos.

## Resumen rápido

| Pregunta | Respuesta |
|---|---|
| ¿Necesito una cuenta? | No. No hay registro ni inicio de sesión. |
| ¿Mis archivos se envían a un servidor? | No. Todo ocurre en tu propio dispositivo. |
| ¿UpPack recopila datos personales? | No. No hay telemetría, analíticas ni anuncios. |
| ¿Se comparten datos con terceros? | No. UpPack no se conecta a ningún servicio externo. |
| ¿Se borra algo de mi PC al subir un archivo? | Nunca. Los originales solo se leen. |
| ¿Quién controla mis datos? | Tú. Puedes borrarlos cuando quieras. |

## 1. Qué datos maneja UpPack

**Los archivos que tú eliges subir.** Solo se procesan los que seleccionas o arrastras tú mismo.

**Metadatos de esos archivos:** nombre, tamaño, fecha de subida y si el escáner los marcó como riesgosos.

**Tus preferencias:** idioma elegido y si activaste la casilla "Liberar 19GB gratis".

UpPack **no** pide ni guarda tu nombre, correo, teléfono, ubicación, contactos ni identificadores del dispositivo.

## 2. Dónde se guardan los datos

### Versión Python (`uppack.py`)

Todo se guarda en una carpeta local de tu usuario: `~/UpPack_Vault`.

- `files/`: tus archivos, **cifrados** (extensión `.upk`).
- `index.json`: la lista de archivos (nombre, tamaño, fecha, marca de riesgo) y tus preferencias.
- `.key`: la clave de cifrado, generada aleatoriamente en tu equipo.

### Versión HTML (`uppack.html`)

Es una **simulación**. Solo guarda nombre, tamaño, fecha y preferencias en el `localStorage` de tu navegador. **El contenido de tus archivos no se guarda ni se envía a ningún lado**; el archivo original solo se lee un momento para escanearlo.

## 3. Lo que UpPack NO hace

- No envía tus archivos ni tus metadatos a ningún servidor.
- No usa cookies, rastreadores, analíticas ni publicidad.
- No vende, alquila ni comparte información con nadie.
- No modifica, mueve ni elimina los archivos originales de tu PC.
- No accede a archivos que no hayas seleccionado.

## 4. El escáner de archivos peligrosos o ilegales

Al subir un archivo, UpPack lo analiza **de forma local** (sin internet) con criterios aproximados: extensiones peligrosas (por ejemplo `.exe`, `.bat`, `.vbs`), ejecutables disfrazados, firmas de malware conocidas y nombres típicos de software pirata (crack/keygen).

- Si detecta algo, **bloquea** el archivo y te muestra un aviso con el motivo y dos botones: **Aceptar** (no se guarda) y **Guardar de todos modos** (se guarda marcado con ⚠).
- Ningún resultado se envía fuera de tu dispositivo.
- **Es una ayuda, no una garantía.** Puede no detectar archivos peligrosos o ilegales, y puede marcar por error archivos inofensivos. No reemplaza a un antivirus ni a tu propio criterio.
- Si eliges "Guardar de todos modos", la decisión y la responsabilidad son tuyas. No subas contenido que sea ilegal.

## 5. Seguridad

En la versión Python, los archivos se cifran antes de guardarse y se verifica su integridad al recuperarlos. Conviene saber sus límites:

- El cifrado usa solo la librería estándar de Python y **no ha sido auditado por terceros**.
- La clave se guarda en la misma carpeta que los archivos, así que **no protege contra alguien que ya tenga acceso a tu cuenta o a tu equipo**.
- Si pierdes o borras el archivo `.key`, **no podrás recuperar** tus archivos cifrados.
- Para proteger información realmente sensible, haz copias de seguridad y usa un cifrado con contraseña propio.

La versión HTML no cifra nada, porque no guarda el contenido de tus archivos.

## 6. Espacio y "19GB gratis"

El almacenamiento es un límite interno de la app: 1 GB de base, y 20 GB al marcar **"Liberar 19GB gratis"**. No se descuenta nada de tu PC, no tiene costo y no requiere datos de pago. En la práctica, el espacio lo ocupa tu propio disco (versión Python) o no se ocupa (versión HTML).

## 7. Tus derechos y controles

- **Eliminar un archivo:** usa el botón de eliminar en la app (solo borra la copia de UpPack, nunca el original).
- **Borrar todo (Python):** cierra la app y elimina la carpeta `~/UpPack_Vault`.
- **Borrar todo (HTML):** borra los datos del sitio en tu navegador.
- **Cambiar de idioma o desactivar la casilla de 19GB:** en cualquier momento. Para desactivar la casilla, tus archivos guardados no pueden superar 1 GB.

Como los datos nunca salen de tu dispositivo, no hay nada que solicitar a un tercero: tú tienes el control total.

## 8. Menores de edad

UpPack no pide edad ni datos personales y no recopila información de nadie. Aun así, los menores deberían usarlo con supervisión de un adulto.

## 9. Cambios en esta política

Si una versión futura añade funciones que cambien el tratamiento de datos (por ejemplo, un servidor real, cuentas o sincronización), esta política se actualizará **antes** y se indicará la fecha del cambio. Este documento describe únicamente el comportamiento actual de las versiones incluidas.

## 10. Contacto

Si tienes preguntas sobre esta política, escribe a: **[ikerdavidg07@gmail.com]**

---

*Este documento es informativo y no constituye asesoría legal. Si publicas UpPack para otras personas, revisa que se ajuste a las leyes de privacidad que te apliquen.*
