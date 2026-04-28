# Commit Message Conventions

Convenciones de commit messages basadas en análisis de 4,500+ PRs del proyecto bancadigital-bm-app.

---

## 📝 Formato Obligatorio

```
[tipo][BC-XXXXX] Módulo: Descripción específica del cambio
```

Donde `XXXXX` representa un identificador numérico (típicamente 5-6 dígitos, por ejemplo, `BC-12345` o `BC-103820`).

### Componentes:

1. **[tipo]**: Una de las opciones válidas
2. **[BC-XXXXX]**: ID del ticket en Azure DevOps (típicamente 5-6 dígitos)
3. **Módulo**: Área del código afectada
4. **Descripción**: Qué cambió (NO qué bug había)

---

## 🏷️ Tipos Válidos (9 tipos)

Orden estándar de tipos:

| Tipo | Nombre | Descripción |
|:----:|--------|-------------|
| `ft` | Feature | Nueva funcionalidad |
| `fx` | Fix | Corrección de bug |
| `tt` | Technical Task | Tarea técnica (config, tests, version bump) |
| `rf` | Refactor | Refactorización sin cambio funcional |
| `cr` | Change Request | Cambio de requirement |
| `wr` | Wording Request | Cambios de textos/traducciones |
| `hf` | Hotfix | Corrección urgente en producción |
| `poc` | Proof of Concept | Prueba de concepto |
| `devops` | DevOps | CI/CD, pipelines, infraestructura |

---

### ft - Feature
Nueva funcionalidad o capacidad agregada al sistema.

```bash
✅ [ft][BC-35367] Payments: Guardar favorito en flujo de pago de servicios
✅ [ft][BC-70876] Billeteras: Seleccionar país y cif para wallet
✅ [ft][BC-74246] Monitoring: Agregar userId a New Relic
```

### fx - Fix
Corrección de un bug o problema existente.

```bash
✅ [fx][BC-103820] Tarjetas: Agregar validación null en checkIfFormIsFilled()
✅ [fx][BC-76054] Solicitudes: Usar cliente existente de NewRelic para evitar error de reinicialización
✅ [fx][BC-77768] Tarjetas: Resolver conflicto RenderBox/RenderSliver en PendingMovementsViewSection
```

### tt - Technical Task
Trabajo técnico que no es una feature ni un fix (configuración, tests, version bumps, refactors menores).

```bash
✅ [tt][BC-98402] App: Version 1.6.0-alpha.10
✅ [tt][BC-64706] Tarjetas: Agregar pruebas unitarias para ui/cards_lobby/view_model
✅ [tt][BC-63536] Monitoring: Integración de Dynatrace
```

### rf - Refactor
Reestructuración de código sin cambio funcional.

```bash
✅ [rf][BC-76880] Biometría facial: Enviar imágenes completas raw en captura de documento
✅ [rf][BC-44197] Accounts: Migrar servicio de listado de cuentas
✅ [rf][BC-72834] Biometría facial: Separar estados de error de pantallas de flujos
```

### cr - Change Request
Cambio en funcionalidad existente por solicitud de producto/diseño.

```bash
✅ [cr][BC-102224] Solicitudes: Ajustar parámetros requeridos para entryPoint de actualización de datos
✅ [cr][BC-63538] Cards: Ajustar texto español en banner de solicitud de tarjeta
```

### wr - Wording Request
Cambios menores relacionados con textos, traducciones, copys.

```bash
✅ [wr][BC-12345] Cards: Actualizar texto de error en banner
✅ [wr][BC-67890] Login: Corregir ortografía en mensaje de bienvenida
```

### hf - Hotfix
Corrección urgente de bug crítico en producción.

```bash
✅ [hf][BC-12345] Auth: Corregir crash en login para usuarios legacy
✅ [hf][BC-67890] Payments: Fix crítico en validación de monto
```

### poc - Proof of Concept
Prueba de concepto o experimento técnico.

```bash
✅ [poc][BC-12345] Architecture: Evaluar migración a Bloc
✅ [poc][BC-67890] Performance: Test de lazy loading en listas
```

### devops - DevOps/Infrastructure
Tareas de infraestructura, CI/CD, configuración de pipelines.

```bash
✅ [devops][BC-12345] Pipeline: Agregar step de análisis de seguridad
✅ [devops][BC-67890] CI: Configurar cache de dependencias en GitHub Actions
```

---

## 🎯 Módulos Comunes

Ejemplos de módulos usados frecuentemente:

- **App**: Cambios globales de la aplicación
- **Auth**: Autenticación y autorización
- **Accounts**: Módulo de cuentas
- **Cards**: Módulo de tarjetas
- **Payments**: Módulo de pagos
- **Transfers**: Transferencias (locales, ACH, SINPE)
- **Solicitudes**: Self services / formularios
- **Monitoring**: Observabilidad (NewRelic, Dynatrace)
- **Biometría facial**: Facial biometrics
- **Login**: Proceso de login
- **DFA**: Dynamic Factor Authentication
- **Pipeline**: CI/CD

---

## ✅ Ejemplos Correctos (Casos Reales)

### Features
```bash
[ft][BC-104048] Solicitar producto: Corregir estado onPressed en cards según especificaciones DS
[ft][BC-70169] Redención Puntos: Implementar pantalla de selección de producto destino
[ft][BC-61192] Enrollment: Agregar pantalla de CBAC activo
```

### Fixes
```bash
[fx][BC-99642] Solicitudes: Agregar validación null de WebViewController en botón retroceso de error
[fx][BC-76360] Pago Préstamos: Actualizar lógica de inicialización para vista de éxito
[fx][BC-76535] Payments: Evitar actualización de referencias cuando hay error
```

### Tareas Técnicas
```bash
[tt][BC-74514] Test: Corregir tests rotos de self_services
[tt][BC-99263] DFAs: Iniciar journey por nombre y por resume URI
[tt][BC-104089] APP: Agregar header x-device-id a headers globales
```

### Change Requests
```bash
[cr][BC-102116] Accounts: Eliminación de botón descargar PDF en detalle de transacción
[cr][BC-104300] Recuperar contraseña: Disparar journey para usuarios bloqueados
```

### Refactors
```bash
[rf][BC-76880] Biometría facial: Enviar imágenes completas raw en captura de documento
[rf][BC-72834] Biometría facial: Separar estado de error interno a nueva pantalla
```

---

## ❌ Ejemplos Incorrectos (Corregidos en Reviews)

### ❌ Tipo Incorrecto

```bash
❌ [ft] Solución de pantalla null en error al pagar
✅ [fx][BC-XXXXX] Payments: Agregar validación null en navigation context

❌ [ft][BC-XXXXX] Fix bug en login
✅ [fx][BC-XXXXX] Auth: Agregar null check en WebViewController

❌ [tt][BC-XXXXX] Nueva funcionalidad de pagos
✅ [ft][BC-XXXXX] Payments: Implementar funcionalidad de guardar favorito
```

**Regla:** Si corrige un bug, es `fx`. Si agrega funcionalidad nueva, es `ft`.

---

### ❌ Uso de Diminutivos

```bash
❌ [cr][BC-63538] Cards: Ajustar txt en español
✅ [cr][BC-63538] Cards: Ajustar texto español en banner de solicitud de tarjeta

❌ [fx][BC-XXXXX] Auth: Corregir btn de login
✅ [fx][BC-XXXXX] Auth: Corregir botón de login en pantalla principal

❌ [tt][BC-XXXXX] App: Actualizar cfg de ambientes
✅ [tt][BC-XXXXX] App: Actualizar configuración de ambientes
```

**Regla:** NO usar txt, btn, cfg, etc. Escribir las palabras completas.

---

### ❌ Descripción del Bug en lugar del Fix

```bash
❌ [fx][BC-XXXXX] Login: Bug cuando usuario no existe
✅ [fx][BC-XXXXX] Auth: Agregar validación de usuario existente en login

❌ [fx][BC-76054] Solicitudes: Error de inicialización de cliente
✅ [fx][BC-76054] Solicitudes: Usar cliente existente de NewRelic para evitar reinicialización

❌ [fx][BC-99642] Solicitudes: App crashea al cerrar error
✅ [fx][BC-99642] Solicitudes: Agregar validación null de WebViewController en botón retroceso
```

**Regla:** Describir QUÉ se cambió, NO qué bug había.

---

### ❌ Descripción Vaga

```bash
❌ [fx][BC-XXXXX] Payments: Ajustes varios
✅ [fx][BC-76561] Payments: Evitar llamado innecesario al endpoint de facturas para pago solo

❌ [tt][BC-XXXXX] App: Cambios menores
✅ [tt][BC-104089] App: Agregar header x-device-id a headers globales

❌ [rf][BC-XXXXX] Auth: Refactor
✅ [rf][BC-76880] Auth: Separar estado de error de flujos de biometría facial
```

**Regla:** La descripción debe ser específica sobre QUÉ cambió.

---

### ❌ Falta Módulo

```bash
❌ [fx][BC-XXXXX] Agregar validación null
✅ [fx][BC-103820] Tarjetas: Agregar validación null en checkIfFormIsFilled()

❌ [tt][BC-98402] Version 1.6.0-alpha.10
✅ [tt][BC-98402] App: Version 1.6.0-alpha.10

❌ [ft][BC-XXXXX] Guardar favoritos
✅ [ft][BC-35367] Payments: Guardar favorito en flujo de pago de servicios
```

**Regla:** Siempre incluir el módulo donde se hizo el cambio.

---

## 🔍 Casos Especiales

### Version Bumps
```bash
[tt][BC-XXXXX] App: Version 1.6.0-alpha.10
[tt][BC-XXXXX] App: Version 1.5.0-rc.3
```

### Actualización de Dependencias
```bash
[tt][BC-99660] CDPs: Actualizar versión a ^2.0.0-alpha.1
[tt][BC-XXXXX] App: Actualizar bancadigital_bm_cards a 1.2.0
```

### Múltiples Módulos Afectados
```bash
[ft][BC-XXXXX] App/Auth: Integrar biometría facial en login
[fx][BC-XXXXX] Cards/Payments: Corregir flujo de pago de tarjetas
```

### Cherry-picks a Release Branches
```bash
[fx][BC-XXXXX] Auth: Agregar validación null en context.mounted (cherry-pick)
```
*(Opcional mencionar cherry-pick en descripción)*

---

## 🛠️ Validación de Commits

### Checklist Pre-Commit:

- [ ] Tipo es uno de: ft, fx, tt, rf, cr, wr, hf, poc, devops
- [ ] Ticket ID tiene formato BC-XXXXX (típicamente 5-6 dígitos)
- [ ] Módulo está presente y corresponde con archivos
- [ ] Descripción es específica, no vaga
- [ ] NO hay diminutivos (txt, btn, cfg)
- [ ] Describe QUÉ cambió, NO qué bug había
- [ ] Ortografía y gramática correctas

---

## 🚨 Errores Comunes Identificados en 4,500 PRs

### Top 5 Errores:

1. **Tipo incorrecto** (30% de correcciones)
   - Usar `ft` en lugar de `fx` para bugs
   - Usar `ft` en lugar de `tt` para tareas técnicas

2. **Uso de diminutivos** (25% de correcciones)
   - txt, btn, cfg, etc.

3. **Descripción del bug vs el fix** (20% de correcciones)
   - "Bug cuando X" → "Agregar validación para X"

4. **Falta de módulo** (15% de correcciones)
   - No especificar dónde se hizo el cambio

5. **Descripción vaga** (10% de correcciones)
   - "Ajustes varios", "Cambios menores"

---

## 📚 Referencias

- **Branching Strategy:** `/docs/collaboration/branching_strategy_and_versioning.md`
- **Azure DevOps:** Tickets en formato BC-XXXXX
- **Code Reviews:** Validación automática del formato en PRs

---

## 🎓 Ejemplos de Correcciones Reales

Estas son correcciones reales solicitadas en code reviews:

### Caso 1: Ernesto Abreu
```bash
❌ "Este PR es una Tarea Técnica, no una feature"
   [ft][BC-67797] Login: Registrar eventos al aceptar contrato

✅ [tt][BC-67797] Login: Registrar TapEvents en NewRelic al Aceptar/Rechazar contrato Servicios Digitales
```

### Caso 2: Fabiana Hurtado
```bash
❌ "Ajustar commit message al formato con el que venimos trabajando"
   [fix] Solucionar null pointer en pago

✅ [fx][BC-XXXXX] Payments: Agregar validación null en payment context
```

### Caso 3: Jhon Muñoz
```bash
❌ "Mejorar commit message, ortografía y redacción"
   [ft][BC-XXXXX] se ajusta botón retroceso

✅ [fx][BC-XXXXX] Solicitudes: Ajustar botón retroceso en pantalla de error
```

---

**Analizado de:** 4,500+ PRs  
**Última actualización:** Febrero 2026  
**Tasa de correcciones:** ~30% de PRs requieren ajuste de commit message
