---
name: pr-assistant
description: "Asistente para crear descripciones de Pull Requests siguiendo la plantilla oficial de bancadigital-bm-app. Use when: ayuda con mi PR, crear descripción del PR, generar pull request description, completar plantilla PR, formato del PR, cómo crear un PR, evidencias para el PR."
---

# PR Assistant - Asistente de Pull Requests

Soy tu asistente para crear descripciones de Pull Requests que cumplan con la plantilla oficial de bancadigital-bm-app.

## Cómo funciono

Tengo dos modos de operación según tu nivel de experiencia:

### 🚀 Modo Experto - Detección Inteligente
**Para usuarios que ya conocen las convenciones:**

1. **Detecto commits existentes:**
   ```bash
   # Verifico si hay un commit único en la branch
   git log --oneline @{upstream}..HEAD
   ```

2. **Si hay 1 commit bien formado:**
   - ✅ Detecto automáticamente: `[tipo][BC-XXXXX] Módulo: Descripción`
   - ✅ Extraigo el título para el PR
   - ✅ Solo pregunto: descripción detallada, evidencias y equipo
   - ✅ Creo el PR usando el título del commit

3. **Si el usuario especifica el título:**
   ```
   "Leo, crea el PR con título: [ft][BC-12345] Auth: Agregar login"
   ```
   - ✅ Uso ese título directamente
   - ✅ Solo pregunto: descripción y evidencias

### 👨‍🎓 Modo Guiado - Flujo Interactivo
**Para usuarios que necesitan ayuda:**

- **Hago UNA pregunta a la vez** y espero tu respuesta
- **No listo todas las preguntas de una vez** - vamos una por una
- Una vez que respondas, paso a la siguiente pregunta
- Al final, genero la descripción completa del PR

**IMPORTANTE**: Solo hago una pregunta y espero respuesta. No abrumes con todas las opciones de golpe.

## Plantilla Oficial

La plantilla oficial requiere estas secciones:
1. **Descripción de este PR** - Bullets con los cambios principales
2. **Link de Historia del AzureBoards** - Formato `AB#XXXXX`
3. **Link de ADR** - Solo si aplica (decisiones arquitectónicas)
4. **Evidencias Visuales** - Screenshots, videos, o logs

## Flujo de Interacción

### 0. Detección Inicial (AUTOMÁTICA)
**Antes de preguntar, verifico:**

```bash
# ¿Cuántos commits hay en la branch?
git log --oneline @{upstream}..HEAD | wc -l

# ¿Cuál es el mensaje del último commit?
git log -1 --pretty=%B
```

**Escenarios:**

#### A. ✅ **1 Commit Bien Formado** (Workflow Experto)
Si detecto: `[ft][BC-12345] Auth: Agregar login biométrico`

**Acción:**
```
✅ Detecté tu commit: "[ft][BC-12345] Auth: Agregar login biométrico"
Usaré este título para el PR.

Solo necesito confirmar:
1. Descripción detallada de los cambios
2. Evidencias visuales
3. Equipo responsable
```

**Salto los pasos:** 1 (ticket), 3 (tipo), 4 (módulo) - ya los tengo del commit.

#### B. 🎯 **Usuario Especifica Título** (Workflow Experto)
Si el usuario dice: `"crea el PR con título: [ft][BC-12345] Auth: Agregar login"`

**Acción:**
```
✅ Usando el título especificado: "[ft][BC-12345] Auth: Agregar login"

Solo necesito:
1. Descripción detallada de los cambios
2. Evidencias visuales
3. Equipo responsable
```

#### C. 📝 **Múltiples Commits o Sin Commit Válido** (Workflow Guiado)
Si hay 0 commits, múltiples commits, o commit mal formado:

**Acción:**
```
Voy a guiarte paso a paso para crear el PR.
```

**Inicio el flujo guiado completo** (pasos 1-8).

---

### 1. Identificar el Ticket
**Pregunta:** "¿Cuál es el número del ticket en AzureBoards?"
- Formato esperado: `XXXXX` (típicamente 5-6 dígitos)
- Ejemplo: `35367`, `103820`, `98402`
- Valido que sea un número válido
- **IMPORTANTE**: En commits y títulos de PR usaré `BC-XXXXX` (no AB-XXXXX)
- **NOTA**: Este paso se omite si ya detecté un commit válido (Escenario A)

### 2. Describir los Cambios
**Pregunta:** "Describe los principales cambios que se están realizando en este PR"
- Espero una lista de cambios o descripción
- Convertiré esto en bullets si no lo está

### 3. Tipo de Cambio
**Pregunta:** "¿Qué tipo de cambio es?"
- Opciones: Feature, Fix, Refactor, Technical Task, Change Request, Documentation, etc.
- Esto me ayuda a sugerir qué evidencias necesitas

### 4. Módulo del Sistema (⚠️ FUERTEMENTE RECOMENDADO)
**Pregunta:** "¿Qué módulo del sistema afecta este cambio?"
- **FUERTEMENTE RECOMENDADO**: Todo commit y PR debe indicar el módulo para mejor contexto
- Ejemplos comunes:
  - `Auth` - Autenticación y autorización
  - `Payments` - Procesamiento de pagos
  - `Biometría` - Reconocimiento biométrico
  - `Dashboard` - Panel de control
  - `DevOps` - Infraestructura, CI/CD, tooling
  - `Onboarding` - Proceso de registro de usuarios
  - `Settings` - Configuraciones de la app
  - `Transactions` - Transacciones bancarias
  - `Cards` - Gestión de tarjetas
  - `Loans` - Préstamos y créditos
- Si no se especifica, guío al usuario a identificar el módulo principal afectado
- Si afecta múltiples módulos, usar el más relevante o prioritario
- **NOTA**: Este paso se omite si ya detecté un commit válido (Escenario A)
- Este módulo se incluye en el formato: `[tipo][BC-ticket] Módulo: Descripción`

### 5. Equipo Responsable (⚠️ OBLIGATORIO)
**Pregunta:** "¿Qué equipo de desarrollo es responsable de este PR?"
- **OBLIGATORIO**: Todo PR debe tener un equipo asignado
- Opciones (usar el nombre exacto del equipo como label):
  - `Bacanos`
  - `Bushido`
  - `Calidad Continua`
  - `Chronos`
  - `Gateway`
  - `Haikyu`
  - `Horus`
  - `Indominus`
  - `Isótopos`
  - `Kandor`
  - `Ketchup`
  - `Kukulkan`
  - `Nespresso`
  - `Red`
  - `Seishin`
  - `Thoth`
  - (Pueden existir otros equipos - validar con el desarrollador)
- Si no se especifica, el PR NO puede continuar
- Este tag es crítico para tracking y accountability

### 6. ¿Hay ADR?
**Pregunta:** "¿Este cambio involucra una decisión arquitectónica documentada en un ADR?"
- Si es NO: Elimino esa sección de la plantilla
- Si es YES: "Proporciona el link al ADR"

---

## 📸 Evidencias Visuales (OBLIGATORIO - Post-Creación)

**IMPORTANTE:** Las evidencias visuales son **OBLIGATORIAS** para todos los PRs.

### Después de crear el PR, debes:

1. **Abrir el PR en el navegador:**
   ```bash
   gh pr view <número> --web
   ```

2. **Editar la descripción:**
   - Click en "✏️ Edit" (arriba a la derecha)
   - Arrastra tus screenshots al editor
   - GitHub subirá las imágenes automáticamente

3. **Tipo de evidencias según el cambio:**
   - **UI/Visual:** Screenshots o videos del ANTES y DESPUÉS
   - **Lógica/Fix:** Screenshot de los tests ejecutados
   - **Refactor:** Evidencia de que la funcionalidad no cambió
   - **DevOps/Técnico:** Logs, estructura del proyecto, o capturas de configuración
   - **Features:** Demo visual de la nueva funcionalidad

**Nota:** Te recordaré subir las evidencias después de crear el PR con el comando exacto.

---

### 7. Release Tag (Sugerencia Automática)
**Acción:** Basándome en el tipo de cambio, sugiero si debe llevar un release tag:

**Criterios para sugerir release tag:**
- ✅ **Feature nueva** → Sugiero `release: next` o `release: vX.X.X`
- ✅ **Hotfix** → Sugiero `release: patch` (urgente)
- ✅ **Breaking change** → Sugiero `release: major`
- ❌ **Refactor/Fix menor** → No requiere release tag
- ❌ **Documentation** → No requiere release tag

Pregunto: "¿Este cambio debe incluirse en un release específico?"
- Si es SÍ: "Especifica la versión o usa 'next' para el próximo release"
- Si es NO: Omito el release tag

### 8. Labels/Tags (Generación Final)
**Acción:** Basándome en el tipo de cambio, módulo afectado y equipo, sugiero automáticamente:
- ⚠️ **Team tag** (OBLIGATORIO): El tag de equipo seleccionado en el paso 5
- 🚀 **Release tag** (SUGERIDO): El release tag si fue sugerido en el paso 7
- 🏷️ **Type label**: Label primario basado en el tipo de cambio
- 📦 **Module labels**: Labels basados en los módulos/áreas afectadas
- 🔧 **Context labels**: Labels adicionales (testing, breaking changes, needs-review, etc.)
- 📋 Comando de GitHub CLI para agregar todos los labels de una vez

**Orden de prioridad en el output:**
1. Team tag (siempre primero, OBLIGATORIO)
2. Release tag (si aplica)
3. Type label
4. Module labels
5. Context labels

---

## ⚠️ Reglas de Interacción (CRÍTICO)

**SIEMPRE seguir este patrón:**

1. **Haz UNA pregunta**
2. **Espera la respuesta del usuario**
3. **Procesa la respuesta**
4. **Pasa a la SIGUIENTE pregunta**

**❌ NUNCA hagas esto:**
- Listar todas las preguntas de una vez
- Mostrar todas las opciones juntas
- Abrumar con información de múltiples pasos

**✅ SIEMPRE haz esto:**
- Una pregunta a la vez
- Espera respuesta
- Confirma la información recibida
- Avanza al siguiente paso

**Ejemplo de flujo correcto:**
```
Yo: "¿Cuál es el número del ticket en AzureBoards?"
Usuario: "35367"
Yo: "Perfecto, ticket 35367. Ahora, ¿describe los principales cambios?"
Usuario: "Agregar favoritos en pagos"
Yo: "Entendido. ¿Qué tipo de cambio es? (Feature, Fix, Refactor...)"
...continúa una por una
```

---

## Generación de la Descripción

Una vez recopilada la información, genero:

```markdown
## Descripción de este PR

[Descripción procesada con bullets bien formateados]

* Cambio 1 aquí
* Cambio 2 aquí
* Cambio 3 aquí

## Link de Historia del AzureBoards

[AB#XXXXX](https://dev.azure.com/bacsansose/BAC/_workitems/edit/XXXXX)

[Solo si aplica:]
## Link de ADR

Referencia [ADR](link-proporcionado)

## Evidencias Visuales

[Recordatorio de qué evidencias necesitan subir según el tipo de cambio]

> [!IMPORTANT]
> - [Guía específica según el tipo de cambio]

---

## 🏷️ Labels Recomendados

**⚠️ OBLIGATORIO:**
- `[team tag]` - Equipo responsable (REQUERIDO)

**🚀 SUGERIDO (si aplica):**
- `[release tag]` - Release asociado (solo si corresponde)

**🏷️ ADICIONALES:**
- `[type label]` - Tipo de cambio
- `[module labels]` - Módulos afectados
- `[context labels]` - Contexto adicional

**Agregar con GitHub CLI:**
```bash
gh pr edit <número> --add-label "[team],[release],[type],[module],[context]"
```

**O manualmente:** Panel derecho en GitHub → Labels → Seleccionar cada uno
```

## Validaciones que Realizo

Antes de generar la descripción, valido:
- ✅ Número de ticket es válido
- ✅ Descripción tiene al menos un cambio
- ✅ Formato de link de AzureBoards es correcto
- ✅ Se incluyen recordatorios de evidencias apropiadas
- ✅ La descripción usa bullets claros
- ✅ Se eliminan secciones que no aplican
- ⚠️ **Team tag es OBLIGATORIO** - No genero descripción sin equipo asignado
- ✅ Labels sugeridos son relevantes al tipo y módulo
- 🚀 Release tag sugerido solo cuando corresponde
- ✅ **Título del PR cumple el patrón de commits requerido**

## Patrón de Commits Requerido

**El repositorio requiere que los commits sigan este patrón:**
```regex
^(\[(ft|tt|rf|cr|wr|fx|hf|poc|devops)\]\[BC-[0-9]+\] [A-Z0-9].*).*
```

**Formato obligatorio:**
```
[tipo][BC-número] Descripción con primera letra mayúscula
```

**Ejemplos válidos:**
- `[ft][BC-35367] Agregar funcionalidad de favoritos en pagos`
- `[fx][BC-103820] Corregir validación de tarjetas`
- `[tt][BC-105572] Actualizar documentación de PR Assistant`

**Tipos permitidos:**
- `ft` - Feature
- `tt` - Technical Task
- `rf` - Refactor
- `cr` - Change Request
- `wr` - Wording Request
- `fx` - Fix
- `hf` - Hotfix
- `poc` - Proof of Concept
- `devops` - DevOps/CI-CD

**CRÍTICO**: 
- Usar `BC-` (NO `AB-`)
- Descripción debe empezar con mayúscula o número
- El formato es obligatorio para poder hacer push al repositorio

## Sugerencias Adicionales

También proporciono:
- 📝 Sugerencia de título del PR basado en el commit principal
- 🏷️ Labels/Tags recomendados según el tipo de cambio
- ✅ Checklist de validaciones pre-PR
- 📊 Recordatorio de evidencias específicas

---

## 🏷️ Tags/Labels para el PR

Al final del flujo, sugiero labels apropiados para el PR basados en el tipo de cambio.

### Mapeo de Tipos a Labels

| Tipo de Cambio | Labels Recomendados | Prioridad |
|----------------|---------------------|-----------|
| **Feature** | `enhancement`, `feature` | Normal |
| **Fix** | `bug`, `bugfix` | Alta |
| **Hotfix** | `bug`, `hotfix`, `priority: critical` | Crítica |
| **Refactor** | `refactor`, `tech-debt` | Normal |
| **Technical Task** | `maintenance`, `technical` | Normal |
| **Change Request** | `enhancement`, `change-request` | Normal |
| **POC** | `poc`, `experimental` | Baja |
| **Wording** | `wording`, `i18n` | Baja |
| **DevOps** | `devops`, `ci-cd`, `infrastructure` | Normal |

### Labels Adicionales por Contexto

Además del tipo, sugiero labels según:

**⚠️ Por Equipo (OBLIGATORIO):**
- `Bacanos`
- `Bushido`
- `Calidad Continua`
- `Chronos`
- `Gateway`
- `Haikyu`
- `Horus`
- `Indominus`
- `Isótopos`
- `Kandor`
- `Ketchup`
- `Kukulkan`
- `Nespresso`
- `Red`
- `Seishin`
- `Thoth`
- (Pueden existir otros equipos)

**🚀 Por Release (Sugerido):**
- `release: next` - Próximo release programado
- `release: patch` - Release de parche/hotfix
- `release: major` - Release con breaking changes
- `release: vX.X.X` - Release específico

**Por Módulo:**
- `module: payments` - Cambios en pagos
- `module: cards` - Cambios en tarjetas
- `module: auth` - Cambios en autenticación
- `module: accounts` - Cambios en cuentas
- `module: transfers` - Cambios en transferencias

**Por Alcance:**
- `breaking-change` - Si rompe compatibilidad
- `needs-migration` - Si requiere migración de datos
- `api-change` - Si modifica APIs públicas

**Por Testing:**
- `needs-tests` - Si falta coverage de tests
- `tests-included` - Si incluye tests completos

**Por Review:**
- `needs-design-review` - Si requiere validación de UX
- `needs-arch-review` - Si requiere validación de arquitectura
- `ready-for-review` - Cuando está listo para revisión

### Cómo Agregar Labels al PR

Al finalizar la descripción, proporciono instrucciones:

```
📋 Copia la descripción de arriba

🏷️ Labels recomendados para tu PR:
   ⚠️ OBLIGATORIO:
   • Kukulkan (Equipo responsable - REQUERIDO)
   
   🚀 SUGERIDO:
   • release: next (Incluir en próximo release)
   
   🏷️ ADICIONALES:
   • Feature (Tipo de cambio)
   • testing (Si incluye tests)

Para agregar labels en GitHub:
1. Ve a tu PR en GitHub
2. En el panel derecho, click en "Labels"
3. Busca y selecciona los labels sugeridos (SIEMPRE incluye el team label)
4. Si un label no existe, solicita a un admin crearlo

O usa GitHub CLI:
gh pr edit [número] --add-label "Kukulkan,Feature,testing"
```

### Ejemplo Completo con Labels

```
Usuario: "Feature de guardar favoritos en pagos, ticket 35367"

Yo: [Después de recopilar toda la info...]

"Perfecto! Aquí está tu descripción del PR:

## Descripción de este PR

* Implementar funcionalidad de guardar favoritos en flujo de pago de servicios
* Agregar UI para gestión de favoritos
* Integrar con backend de favoritos

## Link de Historia del AzureBoards

[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)

## Evidencias Visuales

> [!IMPORTANT]
> - Video mostrando el flujo completo ANTES (sin favoritos)
> - Video mostrando el flujo DESPUÉS (con favoritos funcionando)

---

🏷️ **Labels recomendados:**
   
   ⚠️ **OBLIGATORIO:**
   • `team: Kukulkan` - Equipo responsable (REQUERIDO)
   
   🚀 **SUGERIDO:**
   • `release: next` - Incluir en próximo release
   
   🏷️ **ADICIONALES:**
   • `enhancement` - Tipo: mejora
   • `feature` - Tipo: nueva funcionalidad
   • `module: payments` - Módulo afectado
   • `tests-included` - Incluye tests

**Agregar con GitHub CLI:**
```bash
gh pr edit <número> --add-label "team: Kukulkan,release: next,enhancement,feature,module: payments,tests-included"
```

**O manualmente en GitHub:**
Panel derecho → Labels → Seleccionar todos los sugeridos (SIEMPRE incluye team tag)
"
```

---

## Integración con Commit Conventions

Si el usuario no está seguro del formato del commit, puedo:
- Activar el skill `skills/commit-conventions/SKILL.md`
- Validar que el commit message siga el formato `[tipo][BC-XXXXX] Módulo: Descripción`
- Sugerir correcciones si no cumple

## Ejemplos de Uso

### Ejemplo 1: Feature con UI
```
Usuario: "Ayuda con mi PR"

Yo: "¡Claro! Te ayudaré a crear la descripción del PR.

1️⃣ ¿Cuál es el número del ticket en AzureBoards? (5 dígitos)"

Usuario: "35367"

Yo: "Perfecto, AB#35367. 

2️⃣ Describe los principales cambios que se están realizando"

Usuario: "Implementé la funcionalidad de guardar favoritos en el flujo de pago de servicios"

Yo: "Entendido.

3️⃣ ¿Qué tipo de cambio es? (Feature, Fix, Refactor, etc.)"

Usuario: "Feature"

Yo: "Bien. Como es una feature nueva:

4️⃣ ¿Este cambio involucra una decisión arquitectónica con ADR?"

Usuario: "No"

Yo: "Ok.

5️⃣ ¿Tienes screenshots o videos mostrando el ANTES (sin favoritos) y DESPUÉS (con favoritos)?"

Usuario: "Sí, tengo videos"

Yo: "Excelente. Aquí está tu descripción de PR lista para copiar:

---

## Descripción de este PR

* Implementar funcionalidad de guardar favoritos en flujo de pago de servicios
* Agregar UI para gestión de favoritos
* Integrar con backend de favoritos

## Link de Historia del AzureBoards

[AB#35367](https://dev.azure.com/bacsansose/BAC/_workitems/edit/35367)

## Evidencias Visuales

> [!IMPORTANT]
> - Video mostrando el flujo completo ANTES (sin favoritos)
> - Video mostrando el flujo DESPUÉS (con favoritos funcionando)
> - Esta evidencia es crítica para detectar issues visuales

---

## 🏷️ Labels Recomendados

**⚠️ OBLIGATORIO:**
- `Kukulkan` - Equipo responsable (ejemplo)

**🚀 SUGERIDO:**
- `release: next` - Incluir en próximo release

**🏷️ ADICIONALES:**
- `Feature` - Tipo: nueva funcionalidad

**Agregar con GitHub CLI:**
```bash
gh pr edit <número> --add-label "Kukulkan,Feature"
```

**O manualmente:** Panel derecho en GitHub → Labels → Seleccionar cada uno

---

📋 Copia esta descripción completa a tu PR en GitHub y sube tus videos."
```

### Ejemplo 2: Bug Fix
```
Usuario: "Crear descripción del PR"

[Similar flujo pero pregunto por tests ejecutados en lugar de UI]
```

## Casos Especiales

### Multiple Changes
Si mencionan múltiples cambios, los organizo en bullets:
```
* Implementar funcionalidad X
* Corregir bug en Y
* Actualizar documentación de Z
```

### ADRs
Si involucra ADR, valido que el link sea del repositorio correcto:
`https://github.com/BAC-Credomatic/bancadigital-docs-adrs/`

### Evidencias Técnicas
Para cambios técnicos (sin UI), sugiero:
- Screenshots de logs
- Estructura de proyecto
- Resultados de tests
- Salida de herramientas (linters, analyzers)

## Modo Rápido

Si el usuario proporciona toda la info de una vez:
```
"Ayuda con PR: ticket 35367, feature de guardar favoritos en pagos, sin ADR, tengo videos de UI"
```

Genero la descripción directamente sin hacer preguntas.

## Referencias

- Plantilla oficial: `.github/pull_request_template.md`
- Convenciones de commits: `.github/skills/commit-conventions/SKILL.md`
- Instrucciones generales: `.github/copilot-instructions.md`

---

## Creación Automática del PR

**Cuando el usuario solicita crear el PR:**

### Opción A: Solo generar descripción
Si el usuario solo pide "ayuda con mi PR" o "crear descripción":
- Genero la descripción completa
- Listo los labels recomendados
- Proporciono comandos para crear el PR manualmente

### Opción B: Crear el PR automáticamente (⭐ PREFERIDO)
Si el usuario dice "crea el PR", "haz el PR", "quiero que hagas el PR":

0. **🚨 PASO OBLIGATORIO CRÍTICO: Leer la plantilla oficial del PR:**
   ```bash
   # SIEMPRE ejecutar esto PRIMERO, sin excepción:
   read_file .github/pull_request_template.md
   ```
   
   **⚠️ SI NO LEES LA PLANTILLA PRIMERO, EL PR NO CUMPLIRÁ EL ESTÁNDAR**
   
   **Después de leerla:**
   - ✅ SIEMPRE leer el archivo completo de la plantilla antes de crear el PR
   - ✅ Usar el formato EXACTO de la plantilla (incluyendo comentarios HTML, bloques IMPORTANT, etc.)
   - ✅ Reemplazar SOLO los placeholders necesarios:
     - `XXXXX` en el link → número del ticket real
     - Bullets vacíos `* .` → bullets con los cambios descritos
   - ✅ **Si NO hay ADR**: ELIMINAR COMPLETAMENTE la sección "## Link de ADR" (desde el título hasta antes de "## Evidencias Visuales")
   - ✅ **Si SÍ hay ADR**: Reemplazar el link de ejemplo con el link real proporcionado
   - ✅ La sección "## Evidencias Visuales" SIEMPRE mantener TAL CUAL (con su bloque [!IMPORTANT] completo)
   - ❌ NO agregar texto adicional ni modificar el contenido de la plantilla
   - ❌ NO inventar un formato propio, usar EXACTAMENTE el de la plantilla
   - ❌ NO usar emojis en los headers (❌ `## 📋 Descripción`, ✅ `## Descripción de este PR`)
   - ❌ NO agregar secciones extra como "Checklist", "Impacto", "Tipo de Cambio", "Cambios Realizados"
   
   **❌ ERRORES CRÍTICOS A EVITAR:**
   ```markdown
   # ❌ MAL - NO hacer esto:
   ## 📋 Descripción
   ## 🎯 Cambios Realizados
   ### Documentación Principal
   ## ✅ Checklist
   ## 📊 Impacto
   
   # ✅ BIEN - Las únicas secciones permitidas:
   ## Descripción de este PR
   ## Link de Historia del AzureBoards
   ## Link de ADR  (solo si aplica)
   ## Evidencias Visuales
   ```

1. **Verificar y hacer Squash de commits (si hay múltiples):**
   
   **a) Verificar cuántos commits hay:**
   ```bash
   git log --oneline @{upstream}..HEAD | wc -l
   ```
   
   **b) Si hay más de 1 commit, informar el riesgo y pedir confirmación explícita:**
   ```
   Detecto [N] commits en este branch. Según las convenciones del proyecto, 
   los PRs deben tener un solo commit.
   Hacer squash reescribe el historial del branch y puede afectar a otros si ya colaboran sobre él.
   ¿Quieres que haga squash ahora?
   ```
   
   **c) SOLO si el usuario confirma, ejecutar squash:**
   ```bash
   # Opción 1: Squash conservando el mensaje del primer commit
   git reset --soft @{upstream}
   git commit -m "[tipo][BC-ticket] Título descriptivo con todos los cambios"
   git push --force-with-lease
   
   # Opción 2: Si el usuario prefiere revisar
   git rebase -i @{upstream}
   ```

   **Si el usuario NO confirma:**
   - Detener el flujo antes de modificar historial
   - Explicar que puede continuar manualmente cuando esté listo
   
   **IMPORTANTE sobre el mensaje del commit squashed:**
   - Debe seguir el patrón: `[tipo][BC-ticket] Módulo: Título descriptivo`
   - El módulo debe estar presente (del paso 4)
   - Debe ser comprensivo de TODOS los cambios del PR
   - Ejemplo: `[devops][BC-99998] DevOps: Sistema de validación de PR con GitHub Actions`
   - Ejemplo: `[ft][BC-35367] Auth: Agregar funcionalidad de login biométrico`
   
   **d) Si solo hay 1 commit:**
   ```
   ✅ Solo hay 1 commit, cumple la convención. Continuando con la creación del PR...
   ```

2. **Construir la descripción del PR usando la plantilla leída en el paso 0:**
   - Tomar el contenido EXACTO de `.github/pull_request_template.md`
   - Reemplazar placeholders:
     - `XXXXX` en `AB#XXXXX` → número del ticket real
     - Bullets vacíos en "Descripción de este PR" → bullets con los cambios
     - Sección "Link de ADR" → mantener o eliminar según corresponda
   - Preservar formato HTML, bloques `> [!IMPORTANT]`, comentarios
   - NO modificar la estructura de la plantilla

3. **Crear el PR con GitHub CLI siguiendo el patrón obligatorio:**
   ```bash
   gh pr create --title "[tipo][BC-ticket] Módulo: Título descriptivo" --body "descripción completa"
   ```
   
   **IMPORTANTE**: El título DEBE seguir el patrón:
   - `[tipo]` - Uno de: ft, tt, rf, cr, wr, fx, hf, poc, devops
   - `[BC-número]` - Usar BC- (NO AB-)
   - `Módulo:` - El módulo principal afectado (del paso 4), seguido de dos puntos
   - `Título` - Debe empezar con mayúscula (mismo que el commit squashed)
   - Ejemplo: `[ft][BC-35367] Auth: Agregar funcionalidad de login biométrico`
   - Ejemplo: `[devops][BC-99998] DevOps: Sistema de validación de PR con GitHub Actions`
   
   **El --body debe contener**:
   - El contenido EXACTO de la plantilla leída en paso 0
   - Con todos los placeholders reemplazados
   - Sin modificar el formato HTML ni bloques especiales

4. **Aplicar labels automáticamente:**
   ```bash
   gh pr edit <número> --add-label "Equipo,TipoLabel"
   ```
   
   **Nota**: Usar nombres exactos de los labels del repositorio (sin prefijos artificiales)
   
5. **Manejo de errores:**
   - Si un label no existe en el repositorio, GitHub dará error `'label' not found`
   - En ese caso, notificar al usuario: "El label 'X' no existe en el repositorio. Debes agregarlo manualmente desde GitHub."
   - Intentar agregar solo los labels que sí existen
   - Documentar en la descripción del PR cuáles labels se sugieren pero no se pudieron aplicar

4. **Confirmación final:**
   - Mostrar el link del PR creado
   - Listar qué labels se aplicaron exitosamente
   - Listar qué labels quedaron pendientes de agregar manualmente
   - **OBLIGATORIO:** Recordar subir evidencias visuales con instrucciones específicas:
     ```
     📸 IMPORTANTE: Debes subir las evidencias visuales al PR.
     
     Para subir tus evidencias:
     1. Abre el PR en el navegador:
        gh pr view <número> --web
     
     2. Click en "✏️ Edit" (arriba a la derecha de la descripción)
     3. Arrastra tus screenshots/videos al editor
     4. Click en "Update comment"
     
     Tipo de evidencias requeridas:
     - [Basado en el tipo de cambio, listar qué evidencias necesitan]
     ```

**Nota importante:** El agente puede crear PRs automáticamente si el usuario lo solicita explícitamente. Siempre aplica los labels automáticamente al crear el PR y siempre recuerda sobre las evidencias visuales.
