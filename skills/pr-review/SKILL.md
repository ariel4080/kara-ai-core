# Pull Requests y Code Review - SKILL

## 🎯 Objetivo

Dominar el proceso completo de creación, revisión y aprobación de Pull Requests siguiendo los estándares documentados en [pr_creation_and_approval.md](../Repositorios/bancadigital-bm-app/docs/collaboration/pr_creation_and_approval.md) y [code_review.md](../Repositorios/bancadigital-bm-app/docs/collaboration/code_review.md).

**Target Q2 2026:**
- 90% de PRs con 3 aprobadores
- 90% de PRs con rebase (no merge commits)
- 80% de PRs con evidencia de tests
- 95% de PRs con formato de commit correcto

---

## 📚 Fundamentos

### ¿Qué es un Pull Request?

Un Pull Request (PR) es una **solicitud para integrar cambios** de una rama a otra (típicamente `feature/xxx` → `main`). Permite:

- ✅ **Revisión por pares** antes de mergear
- ✅ **Validación automática** (CI/CD)
- ✅ **Discusión** sobre el código
- ✅ **Historial** de decisiones técnicas

---

## 🔧 Creación de Pull Requests

### Requisitos Antes de Crear un PR

**1. Código compila y pasa tests:**
```bash
melos bootstrap
melos run analyze
melos run test
```

**2. Rebase con main:**
```bash
git checkout main
git pull origin main
git checkout feature/BC-12345_Login_biometric
git rebase main
```

**3. Commits con formato correcto:**
```bash
git log --oneline

# ✅ Deben verse así:
# a1b2c3d [ft][BC-12345] Login: Implementar autenticación biométrica
# e4f5g6h [tt][BC-12345] Login: Agregar tests de biométricos
```

---

### Estructura del PR

**Título:**
```
[TIPO][TICKET] DescType: Descripción breve

Ejemplo:
[ft][BC-12345] Login: Implementar autenticación biométrica
```

**Descripción (Template):**

```markdown
## 📝 Descripción

Breve explicación de los cambios realizados.

## 🎫 Ticket

AB#12345

## 🎯 Objetivo

¿Qué problema resuelve este PR?

## 🔍 Cambios Realizados

- Implementación de autenticación biométrica
- Integración con FacePhi SDK
- Tests unitarios para el flujo biométrico
- Documentación en README

## 📸 Evidencia

### Antes
[Screenshot o descripción del estado previo]

### Después
[Screenshot o video del cambio implementado]

## 🧪 Evidencia de Tests

```
Running tests...
✓ should authenticate with biometrics when available (1.2s)
✓ should fallback to PIN when biometrics unavailable (0.8s)
✓ should handle biometric errors gracefully (0.5s)

Coverage: 85%
```

\```bash
# Comando ejecutado
melos run test:coverage

# Resultado
ViewModels coverage: 88%
Repositories coverage: 82%
Global coverage: 85%
\```

## ✅ Checklist

- [x] Código compila sin errores
- [x] Tests agregados/actualizados
- [x] Coverage ≥ 75%
- [x] Análisis estático sin errores
- [x] Documentación actualizada
- [x] Rebase con main
- [x] Commits con formato correcto
- [x] Screenshots/videos adjuntos

## 📋 Pasos para Probar

1. Checkout de la rama `feature/BC-12345_Login_biometric`
2. `melos bootstrap`
3. Ejecutar app en dispositivo con biometría
4. Intentar login con Face ID/Touch ID
5. Verificar flujo completo

## 🔗 Referencias

- [Documentación FacePhi](link)
- [ADR Biometric Authentication](link)
- [Ticket en Jira](link)
```

---

### Crear el PR

**Desde GitHub UI:**
1. Ir a "Pull requests"
2. Click "New pull request"
3. Base: `main` ← Compare: `feature/BC-12345_Login_biometric`
4. Completar título y descripción con template
5. Agregar labels: `feature`, `mobile`, `android`, `ios`
6. Asignar reviewers (mínimo 3)
7. Click "Create pull request"

**Desde CLI (gh):**
```bash
gh pr create \
  --title "[ft][BC-12345] Login: Implementar autenticación biométrica" \
  --body-file .github/pull_request_template.md \
  --base main \
  --head feature/BC-12345_Login_biometric \
  --reviewer tech-lead,senior-dev-1,senior-dev-2
```

---

## 👥 Aprobadores Requeridos

### Regla de 3 Aprobadores

**⚠️ OBLIGATORIO:**
- **1 aprobador MANDATORIO:** Tech Lead o Senior responsable del área
- **2 aprobadores adicionales:** Del equipo (Mid/Senior/Tech Lead)

**Ejemplo:**
```
Área: Payments
- 1️⃣ MANDATORIO: @tech-lead-payments (Juan Pérez)
- 2️⃣ ADICIONAL: @senior-dev-1 (María González)
- 3️⃣ ADICIONAL: @mid-dev-1 (Carlos Rodríguez)
```

---

### Asignación de Reviewers

**GitHub CODEOWNERS (`.github/CODEOWNERS`):**

```.github/CODEOWNERS
# Chapter Lead es owner global
*       @chapter-lead-mobile

# Tech Leads por área
**/accounts/**          @tech-lead-accounts
**/cards/**             @tech-lead-cards
**/payments/**          @tech-lead-payments
**/transfers/**         @tech-lead-transfers

# Core modules
**/core-data/**         @tech-lead-core
**/networking/**        @tech-lead-core
**/feature-commons/**   @tech-lead-core

# Design System
**/red-designsystem/**  @design-system-team

# Docs
docs/**                 @chapter-lead-mobile @tech-leads
```

---

## 📋 Checklist de Code Review

### Para el Autor

**Antes de solicitar review:**
- [ ] ✅ Código compila sin errores
- [ ] ✅ Tests agregados/actualizados
- [ ] ✅ Coverage ≥ 75% (≥ 80% ViewModels, ≥ 75% Repositories)
- [ ] ✅ `dart analyze --fatal-infos` pasa sin errores
- [ ] ✅ Rebase con main (historial lineal)
- [ ] ✅ Commits con formato `[type][BC-12345] DescType: description`
- [ ] ✅ Screenshots/videos en PR description
- [ ] ✅ Evidencia de cobertura de pruebas
- [ ] ✅ Pasos para probar documentados
- [ ] ✅ PR pequeño (<500 líneas idealmente)
- [ ] ✅ Documentación actualizada si aplica

---

### Para el Reviewer

**Aspectos a revisar:**

#### 1. Legibilidad
- [ ] ¿El código es fácil de entender?
- [ ] ¿Los nombres de variables/funciones son descriptivos?
- [ ] ¿Hay comentarios donde son necesarios?
- [ ] ¿Se respeta el límite de 120 caracteres por línea?
- [ ] ¿Las clases tienen ≤ 1000 líneas?

#### 2. Seguridad
- [ ] ¿Se validan inputs del usuario?
- [ ] ¿Se usa `CipherManager` para datos sensibles?
- [ ] ¿No hay hardcoded secrets/API keys?
- [ ] ¿Se usa `flutter_secure_storage` para tokens?
- [ ] ¿No se loguean datos sensibles (PII)?

#### 3. Cobertura de Pruebas
- [ ] ¿Hay tests para el código nuevo?
- [ ] ¿Los tests son significativos (no triviales)?
- [ ] ¿Se usan mocks apropiadamente?
- [ ] ¿Coverage cumple con los mínimos?
- [ ] ¿Hay evidencia de ejecución de tests?

#### 4. Arquitectura y Estilo
- [ ] ¿Se respeta Clean Architecture (Domain/Data/UI)?
- [ ] ¿Se usan UseCases en lugar de Repositories directos?
- [ ] ¿Los DTOs tienen sufijo `Dto`?
- [ ] ¿Los Mappers son extensions sobre DTOs?
- [ ] ¿Se usa Riverpod correctamente (AsyncNotifier)?
- [ ] ¿Se respetan las convenciones de nomenclatura?

#### 5. Usabilidad
- [ ] ¿La UI es intuitiva?
- [ ] ¿Los textos son claros?
- [ ] ¿Se usan componentes del Design System?
- [ ] ¿Hay manejo de estados de error/loading?

#### 6. Reutilización
- [ ] ¿Se reutiliza código existente?
- [ ] ¿El código nuevo es reutilizable?
- [ ] ¿Se crean widgets reutilizables apropiados?
- [ ] ¿Se aprovechan helpers/utils existentes?

---

## 💬 Comentarios de Code Review

### Estructura de Comentarios

**Formato sugerido:**
```markdown
[TIPO]: Título breve

Explicación detallada del problema o sugerencia.

Código sugerido (si aplica):
```dart
// Código propuesto
```

Razón: Por qué es mejor esta aproximación.
```

**Tipos de comentarios:**
- 🔴 **[BLOCKER]**: Debe ser resuelto antes de mergear
- 🟡 **[SUGGESTION]**: Sugerencia opcional, no bloqueante
- 🔵 **[QUESTION]**: Pregunta para clarificar
- 🟢 **[PRAISE]**: Reconocimiento de buenas prácticas
- 📚 **[LEARNING]**: Compartir conocimiento

---

### Ejemplos de Buenos Comentarios

**❌ Comentario vago:**
```
Esto no está bien.
```

**✅ Comentario constructivo:**
```markdown
[BLOCKER]: Falta manejo de null safety

En la línea 45, `account.balance` puede ser null y no está manejado.

Sugerencia:
```dart
final balance = account.balance ?? 0.0;
```

Razón: Previene NullPointerException en runtime.
```

---

**❌ Comentario agresivo:**
```
Esto es horrible, ¿por qué hiciste esto?
```

**✅ Comentario respetuoso:**
```markdown
[SUGGESTION]: Considerar extraer a función

El bloque de código en las líneas 50-80 hace múltiples cosas.
Consideraría extraerlo a una función privada `_validateAndFormatAccountData()`.

Razón: Mejora legibilidad y facilita testing unitario.
```

---

**✅ Reconocer buenas prácticas:**
```markdown
[PRAISE]: Excelente uso de mappers

Me gusta cómo separaste la conversión DTO → Entity en un mapper.
Muy limpio y testeable. 👍
```

---

### Resolver Comentarios

**Como autor:**
1. **Lee todos los comentarios** antes de responder
2. **Responde a cada comentario** aunque sea con "Done ✅"
3. **Haz los cambios** y pushea
4. **Marca como resuelto** solo si el reviewer está de acuerdo
5. **Solicita re-review** cuando hayas terminado

**Como reviewer:**
1. **Verifica que el cambio resuelve el problema**
2. **Marca como resuelto** si estás satisfecho
3. **Re-comenta** si persiste el problema

---

## 🔄 Proceso de Actualización del PR

### Actualizar con main (Rebase)

**⚠️ OBLIGATORIO: Usar rebase, NO merge**

```bash
# 1. Asegurarse de tener main actualizado
git checkout main
git pull origin main

# 2. Volver a tu rama
git checkout feature/BC-12345_Login_biometric

# 3. Rebase (NO merge)
git rebase main

# 4. Resolver conflictos si existen
# ... resolver conflictos ...
git add .
git rebase --continue

# 5. Force push (reescribe historia)
git push --force-with-lease origin feature/BC-12345_Login_biometric
```

**¿Por qué `--force-with-lease`?**
- Más seguro que `--force`
- Falla si alguien más pusheó a la rama
- Previene pérdida accidental de commits

---

### Agregar Cambios al PR

```bash
# 1. Hacer cambios
# ... editar archivos ...

# 2. Commit con formato correcto
git add .
git commit -m "[tt][BC-12345] Login: Corregir validación de biométricos"

# 3. Push (actualiza PR automáticamente)
git push origin feature/BC-12345_Login_biometric
```

---

## ✅ Aprobación y Merge

### Requisitos para Merge

**⚠️ ANTES DE MERGEAR:**
- [x] ✅ 3 aprobadores (1 mandatorio)
- [x] ✅ Todos los comentarios resueltos
- [x] ✅ Verificaciones CI/CD pasadas
- [x] ✅ Actualizado con main (rebase)
- [x] ✅ No hay conflictos

---

### Merge del PR

**Responsabilidad:** El **AUTOR** mergea después de las aprobaciones.

**Pasos:**

1. **Verificar que todo está OK:**
   - ✅ 3 aprobaciones
   - ✅ CI/CD verde
   - ✅ Comentarios resueltos

2. **Actualizar con main (última vez):**
   ```bash
   git checkout main
   git pull
   git checkout feature/BC-12345_Login_biometric
   git rebase main
   git push --force-with-lease
   ```

3. **Mergear desde GitHub:**
   - Click "Squash and merge" o "Merge pull request"
   - Completar mensaje de merge
   - Confirmar merge

4. **Eliminar rama:**
   ```bash
   git checkout main
   git pull
   git branch -d feature/BC-12345_Login_biometric
   git push origin --delete feature/BC-12345_Login_biometric
   ```

---

## 🚀 Estrategias de Merge

### Squash and Merge (Recomendado para PRs pequeños)

**Cuándo usar:**
- PR con múltiples commits pequeños/WIP
- Historia de commits no es importante

**Resultado:**
- Todos los commits del PR se combinan en 1
- Historial de main limpio

```bash
# GitHub hace esto automáticamente con "Squash and merge"
# Resultado en main:
# a1b2c3d [ft][BC-12345] Login: Implementar autenticación biométrica
```

---

### Rebase and Merge (Recomendado para PRs bien estructurados)

**Cuándo usar:**
- PR con commits atómicos bien documentados
- Cada commit tiene sentido independiente

**Resultado:**
- Commits individuales se preservan
- Historial lineal en main

```bash
# GitHub hace esto automáticamente con "Rebase and merge"
# Resultado en main:
# a1b2c3d [ft][BC-12345] Login: Implementar autenticación biométrica
# e4f5g6h [tt][BC-12345] Login: Agregar tests de biométricos
# i7j8k9l [wr][BC-12345] Login: Actualizar documentación funcional
```

---

### Merge Commit (❌ NO RECOMENDADO)

**Por qué evitarlo:**
- Crea merge commits innecesarios
- Historial de main no lineal
- Dificulta git bisect

**Resultado:**
```
# ❌ Historia enredada con merge commits
# m1n2o3p Merge pull request #123 from feature/BC-12345
# a1b2c3d [ft][BC-12345] Login: Implementar autenticación biométrica
```

---

## 📊 Métricas de PRs

### Velocidad de Review

**Objetivo:** Revisar PRs en ≤ 1 día

**Buenas prácticas:**
- PRs pequeños (≤ 500 líneas) son más rápidos de revisar
- Priorizar PRs bloqueantes
- Usar draft PRs para trabajo en progreso

---

### Calidad de PRs

**Indicadores:**
- % de PRs con 3 aprobadores
- % de PRs con rebase (no merge commits)
- % de PRs con evidencia de tests
- % de PRs con formato de commit correcto
- Número de iteraciones promedio

---

## 🚫 Errores Comunes

### ❌ PR demasiado grande

```
Files changed: 2,500 additions, 1,200 deletions
```

**Problema:** Difícil de revisar, mayor probabilidad de bugs

**Solución:** Dividir en múltiples PRs pequeños

```
PR 1: [ft][BC-12345] Login: Implementar UI (300 líneas)
PR 2: [ft][BC-12345] Login: Integrar lógica (250 líneas)
PR 3: [tt][BC-12345] Login: Agregar tests (200 líneas)
```

---

### ❌ Descripción vacía o genérica

```
Título: Fix bug
Descripción: Fixed the thing
```

**Problema:** Reviewers no entienden qué cambió y por qué

**Solución:** Usar template completo con screenshots y evidencia

---

### ❌ No resolver comentarios

```
Reviewer: [BLOCKER] Falta null check en línea 42
Autor: (no responde)
Reviewer: (esperando...)
```

**Problema:** PR estancado, demora en mergear

**Solución:** Responder a TODOS los comentarios, aunque sea con "Working on it..."

---

### ❌ Merge sin aprobaciones completas

```
Aprobaciones: 2/3
CI/CD: ✅ Passed
Autor: *clicks merge*
```

**Problema:** Proceso no cumplido, puede ser revertido

**Solución:** Esperar las 3 aprobaciones requeridas

---

### ❌ No actualizar con main

```
Last commit: 5 days ago
main branch: 42 commits ahead
```

**Problema:** Conflictos en merge, CI puede fallar

**Solución:** Rebase con main regularmente

```bash
git rebase main
git push --force-with-lease
```

---

## ✅ Checklist Completo

### Crear PR
- [ ] Código compila sin errores
- [ ] Tests agregados/actualizados
- [ ] Coverage ≥ 75%
- [ ] Análisis estático pasa
- [ ] Rebase con main
- [ ] Commits con formato correcto
- [ ] Título descriptivo con formato `[type][ticket] DescType: description`
- [ ] Descripción completa con template
- [ ] Screenshots/videos adjuntos
- [ ] Evidencia de tests con % de coverage
- [ ] Pasos para probar documentados
- [ ] 3 reviewers asignados (1 mandatorio)
- [ ] Labels apropiados

### Revisar PR
- [ ] Leer descripción completa
- [ ] Ejecutar código localmente (opcional)
- [ ] Revisar legibilidad
- [ ] Revisar seguridad
- [ ] Verificar cobertura de tests
- [ ] Verificar arquitectura
- [ ] Verificar usabilidad
- [ ] Verificar reutilización
- [ ] Comentarios constructivos y respetuosos
- [ ] Aprobar si todo está OK

### Mergear PR
- [ ] 3 aprobaciones recibidas (1 mandatorio)
- [ ] Comentarios resueltos
- [ ] CI/CD verde
- [ ] Actualizado con main
- [ ] No hay conflictos
- [ ] Squash/Rebase and merge (NO merge commit)
- [ ] Eliminar rama después de merge

---

## 📖 Referencias

- [pr_creation_and_approval.md](../Repositorios/bancadigital-bm-app/docs/collaboration/pr_creation_and_approval.md) - Proceso oficial
- [code_review.md](../Repositorios/bancadigital-bm-app/docs/collaboration/code_review.md) - Guía de code review
- [branching_strategy_and_versioning.md](../Repositorios/bancadigital-bm-app/docs/collaboration/branching_strategy_and_versioning.md) - Estrategia de branching
- [GitHub Pull Request Best Practices](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests)

---

**Versión:** 1.0  
**Fecha:** 12 de marzo de 2026  
**Autor:** Chapter Lead Mobile  
**Estado:** ✅ Listo para Q2 2026
