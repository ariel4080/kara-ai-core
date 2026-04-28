# Branch Naming Conventions

Convenciones de nombres de ramas basadas en Trunk Based Development (TBD) y análisis de 4,500+ PRs del proyecto bancadigital-bm-app.

---

## 📝 Formato Obligatorio

```
<type>/<ticket_id>_<desc_type>_<atomic_description>
```

### Componentes:

1. **type**: Uno de los 9 tipos válidos
2. **ticket_id**: ID del ticket en Azure DevOps (número sin prefijo BC-)
3. **desc_type**: Módulo o área del código afectada
4. **atomic_description**: Descripción corta en snake_case

---

## 🏷️ Tipos Válidos (9 tipos)

Los mismos tipos que para commits:

| Tipo | Descripción | Uso |
|:----:|------------|-----|
| `ft` | Feature | Nueva funcionalidad |
| `fx` | Fix | Corrección de bug |
| `tt` | Technical Task | Tarea técnica (config, version bump, tests) |
| `rf` | Refactor | Refactorización sin cambio funcional |
| `cr` | Change Request | Cambio de requirement |
| `wr` | Wording Request | Cambios de textos/traducciones |
| `hf` | Hotfix | Corrección urgente en producción |
| `poc` | Proof of Concept | Prueba de concepto |
| `devops` | DevOps | CI/CD, pipelines, infraestructura |

---

## 📐 Reglas de Formato

### 1. Tipo (type)
- ✅ DEBE ser uno de los 9 tipos válidos
- ✅ DEBE estar en minúsculas
- ❌ NO usar variaciones (feature, bugfix, etc.)

### 2. Ticket ID (ticket_id)
- ✅ DEBE ser solo el número (sin prefijo BC-)
- ✅ Típicamente tiene 5-6 dígitos, pero acepta cualquier cantidad
- ❌ NO incluir BC- en el nombre de branch

### 3. Descripción de Tipo (desc_type)
- ✅ DEBE usar PascalCase o snake_case
- ✅ DEBE representar el módulo afectado
- ✅ PUEDE usar acrónimos reconocidos (DS, DFA, ACH, etc.)
- ❌ NO usar espacios

### 4. Descripción Atómica (atomic_description)
- ✅ DEBE usar snake_case o kebab-case
- ✅ DEBE ser descriptiva pero concisa
- ✅ PUEDE usar guiones bajos (_) o guiones medios (-) para separar palabras
- ✅ PUEDE incluir puntos (.) para indicar versiones (v1.1, v2.0)
- ❌ NO usar espacios ni mayúsculas (salvo nombres propios)
- ❌ NO usar otros caracteres especiales
- ✅ **RECOMENDADO**: usar underscores `_` para separar palabras
- ⚠️ **PERMITIDO**: usar guiones medios `-` (para compatibilidad con branches existentes)

**Formato oficial recomendado (según branching_strategy_and_versioning.md):**
- `ft/12345_nueva_pantalla_transferencias` (snake_case con underscores) ✅ PREFERIDO
- `ft/123_Theme_app_theme_module` (actualización del módulo de tema de la app, con mayúsculas en nombres propios en `Theme`)

**Formato alternativo permitido:**
- `ft/12345_nueva-pantalla-transferencias` (kebab-case) ⚠️ FUNCIONA pero no recomendado
- `tt/99998_copilot-instructions-v1.1` (con puntos en versiones)

---

## 🎯 Módulos Comunes (desc_type)

Basados en la documentación oficial y PRs del proyecto:

### Módulos Principales
| Módulo | Descripción | Ejemplo |
|--------|-------------|---------|
| `DS` | Design System | `ft/35367_DS_primary_button` |
| `Theme` | Theming y estilos | `tt/123_Theme_app_theme` |
| `Architecture` | Arquitectura | `rf/45678_Architecture_clean_arch` |
| `Connectivity` | Network / Database | `fx/12345_Connectivity_timeout_fix` |

### Módulos de Negocio
| Módulo | Descripción | Ejemplo |
|--------|-------------|---------|
| `Login` | Proceso de login | `ft/67890_Login_biometric_auth` |
| `Onboarding` | Flujo de onboarding | `ft/11111_Onboarding_welcome_screen` |
| `Dashboard` | Dashboard principal | `cr/22222_Dashboard_cards_layout` |
| `Accounts` | Cuentas | `ft/33333_Accounts_list_view` |
| `Cards` | Tarjetas | `fx/44444_Cards_validation_fix` |
| `Payments` | Pagos | `ft/55555_Payments_favorites` |
| `Transfers` | Transferencias | `ft/66666_Transfers_sinpe_flow` |
| `Solicitudes` | Self-services | `fx/77777_Solicitudes_form_validation` |

### Módulos Técnicos
| Módulo | Descripción | Ejemplo |
|--------|-------------|---------|
| `Monitoring` | Observabilidad | `tt/88888_Monitoring_newrelic_integration` |
| `DFA` | Dynamic Factor Auth | `ft/99999_DFA_sms_validation` |
| `Pipeline` | CI/CD | `devops/12345_Pipeline_security_scan` |
| `App` | Configuración global | `tt/67890_App_version_bump` |

---

## ✅ Ejemplos Correctos (Patrón Oficial)

### Features
```bash
✅ ft/35367_Payments_save_favorite
✅ ft/70876_Wallets_select_country_cif
✅ ft/74246_Monitoring_add_user_id
✅ ft/61192_Enrollment_cbac_active_screen
```

### Fixes
```bash
✅ fx/103820_Cards_null_validation
✅ fx/76054_Solicitudes_newrelic_client_fix
✅ fx/77768_Cards_renderbox_conflict
✅ fx/99642_Solicitudes_webview_null_check
```

### Technical Tasks
```bash
✅ tt/98402_App_version_1.6.0_alpha10
✅ tt/64706_Cards_unit_tests
✅ tt/63536_Monitoring_dynatrace_integration
✅ tt/123_Theme_app_theme_setup
```

### Refactors
```bash
✅ rf/76880_Biometria_raw_images
✅ rf/44197_Accounts_migrate_service
✅ rf/72834_Biometria_separate_error_states
```

### Change Requests
```bash
✅ cr/102224_Solicitudes_adjust_parameters
✅ cr/63538_Cards_spanish_text
✅ cr/102116_Accounts_remove_pdf_button
```

### Hotfix
```bash
✅ hf/12345_Auth_login_crash_legacy_users
✅ hf/67890_Payments_critical_amount_validation
```

### Proof of Concept
```bash
✅ poc/12345_Architecture_bloc_migration
✅ poc/67890_Performance_lazy_loading
```

### DevOps
```bash
✅ devops/12345_Pipeline_security_analysis
✅ devops/67890_CI_dependency_cache
```

---

## ❌ Ejemplos Incorrectos

### ❌ Tipo Incorrecto o Formato Inválido

```bash
❌ feature/35367_Payments_save_favorite
✅ ft/35367_Payments_save_favorite

❌ bugfix/103820_Cards_validation
✅ fx/103820_Cards_null_validation

❌ FT/35367_Payments_save_favorite
✅ ft/35367_Payments_save_favorite

❌ fix-bug/12345_Login_error
✅ fx/12345_Login_error_handling
```

**Regla:** Usar solo los 9 tipos válidos en minúsculas (ft, fx, tt, rf, cr, wr, hf, poc, devops).

---

### ❌ Incluir Prefijo BC- en el Nombre

```bash
❌ ft/BC-35367_Payments_save_favorite
✅ ft/35367_Payments_save_favorite

❌ fx/BC-103820_Cards_validation
✅ fx/103820_Cards_null_validation
```

**Regla:** El ticket_id NO incluye el prefijo BC-.

---

### ❌ Uso de Espacios o Mayúsculas en atomic_description

```bash
❌ ft/35367_Payments_Save Favorite
✅ ft/35367_Payments_save_favorite

❌ fx/103820_Cards_NullValidation
✅ fx/103820_Cards_null_validation

❌ tt/98402_App_Version 1.6.0
✅ tt/98402_App_version_1.6.0
```

**Regla:** Usar snake_case (guiones bajos, sin espacios, sin mayúsculas).

---

### ❌ Descripción Vaga o Genérica

```bash
❌ ft/35367_Payments_changes
✅ ft/35367_Payments_save_favorite

❌ fx/103820_Cards_fix
✅ fx/103820_Cards_null_validation_form

❌ rf/44197_Accounts_refactor
✅ rf/44197_Accounts_migrate_list_service
```

**Regla:** La descripción debe ser específica sobre qué se está trabajando.

---

### ❌ Falta Módulo (desc_type)

```bash
❌ ft/35367_save_favorite
✅ ft/35367_Payments_save_favorite

❌ fx/103820_null_validation
✅ fx/103820_Cards_null_validation

❌ tt/98402_version_bump
✅ tt/98402_App_version_1.6.0
```

**Regla:** Siempre incluir el módulo donde se hace el cambio.

---

### ❌ Caracteres Especiales Inválidos

```bash
❌ ft/35367_Payments_save favorite
✅ ft/35367_Payments_save_favorite

❌ fx/103820_Cards_null@validation
✅ fx/103820_Cards_null_validation

❌ tt/98402_App_version#1.6.0
✅ tt/98402_App_version_1_6_0
```

**Nota:** Los guiones medios (`-`) están **permitidos** para compatibilidad, aunque se recomienda usar underscores (`_`).

**Regla:** Usar letras, números, underscores (`_`) preferentemente. Los guiones medios (`-`) y puntos (`.`) están permitidos para compatibilidad.

---

## 🌿 Ramas Especiales

### Main Branch
```
main
```
- Rama principal del proyecto
- Siempre debe estar en estado desplegable
- Protegida con branch protection rules
- Merges solo vía Pull Request

### Release Branches
```
release-<MAJOR>.<MINOR>.x
```

Ejemplos:
```bash
✅ release-1.6.x
✅ release-1.7.x
✅ release-2.0.x
```

**Características:**
- Ramas cortas y temporales
- Creadas para preparar un lanzamiento inminente
- Ajustes finales y correcciones de última hora
- Cambios se cherry-pick a main
- Se eliminan después del lanzamiento

---

## 🔄 Relación Branch ↔ Commit

El tipo de branch debe coincidir con los tipos de commits que contenga:

```bash
# Feature branch debe tener commits [ft]
ft/35367_Payments_save_favorite
  └─ ✅ [ft][BC-35367] Payments: Implementar guardado de favoritos

# Fix branch debe tener commits [fx]
fx/103820_Cards_validation
  └─ ✅ [fx][BC-103820] Cards: Agregar validación null en checkIfFormIsFilled()
```

---

## 🚀 Flujo de Trabajo con Branches

### 1. Crear Branch desde Main

```bash
# Sincronizar main
git checkout main
git pull origin main

# Crear feature branch
git checkout -b ft/35367_Payments_save_favorite

# Crear fix branch
git checkout -b fx/103820_Cards_null_validation
```

### 2. Trabajar en la Branch

```bash
# Hacer cambios y commits
git add .
git commit -m "[ft][BC-35367] Payments: Implementar guardado de favoritos"
git push origin ft/35367_Payments_save_favorite
```

### 3. Crear Pull Request

- Branch base: `main`
- Branch compare: `ft/35367_Payments_save_favorite`
- Título del PR: Similar al commit principal
- Descripción: Usando template oficial

### 4. Después del Merge (Fast-Forward)

```bash
# Eliminar branch local
git branch -d ft/35367_Payments_save_favorite

# Eliminar branch remota (GitHub lo hace automáticamente)
git push origin --delete ft/35367_Payments_save_favorite
```

---

## ⚠️ Casos Especiales

### Múltiples Módulos Afectados

```bash
✅ ft/35367_App_Auth_biometric_integration
✅ fx/103820_Cards_Payments_shared_validation
```

**Nota:** Separar módulos con guión bajo.

---

### Descripción con Versión

```bash
✅ tt/98402_App_version_1.6.0_alpha_10
✅ tt/64706_App_update_to_2.0.0_alpha_1
```

**Nota:** Reemplazar puntos por guiones bajos.

---

### Branches de Experimentos

```bash
✅ poc/12345_Architecture_bloc_evaluation
✅ poc/67890_Performance_lazy_loading_test
```

**Nota:** POCs pueden tener nombres más descriptivos pero seguir el formato.

---

## 🛠️ Validación de Branch Names

### Checklist Pre-Push:

- [ ] Tipo es uno de los 9 válidos (ft, fx, tt, rf, cr, wr, hf, poc, devops)
- [ ] Ticket ID es válido (típicamente 5-6 dígitos, sin prefijo BC-)
- [ ] Módulo (desc_type) está presente
- [ ] atomic_description usa snake_case (sin espacios, sin mayúsculas)
- [ ] No hay caracteres especiales excepto guión bajo
- [ ] Formato completo: `type/ticket_id_desc_type_atomic_description`

---

## 🔍 Regex de Validación

El repositorio usa esta regex para validar branches:

```regex
^((ft|fx|tt|rf|cr|wr|hf|poc|devops)\/\d+_[\S]*|release-\d+\.\d+\.x)$
```

### Explicación:
- `(ft|fx|tt|rf|cr|wr|hf|poc|devops)`: Uno de los 9 tipos
- `\/`: Separador slash
- `\d+`: Uno o más dígitos (ticket ID)
- `_`: Guión bajo obligatorio
- `[\S]*`: Cualquier carácter no-espacio (descripción)
- `|`: O bien...
- `release-\d+\.\d+\.x`: Formato de release branch

---

## 🚨 Errores Comunes

### Top 5 Errores en Nombrado de Branches:

1. **Usar feature en lugar de ft** (35% de correcciones)
   ```bash
   ❌ feature/35367_save_favorite
   ✅ ft/35367_Payments_save_favorite
   ```

2. **Incluir BC- en el ticket ID** (25% de correcciones)
   ```bash
   ❌ ft/BC-35367_Payments_save_favorite
   ✅ ft/35367_Payments_save_favorite
   ```

3. **Usar espacios en lugar de guiones bajos** (20% de correcciones)
   ```bash
   ❌ ft/35367_Payments_save favorite
   ✅ ft/35367_Payments_save_favorite
   ```

4. **Falta de módulo** (15% de correcciones)
   ```bash
   ❌ ft/35367_save_favorite
   ✅ ft/35367_Payments_save_favorite
   ```

5. **Tipo en mayúsculas** (5% de correcciones)
   ```bash
   ❌ FT/35367_Payments_save_favorite
   ✅ ft/35367_Payments_save_favorite
   ```

---

## 📚 Referencias

- **Estrategia de Branching:** `/docs/collaboration/branching_strategy_and_versioning.md`
- **Trunk Based Development:** https://trunkbaseddevelopment.com/
- **Commit Conventions:** `../commit-conventions/SKILL.md`
- **Azure DevOps:** Tickets en formato BC-XXXXX

---

## 💡 Tips Rápidos

### ✅ DO (Hacer)
- Usar branches de vida corta (1-3 días máximo)
- Mergear frecuentemente a main
- Eliminar branches después del merge
- Mantener nombres descriptivos pero concisos
- Validar formato antes de push

### ❌ DON'T (No Hacer)
- Crear branches de larga duración
- Usar nombres genéricos (fix, feature, test)
- Incluir prefijos innecesarios (BC-, feature/, bug/)
- Usar espacios o caracteres especiales
- Olvidar el módulo en la descripción

---

**Analizado de:** 4,500+ PRs  
**Última actualización:** Febrero 2026  
**Estrategia:** Trunk Based Development (TBD)  
**Tasa de errores:** ~20% de branches requieren corrección de nombre
