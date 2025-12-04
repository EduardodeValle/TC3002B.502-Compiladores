import pytest
import sys
from pathlib import Path
from io import StringIO
import traceback

from BabyDuckError import BabyDuckError
from compiler import run_compiler


class TestBabyDuckCompiler:
    """Suite de pruebas para el compilador BabyDuck"""

    VALID_TESTS_DIR = Path("Tests/Semantica/Validos")
    INVALID_TESTS_DIR = Path("Tests/Semantica/Invalidos")
    RUNTIME_ERRORS_DIR = Path("Tests/ErroresRuntime")

    @staticmethod
    def get_test_files(directory):
        """Obtiene todos los archivos .txt del directorio ordenados"""
        path = Path(directory)
        if not path.exists():
            return []
        return sorted(path.glob("*.txt"))

    @staticmethod
    def print_separator(char="=", length=80):
        """Imprime un separador visual"""
        print(f"\n{char * length}\n")

    @staticmethod
    def print_header(text, char="=", length=80):
        """Imprime un encabezado centrado"""
        padding = (length - len(text) - 2) // 2
        print(f"\n{char * length}")
        print(f"{char}{' ' * padding}{text}{' ' * padding}{char}")
        print(f"{char * length}\n")

    @staticmethod
    def run_single_test(filepath, expected_success=True):
        """
        Ejecuta un solo archivo de prueba

        Args:
            filepath: Ruta al archivo de prueba
            expected_success: True si se espera compilacion exitosa, False si se espera error

        Returns:
            tuple: (success, output, error_message)
        """
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            run_compiler(str(filepath))

            stdout_value = sys.stdout.getvalue()
            stderr_value = sys.stderr.getvalue()

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return True, stdout_value, None

        except BabyDuckError as e:
            stdout_value = sys.stdout.getvalue()
            stderr_value = sys.stderr.getvalue()

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            return False, stdout_value, str(e)

        except Exception as e:
            stdout_value = sys.stdout.getvalue()
            stderr_value = sys.stderr.getvalue()

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            error_msg = f"Error inesperado: {str(e)}\n{traceback.format_exc()}"
            return False, stdout_value, error_msg

    def test_valid_programs(self):
        """Prueba todos los programas validos que deben compilar exitosamente"""
        self.print_header("PRUEBAS DE CASOS VALIDOS", "=", 80)

        valid_files = self.get_test_files(self.VALID_TESTS_DIR)

        if not valid_files:
            pytest.skip(f"No se encontraron archivos en {self.VALID_TESTS_DIR}")

        results = {
            "passed": [],
            "failed": []
        }

        for test_file in valid_files:
            self.print_separator("-", 80)
            print(f" EJECUTANDO: {test_file.name}")
            self.print_separator("-", 80)

            success, output, error = self.run_single_test(test_file, expected_success=True)

            print(output)

            if success:
                print(f" PASO: {test_file.name}")
                results["passed"].append(test_file.name)
            else:
                print(f" FALLO: {test_file.name}")
                if error:
                    print(f"Error: {error}")
                results["failed"].append(test_file.name)

            self.print_separator("-", 80)

        # Resumen de casos validos
        self.print_header("RESUMEN - CASOS VALIDOS", "=", 80)
        print(f"Total de archivos: {len(valid_files)}")
        print(f" Pasaron: {len(results['passed'])}")
        print(f" Fallaron: {len(results['failed'])}")

        if results["failed"]:
            print(f"\nArchivos que fallaron:")
            for filename in results["failed"]:
                print(f"  - {filename}")

        self.print_separator("=", 80)

        # Assertion final
        assert len(results["failed"]) == 0, \
            f"{len(results['failed'])} archivo(s) valido(s) fallaron: {results['failed']}"

    def test_invalid_programs(self):
        """Prueba todos los programas invalidos que deben generar errores semanticos"""
        self.print_header("PRUEBAS DE CASOS INVALIDOS", "=", 80)

        invalid_files = self.get_test_files(self.INVALID_TESTS_DIR)

        if not invalid_files:
            pytest.skip(f"No se encontraron archivos en {self.INVALID_TESTS_DIR}")

        results = {
            "passed": [],
            "failed": []
        }

        for test_file in invalid_files:
            self.print_separator("-", 80)
            print(f" EJECUTANDO: {test_file.name}")
            self.print_separator("-", 80)

            success, output, error = self.run_single_test(test_file, expected_success=False)

            # Para casos invalidos, queremos que FALLE (success=False)
            if not success:
                print(f" PASO: {test_file.name} (detecto el error correctamente)")
                print(f"\nError detectado:")
                print(error)
                results["passed"].append(test_file.name)
            else:
                print(f" FALLO: {test_file.name} (deberia haber generado error)")
                print(output)
                results["failed"].append(test_file.name)

            self.print_separator("-", 80)

        # Resumen de casos invalidos
        self.print_header("RESUMEN - CASOS INVALIDOS", "=", 80)
        print(f"Total de archivos: {len(invalid_files)}")
        print(f" Pasaron (detectaron error): {len(results['passed'])}")
        print(f" Fallaron (no detectaron error): {len(results['failed'])}")

        if results["failed"]:
            print(f"\nArchivos que fallaron (no detectaron error):")
            for filename in results["failed"]:
                print(f"  - {filename}")

        self.print_separator("=", 80)

        # Assertion final
        assert len(results["failed"]) == 0, \
            f"{len(results['failed'])} archivo(s) invalido(s) no detectaron error: {results['failed']}"

    def test_runtime_errors(self):
        """Prueba programas que generan errores en tiempo de ejecucion (no semanticos)"""
        self.print_header("PRUEBAS DE ERRORES EN TIEMPO DE EJECUCION", "=", 80)

        runtime_files = self.get_test_files(self.RUNTIME_ERRORS_DIR)

        if not runtime_files:
            pytest.skip(f"No se encontraron archivos en {self.RUNTIME_ERRORS_DIR}")

        results = {
            "passed": [],
            "failed": []
        }

        for test_file in runtime_files:
            self.print_separator("-", 80)
            print(f" EJECUTANDO: {test_file.name}")
            self.print_separator("-", 80)

            success, output, error = self.run_single_test(test_file, expected_success=False)

            # Para errores de runtime, queremos que FALLE (success=False)
            # pero el error debe ser de runtime (division por cero, stack overflow, etc.)
            if not success and error:
                print(f" PASO: {test_file.name} (error de runtime detectado)")
                print(f"\nError detectado:")
                print(error)
                results["passed"].append(test_file.name)
            elif success:
                print(f" FALLO: {test_file.name} (deberia haber generado error de runtime)")
                print(output)
                results["failed"].append(test_file.name)
            else:
                print(f" FALLO: {test_file.name} (error inesperado)")
                results["failed"].append(test_file.name)

            self.print_separator("-", 80)

        # Resumen de errores de runtime
        self.print_header("RESUMEN - ERRORES DE RUNTIME", "=", 80)
        print(f"Total de archivos: {len(runtime_files)}")
        print(f" Pasaron (error detectado): {len(results['passed'])}")
        print(f" Fallaron (error no detectado): {len(results['failed'])}")

        if results["failed"]:
            print(f"\nArchivos que fallaron:")
            for filename in results["failed"]:
                print(f"  - {filename}")

        self.print_separator("=", 80)

        # Assertion final
        assert len(results["failed"]) == 0, \
            f"{len(results['failed'])} archivo(s) de runtime no generaron el error esperado: {results['failed']}"


class TestIndividualValidCases:
    """Tests individuales para cada caso valido (para poder ejecutarlos por separado)"""

    VALID_TESTS_DIR = Path("Tests/Semantica/Validos")

    @pytest.fixture(params=sorted(VALID_TESTS_DIR.glob("*.txt")) if VALID_TESTS_DIR.exists() else [])
    def valid_file(self, request):
        return request.param

    def test_individual_valid(self, valid_file):
        """Prueba individual de caso valido"""
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            run_compiler(str(valid_file))

            sys.stdout = old_stdout
            sys.stderr = old_stderr

        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            pytest.fail(f"El archivo valido {valid_file.name} fallo: {str(e)}")


class TestIndividualInvalidCases:
    """Tests individuales para cada caso invalido (para poder ejecutarlos por separado)"""

    INVALID_TESTS_DIR = Path("Tests/Semantica/Invalidos")

    @pytest.fixture(params=sorted(INVALID_TESTS_DIR.glob("*.txt")) if INVALID_TESTS_DIR.exists() else [])
    def invalid_file(self, request):
        return request.param

    def test_individual_invalid(self, invalid_file):
        """Prueba individual de caso invalido"""
        old_stdout = sys.stdout
        old_stderr = sys.stderr

        try:
            sys.stdout = StringIO()
            sys.stderr = StringIO()

            run_compiler(str(invalid_file))

            sys.stdout = old_stdout
            sys.stderr = old_stderr

            pytest.fail(f"El archivo invalido {invalid_file.name} deberia haber generado un error")

        except BabyDuckError:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            # Correcto, se esperaba un error
            pass

        except Exception as e:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            pytest.fail(f"Error inesperado en {invalid_file.name}: {str(e)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
