# Design System Patterns

Patrones del Design System homologado (BDS - Bancadigital Design System) identificados en code reviews del proyecto.

---

## 🎨 Componentes Homologados

### Spacing

**Problema:** Uso inconsistente de espaciado con `SizedBox`.

```dart
// ❌ INCORRECTO - No usar SizedBox directamente
Column(
  children: [
    Widget1(),
    SizedBox(height: 16),
    Widget2(),
    SizedBox(height: 24),
    Widget3(),
  ],
)

// ✅ CORRECTO - Usar constantes del DS
Column(
  children: [
    Widget1(),
    Spacing.vertical16,
    Widget2(),
    Spacing.vertical24,
    Widget3(),
  ],
)
```

**Opciones disponibles:**
```dart
// Vertical
Spacing.vertical4
Spacing.vertical8
Spacing.vertical12
Spacing.vertical16
Spacing.vertical24
Spacing.vertical32
Spacing.vertical40
Spacing.vertical48

// Horizontal
Spacing.horizontal4
Spacing.horizontal8
Spacing.horizontal12
Spacing.horizontal16
Spacing.horizontal24
Spacing.horizontal32
```

**Casos Reales:**
```dart
// ✅ Correcto en el repositorio
Spacing.vertical16  // 16px vertical
Spacing.horizontal24  // 24px horizontal
```

---

### Navigation (GoRouter)

**Problema:** Uso de `Navigator` en lugar de `GoRouter`.

```dart
// ❌ INCORRECTO - No usar Navigator directamente
onPressed: () {
  Navigator.pop(context);
  Navigator.pushNamed(context, '/route');
  Navigator.pushReplacementNamed(context, '/route');
}

// ✅ CORRECTO - Usar GoRouter context extensions
onPressed: () {
  context.pop();
  context.push('/route');
  context.pushReplacement('/route');
  context.pushNamed('routeName');
}
```

**Navegación con parámetros:**
```dart
// ✅ Con path parameters
context.push('/cards/$cardId');

// ✅ Con named routes y extra
context.pushNamed(
  'cardDetail',
  pathParameters: {'id': cardId},
  extra: cardData,
);

// ✅ Navigate and remove until
context.go('/home');
```

**Casos Reales del Repositorio:**
```dart
// PR #4985 - Correcto uso de GoRouter
context.pop();
context.push('/success');
context.pushNamed(prePasswordRecovery, extra: {'userName': userName});
```

---

### Accordions

**Problema:** Uso de componentes deprecados del DS.

```dart
// ❌ DEPRECADO - No usar
BacMoleculeContainmentAccordion.externalOpen(
  isOpen: _isOpen,
  onToggle: (value) => setState(() => _isOpen = value),
  title: 'Título',
  child: Content(),
)

// ✅ HOMOLOGADO - Usar nuevo componente
Accordion(
  isOpen: _isOpen,
  onToggle: (value) => setState(() => _isOpen = value),
  title: 'Título',
  child: Content(),
)
```

**Con Riverpod:**
```dart
// ✅ Integración con provider
final isOpen = ref.watch(accordionVisibilityProvider);

Accordion(
  isOpen: isOpen,
  onToggle: (value) {
    ref.read(accordionVisibilityProvider.notifier).state = value;
  },
  title: 'Transacciones Pendientes',
  child: PendingTransactionsList(),
)
```

**Caso Real:**
```dart
// PR #4979 - Migración de accordion
// accounts/lib/ui/pending_transactions/widgets/pending_transactions_section.dart

// ❌ Antes
BacMoleculeContainmentAccordion.externalOpen(...)

// ✅ Después
Accordion(
  isOpen: ref.watch(accordionVisibilityProvider),
  onToggle: (value) => ref.read(accordionVisibilityProvider.notifier).state = value,
  child: PendingTransactionsList(),
)
```

---

## 🚫 Anti-Patterns a Evitar

### 1. Nested Widgets Profundos

**Problema:** Widgets anidados > 4 niveles causan código ilegible.

```dart
// ❌ ANTI-PATTERN - Demasiado anidado
Widget build(BuildContext context) {
  return Column(
    children: [
      Container(
        padding: EdgeInsets.all(16),
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(...),
                child: Column(
                  children: [
                    Container(
                      padding: EdgeInsets.all(8),
                      child: Text('...')  // 6 niveles!
                    )
                  ]
                )
              )
            )
          ]
        )
      )
    ]
  );
}

// ✅ PATRÓN - Extraer a widgets privados
Widget build(BuildContext context) {
  return Column(
    children: [
      _buildHeader(),
      _buildContent(),
      _buildFooter(),
    ],
  );
}

Widget _buildHeader() {
  return Container(
    padding: const EdgeInsets.all(16),
    child: _buildHeaderRow(),
  );
}

Widget _buildHeaderRow() {
  return Row(
    children: [
      Expanded(child: _buildTitle()),
      _buildActions(),
    ],
  );
}

Widget _buildTitle() => Text('Título');
Widget _buildActions() => IconButton(...);
```

**Caso Real:**
```dart
// Comentario en code review - PR #3999
"Organizar un poco mejor el codigo, separar en widgets privados si es necesario,
para evitar tanto nested widgets y que sean métodos tan largos."
```

---

### 2. No Especializar Wrappers del DS

**Problema:** Crear wrappers especializados innecesarios.

```dart
// ❌ ANTI-PATTERN - Wrapper especializado innecesario
class MyCustomButton extends StatelessWidget {
  final VoidCallback onPressed;
  final String text;
  
  const MyCustomButton({required this.onPressed, required this.text});
  
  @override
  Widget build(BuildContext context) {
    return BacButton(  // Solo wrapper sin lógica adicional
      onPressed: onPressed,
      child: Text(text),
    );
  }
}

// ✅ PATRÓN - Usar componente DS directamente
BacButton(
  onPressed: () => handlePress(),
  child: Text('Continuar'),
)
```

**Caso Real:**
```dart
// Comentario en code review
"Revisar wrapper del DS no esta especializando el uso."
```

**Cuándo sí crear wrappers:**
- ✅ Cuando agregan lógica de negocio significativa
- ✅ Cuando combinan múltiples componentes del DS
- ✅ Cuando agregan comportamiento específico del dominio

---

### 3. Hardcodear Valores

**Problema:** Valores mágicos en lugar de constantes del DS.

```dart
// ❌ ANTI-PATTERN - Valores hardcodeados
Container(
  padding: EdgeInsets.all(16),  // ¿De dónde sale 16?
  margin: EdgeInsets.symmetric(horizontal: 24),  // ¿Y 24?
)

// ✅ PATRÓN - Usar constantes del DS
Container(
  padding: BacSpacing.padding16,
  margin: BacSpacing.marginHorizontal24,
)

// O con Spacing widgets
Padding(
  padding: BacSpacing.padding16,
  child: Content(),
)
```

---

## 📐 Patrones de Layout

### Responsive Design

```dart
// ✅ Usar constraints del DS
Container(
  constraints: BacConstraints.maxWidth,  // Definido en DS
  child: Content(),
)

// ✅ Spacing responsive
LayoutBuilder(
  builder: (context, constraints) {
    return Padding(
      padding: constraints.maxWidth > 600
        ? BacSpacing.padding24
        : BacSpacing.padding16,
      child: Content(),
    );
  },
)
```

### SafeArea y Padding

```dart
// ✅ Considerar SafeArea
Scaffold(
  body: SafeArea(
    child: Padding(
      padding: BacSpacing.padding16,
      child: Content(),
    ),
  ),
)
```

---

## 🎯 Componentes Comunes del DS

### Buttons

```dart
// Primary button
BacButton(
  onPressed: () {},
  child: Text('Continuar'),
)

// Secondary button
BacButtonSecondary(
  onPressed: () {},
  child: Text('Cancelar'),
)

// Icon button
BacIconButton(
  icon: Icons.close,
  onPressed: () {},
)

// Overlay ghost button (transparente)
BacOverlayGhostButton(
  onPressed: () {},
  child: BacSvgIcon(icon: AppIcons.close),
)
```

**Caso Real:**
```dart
// PR #4947 - Uso correcto de overlay ghost button
// auth/lib/ui/commons/dfa_flows/otp_blocked/otp_blocked_page.dart

BacOverlayGhostButton(
  onPressed: () => handleClose(),
  child: BacSvgIcon(icon: AppIcons.close),
)
```

---

### Input Fields

```dart
// Text field del DS
BacTextField(
  controller: _controller,
  label: 'Usuario',
  hint: 'Ingrese su usuario',
)

// Con validación
BacTextField(
  controller: _controller,
  label: 'Email',
  validator: (value) => EmailValidator.validate(value),
  errorText: errorMessage,
)
```

---

### Cards y Containers

```dart
// Card del DS
BacCard(
  child: Padding(
    padding: BacSpacing.padding16,
    child: Content(),
  ),
)

// Official Credit Card (componente específico)
OfficialCreditCard(
  cardNumber: '1234',
  cardHolder: 'John Doe',
  balance: '\$1,234.56',
  internationalAmount: showInternational ? '\$567.89' : null,
)
```

**Caso Real:**
```dart
// PR #4980 - Uso de OfficialCreditCard
// cards/lib/ui/cards_section_consolidated/view/widgets/cards_section.dart

OfficialCreditCard(
  cardNumber: card.number,
  cardHolder: card.holder,
  localAmount: card.localBalance,
  internationalAmount: card.showInternationalBalance 
    ? card.internationalBalance 
    : null,
)
```

---

### Headers y AppBars

```dart
// ❌ Usar BacAppBar.transparent deprecado
BacAppBar.transparent(
  leading: BacIconButton.overlayGhost(...),
)

// ✅ Usar Header component
Header(
  leading: BacOverlayGhostButton(
    onPressed: () => context.pop(),
    child: BacSvgIcon(icon: AppIcons.back),
  ),
)
```

**Caso Real:**
```dart
// PR #4947 - Migración de BacAppBar a Header
// auth/lib/ui/commons/dfa_flows/otp_blocked/otp_blocked_page.dart

// ❌ Antes
BacAppBar.transparent(
  leading: BacIconButton.overlayGhost(
    onPressed: () => handleClose(),
    icon: Icons.close,
  ),
)

// ✅ Después  
Header(
  leading: BacOverlayGhostButton(
    onPressed: () => handleClose(),
    child: BacSvgIcon(icon: AppIcons.close),
  ),
)
```

---

## 🔄 Migraciones del DS

### Checklist para Migraciones:

Cuando migras de componentes deprecados:

- [ ] Identificar componente deprecado
- [ ] Buscar reemplazo homologado en DS
- [ ] Verificar API del nuevo componente
- [ ] Actualizar imports
- [ ] Probar visualmente el cambio
- [ ] Agregar evidencia en PR (screenshots antes/después)

---

## 📚 Recursos del DS

### Packages del DS:
```yaml
dependencies:
  bancadigital_design_system: ^X.X.X
```

### Imports Comunes:
```dart
import 'package:bancadigital_design_system/bancadigital_design_system.dart';
```

---

## 🎓 Casos de Estudio

### Caso 1: Migración de Accordion (PR #4979)
**Antes:**
```dart
BacMoleculeContainmentAccordion.externalOpen(
  isOpen: _isOpen,
  onToggle: (value) => setState(() => _isOpen = value),
  child: Content(),
)
```

**Después:**
```dart
final isOpen = ref.watch(accordionVisibilityProvider.notifier).state;

Accordion(
  isOpen: isOpen,
  onToggle: (value) => ref.read(accordionVisibilityProvider.notifier).state = value,
  child: Content(),
)
```

**Beneficios:**
- Componente más moderno
- Mejor integración con Riverpod
- Lifecycle management mejorado con autoDispose

---

### Caso 2: Spacing Consistency (Múltiples PRs)
**Problema:** Inconsistencia en espaciado.

**Solución:** Migración masiva a Spacing del DS.

```dart
// ❌ Antes (inconsistente)
SizedBox(height: 16)
SizedBox(height: 15)  // ⚠️ No estándar
Container(margin: EdgeInsets.all(20))  // ⚠️ No estándar

// ✅ Después (consistente)
Spacing.vertical16
Spacing.vertical16  // Siempre 16
Spacing.all24  // Siempre múltiplo de 4
```

---

## ⚠️ Warnings Comunes

### 1. No usar context después de async sin mounted
```dart
// Aplica también a componentes del DS
onPressed: () async {
  await doSomething();
  if (!mounted) return;  // ✅ Verificar
  showBacDialog(context, ...);  // Componente del DS
}
```

### 2. No hardcodear colores
```dart
// ❌ Hardcodeado
Container(color: Color(0xFF1234AB))

// ✅ Usar tema del DS
Container(color: Theme.of(context).primaryColor)
Container(color: BacColors.primary)
```

### 3. Usar widgets del DS consistentemente
```dart
// ❌ Mezclar widgets nativos con DS
Column(
  children: [
    BacButton(...),  // DS
    ElevatedButton(...),  // ❌ Nativo
  ],
)

// ✅ Consistente con DS
Column(
  children: [
    BacButton(...),
    BacButtonSecondary(...),  // Todo del DS
  ],
)
```

---

**Analizado de:** 4,500+ PRs  
**Última actualización:** Febrero 2026  
**Componentes deprecados identificados:** 15+  
**Patrones documentados:** 25+
