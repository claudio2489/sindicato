from PyQt5 import QtCore
from libs.db import querier
import cerberus
from validadores.validador_proveedor import esquemaProveedor

class ModeloProveedores(QtCore.QAbstractTableModel):
    __querier = querier.Querier()
    __v = cerberus.Validator()

    def __init__(self, propiedades = None, parent = None):
        super(ModeloProveedores, self).__init__()

        self.__propiedades = [
        'id', 'nombre', 'servicios',
        'calle', 'altura', 'localidad',
        'telefono', 'celular',
        'email', 'cuit', 'razon_social',
        'cbu', 'banco', 'cuenta',
        'comision', 'responsable',
        'forma_pago', 'notas'
        ]

        self.__propiedades = self.validarPropiedades(propiedades)
        self.__proveedor = { }
        self.__listaProveedores = []


    def verListaProveedores(self):
        self.__listaProveedores = self.__querier.traerElementos(
            campos = self.__propiedades,
            tabla = 'proveedores')
        if self.__listaProveedores:
            self.layoutChanged.emit()
            return True
        return False

    def verDetallesProveedor(self, proveedor = QtCore.QModelIndex()):
        proveedor = self.__listaProveedores[proveedor.row()]
        idProveedor = proveedor[0]

        respuesta = self.__querier.traerElementos(
            condiciones = [('id', '=', idProveedor)],
            tabla = 'proveedores',
            limite = 1
        )

        proveedor = list(respuesta[0])
        print(proveedor)

        self.__proveedor = proveedor
        return self.__proveedor

    def guardarProveedor(self, proveedor):
        respuesta = self.__querier.traerElementos(
            campos = ['id'],
            condiciones = [('id', '=', proveedor['id'])],
            tabla = 'proveedores',
            limite = 1
            )
        print(respuesta)
        if respuesta:
            self.__querier.actualizarElemento('proveedores', proveedor, [('id', '=', proveedor['id'])])
        else:
            self.__querier.insertarElemento('proveedores', proveedor)

        if not self.__v.validate(proveedor, esquemaProveedor):
            errors = self.__v.document_error_tree
            for propiedad in esquemaProveedor:
                try:
                    print("Hay un error en el campo: " + errors[propiedad].errors[0].document_path[0])
                except:
                    pass
            return False
        return True

    def validarPropiedades(self, propiedades):
        if propiedades:
            prop = []
            for propiedad in propiedades:
                if propiedad in self.__propiedades:
                    prop.append(propiedad)
                else:
                    print("Propiedad '{}' es inválida, no se agregará".format(propiedad))
            return prop

    def rowCount(self, parent):
        return len(self.__listaProveedores)

    def columnCount(self, parent):
        if self.__listaProveedores:
            return len(self.__listaProveedores[0])
        else:
            return 0

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            row = index.row()
            column = index.column()
            value = self.__listaProveedores[row][column]
            return value

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                keys = list(self.__propiedades)
                return keys[section]
