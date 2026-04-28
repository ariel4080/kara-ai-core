# Changelog - Module Creation Skill

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.1.0] - 2026-03-26

### ✅ Added
- **NEW Template**: `module_definition.dart.template` - Generates ModuleDefinition class following Module Pattern
- **NEW Template**: `navigation.dart.template` - Generates navigation configuration with routes, params, and helper methods
- Documentation for Goals Pattern (simple FF redirects via `getRouteRedirectionFlags()`)
- Documentation for Transfers Pattern (complex redirects via `redirectRules()`)
- Examples comparing both redirect patterns in SKILL.md

### 🔧 Changed
- **BREAKING**: Aligned with real architecture from Goals/Transfers modules
- **BREAKING**: Module classes now named `{ModuleName}ModuleDefinition` (not `{ModuleName}Module`)
- **BREAKING**: Constructor uses snake_case: `super('{module_name}')` instead of PascalCase
- **BREAKING**: Files named `{module_name}_module_definition.dart` (not `_module_configuration.dart`)
- **CORRECTED**: Method `getRoutes()` → `getRouterConfig()` (was incorrectly documented as deprecated)
- **CORRECTED**: Property `{ModuleName}Navigation.routes` → `{ModuleName}Navigation.routerConfig`
- Updated imports to use `feature_commons` instead of `core_data` for Module class
- Updated imports to use `flutter/widgets.dart` instead of `flutter/material.dart`
- PR Review Rule #10: Now documents correct usage of `getRouteRedirectionFlags()` vs `redirectRules()`

### ❌ Removed
- **Deleted Template**: `advanced/redirect_rule.dart.template` (replaced by Module Pattern methods)
- Incorrect deprecation warnings for `getRouterConfig()` and `getRouteRedirectionFlags()`
- Standalone RedirectRule classes (now inline in ModuleDefinition via `redirectRules()` or `getRouteRedirectionFlags()`)

### 📝 Improved
- templates/README.md: Added comprehensive documentation for new architecture templates
- templates/README.md: Reorganized structure to prioritize architecture templates
- SKILL.md: Added real examples from Goals and Transfers modules
- SKILL.md: Clarified difference between simple (Goals) and advanced (Transfers) redirect patterns
- SKILL.md: Updated all code examples to match actual production code

### 🐛 Fixed
- Incorrect method names in Module Pattern documentation
- Misaligned architecture vs. actual Goals/Transfers implementation
- Confusing guidance about deprecated methods that were never actually deprecated

---

## [3.0.0] - 2026-03-19

### ✅ Added
- 11 PR Review Rules based on exhaustive analysis of Goals, Payments, Transfers modules
- 8 reusable templates for consistent code generation
- Template system with placeholder replacement
- Migration of 10 legacy skills to modern folder structure
- Comprehensive testing patterns (AAA + ProviderContainer.listen())
- Advanced cache patterns (Interface + Singleton from Transfers)
- Redirects documentation with feature flags
- Deprecated method warnings (later corrected in v3.1.0)

### 🔧 Changed
- Upgraded from StateNotifier → AsyncNotifier/AutoDisposeAsyncNotifier
- Added Freezed to all DTOs
- Added DataSource layer with ApiResponseHandlerMixin
- Migrated to AsyncValue<T> handling
- Updated test coverage expectations (minimum 16 tests per module)

### ❌ Removed
- Legacy StateNotifier patterns
- Manual error handling (replaced with ApiResponse.when())
- Direct API calls without DataSource layer

---

## [2.1.0] - 2026-02-XX

### Initial version
- Basic module scaffolding
- Simple folder structure generation
- Minimal testing setup
- StateNotifier-based patterns

---

## Version Comparison

| Version | Architecture | State Management | Testing | Templates | Real Alignment |
|---------|--------------|------------------|---------|-----------|----------------|
| 2.1.0   | Basic        | StateNotifier    | Minimal | 0         | ❌ No          |
| 3.0.0   | Advanced     | AsyncNotifier    | Robust  | 8         | ⚠️ Partial     |
| 3.1.0   | Production   | AsyncNotifier    | Robust  | 10        | ✅ Full        |

---

## Migration Guide: 3.0.0 → 3.1.0

### If you generated modules with v3.0.0:

#### 1. Update Module Definition Class

**Before (v3.0.0):**
```dart
class GoalsModule extends Module<GoalsLocalizations> {
  GoalsModule() : super("Goals");
  
  List<GoRoute> getRoutes() {
    return GoalsNavigation.routes;
  }
}
```

**After (v3.1.0):**
```dart
class GoalsModuleDefinition extends Module<GoalsLocalizations> {
  GoalsModuleDefinition() : super('goals');
  
  List<GoRoute> getRouterConfig() {
    return GoalsNavigation.routerConfig;
  }
}
```

#### 2. Update Navigation Property

**Before:** `static final List<GoRoute> routes = [...]`  
**After:** `static final List<GoRoute> routerConfig = [...]`

#### 3. Update Redirect Rules (if applicable)

**If using simple redirects (Goals pattern):**
```dart
@override
Map<String, String> getRouteRedirectionFlags() => {
  GoalsNavigation.someRoute: GoalsFeatureFlagIds.SOME_FLAG.id,
};
```

**If using complex redirects (Transfers pattern):**
```dart
@override
List<RedirectRule> redirectRules() {
  return [
    FeatureBehaviorRedirectRule(
      flagId: TransfersFlagIds.SOME_FLAG.id,
      routeNames: [TransfersNavigation.route1, TransfersNavigation.route2],
    ),
  ];
}
```

#### 4. Update main.dart Registration

**Before:**
```dart
moduleManager.registerModule(GoalsModule());
```

**After:**
```dart
moduleManager.registerModule(GoalsModuleDefinition());
```

---

## Contributors

- **Chapter Lead Mobile Team** - Architecture alignment analysis
- **v3.1.0**: Corrección basada en módulos reales Goals/Transfers
- **v3.0.0**: Análisis exhaustivo de 3 módulos de producción
