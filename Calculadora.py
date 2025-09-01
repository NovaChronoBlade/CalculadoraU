from abc import ABC, abstractmethod
from functools import wraps


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
            return a / b
        except ZeroDivisionError:
            return 0

    @abstractmethod
    def _convertir_numero(self, valor):
        """Convierte un valor al sistema numérico de la calculadora"""
        pass

    @abstractmethod
    def _validar_formato(self, valor):
        """Valida el formato del valor de entrada"""
        pass

class CalculadoraDecimal(Calculadora):
    def _convertir_numero(self, valor):
        return int(valor)

    def _validar_formato(self, valor):
        return str(valor).isdigit()


class CalculadoraBinaria(Calculadora):
    def _convertir_numero(self, valor):
        return int(valor, 2)

    def _validar_formato(self, valor):
        return all(c in "01" for c in str(valor))


class CalculadoraHexadecimal(Calculadora):
    def _convertir_numero(self, valor):
        return int(valor, 16)

    def _validar_formato(self, valor):
        try:
            int(str(valor), 16)
            return True
        except ValueError:
            return False
        

bin_calc = CalculadoraBinaria()

print(bin_calc.sumar('1010', '1100'))  # Suma en binario
print(bin_calc.restar('1010', '1100'))  # Resta en binario
print(bin_calc.multiplicar('1010', '1100'))  # Multiplicación en binario
print(bin_calc.dividir('1010', '1100'))  # División en binario