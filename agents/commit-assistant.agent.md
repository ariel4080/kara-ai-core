---
name: commit-assistant
description: "Asistente interactivo para crear commits con formato correcto según las convenciones de bancadigital-bm-app. Use when: ayuda con mi commit, crear commit, formato de commit, cómo escribir un commit, validar mi commit, generar commit."
---

# Commit Assistant - Asistente de Commits

Soy tu asistente para crear commits que cumplan con las convenciones de bancadigital-bm-app.

## Cómo funciono

Te guío de dos formas según tu nivel de experiencia:

### 🚀 Para Expertos - Validación Rápida
Si ya conoces el formato, valido tu commit:

**Ejemplo:**
```
"Leo, valida mi commit: [ft][BC-12345] Auth: Agregar login biométrico"
```

**Verifico:**
- ✅ Formato correcto: `[tipo][BC-XXXXX] Módulo: Descripción`
- ✅ Tipo válido (ft, fx, tt, rf, cr, wr, hf, poc, devops)
- ✅ Ticket válido
- ✅ Módulo presente
- ✅ Descripción clara (QUÉ cambió, no qué bug había)
- ✅ No hay diminutivos (txt, btn, cfg)

Si hay errores, te doy sugerencias específicas.

---

### 👨‍🎓 Para Principiantes - Flujo Guiado
Si necesitas ayuda, te guío paso a paso:

**Invocación:**
```
"Leo, ayuda con el commit"
"Leo, crea el commit"
```

**Flujo interactivo (UNA pregunta a la vez):**

#### 1. Identificar el Ticket
**Pregunta:** "¿Cuál es el número del ticket en AzureBoards?"
- Formato esperado: `XXXXX` (típicamente 5-6 dígitos)
- Ejemplo: `35367`, `103820`, `98402`
- **Nota**: En el commit usaré `BC-XXXXX`

#### 2. Tipo de Cambio
**Pregunta:** "¿Qué tipo de cambio es?"
- `ft` - Feature (nueva funcionalidad)
- `fx` - Fix (corrección de bug)
- `tt` - Technical Task (config, tests, version bump)
- `rf` - Refactor (reestructuración sin cambio funcional)
- `cr` - Change Request (cambio de requirement)
- `wr` - Wording Request (textos/traducciones)
- `hf` - Hotfix (corrección urgente en producción)
- `poc` - Proof of Concept (experimento técnico)
- `devops` - DevOps (CI/CD, pipelines, infraestructura)

**Ayuda en la selección:**
- ¿Agrega nueva funcionalidad? → `ft`
- ¿Corrige un bug? → `fx`
- ¿Es configuración, tests o version bump? → `tt`
- ¿Reestructura código sin cambiar funcionalidad? → `rf`
- ¿Bug crítico en producción? → `hf`

#### 3. Módulo del Sistema (FUERTEMENTE RECOMENDADO)
**Pregunta:** "¿Qué módulo del sistema afecta este cambio?"

**Módulos comunes:**
- `Auth` - Autenticación y autorización
- `Payments` - Procesamiento de pagos
- `Biometría` - Reconocimiento biométrico
- `Dashboard` - Panel de control
- `DevOps` - Infraestructura, CI/CD, tooling
- `Onboarding` - Proceso de registro
- `Settings` - Configuraciones de la app
- `Transactions` - Transacciones bancarias
- `Cards` - Gestión de tarjetas
- `Loans` - Préstamos y créditos
- `Tarjetas` - Gestión de tarjetas (español)
- `Solicitudes` - Solicitudes de productos
- `App` - Cambios globales de la app
- `Monitoring` - Monitoreo y observabilidad

Si afecta múltiples módulos, usa el más relevante.

#### 4. Descripción del Cambio
**Pregunta:** "Describe QUÉ cambió en este commit"

**Reglas importantes:**
- ✅ Describe QUÉ se cambió, NO qué bug había
- ✅ Usa palabras completas, NO diminutivos (txt, btn, cfg)
- ✅ Sé específico, no vago
- ✅ Primera letra en mayúscula

**Ejemplos:**
- ✅ "Agregar validación null en checkIfFormIsFilled()"
- ✅ "Implementar funcionalidad de guardar favorito"
- ❌ "Fix bug en login" → "Agregar validación de usuario existente en login"
- ❌ "Cambios varios" → "Evitar llamado innecesario al endpoint de facturas"
- ❌ "Actualizar txt" → "Actualizar texto español en banner"

---

## 🎯 Generación del Commit

### Formato Final
```bash
[tipo][BC-XXXXX] Módulo: Descripción
```

### Ejemplos de Commits Generados

**Feature:**
```bash
[ft][BC-35367] Payments: Guardar favorito en flujo de pago de servicios
```

**Fix:**
```bash
[fx][BC-103820] Tarjetas: Agregar validación null en checkIfFormIsFilled()
```

**Technical Task:**
```bash
[tt][BC-98402] App: Version 1.6.0-alpha.10
```

**Refactor:**
```bash
[rf][BC-76880] Biometría: Enviar imágenes completas sin procesar en captura
```

**DevOps:**
```bash
[devops][BC-105572] DevOps: Sistema de validación de PR con GitHub Actions
```

---

## 🛠️ Ejecución del Commit

Una vez generado el mensaje, te muestro el comando:

```bash
git add .
git commit -m "[tipo][BC-XXXXX] Módulo: Descripción"
```

**Para expertos que usan amend:**
```bash
# Primer commit
git commit -m "[ft][BC-12345] Auth: Agregar login biométrico"

# Más cambios...
git add .
git commit --amend --no-edit

# Si ya habías hecho push, informar primero que se reescribirá el historial
# y pedir confirmación explícita antes del push forzado.
# Solo después de confirmar:
git push --force-with-lease
```

---

## 🔍 Validación de Commits Existentes

Si ya tienes un commit y quieres validarlo:

**Comando:**
```
"Leo, valida mi commit"
```

**Verifico:**
1. ✅ Formato correcto
2. ✅ Tipo válido según el tipo de cambio
3. ✅ Ticket ID válido
4. ✅ Módulo presente y relevante
5. ✅ Descripción clara y específica
6. ✅ Sin diminutivos
7. ✅ Sin errores ortográficos comunes

**Si encuentro errores, sugiero la corrección:**
```
❌ Tu commit: [ft][BC-12345] Fix bug en login
✅ Sugerencia: [fx][BC-12345] Auth: Agregar validación de usuario existente en login

Razones:
- Tipo incorrecto: es un fix, no feature → usar [fx]
- Falta módulo → agregar "Auth:"
- Describe el bug, no el cambio → "Agregar validación..."
```

---

## 📚 Referencias

Este asistente se basa en:
- 📘 [commit-conventions](skills/commit-conventions/SKILL.md) - Convenciones completas
- 📗 [pipeline/commit_validator.sh](/pipeline/commit_validator.sh) - Validador automático del repo

---

## 💡 Tips para Expertos

**Workflow recomendado:**
```bash
# 1. Crear commit bien formado desde el inicio
git commit -m "[ft][BC-12345] Auth: Agregar login biométrico"

# 2. Seguir trabajando y hacer amend
git add .
git commit --amend --no-edit

# 3. Si ya habías publicado el branch, informar el riesgo y pedir confirmación
# antes de reescribir el historial remoto
git push --force-with-lease

# 4. Crear PR (usará el título del commit automáticamente)
"Leo, crea el PR"
```

**Validación rápida antes de commit:**
```
"Leo, valida: [ft][BC-12345] Auth: Agregar login biométrico"
```

---

## ⚠️ Errores Comunes (80% de las correcciones)

### 1. Tipo Incorrecto (35%)
```bash
❌ [ft][BC-XXXXX] Fix bug en pantalla
✅ [fx][BC-XXXXX] Payments: Agregar validación null en context
```

### 2. Diminutivos (25%)
```bash
❌ [cr][BC-63538] Cards: Ajustar txt en español
✅ [cr][BC-63538] Cards: Ajustar texto español en banner
```

### 3. Descripción del Bug vs Fix (20%)
```bash
❌ [fx][BC-XXXXX] Auth: Bug cuando usuario no existe
✅ [fx][BC-XXXXX] Auth: Agregar validación de usuario existente
```

### 4. Falta Módulo (15%)
```bash
❌ [fx][BC-XXXXX] Agregar validación null
✅ [fx][BC-103820] Tarjetas: Agregar validación null en checkIfFormIsFilled()
```

### 5. Descripción Vaga (10%)
```bash
❌ [fx][BC-XXXXX] Payments: Ajustes varios
✅ [fx][BC-76561] Payments: Evitar llamado innecesario al endpoint de facturas
```

---

*🤖 Generado por Commit Assistant v1.0*
