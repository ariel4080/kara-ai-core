# Pull Request Description Conventions

Convenciones para descripciones de Pull Requests basadas en análisis de 4,500+ PRs del proyecto bancadigital-bm-app y plantilla oficial del repositorio.

---

## 📝 Plantilla Oficial

El repositorio tiene una plantilla oficial que DEBE seguirse:

```markdown
## Descripción de este PR

* Bullet point describiendo cambio principal 1
* Bullet point describiendo cambio principal 2
* Bullet point describiendo cambio principal 3

## Link de Historia del AzureBoards

[AB#XXXXX](https://dev.azure.com/bacsansose/BAC/_workitems/edit/XXXXX)

## Link de ADR
<!-- Solo si aplica, de lo contrario eliminar esta sección -->

Referencia [ADR](https://github.com/BAC-Credomatic/bancadigital-docs-adrs/pull/XXX/...)

## Evidencias Visuales

> [!IMPORTANT]
> - Imagen y/o video según corresponda
> - Esta evidencia tiene como propósito detectar issues visuales
> - Para tareas técnicas: screenshot de logs o estructura
```

---

## 🎯 Componentes Obligatorios

### 1. Descripción de Este PR

**Formato:**
- Usar bullet points (`*` o `-`)
- Cada bullet describe un cambio principal
- Mínimo 1 bullet, recomendado 2-5 bullets
- Ser específico sobre QUÉ cambió

**✅ Correcto:**
```markdown
## Descripción de este PR

* Implementar funcionalidad de guardar favoritos en flujo de pago de servicios
* Agregar UI para gestión de favoritos (añadir, eliminar, editar)
* Integrar con backend de favoritos usando endpoint POST /favorites
* Agregar validación de campos requeridos antes de guardar
```

**❌ Incorrecto:**
```markdown
## Descripción de este PR

* Cambios varios
* Ajustes
* Fix de bugs
```

**Regla:** Cada bullet debe ser específico y descriptivo.

---

### 2. Link de Historia del AzureBoards

**Formato Obligatorio:**
```markdown
[AB#XXXXX](https://dev.azure.com/bacsansose/BAC/_workitems/edit/XXXXX)
```

**Componentes:**
- Texto del link: `AB#XXXXX` donde XXXXX es el número del ticket (típicamente 5-6 dígitos)
- URL: Reemplazar XXXXX en ambos lugares con el mismo número

**✅ Correcto:**
```markdown
[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)
[AB#103820](https://dev.azure.com/bacsansose/BAC/_workitems/edit/103820)
[AB#99999](https://dev.azure.com/bacsansose/BAC/_workitems/edit/99999)
```

**❌ Incorrecto:**
```markdown
❌ [BC#35367](...)  # Debe ser AB#, no BC#
❌ [AB#XXXXX](...)  # XXXXX debe ser reemplazado
❌ AB#35367         # Debe ser un link markdown
❌ [35367](...)     # Falta prefijo AB#
❌ [AB#35367](https://dev.azure.com/.../edit/XXXXX)  # URL sin actualizar
```

**Regla:** El número debe coincidir entre el texto del link y la URL.

---

### 3. Link de ADR (Opcional)

**Solo incluir si:**
- Se tomó una decisión arquitectónica
- Existe un ADR documentado
- El cambio es significativo en arquitectura

**Formato:**
```markdown
Referencia [ADR](https://github.com/BAC-Credomatic/bancadigital-docs-adrs/pull/XXX/commits/HASH#diff-...)
```

**Si NO aplica:**
```markdown
<!-- Eliminar toda la sección "Link de ADR" -->
```

**✅ Correcto (cuando aplica):**
```markdown
## Link de ADR

Referencia [ADR-025: Migración a Riverpod](https://github.com/BAC-Credomatic/bancadigital-docs-adrs/pull/227/commits/2bca6976b8f6666b1b4abd16836659cb5f82f6fe#diff-5c70ab55244664e8b4a72ee34ef390e894fc057c5b89b132e513d11903c804c9)
```

**✅ Correcto (cuando NO aplica):**
```markdown
<!-- No incluir la sección de ADR -->
```

**❌ Incorrecto:**
```markdown
## Link de ADR

N/A  # Mejor eliminar toda la sección
```

**Regla:** Si no hay ADR, eliminar la sección completa.

---

### 4. Evidencias Visuales

**Obligatorio para:**
- Features nuevas o modificadas (UI)
- Fixes de bugs visuales
- Change requests con impacto visual

**Formatos aceptados:**
- Screenshots (PNG, JPG)
- Videos (MP4, GIF)
- Para tareas técnicas: logs, estructura de proyecto, coverage reports

**Estructura recomendada:**

#### Para Features/Fixes Visuales:
```markdown
## Evidencias Visuales

### ANTES
<insertar imagen/video del estado anterior>

### DESPUÉS
<insertar imagen/video con el cambio aplicado>

> [!IMPORTANT]
> - Video mostrando el flujo completo ANTES (sin la feature)
> - Video mostrando el flujo DESPUÉS (con la feature funcionando)
> - Esta evidencia es crítica para detectar issues visuales
```

#### Para Tareas Técnicas:
```markdown
## Evidencias Visuales

### Test Coverage
<screenshot del reporte de coverage>

### Estructura de Archivos
<screenshot de la nueva estructura>

### Logs
<screenshot de logs mostrando el comportamiento correcto>
```

**✅ Correcto:**
```markdown
## Evidencias Visuales

### ANTES
![Pantalla sin favoritos](https://...)

### DESPUÉS
![Pantalla con favoritos](https://...)

> [!IMPORTANT]
> - Video del flujo completo mostrando guardado de favorito
> - Se valida que el botón de favorito aparece correctamente
> - Se verifica la funcionalidad de editar/eliminar favoritos
```

**❌ Incorrecto:**
```markdown
## Evidencias Visuales

Ver en el código  # NO es evidencia visual
```

**Regla:** Siempre incluir imágenes/videos. Para tareas técnicas, incluir screenshots relevantes.

---

## 🎯 Tipos de PR y sus Características

### Feature (ft)

**Descripción debe incluir:**
- Funcionalidad que se agrega
- Pantallas/componentes nuevos
- Integraciones con backend (endpoints)
- Validaciones implementadas

**Evidencias:**
- Video del flujo completo ANTES/DESPUÉS
- Screenshots de cada pantalla nueva
- Casos edge (pantallas vacías, errores, etc.)

**Ejemplo:**
```markdown
## Descripción de este PR

* Implementar funcionalidad de guardar favoritos en flujo de pago de servicios
* Agregar UI para gestión de favoritos con opciones añadir/editar/eliminar
* Integrar con endpoint POST /api/v1/favorites y GET /api/v1/favorites
* Agregar validación de alias único y campos obligatorios
* Implementar confirmación antes de eliminar favorito

## Link de Historia del AzureBoards

[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)

## Evidencias Visuales

### ANTES
![Sin favoritos](...)

### DESPUÉS - Agregar Favorito
![Pantalla agregar](...)

### DESPUÉS - Lista de Favoritos
![Lista con favoritos](...)

### DESPUÉS - Editar/Eliminar
![Opciones de edición](...)

> [!IMPORTANT]
> - Video completo del flujo: agregar → listar → editar → eliminar favorito
> - Se valida comportamiento en caso de error de red
> - Se verifica validación de alias duplicado
```

---

### Fix (fx)

**Descripción debe incluir:**
- Qué bug se corrigió (breve)
- Qué cambió en el código
- Dónde se aplicó el fix
- Por qué funcionaba incorrectamente

**Evidencias:**
- Video/screenshot mostrando el bug ANTES
- Video/screenshot mostrando el fix DESPUÉS
- Logs si aplica

**Ejemplo:**
```markdown
## Descripción de este PR

* Agregar validación `context.mounted` en método `save()` antes de llamar `setState()`
* Corregir crash cuando usuario navega atrás durante operación async
* Implementar pattern recomendado de Flutter lifecycle

## Link de Historia del AzureBoards

[AB#103820](https://dev.azure.com/bacsansose/BAC/_workitems/edit/103820)

## Evidencias Visuales

### ANTES (Crash)
![Log del crash](...)

### DESPUÉS (Sin crash)
![Navegación funcionando correctamente](...)

> [!IMPORTANT]
> - Video mostrando que ya no ocurre el crash al navegar atrás rápidamente
> - Se valida en escenario de red lenta (throttling)
```

---

### Technical Task (tt)

**Descripción debe incluir:**
- Tests agregados/actualizados
- Version bumps
- Configuraciones modificadas
- Refactors menores
- Integraciones de herramientas

**Evidencias:**
- Test coverage reports
- Screenshots de configuración
- Logs de builds exitosos
- Estructura de archivos

**Ejemplo:**
```markdown
## Descripción de este PR

* Agregar tests unitarios para `CardsViewModel`
* Cubrir casos: initState, dispose, cargarTarjetas, manejarError
* Alcanzar 85% de coverage en módulo Cards
* Mockear correctamente dependencias con Mockito

## Link de Historia del AzureBoards

[AB#64706](https://dev.azure.com/bacsansose/BAC/_workitems/edit/64706)

## Evidencias Visuales

### Test Coverage Report
![Coverage 85%](...)

### Tests Pasando
![All tests green](...)

> [!IMPORTANT]
> - Screenshot del coverage report mostrando 85%+ en CardsViewModel
> - Todos los tests pasan exitosamente
```

---

### Refactor (rf)

**Descripción debe incluir:**
- Qué se refactorizó
- Por qué se refactorizó
- Qué mejora aporta
- Confirmar que no hay cambio funcional

**Evidencias:**
- Comparación ANTES/DESPUÉS de estructura
- Screenshots de complejidad reducida
- Tests demostrando que funcionalidad no cambió

**Ejemplo:**
```markdown
## Descripción de este PR

* Extraer lógica de validación de formularios a clase reutilizable `FormValidator`
* Eliminar duplicación de código en 5 ViewModels diferentes
* Simplificar tests al centralizar validaciones
* NO hay cambio funcional, solo reorganización de código

## Link de Historia del AzureBoards

[AB#44197](https://dev.azure.com/bacsansose/BAC/_workitems/edit/44197)

## Link de ADR

Referencia [ADR-018: Centralización de validaciones](...)

## Evidencias Visuales

### ANTES - Código Duplicado
![Duplicación en 5 archivos](...)

### DESPUÉS - Clase Centralizada
![FormValidator reutilizable](...)

### Tests Pasando (Funcionalidad Intacta)
![All tests green](...)

> [!IMPORTANT]
> - Screenshots mostrando eliminación de duplicación
> - Todos los tests existentes siguen pasando
> - Se agregaron tests para FormValidator
```

---

### Change Request (cr)

**Descripción debe incluir:**
- Qué se cambió
- Por qué se solicitó el cambio
- Diferencia con comportamiento anterior

**Evidencias:**
- ANTES/DESPUÉS del cambio visual o funcional
- Referencia a diseño o especificación

**Ejemplo:**
```markdown
## Descripción de este PR

* Cambiar texto del botón de "Continuar" a "Guardar y Continuar"
* Ajustar spacing de 16px a 24px según Design System actualizado
* Modificar color del banner de solicitud de tarjeta según especificación

## Link de Historia del AzureBoards

[AB#63538](https://dev.azure.com/bacsansose/BAC/_workitems/edit/63538)

## Evidencias Visuales

### ANTES
![Botón "Continuar", spacing 16px](...)

### DESPUÉS
![Botón "Guardar y Continuar", spacing 24px](...)

> [!IMPORTANT]
> - Screenshot comparando ANTES/DESPUÉS del texto y spacing
> - Se valida que cumple con especificaciones de diseño
```

---

## 🚨 Elementos Críticos (IMPORTANT Blocks)

Usar bloques `> [!IMPORTANT]` para resaltar información crítica:

**Cuándo usar:**
- Destacar qué validar en las evidencias
- Mencionar casos edge importantes
- Alertar sobre cambios que requieren atención especial
- Recordar dependencias o configuraciones necesarias

**Formato:**
```markdown
> [!IMPORTANT]
> - Punto crítico 1
> - Punto crítico 2
> - Punto crítico 3
```

**Ejemplos:**

```markdown
> [!IMPORTANT]
> - Video mostrando que el flujo funciona con red lenta (throttling)
> - Se valida comportamiento cuando usuario cancela a mitad del proceso
> - Se verifica que no hay memory leaks al salir del flujo
```

```markdown
> [!IMPORTANT]
> - Este cambio requiere actualizar variable de ambiente `API_FAVORITES_URL`
> - Backend debe estar en versión 2.1.0 o superior
> - Cache debe limpiarse después del despliegue
```

---

## ✅ Checklist de Validación de PR

### Antes de Crear el PR:

- [ ] Descripción tiene bullets específicos (NO vagos)
- [ ] Link de AzureBoards usa formato `AB#XXXXX` correcto
- [ ] Link de AzureBoards tiene URL actualizada (no dice XXXXX)
- [ ] Sección ADR eliminada si no aplica
- [ ] Evidencias visuales incluidas (screenshots/videos)
- [ ] Para features: video ANTES/DESPUÉS del flujo completo
- [ ] Para fixes: evidencia del bug y evidencia del fix
- [ ] Para TT: coverage reports o logs relevantes
- [ ] Bloque IMPORTANT incluido con puntos de validación
- [ ] Título del PR coincide con commit principal
- [ ] Commits en squash si hay múltiples (automático con PR Assistant)

---

## ❌ Errores Comunes

### 1. Descripción Vaga

```markdown
❌ INCORRECTO
## Descripción de este PR

* Ajustes varios
* Cambios menores
* Fix de bugs

✅ CORRECTO
## Descripción de este PR

* Agregar validación null en `checkIfFormIsFilled()` para evitar crash
* Implementar pattern `context.mounted` antes de `setState()` en operaciones async
* Corregir timeout en llamado a endpoint de tarjetas (aumentar de 5s a 10s)
```

---

### 2. Link de AzureBoards Incorrecto

```markdown
❌ INCORRECTO
[BC#35367](...)  # Debe ser AB#, no BC#
[AB#XXXXX](...)  # Olvidaron reemplazar XXXXX
AB#35367         # No es un link

✅ CORRECTO
[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)
```

---

### 3. Sin Evidencias Visuales

```markdown
❌ INCORRECTO
## Evidencias Visuales

Ver en el código
No aplica
N/A

✅ CORRECTO
## Evidencias Visuales

### ANTES
![Pantalla sin validación](...)

### DESPUÉS
![Pantalla con validación funcionando](...)
```

---

### 4. Sección ADR Innecesaria

```markdown
❌ INCORRECTO
## Link de ADR

N/A
No aplica
<!-- comentario vacío -->

✅ CORRECTO
<!-- Eliminar toda la sección si no aplica -->
```

---

### 5. Falta Contexto en Evidencias

```markdown
❌ INCORRECTO
## Evidencias Visuales

![screenshot](...)

✅ CORRECTO
## Evidencias Visuales

### Pantalla de Login - ANTES
![Login sin validación biométrica](...)

### Pantalla de Login - DESPUÉS
![Login con opción de Face ID activa](...)

> [!IMPORTANT]
> - Video mostrando flujo completo de autenticación con Face ID
> - Se valida fallback a password cuando Face ID falla
```

---

## 📊 Estructura Completa de un PR Ejemplar

```markdown
## Descripción de este PR

* Implementar guardado de favoritos en flujo de pago de servicios
* Agregar pantalla de gestión de favoritos con listar/editar/eliminar
* Integrar con endpoints POST /api/v1/favorites y GET /api/v1/favorites
* Implementar validación de alias único y campos obligatorios
* Agregar confirmación modal antes de eliminar favorito
* Manejar errores de red con mensajes apropiados y retry

## Link de Historia del AzureBoards

[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)

## Evidencias Visuales

### ANTES - Sin Favoritos
![Pantalla de pago sin opción de favoritos](https://user-images.../before.png)

### DESPUÉS - Agregar Favorito
![Modal para agregar favorito con campos](https://user-images.../add-favorite.png)

### DESPUÉS - Lista de Favoritos
![Pantalla mostrando lista de favoritos guardados](https://user-images.../favorites-list.png)

### DESPUÉS - Editar/Eliminar
![Opciones de edición y confirmación de eliminación](https://user-images.../edit-delete.png)

### Caso Edge - Error de Red
![Mensaje de error cuando falla el guardado](https://user-images.../network-error.png)

### Video Completo
https://user-images.../demo-video.mp4

> [!IMPORTANT]
> - Video mostrando flujo completo: agregar → listar → editar → eliminar favorito
> - Se valida comportamiento cuando hay error de red (retry functionality)
> - Se verifica validación de alias duplicado con mensaje apropiado
> - Se confirma que modal de confirmación aparece antes de eliminar
> - Todos los tests unitarios y de integración pasan (coverage 92%)
```

---

## 💡 Tips para PRs de Calidad

### ✅ DO (Hacer)

1. **Descripción Clara:** Cada bullet debe responder "¿Qué cambió?"
2. **Links Funcionales:** Validar que los links abren correctamente
3. **Evidencias Completas:** ANTES/DESPUÉS para cambios visuales
4. **Casos Edge:** Mostrar manejo de errores y casos límite
5. **Contexto:** Agregar títulos descriptivos a cada evidencia
6. **Critical Points:** Usar bloque IMPORTANT para destacar validaciones clave

### ❌ DON'T (No Hacer)

1. **Descripciones Vagas:** "Cambios varios", "Ajustes", "Fix"
2. **Links Sin Actualizar:** Dejar XXXXX sin reemplazar
3. **Sin Evidencias:** Poner "Ver en el código" o "N/A"
4. **Screenshots Sin Contexto:** Imagen sin título ni explicación
5. **ADR Innecesario:** Dejar sección ADR con "N/A"

---

## 🎯 Relación con Commits

El **título del PR** debe ser similar al commit principal:

```bash
# Commit principal
[ft][BC-35367] Payments: Implementar guardado de favoritos

# Título del PR (automático desde commit)
[ft][BC-35367] Payments: Implementar guardado de favoritos

# Descripción del PR (manual, siguiendo plantilla)
## Descripción de este PR
* Implementar funcionalidad de guardar favoritos...
...
```

---

## 📚 Referencias

- **Pull Request Template:** `.github/pull_request_template.md`
- **Commit Conventions:** `../commit-conventions/SKILL.md`
- **Branch Naming:** `../branch-naming/SKILL.md`
- **AzureBoards:** https://dev.azure.com/bacsansose/BAC/
- **ADRs Repository:** https://github.com/BAC-Credomatic/bancadigital-docs-adrs

---

## 🔍 Revisión por Reviewers

### Checklist para Code Reviewers:

- [ ] Descripción es clara y específica
- [ ] Link de AzureBoards correcto y funcional
- [ ] Evidencias visuales presentes y relevantes
- [ ] Para features: video del flujo completo
- [ ] Para fixes: evidencia del bug y la corrección
- [ ] Bloque IMPORTANT con puntos de validación
- [ ] Commits siguen convenciones del proyecto
- [ ] Branch name sigue formato correcto

### Preguntas Clave:

1. ¿Está claro QUÉ se cambió?
2. ¿Está claro POR QUÉ se cambió?
3. ¿Las evidencias demuestran que funciona?
4. ¿Se cubrieron casos edge?
5. ¿El link de AzureBoards abre correctamente?

---

**Analizado de:** 4,500+ PRs  
**Última actualización:** Febrero 2026  
**Plantilla oficial:** `.github/pull_request_template.md`  
**Tasa de correcciones:** ~40% de PRs requieren mejoras en descripción
