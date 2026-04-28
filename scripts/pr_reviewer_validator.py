#!/usr/bin/env python3
"""
PR Reviewer Validator - Validación Automática de Pull Requests
Basado en: .github/agents/pr-reviewer.agent.md y skills de bancadigital-bm-app
"""

import os
import re
import subprocess
from typing import List
from datetime import datetime


class PRReviewerValidator:
    """Validador automático de PRs basado en reglas de desarrollo"""
    
    # Tipos de commit válidos (de .github/skills/commit-conventions/SKILL.md)
    COMMIT_TYPES = {
        'ft': 'Feature - Nueva funcionalidad',
        'fx': 'Fix - Corrección de bug',
        'tt': 'Technical Task - Tarea técnica',
        'rf': 'Refactor - Refactorización sin cambio funcional',
        'cr': 'Change Request - Cambio de requirement',
        'wr': 'Wording Request - Cambios de textos/traducciones',
        'hf': 'Hotfix - Corrección urgente en producción',
        'poc': 'Proof of Concept - Prueba de concepto',
        'devops': 'DevOps - CI/CD, pipelines, infraestructura'
    }
    
    # Patrones de branch válidos (de .github/skills/branch-naming/SKILL.md y branching_strategy_and_versioning.md)
    # PREFERENCIA: usar underscores (_)
    # PERMITIDO: guiones medios (-) para compatibilidad con branches existentes
    # Permite PascalCase o snake_case en nombres de módulos (Payments, Theme, Cards, etc.)
    # Permite letras (mayúsculas y minúsculas), números, underscores y guiones en descripción
    # Permite puntos (.) para versiones: v1.1, release-1.5.x
    # 9 tipos para branches: ft, fx, tt, rf, cr, wr, hf, poc, devops (consistente con commit_validator.sh)
    # Acepta cualquier cantidad de dígitos (1+) para el número de ticket
    BRANCH_PATTERN = r'^(ft|fx|tt|rf|cr|wr|hf|poc|devops)/(\d+_[a-zA-Z0-9_.-]+)$'
    SPECIAL_BRANCHES = ['main', 'develop', 'staging']
    RELEASE_PATTERN = r'^release-\d+\.\d+\.x$'
    
    # Pattern de commit OFICIAL (alineado con pipeline/commit_validator.sh)
    # Este es el patrón obligatorio que debe pasar el commit
    # Usa [0-9]* (cero o más dígitos) para coincidir exactamente con el pipeline
    # Nota: Aunque [0-9]+ sería más estricto, usamos [0-9]* para alineación exacta
    COMMIT_PATTERN = r'^\[(ft|fx|tt|rf|cr|wr|hf|poc|devops)\]\[BC-[0-9]*\]\s+.+'
    
    # Pattern RECOMENDADO (con módulo explícito)
    # Este es el formato recomendado en .github/skills/commit-conventions/SKILL.md
    # Típicamente con 5-6 dígitos y módulo con dos puntos
    COMMIT_PATTERN_RECOMMENDED = r'^\[(ft|fx|tt|rf|cr|wr|hf|poc|devops)\]\[BC-\d{5,6}\]\s+[^:]+:\s+.+'
    AZURE_BOARDS_BASE_URL = 'https://dev.azure.com/bacsansose/BAC/_workitems/edit/'
    AZURE_BOARDS_LEGACY_PATH = 'ORG-LAT-GSBD/Banca-Digital'
    
    def __init__(self):
        self.bloqueadores = []
        self.warnings = []
        self.aprobaciones = []
        self.pr_number = os.getenv('PR_NUMBER', 'N/A')
        self.pr_title = os.getenv('PR_TITLE', '')
        self.pr_branch = os.getenv('PR_BRANCH', '')
        # Obtener PR body directamente via gh CLI (evita problemas de truncamiento en env vars)
        self.pr_body = self._fetch_pr_body()
        # Cache de commits para evitar múltiples llamadas a GitHub API
        self._commits = None
        # Cache de archivos modificados para reutilizar entre validaciones
        self._changed_files = None
    
    def _fetch_pr_body(self) -> str:
        """Obtener el body del PR directamente vía gh CLI (más robusto que variable de entorno)"""
        print(f"📥 Obteniendo PR body para PR #{self.pr_number}...")
        try:
            result = subprocess.run(
                ['gh', 'pr', 'view', self.pr_number, '--json', 'body', '--jq', '.body'],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            body = result.stdout.strip()
            print(f"✅ PR body obtenido: {len(body)} caracteres")
            return body
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Error al obtener PR body via gh CLI (exit code: {e.returncode})")
            print(f"   Command: {' '.join(e.cmd)}")
            print(f"   stderr: {e.stderr}")
            # Fallback a variable de entorno si falla gh CLI
            fallback_body = os.getenv('PR_BODY', '')
            print(f"🔄 Usando fallback de variable de entorno: {len(fallback_body)} caracteres")
            return fallback_body
        except subprocess.TimeoutExpired:
            print("⚠️ Timeout (30s) al obtener PR body via gh CLI")
            fallback_body = os.getenv('PR_BODY', '')
            print(f"🔄 Usando fallback de variable de entorno: {len(fallback_body)} caracteres")
            return fallback_body
        except Exception as e:
            print(f"⚠️ Error inesperado al obtener PR body: {type(e).__name__}: {e}")
            import traceback
            print(f"   Stack trace: {traceback.format_exc()}")
            fallback_body = os.getenv('PR_BODY', '')
            print(f"🔄 Usando fallback de variable de entorno: {len(fallback_body)} caracteres")
            return fallback_body
        
    def run(self):
        """Ejecutar todas las validaciones"""
        print("🤖 Iniciando validación automática del PR...")
        
        # Validar título del PR
        self.validate_pr_title()
        
        # Validar commits
        self.validate_commits()
        
        # Validar branch name
        self.validate_branch_name()
        
        # Validar descripción del PR
        self.validate_pr_description()
        
        # Validar archivos modificados
        self.validate_changed_files()

        # Validar arquitectura en capas y dependencias críticas
        self.validate_clean_architecture()

        # Validar patrones críticos de Flutter en archivos modificados
        self.validate_flutter_code_review()
        
        # Generar reporte
        self.generate_report()
        
        # Determinar estado final
        self.write_status()
    
    def validate_pr_title(self):
        """Validar que el título del PR siga el formato de commits"""
        print("🏷️  Validando título del PR...")
        
        if not self.pr_title:
            self.warnings.append(
                "⚠️ **TÍTULO DEL PR NO DISPONIBLE**\n"
                "   - No se pudo obtener el título del PR para validación"
            )
            return
        
        # Validar que el título siga el formato de commit
        if not re.match(self.COMMIT_PATTERN, self.pr_title):
            self.warnings.append(
                f"⚠️ **TÍTULO DEL PR NO SIGUE FORMATO DE COMMIT:** `{self.pr_title}`\n"
                f"   - Se recomienda: `[tipo][BC-XXXXX] Módulo: Descripción`\n"
                f"   - Ejemplo: `[ft][BC-35367] Cards: Agregar botón de favoritos`"
            )
        else:
            self.aprobaciones.append(f"✅ Título del PR válido: `{self.pr_title[:60]}...`")
        
    def validate_commits(self):
        """Validar formato y contenido de commits"""
        print("📝 Validando commits...")
        
        # Usar método cacheado _get_commits() en lugar de hacer llamada directa
        commits = self._get_commits()
        
        if not commits:
            # Si _get_commits() devuelve lista vacía, ya agregó el warning correspondiente
            return
            
        for commit in commits:
            self._validate_commit_format(commit)
            
    def _validate_commit_format(self, commit: str):
        """Validar formato de un commit individual"""
        
        # Rastrear warnings iniciales para este commit
        warnings_before = len(self.warnings)
        
        # Validar formato OFICIAL (obligatorio - debe pasar este)
        if not re.match(self.COMMIT_PATTERN, commit):
            self.bloqueadores.append(
                f"❌ **COMMIT INVÁLIDO:** `{commit}`\n"
                f"   - Formato mínimo esperado: `[tipo][BC-XXXXX] Descripción`\n"
                f"   - Formato recomendado: `[tipo][BC-XXXXX] Módulo: Descripción`\n"
                f"   - Ejemplo: `[ft][BC-35367] Cards: Agregar botón de favoritos`"
            )
            return
        
        # Si pasa el oficial pero no el recomendado, generar warning
        if not re.match(self.COMMIT_PATTERN_RECOMMENDED, commit):
            self.warnings.append(
                f"⚠️ **FORMATO NO RECOMENDADO:** `{commit}`\n"
                f"   - Se recomienda incluir el módulo con dos puntos: `[tipo][BC-XXXXX] Módulo: Descripción`\n"
                f"   - Ejemplo: `[ft][BC-35367] Cards: Agregar botón de favoritos`\n"
                f"   - Consulta `.github/skills/commit-conventions/SKILL.md` para ejemplos"
            )
            
        # Validar diminutivos comunes usando límites de palabra para evitar falsos positivos
        # Ejemplo: no queremos match en "context" cuando buscamos "txt"
        diminutivos = ['txt', 'btn', 'cfg', 'img', 'msg', 'usr']
        for dim in diminutivos:
            # \b asegura límites de palabra, \W+ permite separadores no-word
            pattern = r'\b' + re.escape(dim) + r'\b'
            if re.search(pattern, commit, re.IGNORECASE):
                self.warnings.append(
                    f"⚠️ **DIMINUTIVO DETECTADO:** `{dim}` en `{commit}`\n"
                    f"   - Evita diminutivos, usa palabras completas\n"
                    f"   - Ejemplo: 'button' en lugar de 'btn', 'text' en lugar de 'txt'"
                )
                
        # Solo aprobar si no se generaron warnings para este commit
        if len(self.warnings) == warnings_before:
            self.aprobaciones.append(f"✅ Commit válido: `{commit[:60]}...`")
        
    def validate_branch_name(self):
        """Validar nombre de branch según convenciones"""
        print("🌿 Validando nombre de branch...")
        
        branch = self.pr_branch
        
        # Branches especiales permitidos
        if branch in self.SPECIAL_BRANCHES:
            self.aprobaciones.append(f"✅ Branch especial válido: `{branch}`")
            return
            
        # Release branches
        if re.match(self.RELEASE_PATTERN, branch):
            self.aprobaciones.append(f"✅ Branch de release válido: `{branch}`")
            return
            
        # Branches normales: tipo/numero_descripcion
        if not re.match(self.BRANCH_PATTERN, branch):
            self.bloqueadores.append(
                f"❌ **BRANCH NAME INVÁLIDO:** `{branch}`\n"
                f"   - Formato esperado: `tipo/numero_descripcion`\n"
                f"   - Tipos válidos: ft, fx, tt, rf, cr, wr, hf, poc, devops\n"
                f"   - Ejemplo: `ft/35367_agregar_boton_favoritos`\n"
                f"   - Usa snake_case (guiones bajos) en la descripción"
            )
            return
            
        # Validar que el número coincida con algún ticket en commits
        branch_number = re.search(r'/(\d+)_', branch)
        if branch_number:
            number = branch_number.group(1)
            # Extraer todos los IDs de ticket de los commits usando regex para match exacto
            commits_text = ' '.join(self._get_commits())
            # Buscar BC-{number} con límites de palabra para evitar falsos positivos
            # Ejemplo: BC-12345 no debe hacer match con BC-123456
            ticket_pattern = r'\bBC-' + number + r'\b'
            if re.search(ticket_pattern, commits_text):
                self.aprobaciones.append(f"✅ Branch name válido: `{branch}` (ticket BC-{number} encontrado en commits)")
            else:
                self.warnings.append(
                    f"⚠️ **TICKET NO ENCONTRADO:** Branch usa `{number}` pero no hay commits con `[BC-{number}]`"
                )
        else:
            self.aprobaciones.append(f"✅ Branch name válido: `{branch}`")
            
    def validate_pr_description(self):
        """Validar que el PR tenga la plantilla completa con validaciones flexibles"""
        print("📄 Validando descripción del PR...")
        
        body = self.pr_body
        
        if not body or len(body.strip()) < 50:
            self.bloqueadores.append(
                "❌ **DESCRIPCIÓN VACÍA O MUY CORTA**\n"
                "   - El PR debe usar la plantilla completa\n"
                "   - Mínimo 50 caracteres de descripción"
            )
            return
            
        # Validación flexible: buscar patrones en lugar de texto exacto
        has_description = bool(re.search(r'##\s*Descripci[oó]n', body, re.IGNORECASE))
        has_azure_boards_section = bool(re.search(r'##\s*Link.*Azure.*Boards', body, re.IGNORECASE))
        has_evidence = bool(re.search(r'##\s*Evidencias?', body, re.IGNORECASE))
        azure_boards_issues = []
        
        if has_azure_boards_section:
            azure_boards_issues = self._get_azure_boards_link_issues(body)
        
        # Bloqueadores solo si faltan elementos críticos
        critical_missing = []
        if not has_description:
            critical_missing.append("Sección de Descripción")
        if not has_azure_boards_section:
            critical_missing.append("Sección 'Link de Historia del AzureBoards'")
            
        if critical_missing:
            self.bloqueadores.append(
                "❌ **FALTAN ELEMENTOS CRÍTICOS EN EL PR:**\n" +
                '\n'.join(f"   - {item}" for item in critical_missing) +
                "\n   - Usa la plantilla oficial: `.github/pull_request_template.md`"
            )
        else:
            self.aprobaciones.append("✅ PR incluye descripción y sección de Azure Boards")

        if has_azure_boards_section:
            if azure_boards_issues:
                self.bloqueadores.append(
                    "❌ **LINK DE AZURE BOARDS INVÁLIDO:**\n" +
                    '\n'.join(f"   - {issue}" for issue in azure_boards_issues) +
                    f"\n   - Usa el formato `[AB#12345]({self.AZURE_BOARDS_BASE_URL}12345)`"
                )
            else:
                self.aprobaciones.append("✅ PR incluye link válido de Azure Boards")
            
        # Warning si falta evidencias (no bloqueador)
        if not has_evidence:
            self.warnings.append(
                "⚠️ **RECOMIENDA AGREGAR SECCIÓN DE EVIDENCIAS**\n"
                "   - Sección '## Evidencias Visuales' no encontrada\n"
                "   - Considera agregar screenshots/videos/logs según el tipo de cambio"
            )
        else:
            self.aprobaciones.append("✅ PR incluye sección de Evidencias Visuales")
            
        # Validar que tenga descripción con contenido (no solo placeholder)
        if has_description:
            desc_match = re.search(r'##\s*Descripci[oó]n.*?(?=##|$)', body, re.IGNORECASE | re.DOTALL)
            if desc_match:
                desc_section = desc_match.group(0)
                # Remover comentarios HTML y espacios
                desc_clean = re.sub(r'<!--.*?-->', '', desc_section, flags=re.DOTALL).strip()
                # Remover el título de la sección
                desc_clean = re.sub(r'##\s*Descripci[oó]n.*?\n', '', desc_clean, flags=re.IGNORECASE).strip()
                
                # Verificar si tiene contenido real (más de 30 chars sin contar bullets vacíos)
                has_content = len(desc_clean) > 30 and desc_clean not in ['* .', '*', '']
                
                if not has_content:
                    self.warnings.append(
                        "⚠️ **DESCRIPCIÓN PARECE VACÍA O INCOMPLETA**\n"
                        "   - Agrega bullets específicos describiendo QUÉ cambió\n"
                        "   - No dejes solo el placeholder `* .`"
                    )
                else:
                    self.aprobaciones.append("✅ PR tiene descripción con contenido")

    def _get_azure_boards_link_issues(self, body: str) -> List[str]:
        """Validar que el link de Azure Boards sea real, consistente y no use placeholders obsoletos"""
        issues = []

        if 'AB#XXXXX' in body or '/edit/XXXXX' in body:
            issues.append("Reemplaza el placeholder `XXXXX` por el ticket real")

        if self.AZURE_BOARDS_LEGACY_PATH in body:
            issues.append(
                "La URL usa organización/proyecto obsoletos; debe usar `bacsansose/BAC`"
            )

        link_match = re.search(
            r'\[AB#(\d{1,6})\]\((https://dev\.azure\.com/[^\s)]+/_workitems/edit/(\d{1,6}))\)',
            body,
            re.IGNORECASE,
        )

        if not link_match:
            issues.append(
                f"No se encontró un link markdown válido con formato `[AB#12345]({self.AZURE_BOARDS_BASE_URL}12345)`"
            )
            return issues

        link_ticket = link_match.group(1)
        link_url = link_match.group(2)
        url_ticket = link_match.group(3)

        if link_ticket != url_ticket:
            issues.append("El ticket del texto `AB#...` no coincide con el ticket del URL")

        if not link_url.startswith(self.AZURE_BOARDS_BASE_URL):
            issues.append(
                f"La URL debe iniciar con `{self.AZURE_BOARDS_BASE_URL}`"
            )

        return issues
                    
    def validate_changed_files(self):
        """Validar archivos modificados en el PR"""
        print("📂 Validando archivos modificados...")
        
        files = self._get_changed_files()
        
        if not files:
            return
            
        # Análisis de tipos de archivos
        dart_files = [f for f in files if f.endswith('.dart')]
        test_files = [f for f in files if '_test.dart' in f]
        
        # Si hay cambios en código Dart pero no tests
        if dart_files and not test_files:
            # Excluir algunos patrones que no requieren tests obligatorios
            excluded_patterns = ['main.dart', 'routes.dart', 'constants.dart', 'colors.dart']
            # Calcular archivos .dart que NO están en la lista de excluidos
            non_excluded_dart_files = [
                f for f in dart_files
                if not any(pattern in f for pattern in excluded_patterns)
            ]
            # Solo mostrar warning si hay archivos no excluidos
            requires_tests = len(non_excluded_dart_files) > 0
            
            if requires_tests:
                self.warnings.append(
                    f"⚠️ **FALTA AGREGAR TESTS**\n"
                    f"   - Se modificaron {len(dart_files)} archivos .dart\n"
                    f"   - No se encontraron tests (_test.dart)\n"
                    f"   - Se recomienda agregar tests unitarios (cobertura mínima: 80%)"
                )
        elif test_files:
            self.aprobaciones.append(
                f"✅ PR incluye tests ({len(test_files)} archivos _test.dart)"
            )
            
        # Validar que no se modifiquen archivos sensibles
        sensitive_files = ['.env', 'pubspec.yaml', 'ios/Runner/Info.plist', 'android/app/build.gradle']
        modified_sensitive = [f for f in files if any(sens in f for sens in sensitive_files)]
        
        if modified_sensitive:
            self.warnings.append(
                f"⚠️ **ARCHIVOS SENSIBLES MODIFICADOS:**\n" +
                '\n'.join(f"   - {f}" for f in modified_sensitive) +
                "\n   - Verifica que los cambios sean intencionales"
            )

    def validate_clean_architecture(self):
        """Validar reglas base de Clean Architecture en archivos Dart modificados"""
        print("🏗️  Validando Clean Architecture...")

        dart_files = self._get_existing_changed_dart_files()
        if not dart_files:
            return

        architecture_checks = 0
        architecture_findings = 0

        for file_path in dart_files:
            if '/domain/' not in file_path and '/data/' not in file_path:
                continue

            content = self._read_text_file(file_path)
            if not content:
                continue

            architecture_checks += 1
            imports = self._extract_imports(content)

            if '/domain/' in file_path:
                if any(import_path.startswith('package:flutter') for import_path in imports):
                    self.bloqueadores.append(
                        f"❌ **DEPENDENCIA INVÁLIDA EN DOMAIN:** `{file_path}`\n"
                        f"   - La capa Domain no debe depender de Flutter\n"
                        f"   - Mueve esa lógica a UI o Data según corresponda"
                    )
                    architecture_findings += 1

                forbidden_domain_imports = [
                    import_path for import_path in imports
                    if '/data/' in import_path or '/ui/' in import_path
                ]
                if forbidden_domain_imports:
                    self.bloqueadores.append(
                        f"❌ **DEPENDENCIA INVÁLIDA EN DOMAIN:** `{file_path}`\n"
                        f"   - Domain no puede importar Data/UI\n"
                        f"   - Imports detectados: {', '.join(forbidden_domain_imports[:3])}"
                    )
                    architecture_findings += 1

                if '/domain/entities/' in file_path and (
                    '@JsonSerializable' in content or
                    any('json_annotation' in import_path for import_path in imports)
                ):
                    self.bloqueadores.append(
                        f"❌ **ENTITY CON SERIALIZACIÓN:** `{file_path}`\n"
                        f"   - Las Entities de Domain deben ser modelos de negocio puros\n"
                        f"   - Mueve anotaciones/serialización a DTOs en Data"
                    )
                    architecture_findings += 1

            if '/data/' in file_path:
                forbidden_data_imports = [
                    import_path for import_path in imports
                    if '/ui/' in import_path
                ]
                if forbidden_data_imports:
                    self.bloqueadores.append(
                        f"❌ **DEPENDENCIA INVÁLIDA EN DATA:** `{file_path}`\n"
                        f"   - Data no debe depender de UI\n"
                        f"   - Imports detectados: {', '.join(forbidden_data_imports[:3])}"
                    )
                    architecture_findings += 1

                if ('/data/models/' in file_path or file_path.endswith('_dto.dart')) and '@freezed' not in content:
                    self.warnings.append(
                        f"⚠️ **DTO SIN `@freezed`:** `{file_path}`\n"
                        f"   - El skill de arquitectura recomienda DTOs inmutables con `freezed`\n"
                        f"   - Revisa si este modelo debe migrarse a un DTO homologado"
                    )
                    architecture_findings += 1

        if architecture_checks and architecture_findings == 0:
            self.aprobaciones.append(
                "✅ Validaciones de Clean Architecture sin dependencias inválidas entre capas"
            )

    def validate_flutter_code_review(self):
        """Validar patrones críticos de Flutter sobre archivos Dart modificados"""
        print("🧪 Validando patrones críticos de Flutter...")

        dart_files = self._get_existing_changed_dart_files()
        if not dart_files:
            return

        reviewed_files = 0
        findings = 0

        for file_path in dart_files:
            content = self._read_text_file(file_path)
            if not content:
                continue

            reviewed_files += 1

            if self._has_init_state_order_issue(content):
                self.bloqueadores.append(
                    f"❌ **LIFECYCLE INVÁLIDO:** `{file_path}`\n"
                    f"   - `super.initState()` debe ser la primera instrucción del método\n"
                    f"   - Corrígelo para evitar inicializaciones inconsistentes"
                )
                findings += 1

            if self._has_dispose_order_issue(content):
                self.bloqueadores.append(
                    f"❌ **DISPOSE INVÁLIDO:** `{file_path}`\n"
                    f"   - `super.dispose()` debe ejecutarse al final del método\n"
                    f"   - Dispose controllers/streams antes de llamar a `super.dispose()`"
                )
                findings += 1

            if re.search(
                r'\bNavigator(?:\.of\([^\)]*\))?\.(?:pop|push|pushNamed|pushReplacement|pushAndRemoveUntil|maybePop)\s*\(',
                content,
            ):
                self.bloqueadores.append(
                    f"❌ **NAVEGACIÓN NO HOMOLOGADA:** `{file_path}`\n"
                    f"   - Usa extensiones de GoRouter (`context.push`, `context.go`, `context.pop`)\n"
                    f"   - Evita `Navigator` directo según el estándar del proyecto"
                )
                findings += 1

            if self._has_async_navigation_without_mounted(content):
                self.warnings.append(
                    f"⚠️ **NAVEGACIÓN ASÍNCRONA SIN `mounted`:** `{file_path}`\n"
                    f"   - Después de `await`, valida `if (!mounted) return;` o `if (!context.mounted) return;`\n"
                    f"   - Esto evita crashes si el widget fue destruido antes de navegar"
                )
                findings += 1

            if '/ui/' in file_path and re.search(r'SizedBox\s*\(\s*(height|width)\s*:', content):
                self.warnings.append(
                    f"⚠️ **ESPACIADO MANUAL DETECTADO:** `{file_path}`\n"
                    f"   - Considera usar `Spacing` del Design System en lugar de `SizedBox` manual\n"
                    f"   - Mantiene consistencia visual y semántica entre pantallas"
                )
                findings += 1

        if reviewed_files and findings == 0:
            self.aprobaciones.append(
                "✅ Validaciones críticas de Flutter sin hallazgos de lifecycle o navegación"
            )

    def _get_changed_files(self) -> List[str]:
        """Obtener archivos modificados del PR (con cache para evitar llamadas redundantes)"""
        if self._changed_files is not None:
            return self._changed_files

        try:
            result = subprocess.run(
                ['gh', 'pr', 'view', self.pr_number, '--json', 'files', '--jq', '.files[].path'],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )

            self._changed_files = [line.strip() for line in result.stdout.split('\n') if line.strip()]

            if not self._changed_files:
                self.warnings.append("⚠️ No se pudieron obtener archivos modificados")

            return self._changed_files
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.warnings.append(
                f"⚠️ **ERROR AL OBTENER ARCHIVOS:** No se pudieron validar archivos modificados del PR\n"
                f"   - Error: {type(e).__name__}: {str(e)}\n"
                f"   - Verifica que gh CLI esté configurado correctamente"
            )
            self._changed_files = []
            return self._changed_files

    def _get_existing_changed_dart_files(self) -> List[str]:
        """Obtener archivos Dart modificados que existen en el checkout actual"""
        return [
            file_path for file_path in self._get_changed_files()
            if file_path.endswith('.dart') and os.path.exists(file_path)
        ]

    def _read_text_file(self, file_path: str) -> str:
        """Leer archivo de texto del checkout actual"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file_handle:
                return file_handle.read()
        except OSError as e:
            self.warnings.append(
                f"⚠️ **NO SE PUDO LEER ARCHIVO:** `{file_path}`\n"
                f"   - Error: {type(e).__name__}: {str(e)}"
            )
            return ""

    def _extract_imports(self, content: str) -> List[str]:
        """Extraer imports Dart del contenido del archivo"""
        return re.findall(r'import\s+[\'"]([^\'"]+)[\'"];', content)

    def _extract_method_bodies(self, content: str, method_name: str) -> List[str]:
        """Extraer cuerpos de métodos Dart simples usando balanceo de llaves"""
        method_pattern = re.compile(rf'\b{method_name}\s*\([^\)]*\)\s*(?:async\s*)?\{{')
        method_bodies = []

        for match in method_pattern.finditer(content):
            open_brace_index = content.find('{', match.start())
            if open_brace_index == -1:
                continue

            brace_depth = 1
            current_index = open_brace_index + 1

            while current_index < len(content):
                current_char = content[current_index]
                if current_char == '{':
                    brace_depth += 1
                elif current_char == '}':
                    brace_depth -= 1
                    if brace_depth == 0:
                        method_bodies.append(content[open_brace_index + 1:current_index])
                        break
                current_index += 1

        return method_bodies

    def _get_meaningful_lines(self, block: str) -> List[str]:
        """Obtener líneas relevantes ignorando espacios y comentarios"""
        meaningful_lines = []
        inside_block_comment = False

        for raw_line in block.splitlines():
            stripped_line = raw_line.strip()

            if not stripped_line:
                continue

            if inside_block_comment:
                if '*/' in stripped_line:
                    inside_block_comment = False
                    stripped_line = stripped_line.split('*/', 1)[1].strip()
                    if not stripped_line:
                        continue
                else:
                    continue

            if stripped_line.startswith('/*'):
                if '*/' not in stripped_line:
                    inside_block_comment = True
                    continue
                stripped_line = stripped_line.split('*/', 1)[1].strip()
                if not stripped_line:
                    continue

            if stripped_line.startswith('//') or stripped_line.startswith('*'):
                continue

            meaningful_lines.append(stripped_line)

        return meaningful_lines

    def _has_init_state_order_issue(self, content: str) -> bool:
        """Validar que super.initState() sea la primera instrucción"""
        for method_body in self._extract_method_bodies(content, 'initState'):
            meaningful_lines = self._get_meaningful_lines(method_body)
            if meaningful_lines and not meaningful_lines[0].startswith('super.initState();'):
                return True
        return False

    def _has_dispose_order_issue(self, content: str) -> bool:
        """Validar que super.dispose() sea la última instrucción"""
        for method_body in self._extract_method_bodies(content, 'dispose'):
            meaningful_lines = self._get_meaningful_lines(method_body)
            if meaningful_lines and not meaningful_lines[-1].startswith('super.dispose();'):
                return True
        return False

    def _has_async_navigation_without_mounted(self, content: str) -> bool:
        """Detectar navegación después de await sin mounted/context.mounted"""
        navigation_pattern = re.compile(r'\bcontext\.(?:push|pushNamed|go|pop|replace)\s*\(')
        mounted_pattern = re.compile(r'if\s*\(\s*!\s*(?:context\.)?mounted\s*\)\s*return;')
        lines = content.splitlines()

        for line_index, current_line in enumerate(lines):
            if 'await ' not in current_line:
                continue

            mounted_checked = False
            for look_ahead_index in range(line_index + 1, min(line_index + 8, len(lines))):
                candidate_line = lines[look_ahead_index].strip()

                if not candidate_line or candidate_line.startswith('//'):
                    continue

                if mounted_pattern.search(candidate_line):
                    mounted_checked = True
                    continue

                if navigation_pattern.search(candidate_line):
                    if not mounted_checked:
                        return True
                    break

                if candidate_line.startswith('return') or candidate_line.startswith('throw'):
                    break

        return False
            
    def _get_commits(self) -> List[str]:
        """Obtener lista de commits del PR (con cache para evitar múltiples llamadas a GitHub API)"""
        # Si ya tenemos los commits en cache, devolverlos directamente
        if self._commits is not None:
            return self._commits
            
        # Primera vez: hacer la llamada a GitHub API y cachear el resultado
        try:
            result = subprocess.run(
                ['gh', 'pr', 'view', self.pr_number, '--json', 'commits', '--jq', '.commits[].messageHeadline'],
                capture_output=True,
                text=True,
                check=True,
                timeout=30
            )
            self._commits = [line.strip() for line in result.stdout.split('\n') if line.strip()]
            return self._commits
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError) as e:
            # Registrar error para facilitar troubleshooting
            self.warnings.append(
                f"⚠️ **ERROR AL OBTENER COMMITS:** No se pudieron validar commits del PR\n"
                f"   - Error: {type(e).__name__}: {str(e)}\n"
                f"   - Verifica que gh CLI esté configurado correctamente"
            )
            self._commits = []  # Cachear lista vacía para evitar reintentos
            return self._commits
            
    def generate_report(self):
        """Generar reporte en Markdown"""
        print("📊 Generando reporte...")
        
        # Determinar estado general
        if self.bloqueadores:
            status_emoji = "🚫"
            status_text = "BLOQUEADO"
        elif self.warnings:
            status_emoji = "⚠️"
            status_text = "CON ADVERTENCIAS"
        else:
            status_emoji = "✅"
            status_text = "APROBADO"
            
        # Construir reporte
        report = f"""# 🤖 PR Reviewer - Validación Automática - Leo

**Estado:** {status_emoji} **{status_text}**  
**PR:** #{self.pr_number}  
**Branch:** `{self.pr_branch}`  
**Fecha:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

"""
        
        # Bloqueadores
        if self.bloqueadores:
            report += f"""## 🚫 Bloqueadores Críticos ({len(self.bloqueadores)})

Estos problemas **deben corregirse** antes de mergear:

"""
            for bloq in self.bloqueadores:
                report += f"{bloq}\n\n"
            report += "---\n\n"
            
        # Warnings
        if self.warnings:
            report += f"""## ⚠️ Advertencias ({len(self.warnings)})

Se recomienda revisar estos puntos:

"""
            for warn in self.warnings:
                report += f"{warn}\n\n"
            report += "---\n\n"
            
        # Aprobaciones
        if self.aprobaciones:
            report += f"""## ✅ Validaciones Aprobadas ({len(self.aprobaciones)})

"""
            for apr in self.aprobaciones[:10]:  # Limitar a 10 para no saturar
                report += f"{apr}\n"
            if len(self.aprobaciones) > 10:
                report += f"\n*...y {len(self.aprobaciones) - 10} validaciones más*\n"
            report += "\n---\n\n"
            
        # Footer
        report += """## 📚 Referencias

Este review automático se basa en:
- 📘 [commit-conventions](.github/skills/commit-conventions/SKILL.md)
- 📗 [branch-naming](.github/skills/branch-naming/SKILL.md)
- 📙 [pr-description](.github/skills/pr-description/SKILL.md)
- 🏗️ [clean-architecture](.github/skills/clean-architecture/SKILL.md)
- 🧪 [code-review](.github/skills/code-review/SKILL.md)
- 📕 [testing-unified](.github/skills/testing-unified/SKILL.md)
- 🤖 [pr-reviewer.agent.md](.github/agents/pr-reviewer.agent.md)

Para un review manual más detallado, invoca en Copilot Chat:
```
Leo, revisa este PR
```

---

*🤖 Generado automáticamente por PR Reviewer v1.1*
"""
        
        # Guardar reporte
        with open('/tmp/pr-review-report.md', 'w') as f:
            f.write(report)
            
        print("✅ Reporte generado en /tmp/pr-review-report.md")
        
    def write_status(self):
        """Escribir estado final para el workflow"""
        if self.bloqueadores:
            status = "BLOCKED"
        elif self.warnings:
            status = "WARNING"
        else:
            status = "OK"
            
        with open('/tmp/pr-validation-status', 'w') as f:
            f.write(status)
            
        print(f"📊 Estado final: {status}")
        
        # Resumen en consola
        print(f"\n{'='*60}")
        print(f"RESUMEN DE VALIDACIÓN")
        print(f"{'='*60}")
        print(f"🚫 Bloqueadores: {len(self.bloqueadores)}")
        print(f"⚠️  Advertencias: {len(self.warnings)}")
        print(f"✅ Aprobaciones: {len(self.aprobaciones)}")
        print(f"{'='*60}\n")


if __name__ == '__main__':
    validator = PRReviewerValidator()
    validator.run()
