

#=============
#IMPORTACIONES
#=============

# Importamos el módulo sys que provee el acceso a funciones y objetos mantenidos por el intérprete.
import sys
# Importamos las herramientas de PyQT que vamos a utilizar
from PyQt5 import QtWidgets, uic, QtGui
# Importamos los elementos que se encuentran dentro del diseñador
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QStackedWidget
# Importamos los archivos .py necesarios de la carpeta: vistas
from vistas.detalles import detalle_afiliados
# Importamos el modulo uic necesario para levantar un archivo .ui
from PyQt5 import uic

from modelos.modelo_afiliado import ModeloAfiliado

#====================
#DEFINICION DE CLASES
#====================

#Creacion de la clase vistaLista
class ListaAfiliados(QtWidgets.QWidget):
	#Inicializacion del Objeto QWidget
	def __init__(self):
		QWidget.__init__(self)

		#Importamos la vista "listaAfiliados" y la alojamos dentro de la variable "vistaLista"
		self.listadoAfiliados = uic.loadUi("gui/listas/listaAfiliados.ui", self)

# Acá llamo la función __init__() que está en ModeloAfiliado, es la instanciación de la clase en un objeto
# Yo acá quiero los campos que voy a mostrar nomás
		self.model = ModeloAfiliado(
			propiedades = ['legajo', 'apellido', 'nombre', 'dni', 'tipo_afiliado', 'calle', 'altura', 'localidad', 'telefono_particular', 'lugar_trabajo','fecha_ingreso',])

		#variables que alojan las clases que se encuentran dentro del archivo .py. (nombredelArchivo.nombredelaClase)
		self.widgetdelafiliado = detalle_afiliados.DetalleAfiliados()

		# Asignamos el modelo de tabla a la tabla propiamente dicha
		self.tbl_articulos.setModel(self.model)

		#Tomamos los eventos de los botones que se encuentran dentro del archivo .ui y llamamos a las FUNCIONES
		self.listadoAfiliados.btn_nuevo.clicked.connect(self.mostrarDetalleAfiliado)

		self.tbl_articulos.doubleClicked.connect(self.mostrarDetalleAfiliado)
		self.ln_buscar.returnPressed.connect(self.buscarAfiliados)

	#===========================
	#DEFINICION DE LAS FUNCIONES
	#===========================

	def showEvent(self, event):
		self.model.verListaAfiliados()
		# Acá llamo la función, se supone que se ejecuta cada vez que
		# se muestra en pantalla la vista que contiene la tabla 'afiliados'

	def mostrarDetalleAfiliado(self, afiliado):
		if afiliado:
			afiliado = self.model.verDetallesAfiliado(afiliado)
			self.widgetdelafiliado.setAfiliado(afiliado)
		self.widgetdelafiliado.show()

	def buscarAfiliados(self):
		busqueda = self.ln_buscar.text()
		condiciones = []
		try:
			busqueda = "'%{}%' OR dni LIKE '%{}%'".format(busqueda, busqueda)
			condiciones = [('legajo', 'LIKE', busqueda)]
		except:
			busqueda = "'%{}%' OR apellido LIKE '%{}%'".format(busqueda, busqueda)
			condiciones = [('nombre', "LIKE", busqueda)]

		self.model.verListaAfiliados(condiciones)
