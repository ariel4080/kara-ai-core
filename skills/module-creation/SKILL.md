---
name: module-creation
description: "Crea Feature Modules completos para Flutter siguiendo Clean Architecture + MVVM. Use when: crear módulo, nuevo feature, scaffold module, generar módulo Flutter, crear feature module."
---

# Module Creation - Flutter Feature Modules

Workflow interactivo para crear Feature Modules completos en bancadigital-bm-app siguiendo Clean Architecture + MVVM.

## 📦 Templates Disponibles

Este skill incluye **templates reutilizables** para generar código consistente:

- 🏗️ **Architecture**: Module Definition, Navigation
- 🧪 **Testing**: DataSource, Repository, ViewModel tests
- 🚀 **Advanced**: Workflow Enums
- 💾 **Data**: DTO con Freezed, Cache avanzado
- 🎨 **UI**: ViewModel State consolidado

📖 **Ver documentación completa**: `templates/README.md`

**Beneficios:**
- ✅ Código 100% consistente con Goals/Transfers patterns
- ✅ Tests robustos pre-configurados
- ✅ Placeholders automáticos para personalización
- ✅ Basado en arquitectura validada

---

## 🎯 Workflow Interactivo de Creación

Cuando el usuario solicite crear un módulo, sigo este flujo paso a paso:

### Paso 1: Recopilar Información

**Hago estas preguntas UNA POR UNA:**

#### 1. Nombre del módulo
```
¿Cuál es el nombre del módulo? (snake_case, singular, SIN prefijo bancadigital_bm_)

Ejemplos:
- yjcloans
- notifications
- goals  
- transfers
- wallet

IMPORTANTE: 
- Solo el nombre base (ej: "yjcloans")
- El prefijo "bancadigital-bm-" se agregará automáticamente

Nombre: _______
```

#### 2. Descripción breve
```
¿Qué funcionalidad tendrá este módulo?

Ejemplo: "Gestión de metas de ahorro del usuario"

Descripción: _______
```

#### 3. Endpoints/APIs necesarios (opcional)
```
¿Qué endpoints de API necesitará el módulo?

Ejemplos:
- GET /api/v1/goals
- POST /api/v1/goals
- DELETE /api/v1/goals/{id}

O escribe "por definir" si aún no los conoces.

Endpoints: _______
```

#### 4. Modelos principales
```
¿Qué modelos/entidades manejará el módulo?

Ejemplos:
- Goal (id, name, targetAmount, currentAmount)
- Notification (id, title, message, timestamp)

Modelos: _______
```

#### 5. Complejidad
```
¿Qué complejidad tiene el módulo?

1. Simple (1-2 screens, CRUD básico)
2. Medium (3-5 screens, flujos múltiples)
3. Complex (6+ screens, sub-features)

Selección: _______
```

#### 6. Ruta inicial (opcional)
```
¿Este módulo tiene una ruta inicial predeterminada?

Ejemplo: 
- '/accounts' para navegación directa a cuentas
- '/goals/list' para lista de metas

Escribe "ninguna" si no necesita una ruta inicial.

Ruta inicial: _______
```

#### 7. Localizaciones (opcional)
```
¿Este módulo necesitará traducciones/localizaciones propias?

Ejemplo: Si tiene textos específicos del dominio que no están en feature_commons

Opciones:
1. Sí - Generar delegate de localizaciones
2. No - Usar solo localizaciones compartidas

Selección: _______
```

#### 8. Estrategia de caché (opcional)
```
¿Este módulo necesita caché de datos?

Opciones:
1. Sin caché - Siempre fetch desde API
2. In-Memory simple - Cache en Repository con TTL (5 min)
3. In-Memory avanzado - Interface + Singleton con control granular
4. Persistent - SharedPreferences para datos UI
5. Secure - SecureStorage para datos sensibles

Selección: _______
```

#### 9. Control de acceso (opcional)
```
¿Este módulo requiere control de acceso/validaciones?

Ejemplos:
- Validar feature flags antes de acceder
- Verificar permisos/grants del usuario
- Validar sesión activa
- Restricciones basadas en país/segmento

Opciones:
1. Sí - Generar RedirectRule con validaciones
2. No - Acceso libre al módulo

Selección: _______

Si seleccionaste Sí, ¿qué validaciones necesita?
(feature flags / grants / sesión / custom): _______
```

---

### Paso 2: Generar Estructura Base

Basado en las respuestas, creo la estructura completa:

**IMPORTANTE - Convenciones de Nombres:**

1. **Carpeta del repositorio**: `bancadigital-bm-{module_name}/` (kebab-case con guiones)
2. **Package name**: `bancadigital_bm_{module_name}` (snake_case con underscores)
3. **Ubicación**: Al mismo nivel que `bancadigital-bm-app/`, NO dentro de él

**Ejemplo para módulo "yjcloans":**
- Carpeta: `bancadigital-bm-yjcloans/`
- Package: `bancadigital_bm_yjcloans`
- Path: `Repositorios/bancadigital-bm-yjcloans/`

```bash
# Estructura generada automáticamente
bancadigital-bm-{module_name}/          # ← Carpeta con prefijo "bancadigital-bm-"
├── lib/
│   ├── module_definition/
│   │   └── {module_name}_module_configuration.dart
│   ├── navigation/
│   │   └── {module_name}_navigation.dart
│   ├── data/
│   │   ├── api/
│   │   │   └── {module_name}_api.dart
│   │   ├── data_source/
│   │   │   └── dto/
│   │   │       └── {entity}_dto.dart
│   │   ├── providers/
│   │   │   └── {module_name}_repository_provider.dart
│   │   └── repository/
│   │       ├── {module_name}_repository_remote.dart
│   │       ├── mappers/
│   │       │   └── {entity}_mapper.dart
│   │       └── models/
│   │           └── {entity}_entity.dart
│   └── ui/
│       └── {screen_name}/
│           ├── views/
│           │   └── {screen_name}_page.dart
│           ├── view_model/
│           │   ├── {screen_name}_view_model.dart
│           │   └── {screen_name}_view_model_provider.dart
│           ├── params/  # Si recibe parámetros
│           └── widgets/  # Si tiene widgets específicos
├── test/
│   ├── data/
│   │   └── repository/
│   │       └── {module_name}_repository_remote_test.dart
│   └── ui/
│       └── {screen_name}/
│           └── view_model/
│               └── {screen_name}_view_model_test.dart
├── analysis_options.yaml
├── pubspec.yaml
├── README.md
└── CHANGELOG.md
```

---

### Paso 3: Generar Archivos de Configuración

#### pubspec.yaml

```yaml
name: bancadigital_bm_{module_name}    # ← CON prefijo bancadigital_bm_
description: "{description}"
version: 0.0.1
publish_to: none

environment:
  sdk: ">=3.7.2 <4.0.0"
  flutter: ">=3.29.3 <4.0.0"

dependencies:
  core_data:
    hosted: https://gsbd.jfrog.io/artifactory/api/pub/digital-lab-pub-local
    version: ^2.2.0-alpha.1
  feature_commons:
    hosted: https://gsbd.jfrog.io/artifactory/api/pub/digital-lab-pub-local
    version: ^2.2.0-alpha.1
  flutter:
    sdk: flutter
  equatable: ^2.0.5
  freezed_annotation: ^2.4.1
  json_annotation: ^4.9.0
  retrofit: ^4.1.0
  dio: ^5.4.3+1
  flutter_riverpod: ^2.5.1

dev_dependencies:
  flutter_test:
    sdk: flutter
  build_runner: ^2.4.9
  freezed: ^2.5.2
  json_serializable: ^6.7.1
  retrofit_generator: ^8.1.0
  mockito: ^5.4.4
  flutter_lints: ^3.0.2
```

#### analysis_options.yaml

```yaml
include: ../feature_commons/analysis_options.yaml
```

#### README.md

```markdown
# {ModuleName} Module

{Description}

## Features

- Feature 1
- Feature 2
- Feature 3

## APIs

{Endpoints listed}

## Models

{Models listed}

## Installation

Add to `melos.yaml`:
```yaml
packages:
  - bancadigital-bm-{module_name}  # ← Con prefijo
  - ./
```

Register in `ModuleManager`:
```dart
moduleManager.registerModule({ModuleName}Module());
```

## Usage

```dart
// Navigation
{ModuleName}Navigation.goToHome(context);
```

## Testing

```bash
flutter test
```

## Coverage

```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```
```

---

### Paso 4: Generar Código Base

**Para cada modelo identificado, genero:**

#### Entity (Domain Model)
```dart
// lib/data/repository/models/{entity}.dart
import 'package:equatable/equatable.dart';

class {Entity} extends Equatable {
  final String id;
  // Agregar campos según la descripción del usuario
  
  const {Entity}({
    required this.id,
  });
  
  @override
  List<Object?> get props => [id];
}
```

**IMPORTANTE:** NO usar sufijo "Entity" (ej: `Account`, no `AccountEntity`)

#### DTO (Data Transfer Object)

**📦 Template disponible**: `templates/data/dto.dart.template`

```dart
// lib/data/data_source/dto/{entity}_dto.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part '{entity}_dto.freezed.dart';
part '{entity}_dto.g.dart';

@freezed
class {Entity}Dto with _${Entity}Dto {
  const factory {Entity}Dto({
    required String id,
    // Agregar campos según la descripción del usuario
  }) = _{Entity}Dto;
  
  factory {Entity}Dto.fromJson(Map<String, dynamic> json) =>
      _${Entity}DtoFromJson(json);
}
```

**IMPORTANTE:** Usar `@freezed` proporciona:
- ✅ Inmutabilidad automática
- ✅ `copyWith()` generado
- ✅ `==` y `hashCode` automáticos
- ✅ `toString()` mejorado
- ✅ Integración con `json_serializable`

**💡 Tip**: El template incluye comentarios TODO y ejemplos de campos comunes.

#### Mapper
```dart
// lib/data/repository/mappers/{entity}_mapper.dart
import '../models/{entity}.dart';
import '../../data_source/dto/{entity}_dto.dart';

class {Entity}Mapper {
  {Entity} fromDtoToEntity({Entity}Dto dto) {
    return {Entity}(
      id: dto.id,
    );
  }
  
  {Entity}Dto fromEntityToDto({Entity} entity) {
    return {Entity}Dto(
      id: entity.id,
    );
  }
  
  List<{Entity}> fromDtosToEntities(List<{Entity}Dto> dtos) {
    return dtos.map(fromDtoToEntity).toList();
  }
}
```

**IMPORTANTE:** Mappers deben contener SOLO conversión, NO lógica de negocio ni filtrado.

#### API (Retrofit)
```dart
// lib/data/api/{module_name}_api.dart
import 'package:retrofit/retrofit.dart';
import 'package:dio/dio.dart';
import '../data_source/dto/{entity}_dto.dart';

part '{module_name}_api.g.dart';

@RestApi()
abstract class {ModuleName}Api {
  factory {ModuleName}Api(Dio dio, {String baseUrl}) = _{ModuleName}Api;
  
  // Generar endpoints según lo proporcionado
  @GET('/api/v1/{module_name}')
  @Headers({'API_VERSION': '1.0'})
  Future<List<{Entity}Dto>> get{Entities}();
  
  @POST('/api/v1/{module_name}')
  @Headers({'API_VERSION': '1.0'})
  Future<{Entity}Dto> create{Entity}(@Body() {Entity}Dto dto);
  
  @GET('/api/v1/{module_name}/{id}')
  @Headers({'API_VERSION': '1.0'})
  Future<{Entity}Dto> get{Entity}(@Path('id') String id);
}
```

#### DataSource (con ApiResponseHandlerMixin)
```dart
// lib/data/data_source/{module_name}_data_source.dart
import 'package:core_data/core_data.dart';
import '../api/{module_name}_api.dart';
import 'dto/{entity}_dto.dart';

abstract interface class {ModuleName}DataSource {
  Future<ApiResponse<List<{Entity}Dto>>> fetch{Entities}();
  Future<ApiResponse<{Entity}Dto>> create{Entity}({Entity}Dto dto);
  Future<ApiResponse<{Entity}Dto>> get{Entity}(String id);
}

class {ModuleName}DataSourceRemote 
    with ApiResponseHandlerMixin 
    implements {ModuleName}DataSource {
  final {ModuleName}Api _api;
  
  {ModuleName}DataSourceRemote({required {ModuleName}Api api}) : _api = api;
  
  @override
  ApiLogger get logger => ConsoleApiLogger();
  
  @override
  Future<ApiResponse<List<{Entity}Dto>>> fetch{Entities}() async {
    return await executeApiCall(_api.get{Entities}());
  }
  
  @override
  Future<ApiResponse<{Entity}Dto>> create{Entity}({Entity}Dto dto) async {
    return await executeApiCall(_api.create{Entity}(dto));
  }
  
  @override
  Future<ApiResponse<{Entity}Dto>> get{Entity}(String id) async {
    return await executeApiCall(_api.get{Entity}(id));
  }
}
```

**IMPORTANTE:** `ApiResponseHandlerMixin` proporciona:
- ✅ Manejo unificado de errores HTTP
- ✅ Logging automático de requests/responses
- ✅ Retry logic para errores de red
- ✅ Parsing automático a `ApiResponse<T>`

#### Repository
```dart
// lib/data/repository/{module_name}_repository_remote.dart
import 'package:core_data/core_data.dart';
import '../data_source/{module_name}_data_source.dart';
import 'models/{entity}.dart';
import 'mappers/{entity}_mapper.dart';

abstract interface class {ModuleName}Repository {
  Future<List<{Entity}>> get{Entities}();
  Future<{Entity}> create{Entity}({Entity} entity);
  Future<{Entity}> get{Entity}(String id);
}

class {ModuleName}RepositoryRemote implements {ModuleName}Repository {
  final {ModuleName}DataSource _dataSource;
  final {Entity}Mapper _mapper;
  
  {ModuleName}RepositoryRemote({
    required {ModuleName}DataSource dataSource,
    required {Entity}Mapper mapper,
  })  : _dataSource = dataSource,
        _mapper = mapper;
  
  @override
  Future<List<{Entity}>> get{Entities}() async {
    final response = await _dataSource.fetch{Entities}();
    
    return response.when(
      success: (dtos) => dtos.map(_mapper.fromDtoToEntity).toList(),
      error: (error) => throw error,
      empty: () => [],
    );
  }
  
  @override
  Future<{Entity}> create{Entity}({Entity} entity) async {
    final dto = _mapper.fromEntityToDto(entity);
    final response = await _dataSource.create{Entity}(dto);
    
    return response.when(
      success: (dto) => _mapper.fromDtoToEntity(dto),
      error: (error) => throw error,
      empty: () => throw Exception('{Entity} creation returned empty'),
    );
  }
  
  @override
  Future<{Entity}> get{Entity}(String id) async {
    final response = await _dataSource.get{Entity}(id);
    
    return response.when(
      success: (dto) => _mapper.fromDtoToEntity(dto),
      error: (error) => throw error,
      empty: () => throw Exception('{Entity} not found'),
    );
  }
}
```

**Opción: Repository con In-Memory Cache** (basado en Goals)

**📦 Template de cache avanzado**: `templates/data/cache.dart.template` (patrón Transfers)
```dart
class {ModuleName}RepositoryRemote implements {ModuleName}Repository {
  final {ModuleName}DataSource _dataSource;
  final {Entity}Mapper _mapper;
  
  // Cache in-memory
  List<{Entity}>? _cached{Entities};
  DateTime? _cacheTimestamp;
  static const _cacheDuration = Duration(minutes: 5);
  
  {ModuleName}RepositoryRemote({
    required {ModuleName}DataSource dataSource,
    required {Entity}Mapper mapper,
  })  : _dataSource = dataSource,
        _mapper = mapper;
  
  @override
  Future<List<{Entity}>> get{Entities}({bool forceRefresh = false}) async {
    // Retornar cache si es válido
    if (!forceRefresh && _isCacheValid()) {
      return _cached{Entities}!;
    }
    
    // Fetch desde API
    final response = await _dataSource.fetch{Entities}();
    
    return response.when(
      success: (dtos) {
        final entities = dtos.map(_mapper.fromDtoToEntity).toList();
        // Actualizar cache
        _cached{Entities} = entities;
        _cacheTimestamp = DateTime.now();
        return entities;
      },
      error: (error) => throw error,
      empty: () => [],
    );
  }
  
  bool _isCacheValid() {
    if (_cached{Entities} == null || _cacheTimestamp == null) return false;
    return DateTime.now().difference(_cacheTimestamp!) < _cacheDuration;
  }
  
  void clearCache() {
    _cached{Entities} = null;
    _cacheTimestamp = null;
  }
}
```

#### Providers
```dart
// lib/data/providers/{module_name}_repository_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:core_data/core_data.dart';
import '../api/{module_name}_api.dart';
import '../data_source/{module_name}_data_source.dart';
import '../repository/{module_name}_repository_remote.dart';
import '../repository/mappers/{entity}_mapper.dart';

// API Provider
final {moduleName}ApiProvider = Provider<{ModuleName}Api>((ref) {
  final dio = ref.watch(dioProvider);
  return {ModuleName}Api(dio);
});

// DataSource Provider
final {moduleName}DataSourceProvider = Provider<{ModuleName}DataSource>((ref) {
  return {ModuleName}DataSourceRemote(
    api: ref.watch({moduleName}ApiProvider),
  );
});

// Mapper Provider
final {entity}MapperProvider = Provider<{Entity}Mapper>((ref) {
  return {Entity}Mapper();
});

// Repository Provider
final {moduleName}RepositoryProvider = Provider<{ModuleName}Repository>((ref) {
  return {ModuleName}RepositoryRemote(
    dataSource: ref.watch({moduleName}DataSourceProvider),
    mapper: ref.watch({entity}MapperProvider),
  );
});
```

#### ViewModel
```dart
// lib/ui/{screen}/view_model/{screen}_view_model.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../data/repository/models/{entity}.dart';
import '../../../data/repository/{module_name}_repository_remote.dart';

class {Screen}ViewModel extends AutoDisposeAsyncNotifier<List<{Entity}>> {
  @override
  Future<List<{Entity}>> build() async {
    return _load{Entities}();
  }
  
  Future<List<{Entity}>> _load{Entities}() async {
    final repository = ref.read({moduleName}RepositoryProvider);
    return await repository.get{Entities}();
  }
  
  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(_load{Entities});
  }
  
  Future<void> create{Entity}({Entity} entity) async {
    state = const AsyncLoading();
    try {
      final repository = ref.read({moduleName}RepositoryProvider);
      await repository.create{Entity}(entity);
      // Recargar lista
      state = await AsyncValue.guard(_load{Entities});
    } catch (e, stack) {
      state = AsyncError(e, stack);
    }
  }
}
```

**IMPORTANTE:** Usar `AsyncNotifier` o `AutoDisposeAsyncNotifier` (moderno):
- ✅ `AutoDisposeAsyncNotifier<T>` - Se dispone automáticamente cuando no hay listeners
- ✅ `AsyncNotifier<T>` - Persiste mientras exista el provider
- ❌ `StateNotifier<AsyncValue<T>>` - Patrón legacy, NO usar

**Para estado síncrono simple:** Usar `Notifier<T>` o `AutoDisposeNotifier<T>`

#### ViewModel Provider
```dart
// lib/ui/{screen}/view_model/{screen}_view_model_provider.dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../data/repository/models/{entity}.dart';
import '{screen}_view_model.dart';

final {screen}ViewModelProvider =
    AutoDisposeAsyncNotifierProvider<{Screen}ViewModel, List<{Entity}>>(
  {Screen}ViewModel.new,
);
```

#### View
```dart
// lib/ui/{screen}/views/{screen}_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../view_model/{screen}_view_model_provider.dart';

class {Screen}Page extends ConsumerWidget {
  const {Screen}Page({super.key});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch({screen}ViewModelProvider);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('{ModuleName}'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              ref.read({screen}ViewModelProvider.notifier).refresh();
            },
          ),
        ],
      ),
      body: state.when(
        data: (data) => _buildData(context, data),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => _buildError(context, error),
      ),
    );
  }
  
  Widget _buildData(BuildContext context, List data) {
    if (data.isEmpty) {
      return const Center(child: Text('No hay datos disponibles'));
    }
    
    return ListView.builder(
      itemCount: data.length,
      itemBuilder: (context, index) {
        final item = data[index];
        return ListTile(
          title: Text(item.id),
          // Personalizar con campos del entity
        );
      },
    );
  }
  
  Widget _buildError(BuildContext context, Object error) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error_outline, size: 48, color: Colors.red),
          const SizedBox(height: 16),
          Text('Error: $error'),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () {
              // Retry
              ref.read({screen}ViewModelProvider.notifier).refresh();
            },
            child: const Text('Reintentar'),
          ),
        ],
      ),
    );
  }
}
```

#### Navigation
```dart
// lib/navigation/{module_name}_navigation.dart
import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../ui/{screen}/views/{screen}_page.dart';

class {ModuleName}Navigation {
  // Rutas
  static const String homePath = '/{module-name}';
  static const String detailPath = '/{module-name}/detail/:id';
  
  // Definición de rutas
  static final List<GoRoute> routerConfig = [
    GoRoute(
      path: homePath,
      name: '{module-name}-home',
      builder: (context, state) => const {Screen}Page(),
    ),
    GoRoute(
      path: detailPath,
      name: '{module-name}-detail',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return {Screen}DetailPage(id: id);
      },
    ),
  ];
  
  // Métodos de navegación
  static void goToHome(BuildContext context) {
    context.go(homePath);
  }
  
  static void goToDetail(BuildContext context, String id) {
    context.go(detailPath.replaceAll(':id', id));
  }
  
  static void pushToDetail(BuildContext context, String id) {
    context.push(detailPath.replaceAll(':id', id));
  }
}
```

**IMPORTANTE:** 
- ✅ Usar `static final List<GoRoute> routerConfig`
- ✅ Proveer métodos helper para navegación type-safe

#### Module Configuration

**📦 Control de acceso:** usa los métodos del `ModuleDefinition`
- `getRouteRedirectionFlags()` para feature flags simples (Goals pattern)
- `redirectRules()` para validaciones complejas (Transfers pattern)

**Sin localizaciones propias y sin RedirectRules:**
```dart
// lib/module_definition/{module_name}_module_definition.dart
import 'package:feature_commons/feature_commons.dart';
import 'package:flutter/widgets.dart';
import '../navigation/{module_name}_navigation.dart';

class {ModuleName}ModuleDefinition extends Module<dynamic> {
  {ModuleName}ModuleDefinition() : super('{module_name}');
  
  @override
  List<LocalizationsDelegate<dynamic>> getLocalizationDelegate() {
    return [];  // No tiene localizaciones propias
  }
  
  @override
  List<GoRoute> getRouterConfig() {
    return {ModuleName}Navigation.routerConfig;
  }
  
  @override
  String? initialLocation() {
    return null;  // Sin ruta inicial predeterminada
  }
}
```

**Con localizaciones propias:**
```dart
// lib/module_definition/{module_name}_module_definition.dart
import 'package:feature_commons/feature_commons.dart';
import 'package:flutter/widgets.dart';
import '../navigation/{module_name}_navigation.dart';
import '../ui/l10n/generated/{module_name}_localizations.dart';

class {ModuleName}ModuleDefinition extends Module<{ModuleName}Localizations> {
  {ModuleName}ModuleDefinition() : super('{module_name}');
  
  @override
  List<LocalizationsDelegate<{ModuleName}Localizations>> getLocalizationDelegate() {
    return [{ModuleName}Localizations.delegate];
  }
  
  @override
  List<GoRoute> getRouterConfig() {
    return {ModuleName}Navigation.routerConfig;
  }
  
  @override
  String? initialLocation() {
    return null;
  }
}
```

**Con RedirectRules (Control de Acceso via Feature Flags - Goals Pattern):**
```dart
// lib/module_definition/{module_name}_module_definition.dart
import 'package:feature_commons/feature_commons.dart';
import 'package:flutter/widgets.dart';
import '../constants/{module_name}_feature_flags_ids.dart';
import '../navigation/{module_name}_navigation.dart';

class {ModuleName}ModuleDefinition extends Module<dynamic> {
  {ModuleName}ModuleDefinition() : super('{module_name}');
  
  @override
  List<LocalizationsDelegate<dynamic>> getLocalizationDelegate() {
    return [];
  }
  
  @override
  List<GoRoute> getRouterConfig() {
    return {ModuleName}Navigation.routerConfig;
  }
  
  @override
  Map<String, String> getRouteRedirectionFlags() => {
    {ModuleName}Navigation.someRoute: {ModuleName}FeatureFlagIds.SOME_REDIRECT_FLAG.id,
  };
  
  @override
  String? initialLocation() {
    return null;
  }
}
```

**Con RedirectRules Avanzado (Transfers Pattern):**
```dart
// lib/module_definition/{module_name}_module_definition.dart
import 'package:feature_commons/feature_commons.dart';
import 'package:flutter/widgets.dart';
import '../constants/{module_name}_flag_ids.dart';
import '../navigation/{module_name}_navigation.dart';
import '../ui/l10n/generated/{module_name}_localizations.dart';

class {ModuleName}ModuleDefinition extends Module<{ModuleName}Localizations> {
  {ModuleName}ModuleDefinition() : super('{module_name}');

  @override
  List<LocalizationsDelegate<{ModuleName}Localizations>> getLocalizationDelegate() => [
    {ModuleName}Localizations.delegate,
  ];

  @override
  List<GoRoute> getRouterConfig() => {ModuleName}Navigation.routerConfig;

  @override
  List<RedirectRule> redirectRules() {
    return [
      FeatureBehaviorRedirectRule(
        flagId: {ModuleName}FlagIds.FEATURE_A_REDIRECT_TO.id,
        routeNames: [
          {ModuleName}Navigation.featureARoute,
          {ModuleName}Navigation.featureADetailRoute,
        ],
      ),
      FeatureBehaviorRedirectRule(
        flagId: {ModuleName}FlagIds.FEATURE_B_REDIRECT_TO.id,
        routeNames: [
          {ModuleName}Navigation.featureBRoute,
        ],
      ),
    ];
  }
}
```

**📦 Template disponible**: `templates/module_definition.dart.template`

**IMPORTANTE - Métodos del Module Pattern:**
- ✅ `getRouterConfig()` - Retorna List<GoRoute> del módulo
- ✅ `redirectRules()` - Retorna List<RedirectRule> para validaciones complejas (Transfers pattern)
- ✅ `getRouteRedirectionFlags()` - Retorna Map<String, String> para feature flags simples (Goals pattern)
- ✅ `getLocalizationDelegate()` - Retorna delegates de localización
- ✅ `initialLocation()` - Retorna ruta inicial (opcional)

**Diferencia entre getRouteRedirectionFlags() y redirectRules():**
- **Goals Pattern (Simple)**: Usa `getRouteRedirectionFlags()` para mapear rutas → feature flags
- **Transfers Pattern (Advanced)**: Usa `redirectRules()` para validaciones complejas con FeatureBehaviorRedirectRule

---

### Paso 5: Generar Tests Base

**📦 Templates de testing disponibles**:
- `templates/tests/data_source_test.dart.template`
- `templates/tests/repository_test.dart.template`
- `templates/tests/view_model_test.dart.template`

Estos templates incluyen:
- ✅ Patrón AAA completo (Arrange-Act-Assert)
- ✅ ProviderContainer.listen() para ViewModels
- ✅ @GenerateMocks configurado
- ✅ Tests de success, error, empty
- ✅ Basados en Goals (16 tests pattern)

---

#### DataSource Test

**📦 Usar template**: `templates/tests/data_source_test.dart.template`
```dart
// test/data/data_source/{module_name}_data_source_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:core_data/core_data.dart';

@GenerateMocks([{ModuleName}Api])
void main() {
  group('{ModuleName}DataSourceRemote', () {
    late Mock{ModuleName}Api mockApi;
    late {ModuleName}DataSourceRemote dataSource;
    
    setUp(() {
      mockApi = Mock{ModuleName}Api();
      dataSource = {ModuleName}DataSourceRemote(api: mockApi);
    });
    
    group('fetch{Entities}', () {
      test('should return ApiResponse.success when API call succeeds', () async {
        // Arrange
        final dtos = [{Entity}Dto(id: '1'), {Entity}Dto(id: '2')];
        when(mockApi.get{Entities}()).thenAnswer((_) async => dtos);
        
        // Act
        final result = await dataSource.fetch{Entities}();
        
        // Assert
        expect(result, isA<ApiResponseSuccess<List<{Entity}Dto>>>());
        result.when(
          success: (data) => expect(data, equals(dtos)),
          error: (_) => fail('Should not be error'),
          empty: () => fail('Should not be empty'),
        );
        verify(mockApi.get{Entities}()).called(1);
      });
      
      test('should return ApiResponse.error when API call fails', () async {
        // Arrange
        when(mockApi.get{Entities}()).thenThrow(Exception('Network error'));
        
        // Act
        final result = await dataSource.fetch{Entities}();
        
        // Assert
        expect(result, isA<ApiResponseError>());
        verify(mockApi.get{Entities}()).called(1);
      });
    });
  });
}
```

#### Repository Test

**📦 Usar template**: `templates/tests/repository_test.dart.template`
```dart
// test/data/repository/{module_name}_repository_remote_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';
import 'package:core_data/core_data.dart';

@GenerateMocks([{ModuleName}DataSource, {Entity}Mapper])
void main() {
  group('{ModuleName}RepositoryRemote', () {
    late Mock{ModuleName}DataSource mockDataSource;
    late Mock{Entity}Mapper mockMapper;
    late {ModuleName}RepositoryRemote repository;
    
    setUp(() {
      mockDataSource = Mock{ModuleName}DataSource();
      mockMapper = Mock{Entity}Mapper();
      repository = {ModuleName}RepositoryRemote(
        dataSource: mockDataSource,
        mapper: mockMapper,
      );
    });
    
    group('get{Entities}', () {
      test('should return list of entities when successful', () async {
        // Arrange
        final dtos = [{Entity}Dto(id: '1'), {Entity}Dto(id: '2')];
        final entities = [{Entity}(id: '1'), {Entity}(id: '2')];
        
        when(mockDataSource.fetch{Entities}())
            .thenAnswer((_) async => ApiResponse.success(dtos));
        when(mockMapper.fromDtoToEntity(any))
            .thenAnswer((invocation) {
          final dto = invocation.positionalArguments[0] as {Entity}Dto;
          return entities.firstWhere((e) => e.id == dto.id);
        });
        
        // Act
        final result = await repository.get{Entities}();
        
        // Assert
        expect(result, equals(entities));
        verify(mockDataSource.fetch{Entities}()).called(1);
        verify(mockMapper.fromDtoToEntity(any)).called(dtos.length);
      });
      
      test('should throw error when API fails', () async {
        // Arrange
        final error = Exception('API Error');
        when(mockDataSource.fetch{Entities}())
            .thenAnswer((_) async => ApiResponse.error(error));
        
        // Act & Assert
        expect(
          () => repository.get{Entities}(),
          throwsA(isA<Exception>()),
        );
        verify(mockDataSource.fetch{Entities}()).called(1);
        verifyNever(mockMapper.fromDtoToEntity(any));
      });
      
      test('should return empty list when response is empty', () async {
        // Arrange
        when(mockDataSource.fetch{Entities}())
            .thenAnswer((_) async => const ApiResponse.empty());
        
        // Act
        final result = await repository.get{Entities}();
        
        // Assert
        expect(result, isEmpty);
        verify(mockDataSource.fetch{Entities}()).called(1);
      });
    });
  });
}
```

#### ViewModel Test (Patrón Goals con ProviderContainer.listen())

**📦 Usar template**: `templates/tests/view_model_test.dart.template`
```dart
// test/ui/{screen}/view_model/{screen}_view_model_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([{ModuleName}Repository])
void main() {
  group('{Screen}ViewModel', () {
    late ProviderContainer container;
    late Mock{ModuleName}Repository mockRepository;
    
    setUp(() {
      mockRepository = Mock{ModuleName}Repository();
      container = ProviderContainer(
        overrides: [
          {moduleName}RepositoryProvider.overrideWithValue(mockRepository),
        ],
      );
    });
    
    tearDown(() {
      container.dispose();
    });
    
    test('should start in loading state', () {
      // Arrange
      when(mockRepository.get{Entities}())
          .thenAnswer((_) async => []);
      
      // Act
      final state = container.read({screen}ViewModelProvider);
      
      // Assert
      expect(state, isA<AsyncLoading>());
    });
    
    test('should load entities successfully', () async {
      // Arrange
      final entities = [
        {Entity}(id: '1'),
        {Entity}(id: '2'),
      ];
      when(mockRepository.get{Entities}())
          .thenAnswer((_) async => entities);
      
      // Act
      final listener = Listener<AsyncValue<List<{Entity}>>>();
      container.listen<AsyncValue<List<{Entity}>>>(
        {screen}ViewModelProvider,
        listener,
        fireImmediately: true,
      );
      
      await container.read({screen}ViewModelProvider.future);
      
      // Assert
      verify(listener(null, any)).called(1);  // Loading
      verify(listener(any, any)).called(1);   // Data
      
      final state = container.read({screen}ViewModelProvider);
      expect(state, isA<AsyncData<List<{Entity}>>>());
      expect(state.value, equals(entities));
      verify(mockRepository.get{Entities}()).called(1);
    });
    
    test('should handle errors correctly', () async {
      // Arrange
      final error = Exception('Failed to load');
      when(mockRepository.get{Entities}()).thenThrow(error);
      
      // Act
      final listener = Listener<AsyncValue<List<{Entity}>>>();
      container.listen<AsyncValue<List<{Entity}>>>(
        {screen}ViewModelProvider,
        listener,
        fireImmediately: true,
      );
      
      try {
        await container.read({screen}ViewModelProvider.future);
      } catch (_) {}
      
      // Assert
      final state = container.read({screen}ViewModelProvider);
      expect(state, isA<AsyncError>());
      expect(state.error, equals(error));
      verify(mockRepository.get{Entities}()).called(1);
    });
    
    test('refresh should reload data', () async {
      // Arrange
      final entities = [{Entity}(id: '1')];
      when(mockRepository.get{Entities}())
          .thenAnswer((_) async => entities);
      
      // Act - Initial load
      await container.read({screen}ViewModelProvider.future);
      
      // Clear interactions
      clearInteractions(mockRepository);
      
      // Act - Refresh
      await container.read({screen}ViewModelProvider.notifier).refresh();
      
      // Assert
      verify(mockRepository.get{Entities}()).called(1);
      final state = container.read({screen}ViewModelProvider);
      expect(state.value, equals(entities));
    });
  });
}

// Mock listener helper
class Listener<T> extends Mock {
  void call(T? previous, T next);
}
```

**IMPORTANTE - Patrones de Testing:**
- ✅ Usar `@GenerateMocks` para generar mocks automáticamente
- ✅ Usar `ProviderContainer` con overrides para inyectar mocks
- ✅ Usar `.listen()` para verificar transiciones de estado
- ✅ Patrón AAA (Arrange-Act-Assert) en todos los tests
- ✅ Tests para casos success, error y empty
- ✅ `tearDown()` para limpiar providers

---

### Paso 6: Instrucciones de Integración

Después de generar todos los archivos, proporciono instrucciones claras:

```markdown
✅ Módulo {ModuleName} creado exitosamente!

## 📋 Próximos Pasos:

### 1. Agregar a melos.yaml
Edita el archivo `melos.yaml` en la raíz del proyecto:
```yaml
packages:
  - bancadigital-bm-{module_name}  # ← Agregar con prefijo "bancadigital-bm-"
  - ./
```

### 2. Registrar en ModuleManager
Edita `lib/main.dart` (o donde configures la app):
```dart
final moduleManager = ModuleManager()
  ..registerModule({ModuleName}Module());  // ← Agregar esta línea
```

**IMPORTANTE:** ModuleManager centraliza la gestión de módulos:
- **Rutas automáticas**: `moduleManager.getRouterConfig()` retorna todas las rutas registradas
- **Localizaciones consolidadas**: `moduleManager.allLocalizationDelegates()` retorna todos los delegates
- **Gestión dinámica**: Puedes registrar/desregistrar módulos en runtime

Métodos disponibles:
- `registerModule(Module module)` - Registra un módulo
- `unregisterModule(Module module)` - Elimina un módulo
- `unregisterModuleByName(String name)` - Elimina por nombre
- `modules()` - Retorna iterador de todos los módulos
- `findByName(String name)` - Busca módulo por nombre
- `allLocalizationDelegates()` - Obtiene todos los delegates de localización

### 3. Ejecutar comandos de setup
```bash
# 1. Bootstrap - instala dependencias
melos bootstrap

# 2. Generar código (Retrofit, JsonSerializable, etc)
melos run br

# 3. Ejecutar tests
cd bancadigital-bm-{module_name} && flutter test

# 4. Verificar linter
flutter analyze
```

### 4. Personalizar modelos
Los campos de {Entity} se generaron con un ID básico.
Edita los siguientes archivos para agregar campos específicos:
- `lib/data/repository/models/{entity}_entity.dart`
- `lib/data/data_source/dto/{entity}_dto.dart`
- `lib/data/repository/mappers/{entity}_mapper.dart`

### 5. Implementar UI
El View generado es básico. Personaliza:
- `lib/ui/{screen}/views/{screen}_page.dart`
- Agrega widgets en `lib/ui/{screen}/widgets/` si es necesario

## 📚 Documentación de Referencia

Consulta las secciones a continuación para:
- Convenciones de nombres
- Estructura obligatoria
- Errores comunes
- Ejemplos completos
```

---

## 📚 Documentación de Referencia

A continuación se encuentra la documentación completa de referencia para consulta.

---

## 📝 ¿Cuándo Crear un Feature Module?

### Criterios para Crear un Nuevo Módulo

✅ **CREAR módulo cuando:**
- La funcionalidad puede ser **aislada** y tiene lógica independiente
- Representa un flujo de negocio completo (ej: Cuentas, Tarjetas, Pagos)
- Requiere su propia navegación y pantallas
- Tiene modelos de datos específicos del dominio
- Se espera que crezca y evolucione independientemente

❌ **NO CREAR módulo cuando:**
- Es solo un widget reutilizable → Usar `feature_commons`
- Es una utilidad compartida → Usar `core_data`
- Es un componente del Design System → Usar `design_system`
- Es una pantalla aislada dentro de un módulo existente

---

## 🏗️ Estructura Obligatoria de un Módulo

### Estructura Completa

```
bancadigital-bm-myfeature/           # Carpeta con prefijo "bancadigital-bm-" en kebab-case
├── lib/
│   ├── module_definition/           # OBLIGATORIO
│   │   └── myfeature_module_configuration.dart
│   ├── navigation/                  # OBLIGATORIO
│   │   └── myfeature_navigation.dart
│   ├── data/                        # Capa de datos (Clean Architecture)
│   │   ├── api/                     # Definiciones Retrofit
│   │   ├── data_source/            # DTOs y DataSources
│   │   ├── providers/              # Riverpod providers
│   │   ├── repository/             # Implementaciones de repositorios
│   │   │   ├── mappers/            # DTO → Entity mappers
│   │   │   └── models/             # Entities del dominio
│   │   └── services/               # Servicios específicos
│   ├── ui/                          # Capa de presentación (MVVM)
│   │   ├── screen_name/            # Una carpeta por pantalla
│   │   │   ├── params/             # Parámetros de navegación
│   │   │   ├── view_model/         # StateNotifier/ViewModel
│   │   │   ├── views/              # Widgets de la pantalla
│   │   │   └── widgets/            # Widgets específicos de la pantalla
│   │   ├── common/                 # Compartido dentro del módulo
│   │   ├── constants/              # Constantes del módulo
│   │   ├── extensions/             # Extensions del módulo
│   │   └── l10n/                   # Localizaciones (generadas)
│   ├── constants/                   # Constantes globales del módulo
│   └── utils/                       # Utilidades del módulo
├── test/                            # Tests unitarios
│   ├── data/
│   │   └── repository/
│   └── ui/
│       └── screen_name/
│           └── view_model/
├── analysis_options.yaml            # OBLIGATORIO
├── pubspec.yaml                     # OBLIGATORIO (name: bancadigital_bm_myfeature)
├── CHANGELOG.md                     # Recomendado
├── README.md                        # Recomendado
└── l10n.yaml                        # Si usa localizaciones
```

---

## 📐 Convenciones de Nombres

### Nombres de Repositorios/Carpetas
```bash
✅ bancadigital-bm-yjcloans      # kebab-case CON prefijo "bancadigital-bm-"
✅ bancadigital-bm-goals
✅ bancadigital-bm-accounts
✅ bancadigital-bm-self-services

❌ yjcloans                      # Falta prefijo
❌ bancadigital_bm_yjcloans      # Usa underscores en lugar de guiones
❌ BancadigitalBmYjcloans        # No usar PascalCase
```

### Package Names (pubspec.yaml)
```yaml
✅ name: bancadigital_bm_yjcloans    # snake_case CON prefijo "bancadigital_bm_"
✅ name: bancadigital_bm_goals
✅ name: bancadigital_bm_accounts

❌ name: yjcloans                    # Falta prefijo  
❌ name: bancadigital-bm-yjcloans    # Usa guiones en lugar de underscores
❌ name: BancadigitalBmYjcloans      # No usar PascalCase
```

### Resumen de la Convención
| Elemento | Formato | Ejemplo |
|----------|---------|---------|
| **Carpeta/Repo** | kebab-case con prefijo | `bancadigital-bm-yjcloans` |
| **Package Name** | snake_case con prefijo | `bancadigital_bm_yjcloans` |
| **Ubicación** | Mismo nivel que app | `Repositorios/bancadigital-bm-yjcloans/` |

### Nombres de Archivos
```bash
✅ account_view_model.dart, payment_repository_remote.dart
❌ AccountViewModel.dart, payment-repository.dart
```

### Nombres de Clases  
```dart
✅ class AccountViewModel, class PaymentRepositoryRemote
❌ class account_view_model, class paymentRepository
```

---

## ⚠️ Errores Comunes

### 1. Dependencia Cruzada Entre Módulos
❌ NO depender de otros feature modules
✅ Mover código compartido a feature_commons o core_data

### 2. No Usar Include en analysis_options.yaml
✅ SIEMPRE: `include: ../feature_commons/analysis_options.yaml`

### 3. Olvidar publish_to: none
✅ SIEMPRE: `publish_to: none` en pubspec.yaml

### 4. routerConfig No Estática
✅ SIEMPRE: `static final List<GoRoute> routerConfig = [...]`

### 5. Mezclar DTOs con Entities
❌ NO usar DTOs en ViewModels
✅ Usar Entities del dominio en capa de presentación

### 6. No Registrar Módulo en ModuleManager
✅ SIEMPRE registrar: `moduleManager.registerModule(MyModule())`

### 7. Olvidar melos bootstrap
✅ SIEMPRE ejecutar después de crear módulo:
```bash
melos bootstrap && melos run br
```

### 8. No Implementar initialLocation Cuando es Necesario
❌ Retornar siempre `null` si el módulo tiene deep linking
✅ Retornar ruta específica si el módulo es punto de entrada:
```dart
@override
String? initialLocation() {
  return '/accounts';  // Para deep linking o navegación directa
}
```

### 9. Tipo Genérico Incorrecto en Module
❌ `Module<Object>` cuando el módulo tiene localizaciones
✅ `Module<AccountLocalizations>` con delegate específico
✅ `Module<dynamic>` si no tiene localizaciones propias

### 10. Confundir Métodos de Control de Acceso
❌ **Incorrecto:** Usar `redirectRules()` y `getRouteRedirectionFlags()` simultáneamente
✅ **Correcto (Simple):** Usar `getRouteRedirectionFlags()` para feature flags básicos (Goals pattern)
✅ **Correcto (Avanzado):** Usar `redirectRules()` con FeatureBehaviorRedirectRule (Transfers pattern)

**Ejemplo Goals Pattern:**
```dart
@override
Map<String, String> getRouteRedirectionFlags() => {
  GoalsNavigation.earlyWithdrawalOnboarding: GoalsFeatureFlagIds.GOALS_EARLY_RETIREMENT_REDIRECT_TO.id,
};
```

**Ejemplo Transfers Pattern:**
```dart
@override
List<RedirectRule> redirectRules() {
  return [
    FeatureBehaviorRedirectRule(
      flagId: TransfersFlagIds.TRANSFERS_INT_REDIRECT_TO.id,
      routeNames: [
        InternationalTransfersNavigation.transferInternationalRoute,
      ],
    ),
  ];
}
```

### 11. Usar StateNotifier en Lugar de AsyncNotifier
❌ **Legacy:** `StateNotifier<AsyncValue<T>>`
✅ **Moderno:** `AutoDisposeAsyncNotifier<T>` o `AsyncNotifier<T>`

### 12. No Usar Freezed en DTOs
❌ **Incompleto:** Solo `@JsonSerializable`
✅ **Completo:** `@freezed` con `@JsonSerializable` integrado

### 13. Repository sin Manejo de Errores
❌ **Malo:** Exponer excepciones directamente del API
✅ **Bueno:** Usar `ApiResponse<T>.when()` para manejo estructurado

### 14. DataSource sin ApiResponseHandlerMixin
❌ **Malo:** Manejo manual de errores HTTP
✅ **Bueno:** `with ApiResponseHandlerMixin` + `executeApiCall()`

### 15. Sufijo "Entity" en Domain Models
❌ **Incorrecto:** `class AccountEntity`
✅ **Correcto:** `class Account`

### 16. Olvidar Freezed en dev_dependencies
✅ SIEMPRE agregar en pubspec.yaml:
```yaml
dev_dependencies:
  freezed: ^2.5.2
  freezed_annotation: ^2.4.1  # En dependencies
```

---

## � Reglas de Arquitectura y Code Review

Estas reglas están basadas en hallazgos de PRs y se deben cumplir SIEMPRE:

### 1. Workflows para Steps (OBLIGATORIO)
**Regla:** Todo flujo con pasos múltiples DEBE usar Dual Enum Pattern.

❌ **NO hacer:** Estado manual o strings literales
```dart
int currentStep = 0;
String stepName = "personal_data";
```

✅ **SÍ usar:** Dual Enum Pattern (Steps + Groups)
```dart
// lib/ui/workflows/onboarding_workflow.dart
import 'package:core_data/core_data.dart';

enum OnboardingStep implements WorkflowStep {
  welcome(OnboardingGroup.intro),
  personalData(OnboardingGroup.registration),
  addressInfo(OnboardingGroup.registration),
  review(OnboardingGroup.confirmation);

  const OnboardingStep(this.group);

  @override
  final OnboardingGroup group;

  @override
  OnboardingStep? get nextStep {
    final values = OnboardingStep.values;
    final currentIndex = values.indexOf(this);
    return currentIndex < values.length - 1 ? values[currentIndex + 1] : null;
  }

  @override
  OnboardingStep? get previousStep {
    final currentIndex = values.indexOf(this);
    return currentIndex > 0 ? values[currentIndex - 1] : null;
  }
}

enum OnboardingGroup implements WorkflowGroup {
  intro,
  registration,
  confirmation;
}
```

**Ubicación:** `/ui/workflows/` o `/ui/{feature}/workflows/`

**📦 Template completo disponible**: `templates/advanced/workflow_enum.dart.template`
- ✅ Incluye métodos nextStep(), previousStep(), progress()
- ✅ Extensions para routePath y screenName
- ✅ Métodos canGoBack(), isFinal()
- ✅ Títulos y descripciones por grupo

### 2. ViewModel Pattern (SIEMPRE para Lógica de UI)
**Regla:** TODA lógica de UI debe estar en un ViewModel, NUNCA en el Widget.

❌ **NO hacer:** Lógica de negocio en Widgets
```dart
class MyPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final repository = ref.watch(repositoryProvider);
    // ❌ Lógica directamente en build
    final filteredData = repository.data.where((x) => x.active).toList();
    return ListView(...);
  }
}
```

✅ **SÍ usar:** AsyncNotifier/Notifier para ViewModels
```dart
// ViewModel
class MyViewModel extends AutoDisposeAsyncNotifier<List<MyEntity>> {
  @override
  Future<List<MyEntity>> build() async {
    return _loadData();
  }

  Future<List<MyEntity>> _loadData() async {
    final repository = ref.read(repositoryProvider);
    final data = await repository.getData();
    return data.where((x) => x.active).toList();
  }

  Future<void> refresh() async {
    state = const AsyncLoading();
    state = await AsyncValue.guard(_loadData);
  }
}

// Widget
class MyPage extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(myViewModelProvider);
    return state.when(
      data: (data) => ListView(...),
      loading: () => CircularProgressIndicator(),
      error: (e, s) => ErrorWidget(e),
    );
  }
}
```

### 3. Sin Filtrados en Conversión de JSON
**Regla:** Los métodos `fromJson`/`toJson` deben ser CONVERSIÓN PURA, sin lógica de negocio.

❌ **NO hacer:** Filtrar/transformar datos en fromJson
```dart
@freezed
class TransactionDto with _$TransactionDto {
  factory TransactionDto.fromJson(Map<String, dynamic> json) {
    // ❌ Lógica de filtrado en DTO
    final transactions = (json['transactions'] as List)
        .where((t) => t['amount'] > 0)
        .toList();
    return _$TransactionDtoFromJson({...json, 'transactions': transactions});
  }
}
```

✅ **SÍ hacer:** Conversión pura, lógica en Mapper o Repository
```dart
// DTO - Solo conversión
@freezed
class TransactionDto with _$TransactionDto {
  factory TransactionDto.fromJson(Map<String, dynamic> json) =>
      _$TransactionDtoFromJson(json);
}

// Mapper - Aquí va la lógica
class TransactionMapper {
  List<Transaction> fromDtoToEntities(List<TransactionDto> dtos) {
    return dtos
        .where((dto) => dto.amount > 0)  // ✅ Lógica en mapper
        .map(_fromDtoToEntity)
        .toList();
  }
}
```

### 4. Sin Código Mockeado como Final
**Regla:** No dejar datos de prueba hardcodeados en producción.

❌ **NO dejar:** Datos de prueba hardcodeados
```dart
Future<List<Account>> getAccounts() async {
  // ❌ Código mockeado en producción
  return [
    Account(id: '1', name: 'Test Account'),
    Account(id: '2', name: 'Another Test'),
  ];
}
```

✅ **SÍ hacer:** Implementación real o UnimplementedError
```dart
// Opción 1: Implementación real
Future<List<Account>> getAccounts() async {
  final response = await executeApiCall(_api.getAccounts());
  return response.when(
    success: (data) => data.map(_mapper.fromDtoToEntity).toList(),
    error: (error) => throw error,
    empty: () => [],
  );
}

// Opción 2: Si no está listo, usar UnimplementedError
Future<List<Account>> getAccounts() async {
  throw UnimplementedError('getAccounts() pending backend integration');
}
```

### 5. Sin Transformaciones Innecesarias en DTOs
**Regla:** No duplicar lógica entre DTO y Entity.

❌ **NO hacer:** Duplicar lógica entre DTO y Entity
```dart
// DTO con lógica
class AccountDto {
  final double balance;
  
  bool get hasPositiveBalance => balance > 0;  // ❌ Lógica en DTO
}

// Entity con la misma lógica
class Account {
  final double balance;
  
  bool get hasPositiveBalance => balance > 0;  // ❌ Duplicado
}
```

✅ **SÍ hacer:** DTOs puros, lógica solo en Entity
```dart
// DTO puro - Solo datos
@freezed
class AccountDto with _$AccountDto {
  const factory AccountDto({
    required double balance,
  }) = _AccountDto;
  
  factory AccountDto.fromJson(Map<String, dynamic> json) => 
      _$AccountDtoFromJson(json);
}

// Entity - Con lógica de negocio
class Account extends Equatable {
  final double balance;
  
  const Account({required this.balance});
  
  bool get hasPositiveBalance => balance > 0;  // ✅ Lógica solo en Entity
  bool get isOverdrawn => balance < 0;
  
  @override
  List<Object?> get props => [balance];
}
```

### 6. Estándares de Enums
**Regla:** Convenciones estrictas de nombrado y estructura.

**Convenciones de nombrado:**
- ✅ **Sin sufijo** si el contexto es claro: `PaymentStatus`, `GoalType`
- ✅ **Con sufijo Enum** si está en `/enum/`: `AccountStatusEnum`, `LanguageCodeEnum`
- ✅ **Sufijo FeatureFlagIds**: Solo para feature flags

**Estructura estándar:**

**A. Enum Simple (valores puros):**
```dart
enum PaymentStatus {
  pending,
  processing,
  completed,
  failed;
}
```

**B. Enum con Valor (con parsing):**
```dart
enum TransactionType {
  transfer('TRANSFER'),
  payment('PAYMENT'),
  withdrawal('WITHDRAWAL');

  const TransactionType(this.value);
  final String value;

  static TransactionType fromValue(String value) {
    return values.firstWhere(
      (e) => e.value == value,
      orElse: () => throw ArgumentError('Unknown value: $value'),
    );
  }
}
```

**C. Enum con Data (para workflows):**
```dart
enum PaymentStep implements WorkflowStep {
  selectAccount(PaymentGroup.setup),
  enterAmount(PaymentGroup.setup),
  review(PaymentGroup.confirmation);

  const PaymentStep(this.group);
  
  @override
  final PaymentGroup group;
  
  @override
  PaymentStep? get nextStep { /* ... */ }
}
```

❌ **NO hacer:** Valores literales sin enum
```dart
if (status == 'pending') { ... }  // ❌ String literal
```

✅ **SÍ usar:** Enum
```dart
if (status == PaymentStatus.pending) { ... }  // ✅ Type-safe
```

### 7. Evitar Proliferación de Providers
**Regla:** Máximo 15 providers top-level por módulo.

**Límites recomendados:**
- ✅ Máximo 15 providers top-level por módulo
- ✅ Agrupar en subdirectorios si hay >5 del mismo tipo
- ✅ Preferir ViewModels (AsyncNotifier) sobre StateProviders

**Organización correcta:**
```dart
// lib/data/providers/
├── api_providers.dart          // Providers de APIs
├── repository_providers.dart   // Providers de Repositories
└── mapper_providers.dart       // Providers de Mappers

// lib/ui/{screen}/view_model/
├── screen_view_model.dart
└── screen_view_model_provider.dart
```

❌ **NO crear:** Provider para cada estado trivial
```dart
final currentStepProvider = StateProvider<int>((ref) => 0);
final isLoadingProvider = StateProvider<bool>((ref) => false);
final errorMessageProvider = StateProvider<String?>((ref) => null);
final selectedItemProvider = StateProvider<Item?>((ref) => null);
// ❌ Proliferación de providers
```

✅ **SÍ usar:** ViewModel consolidado
```dart
class OnboardingState {
  final int currentStep;
  final bool isLoading;
  final String? errorMessage;
  final Item? selectedItem;
}

class OnboardingViewModel extends Notifier<OnboardingState> {
  @override
  OnboardingState build() => OnboardingState(...);
  
  void nextStep() => state = state.copyWith(currentStep: state.currentStep + 1);
  void selectItem(Item item) => state = state.copyWith(selectedItem: item);
}
```

**📦 Template completo disponible**: `templates/ui/view_model_state.dart.template`
- ✅ State class con Equatable
- ✅ Métodos copyWith(), toLoading(), toSuccess(), toError()
- ✅ Clase Filter opcional
- ✅ Factories para initial() y empty()

### 8. Nombrado de Entities (Sin Sufijo "Entity")
**Regla:** Las entities NO deben tener sufijo "Entity".

❌ **NO usar:** Sufijo "Entity"
```dart
class AccountEntity extends Equatable { ... }  // ❌ Sufijo innecesario
class PaymentEntity extends Equatable { ... }  // ❌ Sufijo innecesario
```

✅ **SÍ usar:** Nombres simples
```dart
class Account extends Equatable { ... }  // ✅ Simple y claro
class Payment extends Equatable { ... }  // ✅ Simple y claro
```

**Ubicación estándar:** `/data/repository/models/`

### 9. No Usar UseCases (Salvo Justificación)
**Regla:** NO crear capa de UseCase innecesaria, usar Repository directamente.

❌ **NO crear:** Capa de UseCase innecesaria
```dart
// ❌ UseCase que solo delega al Repository
class GetAccountsUseCase {
  final AccountRepository _repository;
  
  Future<List<Account>> call() => _repository.getAccounts();
}
```

✅ **SÍ hacer:** Repository directo desde ViewModel
```dart
class AccountsViewModel extends AutoDisposeAsyncNotifier<List<Account>> {
  @override
  Future<List<Account>> build() async {
    final repository = ref.read(accountRepositoryProvider);
    return repository.getAccounts();  // ✅ Directo
  }
}
```

**Excepción justificada:** Lógica compleja que combina múltiples repositories
```dart
// ✅ UseCase justificado - combina múltiples repos
class TransferMoneyUseCase {
  final AccountRepository _accountRepo;
  final TransactionRepository _transactionRepo;
  final NotificationRepository _notificationRepo;
  
  Future<TransferResult> call(TransferRequest request) async {
    // Validar saldo
    final account = await _accountRepo.getAccount(request.fromAccountId);
    if (account.balance < request.amount) {
      throw InsufficientFundsException();
    }
    
    // Crear transacción
    final transaction = await _transactionRepo.createTransfer(request);
    
    // Enviar notificación
    await _notificationRepo.sendTransferConfirmation(transaction);
    
    return TransferResult(transaction: transaction);
  }
}
```

### 10. Minimizar Propiedades Nullable
**Regla:** Preferir `required` sobre nullable siempre que sea posible.

❌ **NO abusar:** Nullables innecesarios
```dart
class User {
  final String? id;        // ❌ El ID nunca debería ser null
  final String? name;      // ❌ El nombre es obligatorio
  final String? email;     // ❌ El email es obligatorio
  
  const User({this.id, this.name, this.email});
}
```

✅ **SÍ usar:** Required para datos obligatorios
```dart
class User {
  final String id;           // ✅ Required - nunca null
  final String name;         // ✅ Required - nunca null
  final String email;        // ✅ Required - nunca null
  final String? middleName;  // ✅ Nullable - opcional
  
  const User({
    required this.id,
    required this.name,
    required this.email,
    this.middleName,
  });
}
```

**Casos válidos para nullable:**
- Estados intermedios en workflows: `DebitAccount? selectedAccount`
- Datos opcionales de API: `String? middleName`
- Resultados que pueden no existir: `User? currentUser`

**Factory para valores por defecto:**
```dart
class Config {
  final int timeout;
  final bool enableLogs;
  
  const Config({
    required this.timeout,
    required this.enableLogs,
  });
  
  // ✅ Factory con defaults en lugar de nullables
  factory Config.defaultConfig() {
    return const Config(
      timeout: 30,
      enableLogs: false,
    );
  }
}
```

### 11. Usar Valores como Literales
**Regla:** Reemplazar strings/números mágicos con Enums o constantes.

❌ **NO hacer:** Valores literales
```dart
if (type == 'CREDIT') { ... }  // ❌ String mágico
if (status == 1) { ... }        // ❌ Número mágico
```

✅ **SÍ usar:** Enums o constantes
```dart
// Opción 1: Enum
enum AccountType { credit, debit }
if (type == AccountType.credit) { ... }

// Opción 2: Constantes
class PaymentStatus {
  static const int pending = 1;
  static const int completed = 2;
}
if (status == PaymentStatus.pending) { ... }
```

---

## �📚 Referencias Adicionales

- **Documentación Arquitectura**: `/docs/architecture/architecture.md`
- **Module Conventions**: `/docs/architecture/module_conventions.md`
- **ModuleManager**: Clase centralizada en `core_data` para gestión de módulos
  - Registro/desregistro dinámico de módulos
  - Consolidación automática de rutas y localizaciones
  - Búsqueda de módulos por nombre
- **Melos**: `/melos.yaml` - Gestión de monorepo
- **Riverpod**: https://riverpod.dev - State management
- **GoRouter**: https://pub.dev/packages/go_router - Navegación
- **Flutter Localizations**: https://docs.flutter.dev/ui/accessibility-and-internationalization/internationalization

---

**Versión:** 3.1  
**Última actualización:** 26 de marzo de 2026  
**Tipo:** Workflow Skill Interactivo  

## Changelog

### v3.1.0 (26 de marzo de 2026) - ARCHITECTURE ALIGNMENT
**Correcciones críticas basadas en arquitectura REAL de Goals/Transfers:**

#### ✅ Added
- ➕ **Nuevo Template:** `module_definition.dart.template` - Genera ModuleDefinition con Module Pattern
- ➕ **Nuevo Template:** `navigation.dart.template` - Genera configuración de navegación completa
- ➕ **Documentación:** Goals Pattern (redirects simples con `getRouteRedirectionFlags()`)
- ➕ **Documentación:** Transfers Pattern (redirects complejos con `redirectRules()`)
- ➕ **Ejemplos:** Comparación entre ambos patrones de redirect

#### 🔧 Changed (CORRECCIONES CRÍTICAS)
- ⚠️ **CORREGIDO**: `getRoutes()` → `getRouterConfig()` (estaba incorrectamente documentado como nuevo método)
- ⚠️ **CORREGIDO**: `{ModuleName}Navigation.routes` → `{ModuleName}Navigation.routerConfig`
- ⚠️ **CORREGIDO**: Clase `{ModuleName}Module` → `{ModuleName}ModuleDefinition`
- ⚠️ **CORREGIDO**: Constructor PascalCase `super("Goals")` → snake_case `super('goals')`
- ⚠️ **CORREGIDO**: Archivo `_module_configuration.dart` → `_module_definition.dart`
- ⚠️ **CORREGIDO**: Imports de `core_data` → `feature_commons` para Module class
- ⚠️ **CORREGIDO**: Imports de `flutter/material.dart` → `flutter/widgets.dart`
- 🔄 **PR Rule #10:** Ahora documenta USO CORRECTO de `getRouteRedirectionFlags()` vs `redirectRules()`

#### ❌ Removed
- ❌ **Eliminado Template:** `advanced/redirect_rule.dart.template` (reemplazado por métodos en Module)
- ❌ **Eliminado:** Advertencias incorrectas de métodos "deprecated" que nunca lo fueron
- ❌ **Eliminado:** Clases RedirectRule standalone (ahora inline en ModuleDefinition)

#### 🐛 Fixed
- 🐛 Métodos documentados como deprecated que en realidad son los correctos
- 🐛 Arquitectura desalineada vs. implementación real de Goals/Transfers
- 🐛 Nombres de archivo inconsistentes con convención real

**⚠️ BREAKING vs v3.0:** Si generaste módulos con v3.0, ver `CHANGELOG.md` sección "Migration Guide"

---

### v3.0 (25-26 de marzo de 2026) - MAJOR UPDATE
**Cambios arquitectónicos basados en análisis de módulos reales (Goals, Payments, Transfers):**

#### ✨ Nuevas Features
- ➕ **Nueva sección:** Reglas de Arquitectura y Code Review (11 reglas del PR)
- ➕ **Pregunta #8:** Estrategia de caché (5 opciones: sin caché, in-memory, avanzado, persistent, secure)
- ➕ **Pregunta #9:** Control de acceso con RedirectRules
- ➕ **Template:** DataSource con ApiResponseHandlerMixin
- ➕ **Template:** RedirectRule completo con ejemplos de validaciones
- ➕ **Template:** Repository con opción de in-memory cache (patrón Goals)
- ➕ **Template:** Tests robustos para DataSource, Repository y ViewModel
- ➕ **📦 Templates Reutilizables (8 archivos):**
  - 🧪 Testing: DataSource, Repository, ViewModel tests
  - 🚀 Advanced: RedirectRule, Workflow Enums
  - 💾 Data: DTO con Freezed, Cache avanzado
  - 🎨 UI: ViewModel State consolidado
  - 📖 Documentación completa en `templates/README.md`

#### 🔄 Cambios Breaking (Arquitectura Modernizada)
- ⚠️ **DTOs:** Migrados de `@JsonSerializable` a `@freezed` + `@JsonSerializable`
- ⚠️ **ViewModels:** Migrados de `StateNotifier` a `AsyncNotifier`/`AutoDisposeAsyncNotifier`
- ⚠️ **Repository:** Ahora usa `ApiResponse<T>` de core_data con `.when()` handler
- ⚠️ **Module:** Se introdujeron dos patrones de control de acceso documentados:
  - `getRouteRedirectionFlags()` para feature flags simples (Goals pattern)
  - `redirectRules()` para validaciones complejas (Transfers pattern)
- ⚠️ **Navigation:** La API canónica del módulo sigue siendo `getRouterConfig()` + `{ModuleName}Navigation.routerConfig`
- ⚠️ **Entities:** Removido sufijo "Entity" (ej: `Account` en lugar de `AccountEntity`)

#### 🛠️ Mejoras Técnicas
- ✅ **Clean Architecture completa:** DataSource → Repository → ViewModel pattern
- ✅ **Error handling unificado:** ApiResponseHandlerMixin en todos los DataSources
- ✅ **Testing robusto:** Patrón AAA completo con ProviderContainer.listen()
- ✅ **Dual Enum Pattern:** Documentado para workflows (Steps + Groups)
- ✅ **3 tipos de Enums:** Simple, con Valor, con Data (workflows)
- ✅ **Strategies de Caché:** 5 niveles documentados

#### 📚 Documentación
- ➕ **11 Reglas de PR:** Workflows, ViewModels, JSON puro, sin mocks, Enums, etc.
- ➕ **Ejemplos completos:** Para cada regla con código ❌ y ✅
- ➕ **Métodos deprecated:** Claramente marcados con alternativas
- ➕ **Patrones avanzados:** Cache, RedirectRules, Testing patterns

#### 🐛 Fixes
- ✅ **pubspec.yaml:** Agregadas dependencias faltantes (freezed, freezed_annotation, flutter_riverpod)
- ✅ **Providers:** Actualizados para incluir DataSource layer
- ✅ **View:** Mejorado manejo de errores con retry button
- ✅ **Navigation:** Agregados métodos helper type-safe

#### 📋 Refactors
- 🔄 **Mapper:** Agregado método `fromDtosToEntities()` para listas
- 🔄 **Repository:** Interface + implementación separadas
- 🔄 **ViewModel:** Métodos `refresh()` y `create{Entity}()` incluidos

### v2.1 (anterior)
- ✅ Agregada pregunta sobre initialLocation
- ✅ Agregada pregunta sobre localizaciones propias
- ✅ Soporte completo para Module con/sin localizaciones
- ✅ Documentación de métodos de ModuleManager
- ✅ Mejores prácticas para tipos genéricos en Module
