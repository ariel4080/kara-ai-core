---
name: pr-evidence
description: "Valida evidencia en Pull Requests. Use when: verificar PR, validar evidencias, revisar screenshots, comprobar tests, verificar evidencia visual."
applyTo:
  - "**/*.md"
---

# PR Evidence Checker

Verifico que cada Pull Request incluya la evidencia apropiada según el tipo de cambio.

---

## 🎯 Evidencia por Tipo de Cambio

### 1. Cambios de UI (ft, cr con cambios visuales)

#### 📸 Requerido:

✅ **Screenshots de ANTES y DESPUÉS**
- Captura del estado previo (si aplica)
- Captura del estado después del cambio
- Imágenes claras y legibles

✅ **Videos si hay:**
- Animaciones
- Flujos complejos multi-pantalla
- Transiciones
- Gestos de usuario

✅ **Pruebas en múltiples dispositivos:**
- Android (diferentes versiones: 11, 12, 13, 14)
- iOS (diferentes versiones: 15, 16, 17)
- Diferentes tamaños de pantalla (phone, tablet)

✅ **Dark mode (si aplica):**
- Screenshots en modo claro
- Screenshots en modo oscuro

#### 📋 Checklist UI:

```markdown
## Evidencias Visuales

### Antes
[Screenshot o descripción del estado previo]

### Después
[Screenshot del cambio implementado]

### Dispositivos Testeados
- [ ] Android 12 - Pixel 4a
- [ ] Android 13 - Samsung S23
- [ ] iOS 16 - iPhone 13
- [ ] iOS 17 - iPhone 15

### Ambientes
- [x] DEV
- [x] QA
- [ ] STAGE (si aplica)

### Dark Mode
- [x] Light theme ✅
- [x] Dark theme ✅
```

---

### 2. Cambios de Lógica (fx, tt, rf)

#### 🧪 Requerido:

✅ **Tests ejecutados (screenshot del output)**
```bash
# Screenshot del output mostrando:
flutter test
# ✅ Todos los tests pasando
```

✅ **Coverage report (si se agregan tests nuevos)**
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
# Screenshot del reporte HTML mostrando coverage
```

✅ **Evidencia de comportamiento correcto**
- Logs mostrando el fix funcionando
- Screenshot de la funcionalidad corregida
- Video del flujo completo (si aplica)

#### 📋 Checklist Lógica:

```markdown
## Evidencia de Tests

### Tests Ejecutados
![Tests output](path/to/screenshot.png)

**Resumen:**
- Total tests: 45
- Passed: 45 ✅
- Failed: 0
- Coverage: 85%

### Comportamiento Verificado
- [x] Caso normal funciona
- [x] Edge cases manejados
- [x] Errores manejados apropiadamente

### Logs/Debugging
```
[Logs relevantes mostrando el fix]
```
```

---

### 3. Refactors (rf)

#### 🔄 Requerido:

✅ **Evidencia de que funcionalidad NO cambió**
- Tests existentes siguen pasando
- Screenshots de flujos principales funcionando igual
- No hay regresiones visuales

✅ **Tests siguen pasando**
```bash
flutter test
# ✅ Screenshot mostrando todos los tests verdes
```

✅ **Coverage no disminuyó**
```bash
# Antes del refactor: 78%
# Después del refactor: 80% ✅
```

✅ **Performance no se degradó (si es relevante)**
- Benchmarks antes/después
- Flamegraphs (si aplica)

#### 📋 Checklist Refactor:

```markdown
## Evidencia de Refactor

### Tests Existentes
![Tests passing](path/to/tests.png)
- [x] Todos los tests existentes pasan
- [x] No se rompió ningún test

### Coverage
- Antes: 78%
- Después: 80% ✅
- Diferencia: +2%

### Funcionalidad Verificada
- [x] Login flow funciona igual
- [x] Payment flow funciona igual
- [x] Navigation no cambió

### Performance (si aplica)
- Antes: 120ms
- Después: 115ms ✅
```

---

### 4. Actualización de Dependencias (tt, devops)

#### 📦 Requerido:

✅ **App compila en iOS**
```bash
cd ios && pod install
flutter build ios --debug
# ✅ Screenshot del build exitoso
```

✅ **App compila en Android**
```bash
flutter build apk --debug
# ✅ Screenshot del build exitoso
```

✅ **Tests siguen pasando**
```bash
flutter test
# ✅ Screenshot de tests pasando
```

✅ **No hay warnings críticos nuevos**
```bash
flutter analyze
# Screenshot mostrando 0 errors, 0 warnings (o mismos que antes)
```

#### 📋 Checklist Dependencias:

```markdown
## Evidencia de Actualización

### Build Status
- [x] iOS build ✅ [screenshot]
- [x] Android build ✅ [screenshot]
- [x] Tests pass ✅ [screenshot]

### Análisis Estático
```bash
$ flutter analyze
Analyzing...
No issues found! ✅
```

### Warnings
- Antes: 5 warnings
- Después: 5 warnings (sin cambios) ✅

### Dependencias Actualizadas
- riverpod: 2.3.0 → 2.4.0
- dio: 5.3.2 → 5.4.0

### Breaking Changes
- [ ] N/A - No hay breaking changes
```

---

### 5. Cambios de Documentación (docs)

#### 📝 Requerido:

✅ **Preview del cambio**
- Screenshot del markdown renderizado
- Links funcionando correctamente

✅ **Spelling/Grammar check**
- Sin typos
- Lenguaje claro y conciso

#### 📋 Checklist Docs:

```markdown
## Evidencia de Documentación

### Preview
[Screenshot del README/doc renderizado]

### Checklist
- [x] Links funcionan correctamente
- [x] Código de ejemplo compila (si aplica)
- [x] Sin typos
- [x] Formato markdown correcto
```

---

## 🚨 Mensajes de Validación

### ⚠️ Falta evidencia:

```markdown
⚠️ **Evidencia Faltante**

Este PR modifica UI pero no incluye evidencia visual.

**Por favor agrega:**
- Screenshots de ANTES y DESPUÉS
- Videos si hay animaciones/flujos
- Lista de dispositivos testeados

**Ubicación:** Sección "Evidencias Visuales" del template del PR
```

---

### ⚠️ Evidencia insuficiente:

```markdown
⚠️ **Evidencia Insuficiente**

La evidencia proporcionada es parcial.

**Falta:**
- [ ] Tests en múltiples dispositivos (solo veo Android)
- [ ] Screenshot de tests ejecutados
- [ ] Verificación de coverage

**Requerido para aprobación:**
- Mínimo 2 dispositivos (Android + iOS)
- Screenshot de tests pasando
- Coverage report si se agregan tests nuevos
```

---

### ✅ Evidencia adecuada:

```markdown
✅ **Evidencia Completa y Adecuada**

**Validado:**
- [x] Screenshots de antes/después incluidos
- [x] Múltiples dispositivos testeados (Android 13, iOS 16)
- [x] Tests ejecutados exitosamente
- [x] Coverage report incluido
- [x] Dark mode verificado

**Comentario:**
Excelente documentación del cambio. La evidencia permite verificar el comportamiento sin necesidad de checkout local.
```

---

## 📏 Estándares de Screenshots

### ✅ Buenos screenshots:

- **Resolución clara** (no borrosos)
- **Área relevante visible** (no solo un botón pequeño)
- **Contexto suficiente** (se entiende dónde está en la app)
- **Tamaño apropiado** (< 2MB preferiblemente)

### ❌ Malos screenshots:

- Borrosos o pixelados
- Muy zoomed in (no se entiende el contexto)
- Muy pequeños (no se ve el detalle)
- Screenshots de código (usar code blocks en su lugar)

---

## 🎥 Estándares de Videos

### ✅ Buenos videos:

- **Duración corta** (< 30 segundos, máx 1 minuto)
- **Muestra el flujo completo** (inicio → fin)
- **Formato compatible** (MP4, GIF)
- **Calidad clara** pero tamaño razonable (< 50MB)

### Herramientas recomendadas:

- **iOS:** QuickTime Screen Recording
- **Android:** Android Studio Screen Recording
- **GIF:** LICEcap, Kap
- **Edición:** iMovie, DaVinci Resolve

---

## 📋 Template de Evidencia por Tipo

### Template para Cambios UI:

```markdown
## Evidencias Visuales

> [!IMPORTANT]
> Screenshots y video del cambio implementado

### Antes
![Antes del cambio](path/to/before.png)

### Después
![Después del cambio](path/to/after.png)

### Video del Flujo
![Demo del flujo](path/to/demo.gif)

### Dispositivos Testeados
| Dispositivo | OS Version | Status |
|-------------|------------|--------|
| Pixel 4a | Android 13 | ✅ OK |
| iPhone 13 | iOS 16 | ✅ OK |
| iPad Air | iOS 17 | ✅ OK |

### Ambientes
- [x] DEV
- [x] QA
```

---

### Template para Cambios de Lógica:

```markdown
## Evidencia de Tests

### Tests Ejecutados
```bash
$ flutter test
00:05 +45: All tests passed!
```

![Tests output](path/to/tests-output.png)

### Coverage Report
- **Total coverage:** 85%
- **New code coverage:** 92%
- **ViewModels:** 88%

![Coverage report](path/to/coverage.png)

### Comportamiento Verificado
- [x] Flujo principal funciona
- [x] Edge cases manejados
- [x] Errores capturados apropiadamente
```

---

## 🔍 Validación Automatizada

### Checklist para revisar PR:

```markdown
## PR Evidence Validation

**Tipo de cambio detectado:** [UI/Logic/Refactor/Dependencies/Docs]

**Evidencia presente:**
- [ ] Screenshots/Videos (si UI)
- [ ] Tests ejecutados (si Logic/Refactor)
- [ ] Coverage report (si tests nuevos)
- [ ] Build status (si Dependencies)
- [ ] Múltiples dispositivos (si UI)
- [ ] Dark mode (si UI y aplica)

**Estado:**
- [ ] ✅ Evidencia completa
- [ ] ⚠️ Evidencia parcial - necesita mejoras
- [ ] ❌ Evidencia faltante - bloqueante
```

---

## 🎓 Referencias

- [PR Template](../pull_request_template.md) - Template oficial del repo
- [pr-description](../pr-description/SKILL.md) - Descripción de PRs
- [Code Review Guidelines](../../docs/collaboration/code_review.md) - Guía de code review

---

**Versión:** 1.0  
**Última actualización:** 25 de marzo de 2026  
**Basado en:** Mejores prácticas de 4,500+ PRs
