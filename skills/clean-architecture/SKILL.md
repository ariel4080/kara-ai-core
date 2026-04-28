# Clean Architecture en Flutter - SKILL

## 🎯 Objetivo

Dominar la implementación de Clean Architecture en proyectos Flutter utilizando MVVM como patrón de presentación, siguiendo los estándares documentados en [architecture.md](../Repositorios/bancadigital-bm-app/docs/architecture/architecture.md) y [module_coventions.md](../Repositorios/bancadigital-bm-app/docs/architecture/module_coventions.md).

**Módulo de Referencia:** RST (Retiro Sin Tarjeta) en [bancadigital-bm-transfers](../Repositorios/bancadigital-bm-transfers/lib/src/rst/) - Único módulo con Clean Architecture completa.

---

## 📚 Conceptos Fundamentales

### ¿Qué es Clean Architecture?

Clean Architecture es un **patrón arquitectónico** propuesto por Robert C. Martin (Uncle Bob) que busca:

1. **Independencia de frameworks**: No depender de bibliotecas específicas
2. **Testeable**: Lógica de negocio independiente de UI/DB/Web
3. **Independencia de UI**: Cambiar UI sin afectar la lógica
4. **Independencia de Base de Datos**: Cambiar persistencia sin afectar reglas de negocio
5. **Independencia de agentes externos**: Reglas de negocio no conocen el mundo externo

### Capas de Clean Architecture

```
┌─────────────────────────────────────────┐
│         UI (Presentation)               │ ← Views, ViewModels, Widgets
├─────────────────────────────────────────┤
│         Domain (Business Logic)         │ ← Entities, UseCases, Interfaces
├─────────────────────────────────────────┤
│         Data (Implementation)           │ ← Repositories, DTOs, DataSources
└─────────────────────────────────────────┘
```

**Regla de dependencia:** Las capas externas pueden depender de las internas, NUNCA al revés.

---

## 🏗️ Estructura de Carpetas Obligatoria

```
feature_module/lib/
├── module_definition/                ⭐ OBLIGATORIO
│   └── [feature]_module_configuration.dart
├── navigation/                       ⭐ OBLIGATORIO
│   └── [feature]_navigation.dart
├── domain/                           ⭐ OBLIGATORIO (nuevos módulos)
│   ├── entities/                    
│   │   └── [entity]_entity.dart     # Modelos de negocio puros
│   ├── repositories/                
│   │   └── [feature]_repository.dart  # Interfaces (abstract interface class)
│   └── usecases/                    
│       ├── fetch_[entity]_usecase.dart
│       └── save_[entity]_usecase.dart
├── data/                             ⭐ OBLIGATORIO
│   ├── models/                      
│   │   └── [entity]_dto.dart        # DTOs con @freezed
│   ├── repositories/                
│   │   ├── [feature]_repository_impl.dart  # Implementación concreta
│   │   └── mappers/
│   │       └── [entity]_mapper.dart  # DTO → Entity conversions
│   └── datasources/
│       ├── remote/
│       │   └── [feature]_remote_datasource.dart
│       └── local/
│           └── [feature]_local_datasource.dart
└── ui/                               ⭐ OBLIGATORIO
    ├── [feature]/
    │   ├── viewmodels/
    │   │   └── [feature]_viewmodel.dart
    │   ├── views/
    │   │   └── [feature]_screen.dart
    │   └── widgets/
    │       └── [feature]_card.dart
    └── common/
```

---

## 🔷 Capa Domain (Lógica de Negocio)

### Entities (Entidades)

Son **objetos de negocio puros** sin dependencias externas.

**Características:**
- ✅ Inmutables (con `freezed`)
- ✅ Sin anotaciones de serialización (`@JsonSerializable`)
- ✅ Lógica de negocio simple si es necesaria
- ❌ NO conocen UI, DB, o APIs

**Ejemplo:**

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'account_entity.freezed.dart';

@freezed
class AccountEntity with _$AccountEntity {
  const AccountEntity._();
  
  const factory AccountEntity({
    required String id,
    required String accountNumber,
    required double balance,
    required CurrencyType currency,
    required AccountType type,
    required bool isActive,
  }) = _AccountEntity;
  
  // Lógica de negocio simple
  bool get hasPositiveBalance => balance > 0;
  
  String get formattedBalance => 
    '${currency.symbol} ${balance.toStringAsFixed(2)}';
}

enum CurrencyType {
  usd('USD', '\$'),
  gtq('GTQ', 'Q'),
  hnl('HNL', 'L');
  
  final String code;
  final String symbol;
  const CurrencyType(this.code, this.symbol);
}

enum AccountType {
  savings,
  checking,
  credit;
}
```

---

### Repository Interfaces

Definen **contratos** sin implementación. Son la **abstracción** entre Domain y Data.

**Características:**
- ✅ `abstract interface class` (Dart 3+)
- ✅ Métodos que retornan Entities
- ✅ Métodos async con `Future<T>`
- ❌ NO conocen DTOs ni DataSources

**Ejemplo:**

```dart
import '../entities/account_entity.dart';

abstract interface class AccountRepository {
  /// Obtiene todas las cuentas del usuario
  Future<List<AccountEntity>> fetchAccounts();
  
  /// Obtiene una cuenta por ID
  Future<AccountEntity> fetchAccountById(String accountId);
  
  /// Actualiza el estado de favorito de una cuenta
  Future<void> toggleFavorite(String accountId, bool isFavorite);
  
  /// Limpia recursos al destruir el repository
  void onDispose();
}
```

⚠️ **IMPORTANTE:** El repository en Domain es una **interfaz**, la implementación va en Data.

---

### UseCases

Encapsulan **una única acción de negocio**. Son el **punto de entrada** a la lógica de dominio.

**Principios:**
- ✅ Una sola responsabilidad (Single Responsibility)
- ✅ Reutilizables entre diferentes UIs
- ✅ Testeables sin dependencias externas
- ✅ Reciben repository desde el constructor

**Estructura:**

```dart
abstract interface class UseCase<Type, Params> {
  Future<Type> call(Params params);
}
```

**Ejemplo básico:**

```dart
import '../entities/account_entity.dart';
import '../repositories/account_repository.dart';

class FetchAccountsUseCase {
  final AccountRepository _repository;
  
  FetchAccountsUseCase(this._repository);
  
  Future<List<AccountEntity>> call() async {
    final accounts = await _repository.fetchAccounts();
    
    // Lógica de negocio: Filtrar solo cuentas activas
    return accounts.where((account) => account.isActive).toList();
  }
}
```

**Ejemplo con parámetros:**

```dart
class ToggleFavoriteAccountUseCase {
  final AccountRepository _repository;
  
  ToggleFavoriteAccountUseCase(this._repository);
  
  Future<void> call({
    required String accountId,
    required bool isFavorite,
  }) async {
    // Validación de negocio
    if (accountId.isEmpty) {
      throw ArgumentError('Account ID cannot be empty');
    }
    
    await _repository.toggleFavorite(accountId, isFavorite);
  }
}
```

**Ejemplo con Result pattern (manejo de errores):**

```dart
import 'package:dartz/dartz.dart';

class FetchAccountByIdUseCase {
  final AccountRepository _repository;
  
  FetchAccountByIdUseCase(this._repository);
  
  Future<Either<Failure, AccountEntity>> call(String accountId) async {
    try {
      if (accountId.isEmpty) {
        return Left(InvalidInputFailure('Account ID is required'));
      }
      
      final account = await _repository.fetchAccountById(accountId);
      return Right(account);
    } on NetworkException {
      return Left(NetworkFailure('No internet connection'));
    } catch (e) {
      return Left(UnexpectedFailure(e.toString()));
    }
  }
}
```

---

## 🔶 Capa Data (Implementación)

### DTOs (Data Transfer Objects)

Son **representaciones de datos** para comunicación con APIs/DB. Con serialización JSON.

**Características:**
- ✅ Usam `freezed` + `json_serializable`
- ✅ Anotaciones `@JsonKey()` para mapeo
- ✅ Sufijo `Dto` en el nombre
- ✅ Método `toJson()` y factory `fromJson()`
- ❌ NO tienen lógica de negocio

**Ejemplo:**

```dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'account_dto.freezed.dart';
part 'account_dto.g.dart';

@freezed
class AccountDto with _$AccountDto {
  const factory AccountDto({
    @JsonKey(name: 'accountId') required String id,
    @JsonKey(name: 'accountNumber') required String accountNumber,
    @JsonKey(name: 'balance') required String balance,  // API envía String
    @JsonKey(name: 'currency') required String currency,
    @JsonKey(name: 'accountType') required String type,
    @JsonKey(name: 'status') required String status,
    @JsonKey(name: 'isFavorite') bool? isFavorite,
  }) = _AccountDto;
  
  factory AccountDto.fromJson(Map<String, dynamic> json) =>
      _$AccountDtoFromJson(json);
}
```

---

### Mappers (Conversión DTO ↔ Entity)

Son **extensiones** que convierten DTOs en Entities y viceversa.

**Características:**
- ✅ Extension sobre DTO para `toEntity()`
- ✅ Extension sobre Entity para `toDto()` (si es necesario)
- ✅ Conversión de tipos (String → double, etc.)
- ✅ Valores por defecto seguros

**Ejemplo:**

```dart
import '../../domain/entities/account_entity.dart';
import '../models/account_dto.dart';

extension AccountDtoMapper on AccountDto {
  AccountEntity toEntity() {
    return AccountEntity(
      id: id,
      accountNumber: accountNumber,
      balance: double.tryParse(balance) ?? 0.0,  // Conversión segura
      currency: _mapCurrency(currency),
      type: _mapAccountType(type),
      isActive: status.toLowerCase() == 'active',
    );
  }
  
  CurrencyType _mapCurrency(String currency) {
    switch (currency.toUpperCase()) {
      case 'USD':
        return CurrencyType.usd;
      case 'GTQ':
        return CurrencyType.gtq;
      case 'HNL':
        return CurrencyType.hnl;
      default:
        return CurrencyType.usd;  // Default seguro
    }
  }
  
  AccountType _mapAccountType(String type) {
    switch (type.toLowerCase()) {
      case 'savings':
        return AccountType.savings;
      case 'checking':
        return AccountType.checking;
      case 'credit':
        return AccountType.credit;
      default:
        return AccountType.savings;
    }
  }
}

// Mapper inverso (si es necesario)
extension AccountEntityMapper on AccountEntity {
  AccountDto toDto() {
    return AccountDto(
      id: id,
      accountNumber: accountNumber,
      balance: balance.toString(),
      currency: currency.code,
      type: type.name,
      status: isActive ? 'active' : 'inactive',
    );
  }
}
```

---

### Repository Implementation

Implementa la **interfaz** del Domain usando DataSources.

**Características:**
- ✅ Implementa `implements [Feature]Repository` del Domain
- ✅ Constructor con DataSources inyectados
- ✅ Usa Mappers para DTO → Entity
- ✅ Maneja excepciones y las convierte a errores de dominio
- ✅ Cache opcional para optimización

**Ejemplo:**

```dart
import '../../domain/entities/account_entity.dart';
import '../../domain/repositories/account_repository.dart';
import '../datasources/remote/account_remote_datasource.dart';
import '../datasources/local/account_local_datasource.dart';
import '../repositories/mappers/account_mapper.dart';

class AccountRepositoryImpl implements AccountRepository {
  final AccountRemoteDataSource _remoteDataSource;
  final AccountLocalDataSource _localDataSource;
  
  // Cache en memoria
  List<AccountEntity>? _cachedAccounts;
  DateTime? _cacheTime;
  static const _cacheDuration = Duration(minutes: 5);
  
  AccountRepositoryImpl({
    required AccountRemoteDataSource remoteDataSource,
    required AccountLocalDataSource localDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource;
  
  @override
  Future<List<AccountEntity>> fetchAccounts() async {
    // Cache validation
    if (_cachedAccounts != null && _isCacheValid()) {
      return _cachedAccounts!;
    }
    
    try {
      // Intentar primero desde la API
      final accountsDto = await _remoteDataSource.getAccounts();
      final accounts = accountsDto.map((dto) => dto.toEntity()).toList();
      
      // Guardar en cache local y memoria
      await _localDataSource.saveAccounts(accountsDto);
      _cachedAccounts = accounts;
      _cacheTime = DateTime.now();
      
      return accounts;
    } catch (e) {
      // Fallback a cache local
      final localAccountsDto = await _localDataSource.getAccounts();
      return localAccountsDto.map((dto) => dto.toEntity()).toList();
    }
  }
  
  @override
  Future<AccountEntity> fetchAccountById(String accountId) async {
    final accountDto = await _remoteDataSource.getAccountById(accountId);
    return accountDto.toEntity();
  }
  
  @override
  Future<void> toggleFavorite(String accountId, bool isFavorite) async {
    await _remoteDataSource.updateFavoriteStatus(accountId, isFavorite);
    
    // Invalidar cache
    _cachedAccounts = null;
  }
  
  @override
  void onDispose() {
    _cachedAccounts = null;
    _cacheTime = null;
  }
  
  bool _isCacheValid() {
    if (_cacheTime == null) return false;
    return DateTime.now().difference(_cacheTime!) < _cacheDuration;
  }
}
```

---

### DataSources

Manejan la **comunicación externa** (API, DB local, etc.).

**Remote DataSource (API):**

```dart
import 'package:dio/dio.dart';
import '../models/account_dto.dart';

abstract interface class AccountRemoteDataSource {
  Future<List<AccountDto>> getAccounts();
  Future<AccountDto> getAccountById(String accountId);
  Future<void> updateFavoriteStatus(String accountId, bool isFavorite);
}

class AccountRemoteDataSourceImpl implements AccountRemoteDataSource {
  final Dio _dio;
  
  AccountRemoteDataSourceImpl(this._dio);
  
  @override
  Future<List<AccountDto>> getAccounts() async {
    final response = await _dio.get('/accounts');
    
    if (response.statusCode == 200) {
      final List<dynamic> data = response.data['accounts'];
      return data.map((json) => AccountDto.fromJson(json)).toList();
    } else {
      throw ServerException('Failed to fetch accounts');
    }
  }
  
  @override
  Future<AccountDto> getAccountById(String accountId) async {
    final response = await _dio.get('/accounts/$accountId');
    
    if (response.statusCode == 200) {
      return AccountDto.fromJson(response.data);
    } else {
      throw ServerException('Account not found');
    }
  }
  
  @override
  Future<void> updateFavoriteStatus(String accountId, bool isFavorite) async {
    await _dio.patch('/accounts/$accountId/favorite', data: {
      'isFavorite': isFavorite,
    });
  }
}
```

**Local DataSource (Cache):**

```dart
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/account_dto.dart';

abstract interface class AccountLocalDataSource {
  Future<List<AccountDto>> getAccounts();
  Future<void> saveAccounts(List<AccountDto> accounts);
  Future<void> clearCache();
}

class AccountLocalDataSourceImpl implements AccountLocalDataSource {
  final SharedPreferences _prefs;
  static const _key = 'cached_accounts';
  
  AccountLocalDataSourceImpl(this._prefs);
  
  @override
  Future<List<AccountDto>> getAccounts() async {
    final jsonString = _prefs.getString(_key);
    if (jsonString == null) {
      return [];
    }
    
    final List<dynamic> jsonList = json.decode(jsonString);
    return jsonList.map((json) => AccountDto.fromJson(json)).toList();
  }
  
  @override
  Future<void> saveAccounts(List<AccountDto> accounts) async {
    final jsonList = accounts.map((dto) => dto.toJson()).toList();
    await _prefs.setString(_key, json.encode(jsonList));
  }
  
  @override
  Future<void> clearCache() async {
    await _prefs.remove(_key);
  }
}
```

---

## 🔵 Capa UI (Presentación con MVVM)

### ViewModels con Riverpod

**Características:**
- ✅ Extienden `AsyncNotifier<T>` o `Notifier<T>`
- ✅ Reciben UseCases desde el constructor
- ✅ Transforman Entities en estado de UI
- ✅ Manejan errores y estados de carga
- ✅ NO conocen detalles de implementación del Domain

**Ejemplo:**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../../domain/entities/account_entity.dart';
import '../../domain/usecases/fetch_accounts_usecase.dart';
import '../../domain/usecases/toggle_favorite_account_usecase.dart';

part 'accounts_viewmodel.g.dart';

@riverpod
class AccountsViewModel extends _$AccountsViewModel {
  late final FetchAccountsUseCase _fetchAccountsUseCase;
  late final ToggleFavoriteAccountUseCase _toggleFavoriteUseCase;
  
  @override
  Future<List<AccountEntity>> build() async {
    // Inyección de UseCases
    _fetchAccountsUseCase = ref.read(fetchAccountsUseCaseProvider);
    _toggleFavoriteUseCase = ref.read(toggleFavoriteAccountUseCaseProvider);
    
    // Cargar datos inicial
    return _fetchAccounts();
  }
  
  Future<List<AccountEntity>> _fetchAccounts() async {
    return await _fetchAccountsUseCase();
  }
  
  Future<void> refreshAccounts() async {
    state = const AsyncValue.loading();
    state = await AsyncValue.guard(() => _fetchAccounts());
  }
  
  Future<void> toggleFavorite(String accountId, bool isFavorite) async {
    await _toggleFavoriteUseCase(
      accountId: accountId,
      isFavorite: isFavorite,
    );
    
    // Refrescar lista
    await refreshAccounts();
  }
}
```

---

### Views (Screens)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../viewmodels/accounts_viewmodel.dart';

class AccountsScreen extends ConsumerWidget {
  const AccountsScreen({super.key});
  
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final accountsAsync = ref.watch(accountsViewModelProvider);
    
    return Scaffold(
      appBar: AppBar(title: const Text('Mis Cuentas')),
      body: accountsAsync.when(
        data: (accounts) => _buildAccountsList(accounts, ref),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (error, stack) => _buildError(error, ref),
      ),
    );
  }
  
  Widget _buildAccountsList(List<AccountEntity> accounts, WidgetRef ref) {
    if (accounts.isEmpty) {
      return const Center(child: Text('No hay cuentas disponibles'));
    }
    
    return RefreshIndicator(
      onRefresh: () => ref.read(accountsViewModelProvider.notifier).refreshAccounts(),
      child: ListView.builder(
        itemCount: accounts.length,
        itemBuilder: (context, index) {
          final account = accounts[index];
          return AccountCard(
            account: account,
            onFavoriteToggle: () {
              ref.read(accountsViewModelProvider.notifier).toggleFavorite(
                account.id,
                !account.isFavorite,
              );
            },
          );
        },
      ),
    );
  }
  
  Widget _buildError(Object error, WidgetRef ref) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.error, size: 48, color: Colors.red),
          const SizedBox(height: 16),
          Text(error.toString()),
          const SizedBox(height: 16),
          ElevatedButton(
            onPressed: () => ref.refresh(accountsViewModelProvider),
            child: const Text('Reintentar'),
          ),
        ],
      ),
    );
  }
}
```

---

## 🔧 Providers Setup

**UseCases Providers:**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../domain/usecases/fetch_accounts_usecase.dart';
import '../domain/usecases/toggle_favorite_account_usecase.dart';
import 'repository_providers.dart';

part 'usecase_providers.g.dart';

@riverpod
FetchAccountsUseCase fetchAccountsUseCase(FetchAccountsUseCaseRef ref) {
  return FetchAccountsUseCase(
    ref.read(accountRepositoryProvider),
  );
}

@riverpod
ToggleFavoriteAccountUseCase toggleFavoriteAccountUseCase(
  ToggleFavoriteAccountUseCaseRef ref,
) {
  return ToggleFavoriteAccountUseCase(
    ref.read(accountRepositoryProvider),
  );
}
```

**Repository Providers:**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import '../domain/repositories/account_repository.dart';
import '../data/repositories/account_repository_impl.dart';
import 'datasource_providers.dart';

part 'repository_providers.g.dart';

@riverpod
AccountRepository accountRepository(AccountRepositoryRef ref) {
  final repository = AccountRepositoryImpl(
    remoteDataSource: ref.read(accountRemoteDataSourceProvider),
    localDataSource: ref.read(accountLocalDataSourceProvider),
  );
  
  ref.onDispose(() {
    repository.onDispose();
  });
  
  return repository;
}
```

**DataSource Providers:**

```dart
import 'package:riverpod_annotation/riverpod_annotation.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../data/datasources/remote/account_remote_datasource.dart';
import '../data/datasources/local/account_local_datasource.dart';
import '../../../core/networking/dio_provider.dart';

part 'datasource_providers.g.dart';

@riverpod
AccountRemoteDataSource accountRemoteDataSource(
  AccountRemoteDataSourceRef ref,
) {
  return AccountRemoteDataSourceImpl(
    ref.read(dioProvider),
  );
}

@riverpod
Future<AccountLocalDataSource> accountLocalDataSource(
  AccountLocalDataSourceRef ref,
) async {
  final prefs = await SharedPreferences.getInstance();
  return AccountLocalDataSourceImpl(prefs);
}
```

---

## ✅ Checklist de Implementación

### Fase 1: Domain Layer
- [ ] Crear carpeta `domain/`
- [ ] Definir Entities (sin anotaciones JSON)
- [ ] Definir Repository Interfaces (`abstract interface class`)
- [ ] Crear UseCases (uno por acción de negocio)
- [ ] Validar que Domain no tenga imports de Data/UI

### Fase 2: Data Layer
- [ ] Crear carpeta `data/`
- [ ] Definir DTOs con `freezed` y `json_serializable`
- [ ] Crear Mappers (extensions DTO → Entity)
- [ ] Implementar DataSources (remote, local)
- [ ] Implementar Repository (`implements` de Domain)
- [ ] Agregar cache si es necesario

### Fase 3: UI Layer
- [ ] Crear ViewModels con `AsyncNotifier<T>`
- [ ] Inyectar UseCases en ViewModels
- [ ] Crear Views que consuman ViewModels
- [ ] Manejar estados (loading, data, error)
- [ ] Implementar widgets reutilizables

### Fase 4: Providers
- [ ] Crear providers de DataSources
- [ ] Crear providers de Repositories
- [ ] Crear providers de UseCases
- [ ] Crear providers de ViewModels
- [ ] Agregar `onDispose` donde sea necesario

### Fase 5: Testing
- [ ] Tests unitarios de Entities
- [ ] Tests de UseCases (con mocks de Repository)
- [ ] Tests de Mappers
- [ ] Tests de Repository (con mocks de DataSources)
- [ ] Tests de ViewModel (con mocks de UseCases)

---

## 🚫 Errores Comunes

### ❌ Domain depende de Data

```dart
// ❌ INCORRECTO
// domain/entities/account_entity.dart
import '../../data/models/account_dto.dart';  // ¡NO!
```

**Solución:** Domain NO debe importar nada de Data.

---

### ❌ UseCases demasiado genéricos

```dart
// ❌ INCORRECTO
class AccountUseCase {
  Future<List<AccountEntity>> getAccounts() {}
  Future<void> deleteAccount() {}
  Future<void> updateAccount() {}
}
```

**Solución:** Un UseCase = Una acción

```dart
// ✅ CORRECTO
class FetchAccountsUseCase { }
class DeleteAccountUseCase { }
class UpdateAccountUseCase { }
```

---

### ❌ Entities con anotaciones JSON

```dart
// ❌ INCORRECTO
@freezed
class AccountEntity with _$AccountEntity {
  const factory AccountEntity({
    @JsonKey(name: 'id') required String id,  // ¡NO!
  }) = _AccountEntity;
  
  factory AccountEntity.fromJson(Map<String, dynamic> json) =>
      _$AccountEntityFromJson(json);  // ¡NO!
}
```

**Solución:** Solo DTOs tienen serialización JSON.

---

### ❌ ViewModel llama directamente a Repository

```dart
// ❌ INCORRECTO
class AccountsViewModel extends AsyncNotifier<List<AccountEntity>> {
  late final AccountRepository _repository;  // ¡NO!
  
  @override
  Future<List<AccountEntity>> build() async {
    _repository = ref.read(accountRepositoryProvider);
    return _repository.fetchAccounts();  // ¡NO!
  }
}
```

**Solución:** ViewModel usa UseCases, no Repositories.

```dart
// ✅ CORRECTO
class AccountsViewModel extends AsyncNotifier<List<AccountEntity>> {
  late final FetchAccountsUseCase _fetchAccountsUseCase;
  
  @override
  Future<List<AccountEntity>> build() async {
    _fetchAccountsUseCase = ref.read(fetchAccountsUseCaseProvider);
    return _fetchAccountsUseCase();
  }
}
```

---

## 📊 Migración de Código Legacy

### Paso a Paso

**Estado Actual (Sin Domain):**
```
lib/
├── data/
│   ├── models/
│   └── repositories/
└── ui/
    ├── viewmodels/  # ViewModel → Repository directamente
    └── views/
```

**1. Crear capa Domain:**

- Extraer lógica de negocio de ViewModels
- Crear Entities (copiar DTOs sin JSON)
- Crear Repository Interfaces
- Crear UseCases

**2. Refactorizar Data:**

- Hacer que Repository implemente la interfaz de Domain
- Crear Mappers DTO → Entity

**3. Refactorizar UI:**

- ViewModels usan UseCases
- ViewModels trabajan con Entities

---

## 🎯 Criterios de Éxito

✅ **Independencia:** Domain no tiene imports de Data/UI
✅ **Testeable:** UseCases testeables con mocks
✅ **Escalable:** Agregar features sin tocar Domain existente
✅ **Mantenible:** Cambiar UI sin tocar lógica de negocio
✅ **Reutilizable:** UseCases usables desde múltiples UIs

---

## 📖 Referencias

- [architecture.md](../Repositorios/bancadigital-bm-app/docs/architecture/architecture.md) - Guía oficial de arquitectura
- [module_coventions.md](../Repositorios/bancadigital-bm-app/docs/architecture/module_coventions.md) - Convenciones de módulos
- Módulo RST: [bancadigital-bm-transfers/lib/src/rst](../Repositorios/bancadigital-bm-transfers/lib/src/rst/)
- Clean Architecture - Robert C. Martin
- [Riverpod Documentation](https://riverpod.dev)

---

**Versión:** 1.0  
**Fecha:** 12 de marzo de 2026  
**Autor:** Chapter Lead Mobile  
**Estado:** ✅ Listo para Q2 2026
