# GitHub Copilot Skills - bancadigital-bm-app

Skills especializados para desarrollo en Flutter siguiendo los estándares de BAC.

---

## 📚 Skills Disponibles

### 🏗️ Desarrollo y Arquitectura

#### 1. Module Creation (`skills/module-creation/`)
**Invoke:** "crear módulo", "nuevo feature", "scaffold module"

Workflow interactivo para crear Feature Modules completos siguiendo Clean Architecture + MVVM:
- ✅ Estructura completa con DataSource, Repository, ViewModel
- ✅ DTOs con Freezed + JsonSerializable
- ✅ ApiResponseHandlerMixin para manejo de errores
- ✅ AsyncNotifier para state management
- ✅ RedirectRules para control de acceso
- ✅ Tests robustos (DataSource, Repository, ViewModel)
- ✅ Integración con melos y navegación

**Uso:**
```
"crear módulo de notificaciones"
"Leo, nuevo feature module para pagos"
```

---

#### 2. Clean Architecture (`skills/clean-architecture/`)
**Invoke:** "clean architecture", "arquitectura limpia", "capas"

Guía completa de Clean Architecture para Flutter:
- ✅ Separación de capas (Data, Domain, Presentation)
- ✅ Dependency injection con Riverpod
- ✅ Mappers entre DTOs y Entities
- ✅ Repository pattern
- ✅ Use cases (cuando aplicar)

**Uso:**
```
"cómo estructurar este módulo?"
"Leo, explica clean architecture"
```

---

### 🎨 UI y Design System

#### 3. Design System Patterns (`skills/design-system-patterns/`)
**Invoke:** "design system", "componentes UI", "navegación"

Estándares de uso del Design System BAC:
- ✅ GoRouter vs Navigator (SIEMPRE GoRouter)
- ✅ Spacing y colores del design system
- ✅ Componentes reutilizables
- ✅ Patrones de navegación
- ✅ Context.mounted validation

**Uso:**
```
"cómo navegar a otra pantalla?"
"Leo, qué componente usar para botones?"
```

**Nota:** Para lifecycle patterns (super.initState(), context.mounted, dispose), consulta el skill `code-review` que incluye estas validaciones.

---

### ✅ Testing

#### 4. Testing Unified (`skills/testing-unified/`) ⭐ CONSOLIDADO
**Invoke:** "tests", "testing", "mockito", "coverage", "riverpod tests"

Guía completa de testing consolidada (antes testing, testing-advanced y testing-expert):
- ✅ Naming: "should X when Y"
- ✅ Estructura AAA (Arrange-Act-Assert)
- ✅ Mocking con Mockito (when, verify, provideDummy)
- ✅ Testing con Riverpod (ProviderContainer, overrides)
- ✅ AsyncNotifier testing patterns
- ✅ Widget tests
- ✅ Coverage requirements (ViewModels 80%, Repositories 75%)
- ✅ Templates completos para ViewModels y Repositories
- ✅ JSON Fixtures
- ✅ Checklist completo pre-PR

**Uso:**
```
"crear tests para este ViewModel"
"Leo, cómo mockear este repository?"
"tests completos para este módulo"
"verificar coverage de mi PR"
```

---

### 📝 Git y Commits

#### 5. Commit Conventions (`skills/commit-conventions/`)
**Invoke:** "commit", "tipo de commit", "convenciones"

Convenciones de commits del proyecto (50+ ejemplos):
- ✅ 9 tipos: [ft], [fx], [rf], [tt], [dx], [dc], [ci], [dp], [rv]
- ✅ Formato: `[tipo][BC-XXXXX] Módulo: Descripción`
- ✅ Ejemplos por módulo y tipo
- ✅ Qué tipo usar según el cambio
- ✅ Commits atómicos

**Uso:**
```
"qué tipo de commit usar para un bugfix?"
"Leo, formato de commit correcto"
```

---

#### 9. Branch Naming (`skills/branch-naming/`)
**Invoke:** "branch", "nombre de rama", "crear branch"

Convenciones de nombres de branches:
- ✅ Formato: `tipo/BC-XXXXX-descripcion-corta`
- ✅ Tipos permitidos
- ✅ Ejemplos correctos e incorrectos
- ✅ Validación automática

**Uso:**
```
"cómo nombrar mi branch?"
"Leo, crear branch para ticket BC-12345"
```

---

### 🔍 Code Review y PRs

#### 10. Code Review (`skills/code-review/`)
**Invoke:** "revisar código", "code review", "validar cambios"

Experto en code review de Flutter siguiendo estándares BAC:
- ✅ Lifecycle management (super.initState, context.mounted)
- ✅ Navigation patterns (GoRouter vs Navigator)
- ✅ Null safety y type safety
- ✅ Design System compliance
- ✅ Clean Architecture compliance
- ✅ Testing requirements
- ✅ Performance y optimizaciones

**Uso:**
```
"Leo, revisa este código"
"valida este componente Flutter"
```

---

#### 11. PR Description (`skills/pr-description/`)
**Invoke:** "PR", "pull request", "descripción PR"

Template y guía para descripciones de Pull Requests:
- ✅ Template oficial del proyecto
- ✅ Secciones obligatorias
- ✅ Checklist por tipo de cambio
- ✅ Ejemplos de buenas descripciones
- ✅ ADR cuando aplica

**Uso:**
```
"Leo, ayuda con descripción del PR"
"formato de PR correcto"
```

---

#### 12. PR Review (`skills/pr-review/`)
**Invoke:** "revisar PR", "review", "feedback PR"

Guía para hacer code review efectivo en PRs:
- ✅ Qué revisar en cada tipo de cambio
- ✅ Cómo dar feedback constructivo
- ✅ Priorización de comentarios
- ✅ Checklist de aprobación
- ✅ Casos de rechazo

**Uso:**
```
"cómo revisar este PR?"
"Leo, checklist para aprobar PR"
```

---

#### 13. PR Evidence (`skills/pr-evidence/`)
**Invoke:** "evidencias PR", "screenshots", "validar evidencias"

Valida que los Pull Requests incluyan evidencia apropiada según tipo:
- ✅ UI: Screenshots antes/después, múltiples dispositivos
- ✅ Lógica: Tests ejecutados, coverage report
- ✅ Refactor: Tests pasan, coverage no disminuye
- ✅ Dependencies: Build iOS/Android exitoso
- ✅ Templates por tipo de cambio

**Uso:**
```
"Leo, verifica evidencias de mi PR"
"qué screenshots necesito para PR de UI?"
```

**Nota:** Para CI/CD, consulta los workflows existentes en `.github/workflows/` que contienen la configuración real del proyecto.

---

## 🎯 Cómo Invocar Skills

### Opción 1: A través de Leo
```
"Leo, [acción que el skill maneja]"
```

Leo detecta automáticamente qué skill necesitas y lo carga.

### Opción 2: Directamente
```
"revisar este código"
"crear tests para este ViewModel"
"verificar evidencias del PR"
"crear módulo notifications"
```

### Opción 3: Slash Commands (en chat)
```
/code-review
/testing-unified
/pr-evidence
/module-creation
```

---

## 📁 Estructura de Skills

Cada skill sigue esta estructura:

```
skills/<skill-name>/
├── SKILL.md              # Skill principal con YAML frontmatter
└── templates/            # Templates opcionales (si aplica)
    ├── template1.dart
    └── template2.yaml
```

### Formato de SKILL.md

```yaml
---
name: skill-name
description: "Descripción del skill. Use when: [triggers]"
applyTo:
  - "**/*.dart"
  - "**/*.yaml"
---

# Skill Name

[Contenido del skill]
```

**IMPORTANTE:**
- `name:` debe coincidir con el nombre de la carpeta
- `description:` debe incluir "Use when:" con palabras clave trigger
- `applyTo:` define en qué archivos se aplica (evitar `"**"`)

---

## ✨ Agregar Nuevos Skills

### 1. Crear estructura
```bash
mkdir -p .github/skills/nuevo-skill
```

### 2. Crear SKILL.md
```yaml
---
name: nuevo-skill
description: "Descripción. Use when: [triggers]"
applyTo:
  - "**/*.ext"
---

# Nuevo Skill

[Contenido]
```

### 3. Actualizar agents/leo.agent.md
Agregar referencia en sección "Detección Inteligente"

### 4. Documentar en este README
Agregar sección con descripción y uso

---

## 🔍 Troubleshooting

### Skill no se carga
- ✅ Verifica que `name:` coincida con carpeta
- ✅ Verifica YAML frontmatter válido (no tabs, quotes en valores con ':')
- ✅ Verifica que `description:` tenga palabras clave claras

### Skill se carga pero da error
- ✅ Verifica que contenido después de `---` sea markdown válido
- ✅ Revisa que templates referenciad os existan
- ✅ Verifica que `applyTo` patterns sean válidos

### Skill aparece cuando no debería
- ✅ Ajusta `applyTo:` para ser más específico
- ✅ Revisa palabras clave en `description:`

---

## 📚 Referencias

- [Agent Customization Skill](copilot-skill:/agent-customization/SKILL.md)
- [VS Code Copilot Documentation](https://code.visualstudio.com/docs/copilot)
- [GitHub Copilot Skills Guide](https://docs.github.com/copilot)

---

**Versión:** 1.0  
**Última actualización:** 25 de marzo de 2026  
**Mantenedor:** Chapter Lead Mobile
