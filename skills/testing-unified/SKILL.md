---
name: testing-unified
description: "Guía completa de testing Flutter. Use when: crear tests, verificar coverage, mockito, riverpod testing, unit tests, widget tests."
applyTo:
  - "**/*_test.dart"
  - "**/test/**"
  - "**/*.dart"
---

# Testing Unified - Flutter & Dart

Guía completa de testing para bancadigital-bm-app. Consolidación de testing, testing-advanced y testing-expert.

---

## 📝 Convenciones Obligatorias

### 1. Nombres de Archivos

**✅ Correcto:**
```
accounts_view_model_test.dart
exchange_rate_repository_remote_test.dart
token_utils_test.dart
```

**❌ Incorrecto:**
```
accounts_view_model_tests.dart  # NO usar plural
accounts_view_model_spec.dart   # NO usar spec
test_accounts_view_model.dart   # NO empezar con test_
```

**Regla:** Archivos SIEMPRE terminan en `_test.dart` (singular).

---

### 2. Nombres de Tests

**Formato obligatorio:**
```
"should [resultado esperado] when [condición]"
```

**✅ Ejemplos correctos:**
```dart
test('should return Transfer when repository succeeds', () async {});
test('should throw NetworkException when device is offline', () async {});
test('should emit loading then data when fetchAccounts succeeds', () {});
test('should cache result when called multiple times', () async {});
test('should filter inactive accounts when fetching', () {});
```

**❌ Ejemplos incorrectos:**
```dart
test('accounts test', () {});           // Muy vago
test('it works', () {});                // No descriptivo
test('fetchAccounts', () {});           // Solo nombre del método
test('test fetch data', () {});         // No usa formato should-when
```

---

### 3. Estructura Arrange-Act-Assert (AAA)

**Patrón obligatorio en TODOS los tests:**

```dart
test('should return AccountEntity when fetchAccounts is successful', () async {
  /// Arrange - Configurar mocks, datos, estado inicial
  final mockRepository = MockAccountsRepository();
  when(mockRepository.fetchAccounts()).thenAnswer((_) async => accountEntity);
  
  final container = ProviderContainer(
    overrides: [
      accountsRepositoryProvider.overrideWithValue(mockRepository),
    ],
  );

  /// Act - Ejecutar la acción a probar
  final notifier = container.read(accountDetailViewModelProvider.notifier);
  notifier.fetchAccounts(top: 3, forceRefresh: false);
  await container.pump();

  /// Assert - Verificar resultados
  final finalState = notifier.state;
  expect(finalState, isA<AsyncData<AccountEntity>>());
  expect(finalState.value, equals(accountEntity));
});
```

**Secciones:**
1. **Arrange:** Setup de mocks, fixtures, estado inicial
2. **Act:** Llamar al método/función bajo prueba
3. **Assert:** Verificar que el resultado es el esperado

---

## 📊 Coverage Requirements (Q2 2026)

### Targets Obligatorios:

| Componente | Coverage Mínimo | Enforcement |
|------------|-----------------|-------------|
| **ViewModels nuevos** | ≥ 80% | 🚨 BLOQUEANTE |
| **ViewModels modificados** | No reducir existente | 🚨 BLOQUEANTE |
| **Repositories nuevos** | ≥ 75% | 🚨 BLOQUEANTE |
| **UseCases nuevos** | ≥ 85% | ⚠️ ADVERTENCIA |
| **Utils/Helpers nuevos** | ≥ 90% | 🚨 BLOQUEANTE |
| **Widgets** | ≥ 60% | ⚠️ ADVERTENCIA |
| **Global** | ≥ 75% | 📊 REPORTADO |

### Evidencia en PR:

- [ ] Screenshot de tests ejecutados (todos verde)
- [ ] Coverage report cuando se agregan tests nuevos
- [ ] Comentar coverage % en descripción del PR

---

## 🎯 Componentes a Probar

### 1. ViewModels (OBLIGATORIO)

**Qué probar:**
- Estados iniciales
- Transiciones de estados (loading → data → error)
- Interacción con repositories
- Manejo de errores
- Operaciones asíncronas

**Patrón con Riverpod:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();
  
  late MockAccountsRepository mockRepository;
  late ProviderContainer container;

  setUp(() {
    mockRepository = MockAccountsRepository();
    container = ProviderContainer(
      overrides: [
        accountsRepositoryProvider.overrideWithValue(mockRepository),
      ],
    );
  });

  tearDown(() {
    container.dispose();
  });

  group('AccountViewModel', () {
    test('should return AsyncData when fetchAccounts succeeds', () async {
      /// Arrange
      final accountEntity = CifAccountData(/* ... */);
      when(mockRepository.fetchCifsAccounts(top: 3, forceRefresh: false))
          .thenAnswer((_) async => accountEntity);

      /// Act
      final notifier = container.read(accountDetailViewModelProvider.notifier);
      notifier.fetchAccounts(top: 3, forceRefresh: false);
      await container.pump();

      /// Assert
      final state = notifier.state;
      expect(state, isA<AsyncData<CifAccountData>>());
      expect(state.value, equals(accountEntity));
    });

    test('should return AsyncError when fetchAccounts fails', () async {
      /// Arrange
      when(mockRepository.fetchCifsAccounts(top: 3, forceRefresh: false))
          .thenThrow(NetworkException('Connection failed'));

      /// Act
      final notifier = container.read(accountDetailViewModelProvider.notifier);
      notifier.fetchAccounts(top: 3, forceRefresh: false);
      await container.pump();

      /// Assert
      final state = notifier.state;
      expect(state, isA<AsyncError>());
    });
  });
}
```

**Elementos clave:**
- `TestWidgetsFlutterBinding.ensureInitialized()`
- `setUp()` y `tearDown()` para inicializar/limpiar
- `ProviderContainer` con `overrides` para inyectar mocks
- `container.pump()` para procesar futures
- `group()` para agrupar tests relacionados

---

### 2. Repositories (OBLIGATORIO)

**Qué probar:**
- Llamadas exitosas al datasource
- Transformación de DTOs a Entities
- Manejo de errores (HTTP 4xx, 5xx)
- Casos edge (data null, listas vacías)

**Patrón:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';

void main() {
  late ExchangeRateDataSource mockDataSource;
  late ExchangeRateRepositoryRemote repository;

  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    mockDataSource = MockExchangeRateDataSource();
    repository = ExchangeRateRepositoryRemote(dataSource: mockDataSource);

    provideDummy<ApiResponse<Map<String, ExchangeRateDto>>>(
      SuccessApiResponse<Map<String, ExchangeRateDto>>({}),
    );
  });

  test('should return ExchangeRate when datasource succeeds', () async {
    /// Arrange
    final successResponse = SuccessApiResponse<Map<String, ExchangeRateDto>>({
      'USD': ExchangeRateDto(
        foreignCurrencyBuy: 600.1234,
        foreignCurrencySell: 610.1234,
        date: DateTime.now(),
      ),
    });

    when(mockDataSource.getExchangeRates(CountryIso.CR.toDto()))
        .thenAnswer((_) async => successResponse);

    /// Act
    final result = await repository.getExchangeRates(CountryIso.CR);

    /// Assert
    expect(result, isA<Map<String, ExchangeRate>>());
    expect(result.keys.length, 1);
    expect(result['USD']?.currencyIsoCode, CurrencyIso.USD);
    expect(result['USD']?.foreignCurrencyBuy, 600.1234);
    expect(result['USD']?.foreignCurrencySell, 610.1234);
  });

  test('should throw ErrorApiResponse when datasource fails with HTTP 500', () async {
    /// Arrange
    final errorResponse = ErrorApiResponse<Map<String, ExchangeRateDto>>(
      httpErrorMessage: 'Internal Server Error',
      httpStatusCode: 500,
    );

    when(mockDataSource.getExchangeRates(CountryIso.CR.toDto()))
        .thenAnswer((_) async => errorResponse);

    /// Act & Assert
    try {
      await repository.getExchangeRates(CountryIso.CR);
      fail('Should have thrown ErrorApiResponse');
    } on ErrorApiResponse catch (error) {
      expect(error.httpStatusCode, 500);
      expect(error.httpErrorMessage, 'Internal Server Error');
    }
  });
}
```

**Elementos clave:**
- `provideDummy()` para tipos genéricos (evita errores Mockito)
- `when().thenAnswer()` para respuestas asíncronas
- Probar transformación DTO → Entity
- Probar TANTO casos exitosos COMO errores

---

### 3. Utils/Helpers/Converters

**Qué probar:**
- Funcionalidad de conversión
- Validaciones de entrada
- Manejo de errores
- Consistencia de resultados

**Patrón:**

```dart
import 'package:test/test.dart';
import 'dart:typed_data';

void main() {
  group('TokenUtils', () {
    test('generateToken should return a 6 digit code', () {
      /// Arrange
      final seed = Seed(seedExample);
      final dateTime = DateTime.now();

      /// Act
      final token = seed.generateToken(dateTime);

      /// Assert
      expect(token.toString().length, 6);
    });

    test('generateToken should produce consistent output for same input', () {
      /// Arrange
      final seed = Seed(seedExample);
      final dateTime = DateTime(2023, 10, 1, 12, 0);

      /// Act
      final token1 = seed.generateToken(dateTime);
      final token2 = seed.generateToken(dateTime);

      /// Assert
      expect(token1, equals(token2));
    });
  });

  group('DateTimeExtensions', () {
    test('generateTimeStampData should produce an 8 length Uint8List', () {
      /// Arrange
      final dateTime = DateTime.now();

      /// Act
      final data = dateTime.generateTimeStampData();

      /// Assert
      expect(data, isA<Uint8List>());
      expect(data.length, equals(8));
    });
  });
}
```

**Elementos clave:**
- `group()` para agrupar tests relacionados
- Tests de consistencia (mismo input = mismo output)
- Tests de formato (longitud, tipo)
- Tests de validación

---

### 4. Mappers

**Qué probar:**
- Transformación DTO → Entity
- Transformación Entity → DTO
- Manejo de campos null
- Valores por defecto

**Patrón:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/services.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('CardMapper', () {
    test('should create valid CardEntity from CardResponse', () async {
      /// Arrange
      final jsonString = await rootBundle.loadString(
        '${Directory.current.path}/test/mock_json/card_response.json',
        cache: false,
      );
      final map = json.decode(jsonString);
      final cardResponse = CardResponse.fromJson(map);
      final mapper = CardMapper();

      /// Act
      final cardEntity = mapper.fromDtoToEntity(cardResponse);

      /// Assert
      expect(cardEntity.cards.length, 2);
      expect(cardEntity.cards.first.alias, 'Tarjeta para compras');
      expect(cardEntity.cards.first.status, CardStatus.ACTIVE);
      expect(cardEntity.cards.first.localBalance, 3700.00);
    });

    test('should handle null values with defaults', () {
      /// Arrange
      final cardResponse = CardResponse(
        alias: null,  // Campo null
        status: 'ACTIVE',
        balance: 0.0,
      );
      final mapper = CardMapper();

      /// Act
      final cardEntity = mapper.fromDtoToEntity(cardResponse);

      /// Assert
      expect(cardEntity.alias, isEmpty);  // Default para null
      expect(cardEntity.status, CardStatus.ACTIVE);
    });
  });
}
```

**Cuándo usar fixtures:**
- Respuestas complejas de API
- Múltiples tests con mismos datos
- Mantener datos de prueba centralizados

---

## 🔧 Mockito Patterns

### Crear Mocks

**Generación automática:**

```dart
// En test/utils/mocks_generator/consolidated_mocks_generator.dart
import 'package:mockito/annotations.dart';
import 'package:accounts/data/repository/accounts_repository.dart';

@GenerateMocks([
  AccountsRepository,
  ExchangeRateDataSource,
])
void main() {}
```

**Generar mocks:**
```bash
flutter pub run build_runner build --delete-conflicting-outputs
```

**Uso:**
```dart
import 'mocks_generator.mocks.dart';

void main() {
  late MockAccountsRepository mockRepository;
  
  setUp(() {
    mockRepository = MockAccountsRepository();
  });
}
```

---

### when() - Configurar Respuestas

**Respuestas síncronas:**
```dart
when(mockRepository.isLoggedIn()).thenReturn(true);
when(mockRepository.getBalance()).thenReturn(1000.50);
```

**Respuestas asíncronas:**
```dart
when(mockRepository.fetchAccounts())
    .thenAnswer((_) async => accountEntity);

when(mockDataSource.getExchangeRates(any))
    .thenAnswer((_) async => Future.value(successResponse));
```

**Lanzar excepciones:**
```dart
when(mockRepository.fetchAccounts())
    .thenThrow(NetworkException('Connection failed'));

when(mockDataSource.getData())
    .thenAnswer((_) async => throw ServerException());
```

**Respuestas condicionales:**
```dart
when(mockRepository.fetchAccounts(forceRefresh: true))
    .thenAnswer((_) async => freshData);

when(mockRepository.fetchAccounts(forceRefresh: false))
    .thenAnswer((_) async => cachedData);
```

**Any matcher:**
```dart
when(mockRepository.fetchAccountById(any))
    .thenAnswer((_) async => testAccount);

when(mockRepository.saveAccount(argThat(isA<AccountEntity>())))
    .thenAnswer((_) async => null);
```

---

### verify() - Verificar Llamadas

**Verificar que se llamó:**
```dart
verify(mockRepository.fetchAccounts()).called(1);
verify(mockRepository.saveCache(any)).called(1);
```

**Verificar con argumentos específicos:**
```dart
verify(mockRepository.fetchAccounts(top: 3, forceRefresh: false)).called(1);
verify(mockDataSource.getExchangeRates(CountryIso.CR.toDto())).called(1);
```

**Verificar que NO se llamó:**
```dart
verifyNever(mockRepository.clearCache());
verifyNoMoreInteractions(mockRepository);
```

**Verificar orden de llamadas:**
```dart
verifyInOrder([
  mockRepository.fetchAccounts(),
  mockRepository.saveCache(any),
]);
```

**Capturar argumentos:**
```dart
final captured = verify(mockRepository.saveAccount(captureAny)).captured;
expect(captured[0], isA<AccountEntity>());
expect(captured[0].id, '123');
```

---

### provideDummy() - Para Tipos Genéricos

**Problema:**
```dart
// Mockito falla si el tipo de retorno es genérico sin dummy
when(mockDataSource.getData()).thenAnswer((_) async => response);
// Error: Missing stub for generic type
```

**Solución:**
```dart
setUp(() {
  provideDummy<ApiResponse<Map<String, ExchangeRateDto>>>(
    SuccessApiResponse<Map<String, ExchangeRateDto>>({}),
  );
});
```

---

## 🧩 Riverpod Testing Patterns

### Providers Básicos

```dart
test('should read value from provider', () {
  /// Arrange
  final container = ProviderContainer();

  /// Act
  final value = container.read(myProvider);

  /// Assert
  expect(value, equals('expected'));
  
  /// Cleanup
  container.dispose();
});
```

### StateNotifier Providers

```dart
test('should update state when method is called', () {
  /// Arrange
  final container = ProviderContainer();
  final notifier = container.read(myStateNotifierProvider.notifier);

  /// Act
  notifier.updateValue('new value');

  /// Assert
  final state = container.read(myStateNotifierProvider);
  expect(state, equals('new value'));
  
  container.dispose();
});
```

### Overriding Providers

```dart
test('should use mocked repository', () {
  /// Arrange
  final mockRepo = MockRepository();
  when(mockRepo.getData()).thenAnswer((_) async => testData);
  
  final container = ProviderContainer(
    overrides: [
      repositoryProvider.overrideWithValue(mockRepo),
    ],
  );

  /// Act
  final result = await container.read(dataProvider.future);

  /// Assert
  expect(result, equals(testData));
  verify(mockRepo.getData()).called(1);
  
  container.dispose();
});
```

### AsyncValue Testing

```dart
test('should handle AsyncValue states', () async {
  /// Arrange
  final container = ProviderContainer();
  
  /// Loading state
  expect(
    container.read(asyncProvider),
    isA<AsyncLoading>(),
  );

  /// Wait for data
  await container.pump();

  /// Data state
  final state = container.read(asyncProvider);
  expect(state, isA<AsyncData>());
  expect(state.value, equals(expectedData));
  
  container.dispose();
});
```

### Testing Listeners

```dart
test('should notify listeners when state changes', () async {
  /// Arrange
  when(mockRepository.fetchData())
      .thenAnswer((_) async => testData);
  
  final listener = Listener<AsyncValue<Data>>();
  
  container.listen(
    dataProvider,
    listener,
    fireImmediately: true,
  );
  
  /// Wait for data
  await container.read(dataProvider.future);
  
  /// Assert
  verifyInOrder([
    listener(null, any),  // Initial loading
    listener(any, any),   // Data loaded
  ]);
});

class Listener<T> extends Mock {
  void call(T? previous, T next);
}
```

---

## 🧪 Casos de Prueba Esenciales

### Para ViewModels (Checklist Completo)

✅ **SIEMPRE probar:**

1. **Estado inicial correcto**
   ```dart
   test('initial state should be loading', () {
     final state = container.read(viewModelProvider);
     expect(state, isA<AsyncLoading>());
   });
   ```

2. **Carga exitosa de datos**
   ```dart
   test('should load data successfully', () async {
     when(mockRepo.fetchData()).thenAnswer((_) async => testData);
     await container.read(viewModelProvider.future);
     final state = container.read(viewModelProvider);
     expect(state.value, equals(testData));
   });
   ```

3. **Manejo de error de red**
   ```dart
   test('should handle network error', () async {
     when(mockRepo.fetchData()).thenThrow(NetworkException());
     try {
       await container.read(viewModelProvider.future);
     } catch (_) {}
     final state = container.read(viewModelProvider);
     expect(state, isA<AsyncError>());
   });
   ```

4. **Manejo de error de servidor (5xx)**
   ```dart
   test('should handle server error 500', () async {
     when(mockRepo.fetchData()).thenThrow(
       ServerException(message: 'Internal error', code: 500),
     );
     // Assert error state
   });
   ```

5. **Manejo de error de validación (4xx)**
   ```dart
   test('should handle validation error 400', () async {
     when(mockRepo.saveData(any)).thenThrow(
       ValidationException(message: 'Invalid data'),
     );
     // Assert error state
   });
   ```

6. **Estados loading → data → error**
   ```dart
   test('should transition through states correctly', () async {
     // Verify state transitions
   });
   ```

7. **Refresh/retry functionality**
   ```dart
   test('should retry after error', () async {
     when(mockRepo.fetchData())
         .thenThrow(NetworkException())
         .thenAnswer((_) async => testData);
     
     final notifier = container.read(viewModelProvider.notifier);
     await notifier.fetchData();  // Falla
     await notifier.retry();     // Retry exitoso
     
     verify(mockRepo.fetchData()).called(2);
   });
   ```

8. **Dispose/cleanup correcto**
   ```dart
   tearDown(() {
     container.dispose();
   });
   ```

---

### Para Repositories (Checklist Completo)

✅ **SIEMPRE probar:**

1. **Llamada exitosa al datasource**
2. **Transformación correcta DTO → Entity**
3. **Error HTTP 400 (Bad Request)**
4. **Error HTTP 401 (Unauthorized)**
5. **Error HTTP 500 (Server Error)**
6. **Timeout de red**
7. **Data null o vacía**

---

### Para Utils/Helpers (Checklist Completo)

✅ **SIEMPRE probar:**

1. **Caso básico (happy path)**
2. **Valores límite (0, null, vacío)**
3. **Validaciones (input inválido)**
4. **Consistencia (mismo input = mismo output)**
5. **Excepciones esperadas**

---

## 🎯 Matchers Comunes

### Tipos
```dart
expect(result, isA<AccountEntity>());
expect(state, isA<AsyncData<Account>>());
expect(error, isA<NetworkException>());
```

### Valores
```dart
expect(value, equals(100));
expect(name, 'John Doe');
expect(isValid, isTrue);
expect(isValid, isFalse);
expect(result, isNull);
expect(result, isNotNull);
```

### Colecciones
```dart
expect(list, isEmpty);
expect(list, isNotEmpty);
expect(list.length, 3);
expect(list, contains('item'));
expect(list, containsAll(['a', 'b']));
```

### Números
```dart
expect(value, greaterThan(10));
expect(value, lessThan(100));
expect(value, greaterThanOrEqualTo(5));
expect(value, inRange(0, 100));
expect(value, closeTo(3.14, 0.01));  // 3.14 ± 0.01
```

### Strings
```dart
expect(text, startsWith('Hello'));
expect(text, endsWith('world'));
expect(text, contains('Flutter'));
expect(text, matches(r'\d{3}-\d{4}'));  // Regex
```

---

## 🎨 Widget Testing

### Estructura básica:

```dart
testWidgets('should display account name', (WidgetTester tester) async {
  /// Arrange
  const account = AccountEntity(id: '1', name: 'Test Account');
  
  /// Act
  await tester.pumpWidget(
    MaterialApp(
      home: AccountCard(account: account),
    ),
  );
  
  /// Assert
  expect(find.text('Test Account'), findsOneWidget);
});
```

### Tests comunes:

1. **Renderizado correcto**
   ```dart
   testWidgets('should render all expected elements', (tester) async {
     await tester.pumpWidget(widget);
     expect(find.byType(Text), findsNWidgets(3));
     expect(find.byIcon(Icons.check), findsOneWidget);
   });
   ```

2. **Interacciones de usuario**
   ```dart
   testWidgets('should call callback when button tapped', (tester) async {
     var tapped = false;
     await tester.pumpWidget(
       MaterialApp(
         home: MyButton(onTap: () => tapped = true),
       ),
     );
     
     await tester.tap(find.byType(ElevatedButton));
     await tester.pump();
     
     expect(tapped, true);
   });
   ```

3. **Estados de carga/error**
   ```dart
   testWidgets('should show loading indicator', (tester) async {
     await tester.pumpWidget(widget);
     expect(find.byType(CircularProgressIndicator), findsOneWidget);
   });
   ```

---

## 📦 JSON Fixtures

### Estructura

```
test/
  mock_json/
    accounts_consolidated/
      cif_account_consolidated.json
    cards/
      card_response.json
    exchange_rate/
      exchange_rate_success.json
```

### Cargar Fixtures

```dart
import 'dart:convert';
import 'dart:io';
import 'package:flutter/services.dart';

void main() {
  late CifAccountData accountEntity;

  setUpAll(() async {
    const path = 'accounts_consolidated/cif_account_consolidated.json';
    final String data = await rootBundle.loadString(
      '${Directory.current.path}/test/mock_json/$path',
      cache: false,
    );

    final dataJson = json.decode(data);
    accountEntity = CifAccountDataMapper().fromDtoToEntity(
      CifAccountResponseData.fromJson(dataJson),
    );
  });

  test('should use fixture data', () {
    expect(accountEntity, isNotNull);
    expect(accountEntity.accounts.length, greaterThan(0));
  });
}
```

---

## 📊 Coverage

### Ejecutar Coverage

```bash
# Todos los tests con coverage
melos run test:coverage

# Tests de un paquete específico
cd packages/accounts
flutter test --coverage

# Generar reporte HTML
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

### Configuración CI/CD

**GitHub Actions:**
```yaml
- name: Run tests with coverage
  run: melos run test:coverage

- name: Check coverage threshold
  run: |
    lcov --summary coverage/lcov.info | \
    grep -oP 'lines\.*: \K[0-9.]+' | \
    awk '{if ($1 < 75) exit 1}'
```

---

## ⚠️ Errores Comunes

### 1. Nombres de Tests Poco Descriptivos

```dart
❌ test('accounts test', () {});
❌ test('it works', () {});
❌ test('test1', () {});

✅ test('should return accounts when repository succeeds', () {});
✅ test('should throw NetworkException when device is offline', () {});
```

---

### 2. No Probar Casos de Error

```dart
❌ SOLO probar happy path
test('should load accounts', () {
  // Solo caso exitoso, falta probar errores
});

✅ Probar TODOS los caminos
test('should load accounts successfully', () { /* ... */ });
test('should handle network error', () { /* ... */ });
test('should handle server error 500', () { /* ... */ });
test('should handle validation error 400', () { /* ... */ });
```

---

### 3. No Usar Arrange-Act-Assert

```dart
❌ Todo mezclado
test('should work', () {
  final repo = MockRepo();
  when(repo.get()).thenReturn(data);
  final result = service.fetch();
  expect(result, data);
});

✅ Secciones claras
test('should return data when fetch succeeds', () {
  /// Arrange
  final repo = MockRepo();
  when(repo.get()).thenReturn(data);
  final service = MyService(repo);

  /// Act
  final result = service.fetch();

  /// Assert
  expect(result, data);
});
```

---

### 4. No Limpiar Recursos

```dart
❌ Sin cleanup
test('test', () {
  final container = ProviderContainer();
  // ... test ...
  // Container nunca se cierra → memory leak
});

✅ Con tearDown
late ProviderContainer container;

setUp(() {
  container = ProviderContainer();
});

tearDown(() {
  container.dispose();
});
```

---

### 5. Mocks Sin provideDummy

```dart
❌ Error con tipos genéricos
when(mockDataSource.getData())
    .thenAnswer((_) async => response);
// Error: Missing stub

✅ Con provideDummy
setUp(() {
  provideDummy<ApiResponse<Data>>(SuccessApiResponse<Data>(data));
  mockDataSource = MockDataSource();
});
```

---

### 6. No Usar await en Tests Asíncronos

```dart
❌ Sin await (test pasa pero no verifica nada)
test('should load', () {
  notifier.loadData();  // Falta await
  expect(state, isData);  // Se ejecuta antes de que termine loadData
});

✅ Con await
test('should load', () async {
  await notifier.loadData();  // ✅ Esperar
  expect(state, isData);
});
```

---

### 7. No Verificar Llamadas a Mocks

```dart
❌ Sin verify
test('should call repository', () async {
  await notifier.loadData();
  // No verifica que se llamó al repository
});

✅ Con verify
test('should call repository once', () async {
  await notifier.loadData();
  verify(mockRepo.fetchData()).called(1);  // ✅ Verificar
});
```

---

### 8. Tests Dependientes Entre Sí

```dart
❌ Estado compartido
var sharedState = [];

test('test 1', () {
  sharedState.add('item');
  expect(sharedState.length, 1);
});

test('test 2', () {
  expect(sharedState.length, 1);  // Depende del orden
});

✅ Estado aislado
test('test 1', () {
  final state = [];
  state.add('item');
  expect(state.length, 1);
});

test('test 2', () {
  final state = [];
  expect(state.length, 0);
});
```

---

## 📋 Checklist Pre-PR

### Tests

- [ ] Todos los ViewModels nuevos/modificados tienen tests
- [ ] Todos los Repositories nuevos tienen tests
- [ ] Coverage mínimo alcanzado (80% ViewModels, 75% Repositories)
- [ ] Tests siguen patrón Arrange-Act-Assert
- [ ] Nombres descriptivos: "should [resultado] when [condición]"
- [ ] Archivos terminan en `_test.dart` (singular)
- [ ] Se prueban casos exitosos Y de error
- [ ] Se usa `verify()` para validar llamadas a mocks
- [ ] Se usa `tearDown()` para cleanup
- [ ] Tests asíncronos usan `await` correctamente

### Evidencias en PR

- [ ] Screenshot de tests ejecutados (todos verde)
- [ ] Coverage report si se agregaron tests nuevos
- [ ] Comentar coverage % en descripción del PR

---

## 🚀 Comandos Útiles

```bash
# Ejecutar todos los tests
melos run test:all

# Ejecutar tests con coverage
melos run test:coverage

# Ejecutar tests de un archivo específico
flutter test test/features/accounts/view_model/accounts_view_model_test.dart

# Ejecutar tests con watch mode
flutter test --watch

# Generar mocks
flutter pub run build_runner build --delete-conflicting-outputs

# Coverage de un paquete específico
cd packages/accounts
flutter test --coverage

# Ver coverage HTML
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

---

## 📚 Templates

### Template ViewModel Test

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([YourRepository])
void main() {
  group('YourViewModel', () {
    late ProviderContainer container;
    late MockYourRepository mockRepository;

    setUp(() {
      mockRepository = MockYourRepository();
      container = ProviderContainer(
        overrides: [
          yourRepositoryProvider.overrideWithValue(mockRepository),
        ],
      );
    });

    tearDown(() {
      container.dispose();
    });

    test('should have correct initial state', () {
      final state = container.read(yourViewModelProvider);
      expect(state, isA<AsyncLoading>());
    });

    test('should load data successfully', () async {
      /// Arrange
      final expectedData = YourEntity(id: '1');
      when(mockRepository.fetchData())
          .thenAnswer((_) async => expectedData);
      
      /// Act
      await container.read(yourViewModelProvider.future);
      
      /// Assert
      final state = container.read(yourViewModelProvider);
      expect(state.value, equals(expectedData));
      verify(mockRepository.fetchData()).called(1);
    });

    test('should handle error', () async {
      /// Arrange
      when(mockRepository.fetchData())
          .thenThrow(Exception('Error'));
      
      /// Act
      try {
        await container.read(yourViewModelProvider.future);
      } catch (_) {}
      
      /// Assert
      final state = container.read(yourViewModelProvider);
      expect(state, isA<AsyncError>());
    });
  });
}
```

---

### Template Repository Test

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([YourDataSource])
void main() {
  late MockYourDataSource mockDataSource;
  late YourRepositoryImpl repository;

  TestWidgetsFlutterBinding.ensureInitialized();

  setUp(() {
    mockDataSource = MockYourDataSource();
    repository = YourRepositoryImpl(dataSource: mockDataSource);
  });

  test('should return entity when datasource succeeds', () async {
    /// Arrange
    final dto = YourDto(/* ... */);
    when(mockDataSource.getData())
        .thenAnswer((_) async => dto);

    /// Act
    final result = await repository.getData();

    /// Assert
    expect(result, isA<YourEntity>());
    verify(mockDataSource.getData()).called(1);
  });

  test('should throw exception when datasource fails', () async {
    /// Arrange
    when(mockDataSource.getData())
        .thenThrow(Exception('Error'));

    /// Act & Assert
    expect(
      () => repository.getData(),
      throwsA(isA<Exception>()),
    );
  });
}
```

---

## 💡 Tips para Tests de Calidad

### ✅ DO (Hacer)

1. **Nombres descriptivos:** "should X when Y"
2. **Arrange-Act-Assert:** Siempre separar en 3 secciones
3. **Probar errores:** No solo happy path
4. **Un concepto por test:** No probar múltiples cosas
5. **Usar fixtures:** Para datos complejos (JSON)
6. **Cleanup resources:** tearDown() siempre
7. **Verificar mocks:** verify() para validar interacciones

### ❌ DON'T (No Hacer)

1. **Nombres vagos:** "test1", "it works"
2. **Todo mezclado:** Sin estructura clara
3. **Solo happy path:** Olvidar casos de error
4. **Tests gigantes:** Probar múltiples escenarios juntos
5. **Datos hardcodeados:** En vez de fixtures
6. **Memory leaks:** No cerrar containers
7. **Asumir llamadas:** Sin verify()

---

## 📖 Referencias

- `/docs/development/unit_testing.md` - Documentación oficial
- [Mockito](https://pub.dev/packages/mockito)
- [Flutter Testing](https://docs.flutter.dev/testing)
- [Riverpod Testing](https://riverpod.dev/docs/essentials/testing)

---

**Última actualización:** 30 de marzo de 2026  
**Consolidación de:** testing (1,108 líneas) + testing-advanced (942 líneas) + testing-expert (487 líneas)  
**Tests en el proyecto:** 39 archivos  
**Coverage promedio:** 65-75%  
**Meta Q2 2026:** 80%+ para código nuevo
