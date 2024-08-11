import csv  # Importa el módulo csv para trabajar con archivos CSV
import os   # Importa el módulo os para interactuar con el sistema operativo

# Define la clase Tarea para representar una tarea individual
class Tarea:
    def __init__(self, id, descripcion, prioridad, categoria="General"):
        self.id = id  # Identificador único de la tarea
        self.descripcion = descripcion  # Descripción de la tarea
        self.prioridad = prioridad  # Prioridad de la tarea (1 = baja, 2 = media, 3 = alta)
        self.completada = False  # Indica si la tarea está completada o no
        self.categoria = categoria  # Categoría de la tarea, por defecto es "General"

# Define la clase Nodo para representar un nodo en la lista enlazada
class Nodo:
    def __init__(self, tarea):
        self.tarea = tarea  # La tarea asociada a este nodo
        self.siguiente = None  # Referencia al siguiente nodo en la lista

# Define la clase ListaEnlazada para gestionar una lista de tareas
class ListaEnlazada:
    def __init__(self):
        self.cabeza = None  # Nodo inicial (cabeza) de la lista enlazada
        self.id_actual = 1  # Controla el ID para nuevas tareas
        self.contador_de_pendi = 0  # Contador de tareas pendientes
        self.contador_de_total = 0  # Contador de tareas totales

    # Verifica si la lista está vacía
    def esta_vacia(self):
        return self.cabeza is None  # Retorna True si la cabeza es None

    # Agrega una nueva tarea a la lista enlazada
    def agregar_tarea(self, descripcion, prioridad, categoria):

        # Verifica si ya existe una tarea con la misma descripción
        if not self.buscar_tarea_descripcion(descripcion):
            self.contador_de_total += 1  # Incrementa el contador de tareas totales
            self.contador_de_pendi += 1  # Incrementa el contador de tareas pendientes
            tarea = Tarea(self.id_actual, descripcion, prioridad, categoria)  # Crea una nueva tarea
            nuevo_nodo = Nodo(tarea)  # Crea un nuevo nodo con la tarea
            self.id_actual += 1  # Incrementa el ID para la siguiente tarea

            # Si la lista está vacía o la prioridad de la nueva tarea es mayor que la cabeza, inserta al inicio
            if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad:
                nuevo_nodo.siguiente = self.cabeza  # El siguiente nodo del nuevo nodo será la cabeza actual
                self.cabeza = nuevo_nodo  # La nueva cabeza será el nuevo nodo
            else:
                actual = self.cabeza  # Comienza desde la cabeza
                # Encuentra la posición correcta según la prioridad
                while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad:
                    actual = actual.siguiente
                nuevo_nodo.siguiente = actual.siguiente  # Inserta el nuevo nodo en la posición correcta
                actual.siguiente = nuevo_nodo  # Ajusta la referencia del nodo anterior

            print("Tarea agregada con éxito.")  # Mensaje de confirmación

        else:
            print("La tarea ya existe")  # Si la tarea ya existe, no se agrega

    # Busca si una tarea con una descripción específica ya existe
    def buscar_tarea_descripcion(self, texto):
        actual = self.cabeza  # Comienza desde la cabeza
        while actual != None:
            if actual.tarea.descripcion == texto:  # Si encuentra la descripción, retorna True
                return True
            actual = actual.siguiente  # Avanza al siguiente nodo
        return False  # Retorna False si no encuentra la tarea

    # Busca una tarea por su ID y la retorna si la encuentra
    def buscar_tarea_id(self, id) -> Tarea:
        tarea = False  # Inicializa la variable tarea como False
        actual = self.cabeza  # Comienza desde la cabeza
        while actual != None:
            if actual.tarea.id == id:  # Si encuentra la tarea con el ID, la asigna a tarea
                tarea = actual.tarea
            actual = actual.siguiente  # Avanza al siguiente nodo
        return tarea  # Retorna la tarea encontrada o False si no la encuentra

    # Marca una tarea como completada
    def completar_tarea(self, id):
        tarea = self.buscar_tarea_id(id)  # Busca la tarea por su ID
        tarea.completada = True  # Marca la tarea como completada
        self.contador_de_pendi -= 1  # Decrementa el contador de tareas pendientes

    # Elimina una tarea de la lista por su ID
    def eliminar_tarea(self, id):
        if self.buscar_tarea_id(id) != False:  # Verifica si la tarea existe
            actual = self.cabeza  # Comienza desde la cabeza
            previo = None  # Inicializa el nodo previo como None
            while actual is not None:
                if actual.tarea.id == id:  # Si encuentra la tarea con el ID
                    if previo is None:  # Si es la primera tarea
                        self.cabeza = actual.siguiente  # La cabeza pasa a ser el siguiente nodo
                    else:
                        previo.siguiente = actual.siguiente  # Elimina el nodo de la lista
                    if actual.tarea.completada == False:
                        self.contador_de_pendi -= 1  # Decrementa el contador de pendientes si la tarea no estaba completada
                    self.contador_de_total -= 1  # Decrementa el contador de tareas totales
                    print(f"Tarea eliminada: {actual.tarea.descripcion}")  # Muestra mensaje de eliminación
                    return
                previo = actual  # Actualiza el nodo previo
                actual = actual.siguiente  # Avanza al siguiente nodo
            print(f"Tarea con ID {id} no encontrada.")  # Mensaje si no encuentra la tarea
        else:
            print("La tarea NO existe.")  # Mensaje si la tarea no existe

    # Muestra todas las tareas en la lista
    def mostrar_tareas(self):
        actual = self.cabeza  # Comienza desde la cabeza
        if actual is None:
            print("No hay tareas")  # Si no hay tareas, muestra mensaje
        while actual is not None:
            self.mostrar_una_tarea(actual.tarea)  # Muestra cada tarea
            actual = actual.siguiente  # Avanza al siguiente nodo

    # Muestra solo las tareas pendientes
    def mostrar_tareas_pendientes(self):
        actual = self.cabeza  # Comienza desde la cabeza
        if actual is None:
            print("No hay tareas")  # Si no hay tareas, muestra mensaje
        while actual is not None:
            if not actual.tarea.completada:  # Solo muestra tareas que no están completadas
                self.mostrar_una_tarea(actual.tarea)
            actual = actual.siguiente  # Avanza al siguiente nodo

    # Muestra los detalles de una tarea individual
    def mostrar_una_tarea(self, tarea):
        estado = "Completada" if tarea.completada else "Pendiente"  # Determina el estado de la tarea
        print(f"ID: {tarea.id}, Descripción: {tarea.descripcion}, Prioridad: {tarea.prioridad}, Categoría: {tarea.categoria}, Estado: {estado}")  # Muestra detalles

    # Muestra tareas que contienen un texto en su descripción
    def mostrar_tareas_descripcion(self, text) -> None:
        actual = self.cabeza  # Comienza desde la cabeza
        while actual is not None:
            if text in actual.tarea.descripcion:  # Si el texto está en la descripción, muestra la tarea
                self.mostrar_una_tarea(actual.tarea)
            actual = actual.siguiente  # Avanza al siguiente nodo

    # Cuenta las tareas pendientes de manera lineal
    def contar_tareas_pendientes_lineal(self) -> int:
        actual = self.cabeza  # Comienza desde la cabeza
        contador = 0  # Inicializa el contador en 0
        while actual is not None:
            if actual.tarea.completada == False:  # Cuenta solo tareas que no están completadas
                contador += 1
            actual = actual.siguiente  # Avanza al siguiente nodo
        return contador  # Retorna el número de tareas pendientes

    # Retorna el número de tareas pendientes de manera constante
    def contar_tareas_pendientes_cte(self) -> int:
        return self.contador_de_pendi  # Retorna el contador de tareas pendientes

    # Muestra estadísticas de las tareas
    def mostrar_estadisticas(self) -> None:
        completadas = self.contador_de_total - self.contar_tareas_pendientes_cte()  # Calcula el número de tareas completadas
        pendientes = self.contar_tareas_pendientes_cte()  # Obtiene el número de tareas pendientes
        total = self.contador_de_total  # Obtiene el total de tareas
        
        if total > 0:
            porcentaje_completadas = (completadas / total) * 100  # Calcula el porcentaje de tareas completadas
            porcentaje_pendientes = (pendientes / total) * 100  # Calcula el porcentaje de tareas pendientes
        else:
            porcentaje_completadas = 0
            porcentaje_pendientes = 0
    
        print(f"Total de tareas: {total}")
        print(f"Tareas completadas: {completadas} ({porcentaje_completadas:.2f}%)")
        print(f"Tareas pendientes: {pendientes} ({porcentaje_pendientes:.2f}%)")

    # Guarda las tareas en un archivo CSV
    def guardar_en_csv(self, archivo):
        with open(archivo, mode='w', newline='') as file:  # Abre el archivo en modo escritura
            writer = csv.writer(file)  # Crea un escritor de CSV
            actual = self.cabeza  # Comienza desde la cabeza
            while actual is not None:
                writer.writerow([actual.tarea.id, actual.tarea.descripcion, actual.tarea.prioridad, actual.tarea.categoria, actual.tarea.completada])  # Escribe cada tarea en una fila
                actual = actual.siguiente  # Avanza al siguiente nodo
        print(f"Tareas guardadas en {archivo} con éxito.")  # Muestra mensaje de éxito

    # Carga las tareas desde un archivo CSV
    def cargar_desde_csv(self, archivo):
        if not os.path.exists(archivo):  # Verifica si el archivo existe
            print(f"Archivo {archivo} no encontrado.")  # Muestra mensaje si no existe
            return
        with open(archivo, mode='r') as file:  # Abre el archivo en modo lectura
            reader = csv.reader(file)  # Crea un lector de CSV
            for row in reader:
                id, descripcion, prioridad, categoria, completada = int(row[0]), row[1], int(row[2]), row[3], row[4] == 'True'  # Lee y convierte los valores de cada fila
                tarea = Tarea(id, descripcion, prioridad, categoria)  # Crea una nueva tarea con los datos
                tarea.completada = completada  # Marca la tarea como completada si corresponde
                self.agregar_tarea_existente(tarea)  # Agrega la tarea a la lista
            print(f"Tareas cargadas desde {archivo} con éxito.")  # Muestra mensaje de éxito

    # Agrega una tarea existente a la lista (usado al cargar desde CSV)
    def agregar_tarea_existente(self, tarea):

        if not self.buscar_tarea_descripcion(tarea.descripcion):  # Verifica si la tarea ya existe
        
            if tarea.completada is not True:
                self.contador_de_pendi += 1  # Incrementa el contador de pendientes si la tarea no está completada
            self.contador_de_total += 1  # Incrementa el contador de tareas totales
            nuevo_nodo = Nodo(tarea)  # Crea un nuevo nodo con la tarea
            if self.esta_vacia() or tarea.prioridad > self.cabeza.tarea.prioridad:
                nuevo_nodo.siguiente = self.cabeza  # Inserta el nuevo nodo al principio si corresponde
                self.cabeza = nuevo_nodo  # La nueva cabeza será el nuevo nodo
            else:
                actual = self.cabeza  # Comienza desde la cabeza
                while actual.siguiente is not None and actual.siguiente.tarea.prioridad >= tarea.prioridad:
                    actual = actual.siguiente  # Encuentra la posición correcta
                nuevo_nodo.siguiente = actual.siguiente  # Inserta el nuevo nodo en la posición correcta
                actual.siguiente = nuevo_nodo
    
            if tarea.id >= self.id_actual:
                self.id_actual = tarea.id + 1  # Actualiza el ID para nuevas tareas
        
        else:
            print("La tarea NO existe.")  # Muestra mensaje si la tarea ya existe

# Función que muestra el menú de opciones
def menu():
    print("\nMenú:")
    print("1. Agregar tarea")
    print("2. Completar tarea")
    print("3. Eliminar tarea")
    print("4. Mostrar todas las tareas")
    print("5. Mostrar tareas pendientes")
    print("6. Guardar tareas en archivo CSV")
    print("7. Cargar tareas desde archivo CSV")
    print("8. Mostrar estadísticas")
    print("9. Salir")

# Función principal que ejecuta el programa
def main():
    lista_tareas = ListaEnlazada()  # Crea una nueva lista enlazada para gestionar las tareas
    archivo_csv = 'tareas.csv'  # Nombre del archivo CSV para guardar/cargar tareas

    # Cargar tareas desde CSV si el archivo existe
    lista_tareas.cargar_desde_csv(archivo_csv)

    while True:
        menu()  # Muestra el menú de opciones
        opcion = input("Seleccione una opción: ")  # Pide al usuario que seleccione una opción
        
        if opcion == "1":
            descripcion = input("Ingrese la descripción de la tarea: ")  # Pide la descripción de la tarea
            while True:
                try:
                    prioridad = int(input("Ingrese la prioridad de la tarea (1 = baja, 2 = media, 3 = alta): "))  # Pide la prioridad de la tarea
                    if prioridad in [1, 2, 3]:  # Verifica que la prioridad sea válida
                        break
                    else:
                        print("Por favor, ingrese un número entre 1 y 3.")  # Mensaje de error para prioridad inválida
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")  # Mensaje de error si no es un número
            
            categoria = input("Ingrese la categoría de la tarea: ")  # Pide la categoría de la tarea
            lista_tareas.agregar_tarea(descripcion, prioridad, categoria)  # Agrega la tarea a la lista
        
        elif opcion == "2":
            while True:
                try:
                    id_tarea = int(input("Ingrese el ID de la tarea a completar: "))  # Pide el ID de la tarea a completar
                    lista_tareas.completar_tarea(id_tarea)  # Marca la tarea como completada
                    break
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")  # Mensaje de error si no es un número
                except Exception as e:
                    print(f"Error: {e}")  # Muestra cualquier otro error
                    break
        
        elif opcion == "3":
            while True:
                try:
                    id_tarea = int(input("Ingrese el ID de la tarea a eliminar: "))  # Pide el ID de la tarea a eliminar
                    lista_tareas.eliminar_tarea(id_tarea)  # Elimina la tarea de la lista
                    break
                except ValueError:
                    print("Entrada no válida. Debe ingresar un número entero.")  # Mensaje de error si no es un número
                except Exception as e:
                    print(f"Error: {e}")  # Muestra cualquier otro error
                    break

        elif opcion == "4":
            lista_tareas.mostrar_tareas()  # Muestra todas las tareas
        
        elif opcion == "5":
            lista_tareas.mostrar_tareas_pendientes()  # Muestra solo las tareas pendientes
        
        elif opcion == "6":
            lista_tareas.guardar_en_csv(archivo_csv)  # Guarda las tareas en un archivo CSV
        
        elif opcion == "7":
            lista_tareas.cargar_desde_csv(archivo_csv)  # Carga las tareas desde un archivo CSV
        
        elif opcion == "8":
            lista_tareas.mostrar_estadisticas()  # Muestra las estadísticas de las tareas
        
        elif opcion == "9":
            print("Saliendo del sistema de gestión de tareas.")  # Mensaje de salida
            break
        
        else:
            print("Opción no válida. Por favor, seleccione una opción válida.")  # Mensaje si la opción es inválida

# Punto de entrada del programa
if __name__ == "__main__":
    main()  # Llama a la función principal para iniciar el programa