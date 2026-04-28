# 🤖 Sistema de Agentes y Skills de GitHub Copilot

Este directorio contiene la configuración de agentes inteligentes y skills especializados para asistir en el desarrollo de **bancadigital-bm-app**.

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────┐
│  👥 Usuario                             │
│  "Leo, ayuda", "Leo revisar código"     │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  👑 Leo (Orquestador)                   │
│  - Detecta qué necesitas                │
│  - Decide: delegar o responder          │
└─────┬───────────────────────┬───────────┘
      │                       │
      ▼                       ▼
┌─────────────┐         ┌──────────────────┐
│ 🤖 Agentes  │         │ 📚 Skills        │
│ Especializ. │         │ (Conocimiento)   │
├─────────────┤         ├──────────────────┤
│ PR Asst.    │         │ Commits          │
│ PR Reviewer │         │ Branches         │
│ Commit Asst.│         │ PR Description   │
│ Leo (Hub)   │         │ Testing          │
│             │         │ Modules          │
└─────────────┘         │ Lifecycle        │
                        │ Design System    │
                        │ Security         │
                        └──────────────────┘
```

### Principio de Diseño

**Un solo punto de entrada → Delegación inteligente → Conocimiento especializado**

---

## 📁 Archivos del Sistema

### 🎯 Orquestador
- **`agents/leo.agent.md`** - Agente principal (tu punto de entrada)
  - Nombre: Leo
  - Identificador único: Siempre inicia con "👨‍💻 Leo - Asistente Banca Digital"
  - Invocación: "Leo, ayuda" o "Leo crea el commit"
  - Detecta qué necesitas
  - Consulta skills o delega a especialistas
  - Responde consultas generales

### 🤖 Agentes Especializados
- **`agents/commit-assistant.agent.md`** - Experto en crear commits
  - Validación rápida para expertos: `"Leo, valida mi commit: [mensaje]"`
  - Flujo guiado para principiantes
  - Genera commits con formato correcto
  - Verifica formato `[tipo][BC-XXXXX] Módulo: Descripción`
  
- **`agents/pr-assistant.agent.md`** - Experto en crear Pull Requests
  - Detección inteligente de commits existentes
  - Modo experto: usa título del commit automáticamente
  - Flujo interactivo guiado para principiantes
  - Valida plantilla oficial
  - Genera descripciones completas
  
- **`agents/pr-reviewer.agent.md`** - Experto en revisar Pull Requests
  - Valida compliance con todas las reglas
  - Revisa arquitectura, testing, code quality
  - Genera reportes detallados con bloqueadores/warnings
  - Consulta todos los skills y documentación oficial

### 📚 Skills (Base de Conocimiento)
- **`skills/commit-conventions/SKILL.md`** - Todo sobre commits
  - 50+ ejemplos reales del proyecto
  - 9 tipos de commit documentados (ft, fx, tt, rf, cr, wr, hf, poc, devops)
  - Errores comunes y correcciones

- **`skills/code-review/SKILL.md`**
  - Patrones de initState, dispose
  - context.mounted, autoDispose
  - Memory leaks y cómo evitarlos

- **`skills/design-system-patterns/SKILL.md`**
  - GoRouter vs Navigator
  - Spacing del Design System
  - Componentes homologados

### 📋 Otros Archivos
- **`copilot-instructions.md`** - Instrucciones generales del proyecto
- **`pull_request_template.md`** - Plantilla oficial de PRs
- **`CODEOWNERS`** - Aprobadores por área del código

---

## 🎯 Cómo Usar el Sistema

> **💡 Identificación:** Cuando Leo responda, siempre iniciará con "👨‍💻 Leo - Asistente Banca Digital" para que sepas que estás hablando con el orquestador principal.

### Opción 1: Pregunta General (Recomendado)

Simplemente pregunta a Copilot invocando a Leo:

```
"Leo, ayuda"
"Leo, cómo formateo commits?"
"Leo, revisar mi código"
"Leo, qué tipo de commit usar?"
```

**Leo** detectará qué necesitas y:
- Consultará el skill apropiado
- Te dará respuesta directa con ejemplos
- O te delegará a un especialista si es necesario

### Opción 2: Invocar Agente Específico

Para flujos complejos, invoca directamente:

```
"Leo, ayuda con mi PR"          → Activa PR Assistant (crear PR)
"Leo, crear descripción del PR" → Activa PR Assistant
"Leo, revisa mi PR"             → Activa PR Reviewer (revisar PR)
"Leo, valida este PR"           → Activa PR Reviewer
```

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Consulta Simple de Commits

```
👤 Usuario: "Leo, qué tipo de commit usar para un bug fix?"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

Para bug fixes usa [fx].

📝 Formato: [fx][BC-XXXXX] Módulo: Descripción específica

Ejemplo real del proyecto:
✅ [fx][BC-103820] Tarjetas: Agregar validación null en checkIfFormIsFilled()

Recuerda:
- Describe QUÉ cambió (el fix)
- NO describas qué bug había
- Incluye el módulo afectado

¿Necesitas validar tu commit message?"
```

**¿Qué pasó?**
- Leo detectó "commit" y "tipo"
- Consultó `skills/commit-conventions/SKILL.md`
- Respondió con ejemplo del proyecto

---

### Ejemplo 2: Workflow Completo - Experto (Commit + PR)

**Flujo rápido para desarrolladores que conocen las convenciones:**

```
👤 Usuario: "Leo, valida mi commit: [ft][BC-12345] Auth: Agregar login biométrico"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

✅ Commit válido! 
- Tipo: [ft] ✓
- Ticket: [BC-12345] ✓
- Módulo: Auth ✓
- Descripción: Clara y específica ✓

Puedes hacer el commit:
git commit -m "[ft][BC-12345] Auth: Agregar login biométrico"

💡 Tip: Para más cambios usa:
git commit --amend --no-edit
Si ese commit ya fue publicado, primero confirma que quieres reescribir el historial y luego usa:
git push --force-with-lease"

───── Después de trabajar y hacer amend ─────

👤 Usuario: "Leo, crea el PR"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

✅ Detecté tu commit: "[ft][BC-12345] Auth: Agregar login biométrico"
Usaré este título para el PR.

Solo necesito:
1. ¿Descripción detallada de los cambios?
2. ¿Tienes evidencias visuales?
3. ¿Qué equipo es responsable?"

👤 Usuario: "Implementa login con Face ID y Touch ID. 
Screenshots listos. Equipo Seishin"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

✅ PR creado: #5125
🔗 https://github.com/BAC-Credomatic/bancadigital-bm-app/pull/5125

Labels aplicados:
✅ Seishin
✅ enhancement

Recuerda subir tus screenshots a la descripción del PR."
```

---

### Ejemplo 3: Workflow Completo - Principiante (Commit + PR Guiado)

**Flujo paso a paso con ayuda en cada etapa:**

```
👤 Usuario: "Leo, ayuda con el commit"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

Te guiaré para crear el commit. 

Pregunta 1/4: ¿Cuál es el número del ticket en AzureBoards?
(Ejemplo: 35367, 103820)"

👤 Usuario: "12345"

🤖 Leo: "✅ Ticket: BC-12345

Pregunta 2/4: ¿Qué tipo de cambio es?
- ft - Nueva funcionalidad
- fx - Corrección de bug  
- tt - Tarea técnica (config, tests)
- rf - Refactor
- cr - Change Request
- hf - Hotfix urgente
- poc - Prueba de concepto
- devops - CI/CD, infraestructura"

👤 Usuario: "ft"

🤖 Leo: "✅ Tipo: Feature

Pregunta 3/4: ¿Qué módulo del sistema afecta?
(Ejemplos: Auth, Payments, Cards, Dashboard, etc.)"

👤 Usuario: "Auth"

🤖 Leo: "✅ Módulo: Auth

Pregunta 4/4: Describe QUÉ cambió en este commit
(No describas el bug, sino la solución)"

👤 Usuario: "Agregar login biométrico con Face ID y Touch ID"

🤖 Leo: "✅ Commit generado:

git commit -m '[ft][BC-12345] Auth: Agregar login biométrico con Face ID y Touch ID'

¿Ejecuto este comando?"

👤 Usuario: "sí"

🤖 Leo: "✅ Commit creado exitosamente!

💡 Tip: Si haces más cambios, usa:
git commit --amend --no-edit

Cuando estés listo para hacer el PR, dime 'Leo, crea el PR'"

───── Después de trabajar y hacer amend ─────

👤 Usuario: "Leo, crea el PR"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

✅ Detecté tu commit: "[ft][BC-12345] Auth: Agregar login biométrico..."
Usaré este título para el PR.

Ahora necesito más detalles...
(continúa con flujo de PR Assistant)"
```

---

### Ejemplo 4: Code Review de Lifecycle

```
👤 Usuario: "Leo, revisar este código:

Future<void> save() async {
  await repository.save();
  setState(() => isSaved = true);
}"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

⚠️ Problema detectado: Falta validación context.mounted

Tu código:
❌ INCORRECTO
Future<void> save() async {
  await repository.save();
  setState(() => isSaved = true); // 🚨 PELIGRO
}

✅ CORRECTO
Future<void> save() async {
  await repository.save();
  if (!mounted) return; // ✅ VALIDAR PRIMERO
  setState(() => isSaved = true);
}

Razón: El widget puede estar disposed después del await.

¿Quieres que revise otros aspectos del código?"
```

**¿Qué pasó?**
- Leo analizó el código
- Usó conocimiento de `copilot-instructions.md`
- Detectó patrón peligroso de lifecycle
- Explicó el problema y la solución

---

### Ejemplo 3: Revisar un Pull Request (Delegación a Especialista)

```
👤 Usuario: "Leo, revisa mi PR"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

Perfecto, te paso con PR Reviewer para hacer 
    una revisión exhaustiva siguiendo todas las 
    reglas del proyecto.
    
    @pr-reviewer: Revisa el PR"

───────────────────────────────────────

🤖 PR Reviewer: "🔍 Iniciando revisión del PR...

¿Quieres un review completo automático o 
prefieres que te haga preguntas sobre áreas 
específicas?

1️⃣ Review completo (recomendado)
2️⃣ Review de área específica (testing, arquitectura, etc.)"

👤 Usuario: "1"

🤖 PR Reviewer: "📊 Review completado. Encontré:
- ✅ 5 aprobaciones automáticas
- ⚠️ 2 advertencias
- ❌ 1 bloqueador

## ✅ Aprobaciones Automáticas

✅ Commits: Formato correcto (3/3 commits)
✅ Branch: Nombre válido ft/35367_payments_favorites
✅ Tests: Coverage 87% (supera 80% requerido)
✅ Arquitectura: Clean Architecture respetada

## ❌ Bloqueadores (Debe Arreglarse)

❌ **Lifecycle:**
   - `payment_view.dart:145` - `setState()` después de `await` sin validar `mounted`
   - Riesgo: Crash si widget está disposed
   - Corrección:
     ```dart
     if (!mounted) return;
     setState(() => ...);
     ```

**Recomendación Final:** 🔴 Cambios Requeridos

Arreglar el bloqueador antes de aprobar."
```

**¿Qué pasó?**
- Leo detectó "revisar PR"
- Delegó a PR Reviewer (especialista)
- PR Reviewer hizo análisis exhaustivo
- Generó reporte con aprobaciones, warnings y bloqueadores
- Identificó problema crítico en lifecycle
- Proporcionó corrección específica

---

### Ejemplo 4: Crear un Pull Request (Flujo Guiado)

```
👤 Usuario: "Leo, ayuda con mi PR"

🤖 Leo: "👨‍💻 Leo - Asistente Banca Digital

Perfecto, te paso con PR Assistant para crear 
    la descripción del PR siguiendo la plantilla oficial.
    
    @pr-assistant: Ayuda a crear la descripción"

───────────────────────────────────────

🤖 PR Assistant: "¡Claro! Te ayudaré a crear la descripción del PR.

1️⃣ ¿Cuál es el número del ticket en AzureBoards? (5 dígitos)"

👤 Usuario: "35367"

🤖 PR Assistant: "Perfecto, AB#35367.

2️⃣ Describe los principales cambios que se están realizando"

👤 Usuario: "Implementé guardar favoritos en pagos"

🤖 PR Assistant: "Entendido.

3️⃣ ¿Qué tipo de cambio es? (Feature, Fix, Refactor, etc.)"

👤 Usuario: "Feature"

🤖 PR Assistant: "Bien. Como es una feature nueva:

4️⃣ ¿Este cambio involucra una decisión arquitectónica con ADR?"

👤 Usuario: "No"

🤖 PR Assistant: "Ok.

5️⃣ ¿Tienes screenshots o videos mostrando el ANTES y DESPUÉS?"

👤 Usuario: "Sí, tengo videos"

🤖 PR Assistant: "Excelente. Aquí está tu descripción de PR:

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

Copia esta descripción a tu PR en GitHub y sube tus videos."
```

**¿Qué pasó?**
- Leo detectó "ayuda con mi PR"
- Delegó a PR Assistant (especialista)
- PR Assistant hizo preguntas secuenciales
- Generó descripción siguiendo plantilla oficial
- Validó formato de AzureBoards
- Recordó evidencias necesarias

---

## 🎨 Flujos del Sistema

### Flujo 1: Consulta Simple → Respuesta Directa

```
Usuario pregunta algo simple
        ↓
Leo consulta skill apropiado
        ↓
Responde con ejemplo del proyecto
        ↓
[FIN]
```

**Casos:**
- Formato de commits
- Validaciones rápidas
- Preguntas de sintaxis
- Conceptos de lifecycle
- Uso del Design System

### Flujo 2: Tarea Compleja → Delegación a Especialista

```
Usuario necesita ayuda compleja
        ↓
Leo detecta complejidad
        ↓
Delega a agente especializado
        ↓
Especialista ejecuta flujo guiado
        ↓
[FIN con resultado completo]
```

**Casos:**
- Crear descripción de PR
- Generar múltiples commits
- Configurar tests complejos
- Refactors arquitectónicos

### Flujo 3: Code Review → Análisis con Múltiples Skills

```
Usuario comparte código
        ↓
Leo analiza
        ↓
Consulta múltiples skills:
  - Lifecycle patterns
  - Design System rules
  - Security guidelines
  - Testing requirements
        ↓
Responde con análisis detallado
        ↓
[FIN]
```

**Casos:**
- Revisar ViewModels
- Validar widgets
- Chequear integraciones
- Verificar seguridad

---

## 🚀 Ventajas de Esta Arquitectura

### ✅ Para Desarrolladores

1. **Un solo punto de entrada** - Solo di "Leo, ayuda"
2. **Respuestas contextuales** - Basadas en el proyecto real
3. **Ejemplos del proyecto** - No genéricos, de bancadigital-bm-app
4. **Flujos guiados** - Para tareas complejas como PRs
5. **Validación automática** - Detecta errores comunes

### ✅ Para el Proyecto

1. **Consistencia** - Todos siguen las mismas convenciones
2. **Calidad** - Previene errores comunes documentados
3. **Velocidad** - Respuestas inmediatas sin buscar docs
4. **Escalabilidad** - Fácil agregar nuevos agentes/skills
5. **Mantenibilidad** - Conocimiento centralizado

### ✅ Para Arquitectura de Software

1. **Separación de responsabilidades** - Cada agente/skill tiene un propósito
2. **Reutilización** - Skills compartidos entre agentes
3. **Extensibilidad** - Agregar especialistas sin modificar existentes
4. **Composición** - Orquestador combina capacidades
5. **Single Source of Truth** - Skills son la fuente única de conocimiento

---

## 📊 Estado Actual del Sistema

### ✅ Implementado

| Componente | Estado | Descripción |
|------------|--------|-------------|
| Leo (Orquestador) | ✅ Completo | Agente principal |
| PR Assistant | ✅ Completo | Especialista en crear PRs |
| PR Reviewer | ✅ Completo | Especialista en revisar PRs |
| **GitHub Actions Automation** | ✅ Completo | Validación automática de PRs |
| Commit Conventions Skill | ✅ Completo | 50+ ejemplos reales |
| Branch Naming Skill | ✅ Completo | Convenciones y ejemplos |
| PR Description Skill | ✅ Completo | Plantilla oficial |
| Testing Skill | ✅ Completo | Mockito, Riverpod, coverage |
| Module Creation Skill | ✅ Completo | Clean Architecture + MVVM |
| Copilot Instructions | ✅ Completo | Reglas generales |
| PR Template | ✅ Completo | Plantilla oficial |

### 🔄 En Desarrollo

| Componente | Estado | Prioridad |
|------------|--------|-----------|
| Flutter Lifecycle Skill | 📝 Planificado | Alta |
| Design System Skill | 📝 Planificado | Alta |
| Security Guidelines Skill | 📝 Planificado | Media |

---

## ⚡ Automatización con GitHub Actions

### 🤖 PR Reviewer Automático

Además del agent manual que puedes invocar en VS Code, ahora tenemos **validación automática** cada vez que se crea o actualiza un PR.

#### ¿Cómo Funciona?

**Workflow**: `.github/workflows/pr-reviewer-automation.yml`

Se activa automáticamente en:
- ✅ PR nuevo abierto
- ✅ PR actualizado con nuevos commits  
- ✅ Descripción del PR editada

**Validaciones Automáticas:**
1. 📝 **Commits**: Formato, tipo correcto, ticket ID, módulo
2. 🌿 **Branch name**: Convenciones tipo/numero_descripcion
3. 📄 **PR Description**: Plantilla completa, Azure Boards link
4. 📂 **Archivos**: Tests agregados, archivos sensibles

**Resultado**: Comentario automático en el PR con:
- 🚫 **Bloqueadores** (debe corregirse, workflow falla)
- ⚠️ **Advertencias** (se recomienda corregir)
- ✅ **Aprobaciones** (todo correcto)

#### Ejemplo de Comentario Automático

```markdown
# 🤖 PR Reviewer - Validación Automática - Leo

**Estado:** ⚠️ **CON ADVERTENCIAS**
**PR:** #5052
**Branch:** `feature/35367_agregar_boton_favoritos`

---

## ⚠️ Advertencias (2)

⚠️ **FALTA AGREGAR TESTS**
   - Se modificaron 5 archivos .dart
   - No se encontraron tests (_test.dart)

⚠️ **DIMINUTIVO DETECTADO:** `btn` en commit
   - Evita diminutivos, usa palabras completas

---

## ✅ Validaciones Aprobadas (8)

✅ Commit válido: [ft][BC-35367] Cards: Agregar botón...
✅ Branch name válido: feature/35367_agregar_boton_favoritos
✅ PR tiene todas las secciones requeridas
...

---

*🤖 Generado automáticamente por PR Reviewer v1.0*
```

#### Automatización vs Manual

| Aspecto | 🤖 Automático (GitHub Actions) | 🧠 Manual (Copilot Agent) |
|---------|-------------------------------|---------------------------|
| **Timing** | ⚡ Inmediato (1-2 min) | 🧠 Bajo demanda |
| **Commits** | ✅ Formato y estructura | ✅ Cohesión y atomicidad |
| **Branch** | ✅ Nomenclatura | ✅ Estrategia de versionado |
| **PR Desc** | ✅ Plantilla completa | ✅ Claridad y contexto |
| **Arquitectura** | ⚠️ Dependencias y capas base | ✅ Clean Arch + MVVM |
| **Testing** | ✅ Presencia | ✅ Calidad y coverage |
| **Code Quality** | ⚠️ Lifecycle y navegación crítica | ✅ Anti-patterns, leaks |
| **Performance** | ❌ No valida | ✅ Optimizaciones |

**💡 Recomendación:** Usa ambos
1. **Automático** - Corrige errores básicos rápido
2. **Manual** (`Leo, revisa mi PR`) - Review profundo antes de solicitar aprobación

#### Documentación Completa

Ver [workflows/README.md](workflows/README.md) para:
- Configuración detallada
- Personalizar validaciones
- Troubleshooting
- Desactivar temporalmente

---

## 🛠️ Agregar Nuevos Componentes

### Agregar un Nuevo Skill

1. Crear archivo: `skills/nuevo-tema/SKILL.md`
2. Documentar patrones identificados en PRs
3. Incluir ejemplos reales del proyecto
4. Agregar referencia en `agents/leo.agent.md` si Leo debe consultarlo directamente

```markdown
---
## Título del Skill

### Patrón 1
✅ Forma correcta
❌ Forma incorrecta
Razón: ...

### Patrón 2
...
```

### Agregar un Nuevo Agente Especializado

1. Crear archivo: `agents/tema-assistant.agent.md`
2. Definir una `description` rica en triggers con `Use when:`
3. Documentar flujo de preguntas
4. Agregar referencia en `agents/leo.agent.md`

```yaml
---
name: tema-assistant
description: "Descripción del agente. Use when: patrón 1, patrón 2"
---
```

---

## 🔧 Troubleshooting

### Problemas Comunes y Soluciones

#### 1. Error: "gh: command not found"

**Problema:** El comando `gh pr create` falla.

**Solución:**
```bash
# macOS
brew install gh

# Linux
sudo apt install gh

# Autenticar
gh auth login
```

#### 2. Commit rechazado por el pipeline

**Problema:** Push fallido con error "commit message format invalid".

**Solución:**
```bash
# Verificar formato con Leo
"Leo, valida mi commit: [mensaje]"

# Corregir último commit
git commit --amend -m "[tipo][BC-XXXXX] Módulo: Descripción correcta"

# Si ya hiciste push, confirma primero que quieres reescribir historial remoto
git push --force-with-lease
```

#### 3. PR sin evidencias visuales

**Problema:** Olvidé subir screenshots.

**Solución:**
```bash
# Abrir PR en navegador
gh pr view <número> --web

# Editar descripción → Arrastrar imágenes al editor → Guardar
```

#### 4. Branch name inválido

**Problema:** No puedo crear el PR, branch no sigue convenciones.

**Solución:**
```bash
# Renombrar branch local
git branch -m nuevo_nombre

# Ejemplo correcto: tipo/numero_descripcion
git branch -m ft/12345_agregar_login_biometrico

# Force push con nuevo nombre
git push origin -u ft/12345_agregar_login_biometrico
```

#### 5. Leo no responde o da respuesta genérica

**Problema:** Leo no activa el agente correcto.

**Causas comunes:**
- Pregunta demasiado vaga
- No incluiste "Leo" al inicio
- Pregunta fuera del scope del proyecto

**Solución:**
```
❌ "ayuda con esto"
✅ "Leo, ayuda con mi commit"

❌ "crear PR"
✅ "Leo, crea el PR"

❌ "revisar código"
✅ "Leo, revisa mi PR"
```

#### 6. Validator muestra errores pero código está correcto

**Problema:** PR Reviewer automation marca bloqueadores incorrectos.

**Solución:**
1. Verificar que el commit siga el formato exacto
2. Revisar que el tipo sea uno de los 9 válidos (ft, fx, tt, rf, cr, wr, hf, poc, devops)
3. Verificar que el ticket sea BC-XXXXX (típicamente 5-6 dígitos)
4. Si persiste, revisar logs del workflow en Actions

#### 7. No puedo hacer amend porque ya hice push

**Problema:** Necesito corregir commit pero ya está en remoto.

**Solución:**
```bash
# Corregir el último commit
git commit --amend -m "[tipo][BC-XXXXX] Módulo: Descripción corregida"

# Confirmar primero que el branch es tuyo o que no afectará a otros colaboradores
# antes de reescribir el historial remoto
git push --force-with-lease

# Si hay colaboradores en el branch, crear nuevo commit
git commit -m "[tipo][BC-XXXXX] Módulo: Corrección del commit anterior"
git push
```

#### 8. El workflow tarda mucho o falla

**Problema:** GitHub Actions en "pending" por mucho tiempo.

**Solución:**
1. Revisar status en la pestaña "Checks" del PR
2. Ver logs detallados en Actions tab del repositorio
3. Si falla por timeout, re-ejecutar el workflow
4. Si persiste, notificar al equipo de DevOps

---

## 📚 Referencias

### Documentación del Proyecto
- [Arquitectura](../docs/architecture/architecture.md)
- [Colaboración](../docs/collaboration/collaboration.md)
- [Branching Strategy](../docs/collaboration/branching_strategy_and_versioning.md)

### Archivos del Sistema
- [Leo](agents/leo.agent.md) - Orquestador principal
- [PR Assistant](agents/pr-assistant.agent.md) - Especialista en crear PRs
- [PR Reviewer](agents/pr-reviewer.agent.md) - Especialista en revisar PRs
- 🤖 **[GitHub Actions Automation](workflows/README.md)** - Validación automática de PRs
- [Commit Conventions](skills/commit-conventions/SKILL.md) - Conocimiento commits (50+ ejemplos)
- [Branch Naming](skills/branch-naming/SKILL.md) - Convenciones de branches
- [PR Description](skills/pr-description/SKILL.md) - Plantilla oficial de PRs
- [Testing](skills/testing-unified/SKILL.md) - Patrones de testing, Mockito, coverage
- [Module Creation](skills/module-creation/SKILL.md) - Estructura de módulos, Clean Architecture
- [Copilot Instructions](copilot-instructions.md) - Reglas generales

### Recursos Externos
- [GitHub Copilot Agents](https://docs.github.com/en/copilot/using-github-copilot/using-copilot-agents)
- [Copilot Instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-custom-instructions-for-github-copilot)

---

## 🤝 Contribuir

### Mejorar un Skill Existente

1. Identifica patrón en code reviews
2. Documenta el patrón con ejemplos
3. Agrega a skill correspondiente
4. Actualiza fecha de última modificación

### Reportar Problemas

Si un agente o skill:
- Da respuestas incorrectas
- No detecta tu pregunta
- Falta información

Crea un issue documentando:
- Pregunta realizada
- Respuesta esperada
- Respuesta obtenida

---

## 📈 Métricas de Éxito

El sistema se considera exitoso si:

- ✅ Reduce correcciones de commits en code reviews (>30%)
- ✅ Acelera creación de PRs con formato correcto
- ✅ Previene errores comunes de lifecycle
- ✅ Aumenta adopción del Design System
- ✅ Mejora coverage de tests en PRs

---

**Sistema de Agentes y Skills v1.0**  
Última actualización: 24 de febrero de 2026  
Proyecto: bancadigital-bm-app  
Organización: BAC-Credomatic
