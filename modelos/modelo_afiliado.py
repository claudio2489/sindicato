from PyQt5 import QtCore
from libs.db import querier
import cerberus
from validadores.validador_afiliado import esquemaAfiliado

class ModeloAfiliado(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloAfiliado, self).__init__()

        # La idea ahora es separar el esquema de validación de los datos y campos que se van a usar, nosotros no vamos a usar
        # todos los campos en la tabla, habíamos definido los que se encuentran en el archivo 'cosas para hacer.md'
        # | Legajo | Apellido | Nombre | DNI | Dirección | Teléfono | Ordenado alfabéticamente por apellido
        # Calle + Altura + Piso + Depto + (Localidad)

        self.__propiedades = ['legajo','dni',
        'tipo_afiliado','cuil',
        'apellido','nombre',
        'fecha_nacimiento', 'edad', 'estado_civil',
        'nacionalidad', 'calle', 'altura',
        'piso', 'depto','cod_postal', 'barrio',
        'localidad', 'telefono',
        'celular','email'
        ]

        self.__propiedades = self.validarPropiedades(propiedades)

        self.__afiliado = { }

# Esta lista de listas es la que aparece en la tabla de afiliados apenas arranca
# el programa
# Tengo que hacer que el programa levante esta lista desde la base de datos.
# En la base de datos tengo solamente un objeto que tiene todos los campos vacíos salvo el dni
# El legajo hay que modificarlo porque tiene auto-incremento

        self.__listaAfiliados = [] # Los valores de prueba los saco del archivo fuente

# Legajo : 1, dni : 37537040 es lo que tiene que aparecer cuando uso esta función
    def verListaAfiliados(self):
        self.__listaAfiliados = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'afiliados')
        if self.__listaAfiliados:
            self.layoutChanged.emit()
            return True
        return False

    def verDetallesAfiliado(self, afiliado = QtCore.QModelIndex()):
        afiliado = self.__listaAfiliados[afiliado.row()]
        legajo = afiliado[0]

        respuesta = self.__querier.traerElementos(
            condiciones = [('legajo', '=', legajo)],
            tabla = 'afiliados',
            limite = 1
            )

        afiliado = list(respuesta[0])
        print(afiliado)

        self.__afiliado = afiliado

    def guardarAfiliado():
        pass

    def borrarAfiliado():
        pass

    def validarPropiedades(self, propiedades):
# ahora mi función se asegura que las propieades existan en la lista, debería encontrar si hay alguna forma mas elegante de hacer esto
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

# Estas son las funciones específicas de Qt para las tablas
    def rowCount(self, parent):
        return len(self.__listaAfiliados)

    def columnCount(self, parent):
        if self.__listaAfiliados:
            return len(self.__listaAfiliados[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
# Acá es donde definí de dónde (De qué lista) voy a levantar los datos
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaAfiliados[row][column] # value contiene la lista de listas que contiene los afiliados

            return value # el valor que retorno es el que aparecería en la tabla

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            column = index.column()

            value = self.articulos[row][column]

            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
# Los objetos tipo diccionario no ordenan sus elementos, por eso usar dict.keys() me tira los nombres
# de las columnas en cualquier orden. Acá debería usar la lista propiedades.
# además de salir ordenado, se ajusta la cantidad de columnas correspondiente
                keys = list(self.__propiedades)
                return keys[section]
