from abc import ABC, abstractmethod
from functools import wraps
import os
import sys

def limpiar_pantalla():
    """Limpia la pantalla de la consola"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_entradas(func):
    """Decorador que permite validar si el formato requerido es correcto"""
    @wraps(func)
    def wrapper(self, a, b, *args, **kwargs):
        if not self._validar_formato(a):
            raise ValueError(f"Formato inválido para '{a}'")
        if not self._validar_formato(b):
            raise ValueError(f"Formato inválido para '{b}'")
        a_convertido = self._convertir_numero(a)
        b_convertido = self._convertir_numero(b)
        return func(self, a_convertido, b_convertido, *args, **kwargs)
    return wrapper

class Calculadora(ABC):
    """Clase abstracta base para calculadoras de diferentes sistemas numéricos"""
    
    @validar_entradas
    def sumar(self, a, b):
        return a + b
    
    @validar_entradas
    def restar(self, a, b):
        return a - b
    
    @validar_entradas
    def multiplicar(self, a, b):
        return a * b
    
    @validar_entradas
    def dividir(self, a, b):
        try:
            if b == 0:
                raise ZeroDivisionError("División por cero no permitida")
            return a / b
        except ZeroDivisionError as e:
            raise e
    
    @validar_entradas
    def potencia(self, a, b):
        return a ** b
    
    @validar_entradas
    def modulo(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Módulo por cero no permitido")
        return a % b
    
    @abstractmethod
    def _convertir_numero(self, valor):
        """Convierte un valor al sistema numérico de la calculadora"""
        pass
    
    @abstractmethod
    def _validar_formato(self, valor):
        """Valida el formato del valor de entrada"""
        pass
    
    @abstractmethod
    def convertir_resultado(self, resultado):
        """Convierte el resultado de vuelta al sistema numérico correspondiente"""
        pass
    
    @abstractmethod
    def get_nombre_sistema(self):
        """Retorna el nombre del sistema numérico"""
        pass

class CalculadoraDecimal(Calculadora):
    """Calculadora para sistema decimal"""
    
    def _convertir_numero(self, valor):
        try:
            # Intenta convertir a float primero para números decimales
            return float(valor)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número decimal válido")
    
    def _validar_formato(self, valor):
        try:
            float(str(valor))
            return True
        except ValueError:
            return False
    
    def convertir_resultado(self, resultado):
        # Si es un número entero, mostrarlo sin decimales
        if isinstance(resultado, float) and resultado.is_integer():
            return str(int(resultado))
        return str(resultado)
    
    def get_nombre_sistema(self):
        return "Decimal"

class CalculadoraBinaria(Calculadora):
    """Calculadora para sistema binario"""
    
    def _convertir_numero(self, valor):
        try:
            return int(valor, 2)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número binario válido")
    
    def _validar_formato(self, valor):
        return all(c in "01" for c in str(valor)) and str(valor) != ""
    
    def convertir_resultado(self, resultado):
        if isinstance(resultado, float):
            if resultado.is_integer():
                return bin(int(resultado))[2:]  # Quitar el prefijo '0b'
            else:
                return f"{bin(int(resultado))[2:]} (parte entera)"
        return bin(int(resultado))[2:]
    
    def get_nombre_sistema(self):
        return "Binario"

class CalculadoraHexadecimal(Calculadora):
    """Calculadora para sistema hexadecimal"""
    
    def _convertir_numero(self, valor):
        try:
            return int(valor, 16)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número hexadecimal válido")
    
    def _validar_formato(self, valor):
        try:
            int(str(valor), 16)
            return True
        except ValueError:
            return False
    
    def convertir_resultado(self, resultado):
        if isinstance(resultado, float):
            if resultado.is_integer():
                return hex(int(resultado))[2:].upper()  # Quitar prefijo '0x' y usar mayúsculas
            else:
                return f"{hex(int(resultado))[2:].upper()} (parte entera)"
        return hex(int(resultado))[2:].upper()
    
    def get_nombre_sistema(self):
        return "Hexadecimal"

class CalculadoraOctal(Calculadora):
    """Calculadora para sistema octal"""
    
    def _convertir_numero(self, valor):
        try:
            return int(valor, 8)
        except ValueError:
            raise ValueError(f"'{valor}' no es un número octal válido")
    
    def _validar_formato(self, valor):
        return all(c in "01234567" for c in str(valor)) and str(valor) != ""
    
    def convertir_resultado(self, resultado):
        if isinstance(resultado, float):
            if resultado.is_integer():
                return oct(int(resultado))[2:]  # Quitar prefijo '0o'
            else:
                return f"{oct(int(resultado))[2:]} (parte entera)"
        return oct(int(resultado))[2:]
    
    def get_nombre_sistema(self):
        return "Octal"

class InterfazCalculadora:
    """Interfaz gráfica de consola para la calculadora"""
    
    def __init__(self):
        self.calculadoras = {
            '1': CalculadoraDecimal(),
            '2': CalculadoraBinaria(),
            '3': CalculadoraHexadecimal(),
            '4': CalculadoraOctal()
        }
        self.calculadora_actual = None
        self.historial = []
    
    def mostrar_banner(self):
        """Muestra el banner principal"""
        print("=" * 60)
        print("           CALCULADORA MULTI-SISTEMA")
        print("=" * 60)
        print()
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal de selección de sistema"""
        print("\n┌─────────────────────────────────────┐")
        print("│      SELECCIONAR SISTEMA NUMÉRICO   │")
        print("├─────────────────────────────────────┤")
        print("│ 1. Sistema Decimal                  │")
        print("│ 2. Sistema Binario                  │")
        print("│ 3. Sistema Hexadecimal              │")
        print("│ 4. Sistema Octal                    │")
        print("│ 5. Ver Historial                    │")
        print("│ 6. Limpiar Historial                │")
        print("│ 7. Salir                            │")
        print("└─────────────────────────────────────┘")
    
    def mostrar_menu_operaciones(self):
        """Muestra el menú de operaciones"""
        sistema = self.calculadora_actual.get_nombre_sistema()
        print(f"\n┌─────────────────────────────────────┐")
        print(f"│        CALCULADORA {sistema.upper():^11}        │")
        print("├─────────────────────────────────────┤")
        print("│ 1. Sumar                            │")
        print("│ 2. Restar                           │")
        print("│ 3. Multiplicar                      │")
        print("│ 4. Dividir                          │")
        print("│ 5. Potencia                         │")
        print("│ 6. Módulo                           │")
        print("│ 7. Volver al menú principal         │")
        print("└─────────────────────────────────────┘")
    
    def mostrar_ayuda_formato(self, sistema):
        """Muestra ayuda sobre el formato de entrada para cada sistema"""
        formatos = {
            "Decimal": "Números enteros o decimales (ej: 123, 45.67, -89)",
            "Binario": "Solo dígitos 0 y 1 (ej: 1010, 1100, 111)",
            "Hexadecimal": "Dígitos 0-9 y letras A-F (ej: A1, FF, 2B4)",
            "Octal": "Solo dígitos 0-7 (ej: 123, 456, 777)"
        }
        print(f"\n💡 Formato para {sistema}: {formatos[sistema]}")
    
    def obtener_entrada(self, mensaje, sistema):
        """Obtiene entrada del usuario con validación"""
        while True:
            try:
                entrada = input(f"{mensaje}: ").strip()
                if entrada.lower() == 'menu':
                    return None
                if entrada == '':
                    print("❌ Entrada vacía. Intente nuevamente.")
                    continue
                # Validar formato usando la calculadora actual
                if not self.calculadora_actual._validar_formato(entrada):
                    print(f"❌ Formato inválido para sistema {sistema}")
                    self.mostrar_ayuda_formato(sistema)
                    continue
                return entrada
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                sys.exit(0)
    
    def realizar_operacion(self, operacion, nombre_operacion):
        """Realiza una operación específica"""
        sistema = self.calculadora_actual.get_nombre_sistema()
        print(f"\n--- {nombre_operacion.upper()} EN {sistema.upper()} ---")
        self.mostrar_ayuda_formato(sistema)
        print("(Escribe 'menu' para volver al menú)")
        
        # Obtener primer número
        a = self.obtener_entrada("Ingrese el primer número", sistema)
        if a is None:
            return
        
        # Obtener segundo número
        b = self.obtener_entrada("Ingrese el segundo número", sistema)
        if b is None:
            return
        
        try:
            # Realizar la operación
            resultado_decimal = operacion(a, b)
            resultado_sistema = self.calculadora_actual.convertir_resultado(resultado_decimal)
            
            # Mostrar resultado
            print(f"\n✅ RESULTADO:")
            print(f"   {a} {self.obtener_simbolo_operacion(nombre_operacion)} {b} = {resultado_sistema}")
            
            # Agregar al historial
            operacion_str = f"{sistema}: {a} {self.obtener_simbolo_operacion(nombre_operacion)} {b} = {resultado_sistema}"
            self.historial.append(operacion_str)
            
            input("\nPresiona Enter para continuar...")
            
        except Exception as e:
            print(f"\n❌ Error: {e}")
            input("\nPresiona Enter para continuar...")
    
    def obtener_simbolo_operacion(self, nombre):
        """Retorna el símbolo matemático de la operación"""
        simbolos = {
            "suma": "+",
            "resta": "-", 
            "multiplicación": "×",
            "división": "÷",
            "potencia": "^",
            "módulo": "%"
        }
        return simbolos.get(nombre, "?")
    
    def mostrar_historial(self):
        """Muestra el historial de operaciones"""
        limpiar_pantalla()
        self.mostrar_banner()
        print("📋 HISTORIAL DE OPERACIONES")
        print("-" * 60)
        
        if not self.historial:
            print("   No hay operaciones en el historial.")
        else:
            for i, operacion in enumerate(self.historial, 1):
                print(f"{i:2d}. {operacion}")
        
        input("\nPresiona Enter para continuar...")
    
    def limpiar_historial(self):
        """Limpia el historial de operaciones"""
        if self.historial:
            confirmar = input("¿Estás seguro de que deseas limpiar el historial? (s/n): ")
            if confirmar.lower() in ['s', 'si', 'sí', 'y', 'yes']:
                self.historial.clear()
                print("✅ Historial limpiado.")
            else:
                print("❌ Operación cancelada.")
        else:
            print("ℹ  El historial ya está vacío.")
        input("\nPresiona Enter para continuar...")
    
    def ejecutar(self):
        """Ejecuta la interfaz principal"""
        try:
            while True:
                limpiar_pantalla()
                self.mostrar_banner()
                self.mostrar_menu_principal()
                
                try:
                    opcion = input("\nSeleccione una opción: ").strip()
                    
                    if opcion == '7':
                        print("\n👋 ¡Gracias por usar la calculadora!")
                        break
                    
                    elif opcion in ['1', '2', '3', '4']:
                        self.calculadora_actual = self.calculadoras[opcion]
                        self.menu_operaciones()
                    
                    elif opcion == '5':
                        self.mostrar_historial()
                    
                    elif opcion == '6':
                        self.limpiar_historial()
                    
                    else:
                        print("❌ Opción inválida. Seleccione del 1 al 7.")
                        input("Presiona Enter para continuar...")
                        
                except KeyboardInterrupt:
                    print("\n\n👋 ¡Hasta luego!")
                    break
                    
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            input("Presiona Enter para salir...")
    
    def menu_operaciones(self):
        """Menú de operaciones para la calculadora seleccionada"""
        while True:
            limpiar_pantalla()
            self.mostrar_banner()
            self.mostrar_menu_operaciones()
            
            try:
                opcion = input("\nSeleccione una operación: ").strip()
                
                if opcion == '7':
                    break
                elif opcion == '1':
                    self.realizar_operacion(self.calculadora_actual.sumar, "suma")
                elif opcion == '2':
                    self.realizar_operacion(self.calculadora_actual.restar, "resta")
                elif opcion == '3':
                    self.realizar_operacion(self.calculadora_actual.multiplicar, "multiplicación")
                elif opcion == '4':
                    self.realizar_operacion(self.calculadora_actual.dividir, "división")
                elif opcion == '5':
                    self.realizar_operacion(self.calculadora_actual.potencia, "potencia")
                elif opcion == '6':
                    self.realizar_operacion(self.calculadora_actual.modulo, "módulo")
                else:
                    print("❌ Opción inválida. Seleccione del 1 al 7.")
                    input("Presiona Enter para continuar...")
                    
            except KeyboardInterrupt:
                break

def main():
    """Función principal"""
    print("Iniciando calculadora...")
    interfaz = InterfazCalculadora()
    interfaz.ejecutar()

if __name__ == "__main__":
    main()