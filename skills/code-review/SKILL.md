---
name: code-review
description: "Experto en code review de Flutter siguiendo estándares BAC. Use when: revisar código, code review, validar cambios, verificar estándares, review de Flutter, validar lifecycle, verificar null safety."
applyTo:
  - "**/*.dart"
---

# Code Review Expert - Flutter BAC Standards

Reviso código Flutter enfocándome en los estándares críticos de bancadigital-bm-app.

---

## 🎯 Aspectos Críticos a Revisar

### 1. Lifecycle Management (PRIORIDAD ALTA)

#### ✅ Verificaciones Obligatorias:

**super.initState() SIEMPRE PRIMERO:**
```dart
// ❌ INCORRECTO - super después de lógica
@override
void initState() {
  _controller.text = widget.value;
  super.initState();  // ⚠️ DEBE SER PRIMERO
}

// ✅ CORRECTO
@override
void initState() {
  super.initState();  // ✅ SIEMPRE PRIMERO
  _controller.text = widget.value;
}
```

**context.mounted antes de navegación asíncrona:**
```dart
// ❌ INCORRECTO - crash potencial
Future<void> _handleSubmit() async {
  await submitData();
  context.push('/success');  // ⚠️ Widget puede estar disposed
}

// ✅ CORRECTO
Future<void> _handleSubmit() async {
  await submitData();
  if (!mounted) return;  // ✅ VERIFICAR SIEMPRE
  context.push('/success');
}
```

**autoDispose en providers temporales:**
```dart
// ❌ INCORRECTO - memory leak en providers de pantalla
final dataProvider = StateNotifierProvider<DataVM, DataState>((ref) {
  return DataVM();
});

// ✅ CORRECTO - para datos temporales/de pantalla
final dataProvider = StateNotifierProvider.autoDispose<DataVM, DataState>((ref) {
  return DataVM();
});

// ℹ️ Sin autoDispose solo para datos compartidos/persistentes globales
```

**Controllers disposed correctamente:**
```dart
// ✅ CORRECTO
@override
void dispose() {
  _textController.dispose();
  _animationController.dispose();
  super.dispose();  // ✅ SIEMPRE AL FINAL en dispose
}
```

---

### 2. Navigation Patterns

#### ✅ Usar GoRouter (context extensions):
```dart
✅ context.pop()
✅ context.push('/route')
✅ context.pushNamed('routeName')
✅ context.go('/route')
```

#### ❌ Rechazar Navigator directo:
```dart
❌ Navigator.pop(context)
❌ Navigator.push(context, MaterialPageRoute(...))
❌ Navigator.of(context).push(...)
```

**Razón:** GoRouter es el estándar del proyecto y provee type-safe routing.

---

### 3. Null Safety

#### ✅ Validaciones defensivas:

```dart
// ✅ Usar ?? para defaults
final cards = ref.watch(cardsProvider) ?? [];

// ✅ Usar ?. para safe access
final name = user?.name ?? 'Unknown';

// ✅ Null checks antes de usar
if (controller != null) {
  controller.animateTo(0);
}

// ❌ RECHAZAR acceso directo sin validación
final cards = ref.watch(cardsProvider);
return ListView.builder(
  itemCount: cards.length,  // ⚠️ NPE si cards es null
);
```

---

### 4. Design System Compliance

#### ✅ Componentes Homologados:

```dart
// ✅ CORRECTO - Componente homologado
import 'package:bancadigital_bm_red_designsystem/accordion.dart';
Accordion(...)

// ❌ INCORRECTO - Wrapper especializado deprecated
BacMoleculeContainmentAccordion(...)
```

#### ✅ Spacing del Design System:

```dart
// ✅ CORRECTO - Usar Spacing del DS
import 'package:bancadigital_bm_red_designsystem/spacing.dart';

Column(
  children: [
    Widget1(),
    Spacing.vertical16,
    Widget2(),
  ],
)

// ❌ INCORRECTO - SizedBox manual
Column(
  children: [
    Widget1(),
    SizedBox(height: 16),  // ⚠️ Usar Spacing en su lugar
    Widget2(),
  ],
)
```

**Espaciados disponibles:**
- `Spacing.vertical4`, `Spacing.vertical8`, `Spacing.vertical12`, `Spacing.vertical16`, `Spacing.vertical24`
- `Spacing.horizontal4`, `Spacing.horizontal8`, etc.

---

### 5. Code Structure

#### ❌ Rechazar nested widgets excesivos (> 4 niveles):

```dart
// ❌ INCORRECTO - Nesting excesivo
return Container(
  child: Padding(
    child: Column(
      children: [
        Row(
          children: [
            Container(
              child: Padding(
                child: Column(  // ⚠️ > 4 niveles profundos
                  children: [...]
                ),
              ),
            ),
          ],
        ),
      ],
    ),
  ),
);

// ✅ CORRECTO - Extraer a widgets privados
return Column(
  children: [
    _buildHeader(),
    _buildContent(),
    _buildFooter(),
  ],
);

Widget _buildHeader() {
  return Row(...);
}
```

#### ✅ Métodos < 50 líneas cuando sea posible:

```dart
// ⚠️ Si un método supera 50 líneas, considerar:
// 1. Extraer submétodos
// 2. Mover lógica a ViewModel
// 3. Crear widgets privados
```

---

### 6. Testing Requirements

#### ✅ Tests OBLIGATORIOS para:

1. **ViewModels nuevos o modificados** (coverage ≥ 80%)
2. **Repositories nuevos** (coverage ≥ 75%)
3. **Utils/Helpers nuevos** (coverage ≥ 90%)

#### ✅ Naming convention:
```dart
test('should [resultado esperado] when [condición]', () {
  // Arrange
  // Act
  // Assert
});
```

#### ✅ Archivos terminan en `_test.dart` (NO `_tests.dart`):
```
✅ accounts_view_model_test.dart
❌ accounts_view_model_tests.dart
```

---

## 🚫 Checklist de Rechazo Automático

NO aprobar código que:

- [ ] Use `Navigator` en lugar de `context` extensions de GoRouter
- [ ] No valide `context.mounted` en navegación asíncrona
- [ ] Tenga `super.initState()` después de lógica de inicialización
- [ ] Tenga nested widgets > 4 niveles sin extraer a métodos/widgets
- [ ] Use `SizedBox` cuando debería usar `Spacing` del Design System
- [ ] Use wrappers deprecated del DS (ej: `BacMoleculeContainmentAccordion`)
- [ ] No tenga tests para ViewModels modificados
- [ ] No use `autoDispose` en providers de pantalla/temporales
- [ ] Tenga acceso directo a nullables sin validación (`??`, `?.`, `if`)

---

## 📋 Formato de Feedback

Cuando encuentres problemas, usa este formato:

```markdown
### ❌ [Categoría]: [Archivo]:[Línea]

**Problema:**
[Descripción del problema]

**Código actual:**
```dart
[snippet del código problemático]
```

**Sugerencia:**
```dart
[snippet del código correcto]
```

**Razón:**
[Por qué es importante este cambio]
```

---

## ✅ Formato de Aprobación

Cuando todo esté correcto:

```markdown
### ✅ Code Review Completado

**Aspectos validados:**
- [x] Lifecycle management correcto
- [x] Navigation usando GoRouter
- [x] Null safety adecuado
- [x] Design System compliance
- [x] Code structure apropiada
- [x] Tests incluidos (si aplica)

**Comentarios adicionales:**
[Cualquier sugerencia de mejora no bloqueante]

**Estado:** ✅ Aprobado para merge
```

---

## 🎓 Referencias

- [copilot-instructions.md](../copilot-instructions.md) - Convenciones globales
- [commit-conventions](../commit-conventions/SKILL.md) - Formato de commits
- [testing-unified](../testing-unified/SKILL.md) - Testing standards

---

**Versión:** 1.0  
**Última actualización:** 25 de marzo de 2026  
**Basado en:** Patrones de 4,500+ PRs y Flutter best practices
