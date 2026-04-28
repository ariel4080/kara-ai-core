# ✅ PR Template Checklist

**Este documento es una guía rápida para validar que un PR siga el formato oficial.**

## 🚨 REGLA DE ORO

**SIEMPRE leer `.github/pull_request_template.md` con `read_file` ANTES de crear cualquier PR.**

---

## 📋 Checklist Pre-Creación

Antes de ejecutar `gh pr create`, verificar:

- [ ] ¿Leí el template con `read_file .github/pull_request_template.md`?
- [ ] ¿Estoy usando el contenido EXACTO del template?
- [ ] ¿Solo tengo las 3-4 secciones oficiales?
- [ ] ¿NO agregué secciones extra?
- [ ] ¿NO usé emojis en los headers?
- [ ] ¿Reemplacé los placeholders correctamente?
- [ ] ¿Eliminé la sección ADR si no aplica?
- [ ] ¿Preservé los comentarios HTML?
- [ ] ¿Preservé los bloques `> [!IMPORTANT]`?

---

## ✅ Secciones Permitidas (Template Oficial)

```markdown
## Descripción de este PR
<!-- Sin emoji -->

* Bullet 1
* Bullet 2

## Link de Historia del AzureBoards
<!-- Sin emoji -->

[AB#XXXXX](https://dev.azure.com/bacsansose/BAC/_workitems/edit/XXXXX)

## Link de ADR
<!-- SOLO si aplica - eliminar toda la sección si no aplica -->

Referencia [ADR](URL_DEL_ADR)

## Evidencias Visuales
<!-- Sin emoji -->

> [!IMPORTANT]
> - Imagen y/o video según corresponda
```

**Total de secciones:** 3 (sin ADR) o 4 (con ADR)

---

## ❌ Secciones NO Permitidas

Estas secciones **NO están en el template** y **NO deben agregarse:**

- ❌ `## 📋 Descripción` (con emoji)
- ❌ `## 🎯 Cambios Realizados`
- ❌ `### Documentación Principal` (sub-secciones)
- ❌ `## ✅ Checklist`
- ❌ `## 📊 Impacto`
- ❌ `## 🔍 Tipo de Cambio`
- ❌ `## 🏷️ Labels Recomendados`
- ❌ Cualquier otra sección personalizada

---

## 🔍 Validación del Formato

### Headers Correctos vs Incorrectos

| ❌ Incorrecto | ✅ Correcto |
|--------------|-------------|
| `## 📋 Descripción` | `## Descripción de este PR` |
| `## Descripción` | `## Descripción de este PR` |
| `## 🎯 Cambios` | (No existe esta sección) |
| `## Link del AzureBoards` | `## Link de Historia del AzureBoards` |
| `## 🔍 Evidencias` | `## Evidencias Visuales` |

### Links Correctos vs Incorrectos

| ❌ Incorrecto | ✅ Correcto |
|--------------|-------------|
| `[AB#12345](https://dev.azure.com/ORG-LAT-GSBD/Banca-Digital/...)` | `[AB#12345](https://dev.azure.com/bacsansose/BAC/...)` |
| `BC#12345` en el link | `AB#12345` en el link |
| Link sin formato markdown | `[AB#XXXXX](url completa)` |

---

## 🛠️ Reemplazo de Placeholders

**Desde el template:**
```markdown
[AB#XXXXX](https://dev.azure.com/bacsansose/BAC/_workitems/edit/XXXXX)
```

**Reemplazar:**
1. `XXXXX` → Número del ticket (ej: `105572`)

**Resultado:**
```markdown
[AB#105572](https://dev.azure.com/bacsansose/BAC/_workitems/edit/105572)
```

---

## 🎯 Ejemplo Completo Correcto

```markdown
## Descripción de este PR

* Corrección de estructura con headings markdown en documentación de agentes
* Actualización de '5 Skills' a '4 Skills' removiendo módulo no documentado
* Mejoras en jerarquía visual y navegación del documento

## Link de Historia del AzureBoards

[AB#105572](https://dev.azure.com/bacsansose/BAC/_workitems/edit/105572)

## Evidencias Visuales

> [!IMPORTANT]
> - Screenshot de la estructura mejorada del documento con headings correctos
> - Comparación ANTES/DESPUÉS de la jerarquía visual
```

**Nota:** Sección "Link de ADR" eliminada porque no aplica.

---

## 🚨 Validación Post-Creación

Después de crear el PR con `gh pr create`:

1. **Abrir el PR en el navegador:**
   ```bash
   gh pr view [número] --web
   ```

2. **Verificar visualmente:**
   - ✅ Headers sin emojis
   - ✅ Solo 3-4 secciones
   - ✅ Link de AzureBoards funciona
   - ✅ Bloques `> [!IMPORTANT]` se renderizan correctamente

3. **Si hay errores, editar inmediatamente:**
   ```bash
   gh pr edit [número] --body "contenido corregido"
   ```

---

## 📚 Referencias

- **Template oficial:** `.github/pull_request_template.md`
- **PR Assistant:** `.github/agents/pr-assistant.agent.md`
- **Leo Agent:** `.github/agents/leo.agent.md`

---

*Última actualización: 5 de marzo de 2026*
