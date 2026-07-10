
def validar_codigo(codigo):
    """No vacío ni solo espacios en blanco."""
    return codigo.strip() != ""


def validar_nombre(nombre):
    """No vacío ni solo espacios en blanco."""
    return nombre.strip() != ""


def validar_tipo(tipo):
    """Debe ser exactamente 'Mensual', 'Trimestral' o 'Anual'."""
    return tipo in ("Mensual", "Trimestral", "Anual")


def validar_duracion(duracion):
    """Número entero debe ser mayor que cero."""
    try:
        return int(duracion) > 0
    except ValueError:
        return False


def validar_acceso_piscina(valor):
    """El usuario debe ingresar 's' o 'n'."""
    return valor.strip().lower() in ("s", "n")


def validar_incluye_clases(valor):
    """El usuario debe ingresar 's' o 'n'."""
    return valor.strip().lower() in ("s", "n")


def validar_horario(horario):
    """No vacío ni solo espacios en blanco."""
    return horario.strip() != ""


def validar_precio(precio):
    """Número entero mayor que cero."""
    try:
        return int(precio) > 0
    except ValueError:
        return False


def validar_cupos(cupos):
    """Número entero mayor o igual a cero."""
    try:
        return int(cupos) >= 0
    except ValueError:
        return False


def mostrar_menu():
    print("========== MENÚ PRINCIPAL ==========")
    print("1. Cupos por tipo de plan")
    print("2. Búsqueda de planes por rango de precio")
    print("3. Actualizar precio de plan")
    print("4. Agregar plan")
    print("5. Eliminar plan")
    print("6. Salir")
    print("=====================================")


def leer_opcion():
    """No recibe parámetros. Valida que sea un entero dentro del rango 1-6."""
    while True:
        try:
            opcion = int(input("Ingrese opción: "))
            if 1 <= opcion <= 6:
                return opcion
            print("Debe seleccionar una opción válida")
        except ValueError:
            print("Debe seleccionar una opción válida")


def cupos_tipo(tipo, planes, inscripciones):
    """Recibe el tipo de plan, no retorna ningún valor, muestra el resultado."""
    total = 0
    tipo = tipo.lower()
    for codigo, datos in planes.items():
        if datos[1].lower() == tipo:
            total += inscripciones[codigo][1]
    print(f"El total de cupos disponibles es: {total}")


def busqueda_precio(p_min, p_max, planes, inscripciones):
    """Recibe precio mínimo y máximo, no retorna ningún valor, muestra resultados."""
    resultados = []
    for codigo, datos in inscripciones.items():
        precio, cupos = datos
        if p_min <= precio <= p_max and cupos != 0:
            nombre_plan = planes[codigo][0]
            resultados.append(f"{nombre_plan}--{codigo}")
    resultados.sort()
    if resultados:
        print(f"Los planes encontrados son: {resultados}")
    else:
        print("No hay planes en ese rango de precios.")



def buscar_codigo(codigo, diccionario):
    """Recorre el diccionario y retorna True si el código existe, False si no."""
    return codigo.strip().upper() in diccionario


def actualizar_precio(codigo, nuevo_precio, inscripciones):
    """Verifica existencia (usando buscar_codigo) y actualiza el precio si corresponde."""
    codigo = codigo.strip().upper()
    if buscar_codigo(codigo, inscripciones):
        inscripciones[codigo][0] = nuevo_precio
        return True
    return False



def agregar_plan(codigo, nombre, tipo, duracion, acceso_piscina, incluye_clases,
                  horario, precio, cupos, planes, inscripciones):
    """Agrega el registro en ambos diccionarios. Retorna True si fue agregado,
    False si el código ya existía."""
    codigo = codigo.strip().upper()
    if buscar_codigo(codigo, planes):
        return False
    planes[codigo] = [nombre, tipo, duracion, acceso_piscina, incluye_clases, horario]
    inscripciones[codigo] = [precio, cupos]
    return True



def eliminar_plan(codigo, planes, inscripciones):
    """Verifica existencia (usando buscar_codigo) y elimina el registro de
    ambos diccionarios. Retorna True/False."""
    codigo = codigo.strip().upper()
    if buscar_codigo(codigo, planes):
        del planes[codigo]
        del inscripciones[codigo]
        return True
    return False



def main():
    planes = {
        'F001': ['Plan Básico', 'mensual', 1, False, False, 'libre'],
        'F002': ['Plan Full', 'mensual', 1, True, True, 'libre'],
        'F003': ['Plan Estudiante', 'trimestral', 3, False, True, 'tarde'],
        'F004': ['Plan Senior', 'trimestral', 3, True, False, 'mañana'],
        'F005': ['Plan Anual Pro', 'anual', 12, True, True, 'libre'],
        'F006': ['Plan Nocturno', 'mensual', 1, False, True, 'noche'],
    }

    inscripciones = {
        'F001': [14990, 30],
        'F002': [22990, 10],
        'F003': [39990, 0],
        'F004': [35990, 6],
        'F005': [159990, 2],
        'F006': [18990, 15],
    }

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        #---------- Opción 1 ----------
        if opcion == 1:
            tipo = input("Ingrese tipo de plan a consultar: ")
            cupos_tipo(tipo, planes, inscripciones)

        #---------- Opción 2 ----------
        elif opcion == 2:
            while True:
                try:
                    p_min = int(input("Ingrese precio mínimo: "))
                    p_max = int(input("Ingrese precio máximo: "))
                    if p_min < 0 or p_max < 0 or p_min > p_max:
                        print("Debe ingresar valores enteros")
                        continue
                    break
                except ValueError:
                    print("Debe ingresar valores enteros")
            busqueda_precio(p_min, p_max, planes, inscripciones)

        # --------- Opción 3 ----------
        elif opcion == 3:
            while True:
                codigo = input("Ingrese código del plan: ")
                while True:
                    try:
                        nuevo_precio = int(input("Ingrese nuevo precio: "))
                        if nuevo_precio <= 0:
                            print("Debe ingresar un valor entero positivo")
                            continue
                        break
                    except ValueError:
                        print("Debe ingresar un valor entero positivo")

                exito = actualizar_precio(codigo, nuevo_precio, inscripciones)
                print("Precio actualizado" if exito else "El código no existe")

                resp = input("¿Desea actualizar otro precio (s/n)?: ").strip().lower()
                if resp != 's':
                    break

        #---------- Opción 4 ----------
        elif opcion == 4:
            codigo = input("Ingrese código del plan: ")
            nombre = input("Ingrese nombre del plan: ")
            tipo = input("Ingrese tipo (mensual/trimestral/anual): ")
            duracion = input("Ingrese duración (meses): ")
            acceso_piscina = input("¿Incluye acceso a piscina? (s/n): ")
            incluye_clases = input("¿Incluye clases grupales? (s/n): ")
            horario = input("Ingrese horario: ")
            precio = input("Ingrese precio: ")
            cupos = input("Ingrese cupos: ")

            if not validar_codigo(codigo):
                print("El código no puede estar vacío")
            elif not validar_nombre(nombre):
                print("El nombre no puede estar vacío")
            elif not validar_tipo(tipo):
                print("Tipo inválido. Debe ser 'mensual', 'trimestral' o 'anual'")
            elif not validar_duracion(duracion):
                print("Duración inválida. Debe ser un entero mayor a cero")
            elif not validar_acceso_piscina(acceso_piscina):
                print("Valor inválido. Ingrese 's' o 'n'")
            elif not validar_incluye_clases(incluye_clases):
                print("Valor inválido. Ingrese 's' o 'n'")
            elif not validar_horario(horario):
                print("El horario no puede estar vacío")
            elif not validar_precio(precio):
                print("Precio inválido. Debe ser un entero mayor a cero")
            elif not validar_cupos(cupos):
                print("Cupos inválidos. Debe ser un entero mayor o igual a cero")
            else:
                exito = agregar_plan(
                    codigo, nombre, tipo, int(duracion),
                    acceso_piscina.strip().lower() == 's',
                    incluye_clases.strip().lower() == 's',
                    horario, int(precio), int(cupos),
                    planes, inscripciones
                )
                print("Plan agregado" if exito else "El código ya existe")

        #---------- Opción 5 ----------
        elif opcion == 5:
            codigo = input("Ingrese código del plan: ")
            exito = eliminar_plan(codigo, planes, inscripciones)
            print("Plan eliminado" if exito else "El código no existe")

        #---------- Opción 6 ----------
        elif opcion == 6:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()
