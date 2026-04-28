# Module Creation Templates

Templates reutilizables para generación de Feature Modules en Flutter.

## 📂 Estructura

```
templates/
├── README.md (este archivo)
├── module_definition.dart.template   # Module definition class
├── navigation.dart.template          # Navigation configuration
├── tests/                            # Templates de testing
│   ├── data_source_test.dart.template
│   ├── repository_test.dart.template
│   └── view_model_test.dart.template
├── advanced/                         # Casos avanzados
│   └── workflow_enum.dart.template
├── data/                             # Capa de datos
│   ├── dto.dart.template
│   └── cache.dart.template
└── ui/                               # Capa de UI
    └── view_model_state.dart.template
```

---

## 🎯 Cómo Usar los Templates

### Paso 1: Identificar Placeholders

Cada template tiene placeholders que deben ser reemplazados:

| Placeholder | Descripción | Ejemplo |
|-------------|-------------|---------|
| `{ModuleName}` | Nombre del módulo (PascalCase) | `Loans` |
| `{moduleName}` | Nombre del módulo (camelCase) | `loans` |
| `{module_name}` | Nombre del módulo (snake_case) | `loans` |
| `{module-name}` | Nombre del módulo (kebab-case) | `loans` |
| `{Entity}` | Nombre de la entity (PascalCase) | `Loan` |
| `{entity}` | Nombre de la entity (snake_case) | `loan` |
| `{Screen}` | Nombre de la pantalla (PascalCase) | `LoanList` |
| `{screen}` | Nombre de la pantalla (snake_case) | `loan_list` |
| `{Workflow}` | Nombre del workflow (PascalCase) | `LoanRequest` |
| `{workflow}` | Nombre del workflow (snake_case) | `loan_request` |

### Paso 2: Aplicar Transformaciones

```bash
# Ejemplo: Crear test de ViewModel para módulo "loans"
# Input:  templates/tests/view_model_test.dart.template
# Output: test/ui/loan_list/view_model/loan_list_view_model_test.dart

Reemplazos:
{Screen} → LoanList
{screen} → loan_list
{ModuleName} → Loans
{moduleName} → loans
{module_name} → loans
{Entity} → Loan
{entity} → loan
```

### Paso 3: Crear Archivo

```bash
# Copiar template
cat templates/tests/view_model_test.dart.template > \
    test/ui/loan_list/view_model/loan_list_view_model_test.dart

# Ejecutar reemplazos (ejemplo con sed)
sed -i '' 's/{Screen}/LoanList/g' test/ui/.../loan_list_view_model_test.dart
sed -i '' 's/{screen}/loan_list/g' test/ui/.../loan_list_view_model_test.dart
# ... etc
```

---

## 📋 Templates Disponibles

### 🏗️ Architecture Templates

#### `module_definition.dart.template`
**Uso:** Clase ModuleDefinition que extiende Module<L>

**Incluye:**
- ✅ Implementación de getLocalizationDelegate()
- ✅ Implementación de getRouterConfig()
- ✅ Placeholder para redirect rules (3 opciones)
- ✅ Documentación inline de patrones Goals/Transfers
- ✅ Imports correctos de feature_commons

**Opciones de Redirect:**
- **Opción A (Goals pattern)**: getRouteRedirectionFlags() con Map<String, String>
- **Opción B (Transfers pattern)**: redirectRules() con List<RedirectRule>
- **Opción C (Sin redirects)**: Comentario explicando que no se necesitan

**Cuándo usar:**
- Siempre al crear un Feature Module
- Requerido por convención Module Pattern

**Placeholders:**
- `{ModuleName}`, `{module_name}`, `REDIRECT_RULES_PLACEHOLDER`

**Ubicación final:**
`lib/module_definition/{module_name}_module_definition.dart`

**Registro en main.dart:**
```dart
final moduleManager = ModuleManager()
  ..registerModule({ModuleName}ModuleDefinition());
```

---

#### `navigation.dart.template`
**Uso:** Archivo de configuración de navegación del módulo

**Incluye:**
- ✅ Constantes de rutas (paths y names)
- ✅ Constantes de parámetros de ruta
- ✅ RouteObserver para lifecycle tracking (opcional)
- ✅ Lista routerConfig con GoRoute configurados
- ✅ Helper methods para navegación
- ✅ Comentarios para expansión según complejidad

**Patrones por complejidad:**
- **Simple (1-2 screens)**: Lobby + Detail routes
- **Medium (3-5 screens)**: + Child routes con tabs
- **Complex (6+ screens)**: Sub-navigation imports

**Cuándo usar:**
- Siempre al crear un Feature Module
- Base para definir todas las rutas del módulo

**Placeholders:**
- `{ModuleName}`, `{module_name}`, `{Entity}`, `{entity}`, `{Screen}`, `{screen}`
- `ADD_MORE_ROUTES_HERE`, `ADD_MORE_PARAMS_HERE`, `ADD_MORE_NAVIGATION_METHODS_HERE`

**Ubicación final:**
`lib/navigation/{module_name}_navigation.dart`

---

### 🧪 Testing Templates

#### `tests/data_source_test.dart.template`
**Uso:** Test de DataSource con ApiResponseHandlerMixin

**Incluye:**
- ✅ Mockito @GenerateMocks
- ✅ Tests de success/error/empty
- ✅ Verificación de ApiResponse.when()
- ✅ Patrón AAA (Arrange-Act-Assert)

**Cuándo usar:**
- Siempre que generes un DataSource

**Placeholders:**
- `{ModuleName}`, `{moduleName}`, `{module_name}`, `{Entity}`, `{entity}`

---

#### `tests/repository_test.dart.template`
**Uso:** Test de Repository con mappers

**Incluye:**
- ✅ Mock de DataSource y Mapper
- ✅ Tests de transformación DTO → Entity
- ✅ Manejo de errores
- ✅ Casos empty

**Cuándo usar:**
- Siempre que generes un Repository

**Placeholders:**
- `{ModuleName}`, `{moduleName}`, `{Entity}`, `{entity}`

---

#### `tests/view_model_test.dart.template`
**Uso:** Test de ViewModel con AsyncNotifier

**Incluye:**
- ✅ ProviderContainer con overrides
- ✅ Listener pattern para state transitions
- ✅ Tests de loading/success/error
- ✅ Test de refresh()
- ✅ Mock helper class

**Cuándo usar:**
- Siempre que generes un ViewModel con AsyncNotifier

**Placeholders:**
- `{Screen}`, `{screen}`, `{ModuleName}`, `{moduleName}`, `{Entity}`

---

### 🚀 Advanced Templates

#### `advanced/workflow_enum.dart.template`
**Uso:** Dual Enum Pattern para workflows

**Incluye:**
- ✅ Enum de Steps con WorkflowStep interface
- ✅ Enum de Groups con WorkflowGroup interface
- ✅ Métodos nextStep(), previousStep()
- ✅ Métodos canGoBack(), isFinal(), progress()
- ✅ Extensions para routePath y screenName

**Cuándo usar:**
- Flujos con múltiples steps/pantallas
- Regla #1 del PR: "Usar workflows para steps"

**Placeholders:**
- `{Workflow}`, `{workflow}`, `{ModuleName}`, `{module-name}`

**Importante:**
- Ajustar steps según flujo de negocio
- Ubicar en: `lib/ui/workflows/`

---

### 💾 Data Templates

#### `data/dto.dart.template`
**Uso:** DTO con Freezed + JsonSerializable

**Incluye:**
- ✅ @freezed annotation
- ✅ Part directives para generated files
- ✅ Constructor factory const
- ✅ fromJson factory
- ✅ Comentarios TODO para campos

**Cuándo usar:**
- Siempre para DTOs (no usar solo @JsonSerializable)

**Placeholders:**
- `{Entity}`, `{entity}`, `{module_name}`

**Importante:**
- NO agregar lógica de negocio
- Solo conversión pura JSON ↔ DTO

---

#### `data/cache.dart.template`
**Uso:** Cache Interface + InMemory implementation

**Incluye:**
- ✅ Interface con métodos básicos
- ✅ Singleton InMemoryCache
- ✅ TTL de 5 minutos
- ✅ Cache por lista y por ID
- ✅ Método isValid()

**Cuándo usar:**
- Respuesta "In-Memory avanzado" en pregunta #8
- Cuando necesites cache sofisticado (patrón Transfers)

**Placeholders:**
- `{Entity}`, `{entity}`

**Importante:**
- Llamar clear() cuando se modifiquen datos
- TTL configurable según necesidades

---

### 🎨 UI Templates

#### `ui/view_model_state.dart.template`
**Uso:** State class consolidado para ViewModel

**Incluye:**
- ✅ Clase State con Equatable
- ✅ Múltiples propiedades consolidadas
- ✅ Métodos copyWith(), toLoading(), toSuccess(), toError()
- ✅ Clase Filter optional
- ✅ Factories para initial() y empty()

**Cuándo usar:**
- ViewModels con estado complejo
- Para evitar proliferación de providers (regla #7)
- Alternativa a múltiples StateProviders

**Placeholders:**
- `{Screen}`, `{Entity}`

**Importante:**
- Usar `Notifier<{Screen}State>` en lugar de StateNotifier
- Máximo 15 providers por módulo

---

## 🔧 Automatización con Scripts

### Script de Generación (ejemplo)

```bash
#!/bin/bash
# generate_from_template.sh

MODULE_NAME=$1        # loans
ENTITY_NAME=$2        # loan
SCREEN_NAME=$3        # loan_list
TEMPLATE=$4           # view_model_test

# PascalCase conversions
MODULE_PASCAL=$(echo $MODULE_NAME | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^\([a-z]\)/\U\1/')
ENTITY_PASCAL=$(echo $ENTITY_NAME | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^\([a-z]\)/\U\1/')
SCREEN_PASCAL=$(echo $SCREEN_NAME | sed 's/_\([a-z]\)/\U\1/g' | sed 's/^\([a-z]\)/\U\1/')

# camelCase conversions
MODULE_CAMEL=$(echo $MODULE_NAME | sed 's/_\([a-z]\)/\U\1/g')

# kebab-case
MODULE_KEBAB=$(echo $MODULE_NAME | tr '_' '-')

# Read template
TEMPLATE_FILE="templates/tests/${TEMPLATE}.dart.template"
OUTPUT_FILE="test/ui/${SCREEN_NAME}/view_model/${SCREEN_NAME}_view_model_test.dart"

# Apply transformations
cat $TEMPLATE_FILE | \
  sed "s/{ModuleName}/$MODULE_PASCAL/g" | \
  sed "s/{moduleName}/$MODULE_CAMEL/g" | \
  sed "s/{module_name}/$MODULE_NAME/g" | \
  sed "s/{module-name}/$MODULE_KEBAB/g" | \
  sed "s/{Entity}/$ENTITY_PASCAL/g" | \
  sed "s/{entity}/$ENTITY_NAME/g" | \
  sed "s/{Screen}/$SCREEN_PASCAL/g" | \
  sed "s/{screen}/$SCREEN_NAME/g" > $OUTPUT_FILE

echo "✅ Generated: $OUTPUT_FILE"
```

**Uso:**
```bash
./generate_from_template.sh loans loan loan_list view_model_test
```

---

## ✅ Checklist de Uso

Cuando uses un template:

- [ ] Identificar todos los placeholders necesarios
- [ ] Aplicar transformaciones (PascalCase, camelCase, snake_case, kebab-case)
- [ ] Crear archivo en la ubicación correcta
- [ ] Revisar TODOs en el código generado
- [ ] Ejecutar `dart format` en el archivo generado
- [ ] Ejecutar `dart fix --apply` si hay warnings
- [ ] Agregar imports faltantes si los hay
- [ ] Ejecutar tests para verificar que compila

---

## 📚 Referencias

- **SKILL.md**: Workflow principal de creación de módulos
- **Goals Module**: Referencia para testing patterns
- **Transfers Module**: Referencia para cache avanzado
- **Core Data**: ApiResponse, RedirectRule, WorkflowStep/Group

---

**Versión:** 1.0  
**Última actualización:** 26 de marzo de 2026  
**Mantenido por:** Chapter Lead Mobile
