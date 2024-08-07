# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ActualitzaGTC
                                 A QGIS plugin
 ActualitzaGTC
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-11-14
        git sha              : $Format:%H$
        copyright            : (C) 2018 by CCU
        email                : jlopez@tecnocampus.cat
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import os.path
from os.path import expanduser

import psycopg2
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtWidgets import (QAction, QApplication, QInputDialog, QLineEdit,
                             QMessageBox, QToolBar)
from qgis.core import (QgsDataSourceUri, QgsLayerTreeLayer, QgsProject,
                       QgsRenderContext, QgsVectorLayer)
from qgis.utils import iface

# Import the code for the dialog
from .ActualitzaGTC_dialog import ActualitzaGTCDialog
# Initialize Qt resources from file resources.py
from .resources import *

"""
Variables globals per a la connexio
i per guardar el color dels botons
"""
Versio_modul="V_Q3.240701"
micolorArea = None
micolor = None
nomBD1=""
contra1=""
host1=""
port1=""
usuari1=""
schema=""
entitat_poi=""
Fitxer=""
Path_Inicial=expanduser("~")
cur=None
conn=None
progress=None
aux=False
itemSel=None
lbl_Cost = ''

class ActualitzaGTC:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ActualitzaGTC_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        '''
        Connexio dels botons amb les funcions que han de realitzar
        '''        
        self.dlg = ActualitzaGTCDialog()
        self.dlg.bt_sortir.clicked.connect(self.on_click_Sortir)
        self.dlg.bt_inici.clicked.connect(self.on_click_Inici)
        self.dlg.bt_carregar.clicked.connect(self.on_click_Carregar)
        self.dlg.comboConnexio.currentIndexChanged.connect(self.on_Change_ComboConn)
        
        # Declare instance attributes
        self.actions = []
        self.menu = self.tr('&CCU')
        # TODO: We are going to let the user set this up in a future iteration
        #self.toolbar = self.iface.addToolBar('CCU')
        #self.toolbar.setObjectName('Actualitza GTC')
        trobat=False
        for x in iface.mainWindow().findChildren(QToolBar,'CCU'): 
            self.toolbar = x
            trobat=True
        
        if not trobat:
            self.toolbar = self.iface.addToolBar('CCU')
            self.toolbar.setObjectName('CCU')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ActualitzaGTC', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/ActualitzaGTC/icon.png'
        self.add_action(
            icon_path,
            text=self.tr('Actualitza GTC'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr('&CCU'),
                action)
            #self.iface.removeToolBarIcon(action)
            self.toolbar.removeAction(action)


    def on_click_Sortir(self):
        '''
        Tanca la finestra del plugin 
        '''
        self.estatInicial()
        self.dlg.close()

    def getConnections(self):
        """Aquesta funcio retorna les connexions que estan guardades en el projecte."""
        s = QSettings() 
        s.beginGroup("PostgreSQL/connections")
        currentConnections = s.childGroups()
        s.endGroup()
        return currentConnections
    
    def populateComboBox(self,combo,list,predef,sort):
        """Procediment per omplir el combo especificat amb la llista suministrada"""
        combo.blockSignals (True)
        combo.clear()
        model=QStandardItemModel(combo)
        predefInList = None
        for elem in list:
            try:
                item = QStandardItem(str(elem))
            except TypeError:
                item = QStandardItem(str(elem))
            model.appendRow(item)
            if elem == predef:
                predefInList = elem
        if sort:
            model.sort(0)
        combo.setModel(model)
        if predef != "":
            if predefInList:
                combo.setCurrentIndex(combo.findText(predefInList))
            else:
                combo.insertItem(0,predef)
                combo.setCurrentIndex(0)
        combo.blockSignals (False)
        
    def estatInicial(self):
        '''
        @param self:
        Resteja tots els valors per defecte del plugin: estat inicial.
        '''
        global aux
        global Versio_modul
        aux = False
        self.barraEstat_noConnectat()
        self.dlg.versio.setText(Versio_modul)
        self.dlg.text_info.setText('')
        
    def on_click_CarregarAux(self,label):
        qid = QInputDialog()
        title = "Afegeix la paraula clau"
        mode = QLineEdit.Normal
        default = ""
        text, ok = QInputDialog.getText(qid, title, label, mode, default)
        return text

    def controlErrorsCarrega(self):
        global aux
        errors = []
        if not aux:
            errors.append("No hi ha la connexió.")

        return errors

        
    def on_click_Carregar(self):
        global cur
        global conn
        global nomBD1
        global contra1
        global host1
        global port1
        global usuari1

        llistaErrors = self.controlErrorsCarrega()
        if len(llistaErrors) != 0:
            llista = "Llista d'errors:\n\n"
            for i in range(0, len(llistaErrors)):
                llista += ("- " + llistaErrors[i] + '\n')
            QMessageBox.information(None, "Error", llista)
            return
        
        select = 'select * from "GTC_Update"."ControlActualitzacio";'
        try:
            cur.execute(select)
            vec = cur.fetchall()
            conn.commit()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR select Control")

            
        if (vec[0][0]):
            label = "Actualment s'està modificant el GTC.\nIntrodueix la paraula clau per carregar la capa."
            val = self.on_click_CarregarAux(label)
            if val == '':
                return
            comprovarParaulaClau = vec[0][3]
            if (comprovarParaulaClau != val):
                QMessageBox.information(None, "Error", "La paraula clau no és la correcta.")
                return 
        else:
            label = "Actualment NO s'està modificant el GTC.\nIntrodueix la paraula clau per carregar la capa."
            val = self.on_click_CarregarAux(label)
            if val == '':
                return
            update = 'update "GTC_Update"."ControlActualitzacio" set "modificant" = true;\n'
            update += 'update "GTC_Update"."ControlActualitzacio" set "usuariModificador" = \''+ val +'\';\n'
            update += 'update "GTC_Update"."ControlActualitzacio" set "horaModificacio" = CURRENT_TIMESTAMP;' 
            try:
                cur.execute(update)
                conn.commit()
            except Exception as e:
                print (e.message, e.args)
                print ("ERROR update Control (modificant, paraula clau)")


            if (not vec[0][1]):
                create = 'drop table if exists "GTC_Update"."UpdateGTC";\n'
                create += 'create table "GTC_Update"."UpdateGTC" as (select * from "SegmentsXarxaCarrers" order by id);\n'
                create += 'ALTER TABLE "GTC_Update"."UpdateGTC" DROP COLUMN id;\n'
                create += 'ALTER TABLE "GTC_Update"."UpdateGTC" ADD COLUMN id serial;\n'
                create += 'ALTER TABLE "GTC_Update"."UpdateGTC" ADD PRIMARY KEY (id);\n'
                try:
                    cur.execute(create)
                    conn.commit()
                except Exception as e:
                    print ("ERROR create GTC per actualitzar")
                    print (e.message.encode('utf8','strict'), e.args.encode('utf8','strict'))
                

        select = 'select to_char("horaModificacio", \'DD/MM/YY HH24:MI\') from "GTC_Update"."ControlActualitzacio";'
        try:
            cur.execute(select)
            vec = cur.fetchall()
            conn.commit()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR select Control")
        self.dlg.text_info.setText("Data de l'inici de la modificació: " + vec[0][0])
        
        uri = QgsDataSourceUri()
        try:
            uri.setConnection(host1,port1,nomBD1,usuari1,contra1)
        except Exception as e:
            print (e.message, e.args)
            print ("Error a la connexió")
            
            
        sql_total = 'select * from "GTC_Update"."UpdateGTC" order by id'
        QApplication.processEvents()
        uri.setDataSource("GTC_Update","UpdateGTC","the_geom","","")
        QApplication.processEvents()
        
        '''
        #    13.2 Es prepara el titol de la capa que apareixerà a la llegenda
        '''
        titol="UpdateGTC"
        vlayer = QgsVectorLayer(uri.uri(False), titol, "postgres")
        QApplication.processEvents()
        
        if vlayer.isValid():
            symbols = vlayer.renderer().symbols(QgsRenderContext())
            symbol=symbols[0]
            '''S'afegeix el color a la nova entitat'''
            symbol.setColor(QColor.fromRgb(0,0,0))
            QgsProject.instance().addMapLayer(vlayer,False)
            root = QgsProject.instance().layerTreeRoot()
            myLayerNode=QgsLayerTreeLayer(vlayer)
            root.insertChildNode(0,myLayerNode)
            myLayerNode.setCustomProperty("showFeatureCount", False)
            QApplication.processEvents()
            ''''S'afegeix la capa a la pantalla'''
            iface.mapCanvas().refresh()
        else:
            print ("No s'ha carregat la capa")

    def controlErrorsValida(self):
        global aux
        errors = []
        if not aux:
            errors.append("No hi ha la connexió.")
        select = 'select * from "GTC_Update"."ControlActualitzacio";'
        try:
            cur.execute(select)
            vec = cur.fetchall()
            conn.commit()
        
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR select Control")
        if (not vec[0][1]) and (not vec[0][0]):
            errors.append("El graf no s'ha creat")

        return errors

    def on_click_Inici(self):
        llistaErrors = self.controlErrorsValida()
        if len(llistaErrors) != 0:
            llista = "Llista d'errors:\n\n"
            for i in range(0, len(llistaErrors)):
                llista += ("- " + llistaErrors[i] + '\n')
            QMessageBox.information(None, "Error", llista)
            return

        textBox = 'INICI DEL PROCÉS DE VALIDACIÓ:\n'
        textBox += 'Elminació dels vertex:'
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()
        conta_errors=0
        self.barraEstat_processant()
        drop = 'DROP TABLE IF EXISTS "GTC_Update"."UpdateGTC_vertices_pgr";'
        try:
            cur.execute(drop)
            conn.commit()
        except Exception as e:
            print ("ERROR drop vertexs GTC per actualitzar")
            self.barraEstat_connectat()
            print (e.message, e.args)
        textBox += '...OK\n'
        textBox += 'Creació d\'una nova topologia'
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()

        create = 'select pgr_createTopology(\'GTC_Update.UpdateGTC\', 0.001,clean:=true);'            
        try:
            cur.execute(create)
            vec = cur.fetchall()
            conn.commit()
            if vec[0][0] != 'OK':
                QMessageBox.information(None, "Error", "No s'ha creat la topologia correctament.")
                print(vec)
                return
        except Exception as e:
            self.barraEstat_connectat()
            print ("ERROR create vertexs GTC per actualitzar")
            print (e.message, e.args)

        textBox += '...OK\n'
        textBox += 'Comprovació de la nova topologia'
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()

        create = 'SELECT pgr_analyzeGraph(\'GTC_Update.UpdateGTC\', 0.001);'            
        try:
            cur.execute(create)
            vec = cur.fetchall()
            conn.commit()
            if vec[0][0] != 'OK':
                QMessageBox.information(None, "Error", "S'ha detectat un error a la topologia.")
                self.barraEstat_connectat()
                return
        except Exception as e:
            self.barraEstat_connectat()
            print ("ERROR create vertexs GTC per actualitzar")
            print (e.message, e.args)

        textBox += '...OK\n'
        textBox += 'Comprovació dels punts amb possibles errors: '
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()
            
        select = 'SELECT * FROM "GTC_Update"."UpdateGTC_vertices_pgr" WHERE chk = 1;'
        try:
            cur.execute(select)
            vec = cur.fetchall()
            conn.commit()
            if (len(vec)!=0):
                uri = QgsDataSourceUri()
                try:
                    uri.setConnection(host1,port1,nomBD1,usuari1,contra1)
                except:
                    print ("Error a la connexio")
                
                select = 'SELECT * FROM "GTC_Update"."UpdateGTC_vertices_pgr" WHERE chk = 1'
                QApplication.processEvents()
                uri.setDataSource("","("+select+")","the_geom","","id")
                QApplication.processEvents()
                
                '''
                #    13.2 Es prepara el titol de la capa que apareixerà a la llegenda
                '''
                titol="Nodes a revisar"
                vlayer = QgsVectorLayer(uri.uri(False), titol, "postgres")
                QApplication.processEvents()
                
                if vlayer.isValid():
                    symbols = vlayer.renderer().symbols(QgsRenderContext())
                    symbol=symbols[0]
                    '''S'afegeix el color a la nova entitat'''
                    symbol.setColor(QColor.fromRgb(255,0,0))
                    QgsProject.instance().addMapLayer(vlayer,False)
                    root = QgsProject.instance().layerTreeRoot()
                    myLayerNode=QgsLayerTreeLayer(vlayer)
                    root.insertChildNode(0,myLayerNode)
                    myLayerNode.setCustomProperty("showFeatureCount", False)
                    QApplication.processEvents()
                    ''''S'afegeix la capa a la pantalla'''
                    iface.mapCanvas().refresh()
                else:
                    print ("No s'ha carregat la capa de punts")
                self.barraEstat_connectat()
                QApplication.processEvents()
                textBox += 'S\'ha(n) detectat '+ str(len(vec)) + ' punt(s) amb possibles errades.\n'
                self.dlg.text_info.setText(textBox)
                self.MouText()
                QApplication.processEvents()
                return
        except Exception as e:
            self.barraEstat_connectat()
            print ("ERROR create vertexs GTC per actualitzar")
            print (e.message[0].decode('utf8'), e.args)
            return

        textBox += 'No s\'han detectat errades.\n'
        textBox += 'Detecció de trams aïllats: '
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()
        
        select = 'SELECT a.* FROM "GTC_Update"."UpdateGTC" a, "GTC_Update"."UpdateGTC_vertices_pgr" b, "GTC_Update"."UpdateGTC_vertices_pgr" c WHERE a.source=b.id AND b.cnt=1 AND a.target=c.id AND c.cnt=1;'
        try:
            cur.execute(select)
            vec = cur.fetchall()
            conn.commit()
            if (len(vec)!=0):
                uri = QgsDataSourceUri()
                try:
                    uri.setConnection(host1,port1,nomBD1,usuari1,contra1)
                except:
                    print ("Error a la connexio")
                
                select = 'SELECT a.* FROM "GTC_Update"."UpdateGTC" a, "GTC_Update"."UpdateGTC_vertices_pgr" b, "GTC_Update"."UpdateGTC_vertices_pgr" c WHERE a.source=b.id AND b.cnt=1 AND a.target=c.id AND c.cnt=1'
                QApplication.processEvents()
                uri.setDataSource("","("+select+")","the_geom","","id")
                QApplication.processEvents()
                
                '''
                #    13.2 Es prepara el titol de la capa que apareixerà a la llegenda
                '''
                titol="Trams sense connectivitat a revisar"
                vlayer = QgsVectorLayer(uri.uri(False), titol, "postgres")
                QApplication.processEvents()
                
                if vlayer.isValid():
                    symbols = vlayer.renderer().symbols(QgsRenderContext())
                    symbol=symbols[0]
                    '''S'afegeix el color a la nova entitat'''
                    symbol.setColor(QColor.fromRgb(255,0,0))
                    symbol.setWidth(1)
                    QgsProject.instance().addMapLayer(vlayer,False)
                    root = QgsProject.instance().layerTreeRoot()
                    myLayerNode=QgsLayerTreeLayer(vlayer)
                    root.insertChildNode(0,myLayerNode)
                    myLayerNode.setCustomProperty("showFeatureCount", False)
                    QApplication.processEvents()
                    ''''S'afegeix la capa a la pantalla'''
                    iface.mapCanvas().refresh()
                    #qgis.utils.iface.legendInterface().refreshLayerSymbology(vlayer)
                else:
                    print ("No s'ha carregat la capa de segments aïllats")
                self.barraEstat_connectat()
                QApplication.processEvents()
                textBox += 'S\'ha(n) detectat '+ str(len(vec)) + ' tram(s) aïllat(s).\n'
                self.dlg.text_info.setText(textBox)
                self.MouText()
                QApplication.processEvents()
                return
        except Exception as e:
            self.barraEstat_connectat()
            print ("ERROR Segments aillats")
            print (e.message, e.args)
            return
        
        textBox += 'No s\'han detectat segments aïllats.\n'
        self.dlg.text_info.setText(textBox)
        self.MouText()
        QApplication.processEvents()
            
        #==============================================
        #    1. LINIES AMB DOS PUNTS I CAMP SOURCE
        #==============================================

        self.barraEstat_processant()   
        sql_xarxa = 'select distinct(R.id) id,R.source Vertex, camp from (select S."the_geom",S."id",st_x(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_startpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr")) union ';
        sql_xarxa +='select S."the_geom",S."id",st_x(st_endpoint(S."the_geom")),S."target", \'T\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_endpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_startpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_endpoint(S."the_geom")),S."target",\'T\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_endpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )))R where (ST_NPoints(R.the_geom)=2 and R.camp=\'S\') order by R.id,R.source;';
        try:
            cur.execute(sql_xarxa)
            vec = cur.fetchall()
            conta_errors+=len(vec)
            for x in range (0,len(vec)):
                sql_1='select "source","target" from "GTC_Update"."UpdateGTC" where "id"='+str(vec[x][0])+';'
                cur.execute(sql_1)
                vec2 = cur.fetchall()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][1])+'),1) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, 0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][0])+'),0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, ST_NPoints(the_geom) - 1) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR SQL_XARXA")

        #==============================================
        #    2. LINIES AMB DOS PUNTS I CAMP TARGET
        #==============================================

        sql_xarxa = 'select distinct(R.id) id,R.source Vertex, camp from (select S."the_geom",S."id",st_x(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_startpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr")) union ';
        sql_xarxa +='select S."the_geom",S."id",st_x(st_endpoint(S."the_geom")),S."target", \'T\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_endpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_startpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_endpoint(S."the_geom")),S."target",\'T\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_endpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )))R where (ST_NPoints(R.the_geom)=2 and R.camp=\'T\') order by R.id,R.source;';
        try:
            cur.execute(sql_xarxa)
            vec = cur.fetchall()
            conta_errors+=len(vec)
            for x in range (0,len(vec)):
                sql_1='select "source","target" from "GTC_Update"."UpdateGTC" where "id"='+str(vec[x][0])+';'
                cur.execute(sql_1)
                vec2 = cur.fetchall()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][0])+'),0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, ST_NPoints(the_geom) - 1) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][1])+'),ST_NPoints(the_geom)) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, 0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR SQL_XARXA")
        
        #==============================================
        #    3. LINIES AMB MES DE DOS PUNTS I CAMP SOURCE
        #==============================================
        
        sql_xarxa = 'select distinct(R.id) id,R.source Vertex, camp from (select S."the_geom",S."id",st_x(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_startpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr")) union ';
        sql_xarxa +='select S."the_geom",S."id",st_x(st_endpoint(S."the_geom")),S."target", \'T\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_endpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_startpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union ';
        sql_xarxa +='select S."the_geom",S."id",st_y(st_endpoint(S."the_geom")),S."target",\'T\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_endpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )))R where (ST_NPoints(R.the_geom)<>2 and R.camp=\'S\') order by R.id,R.source;';
        try:
            cur.execute(sql_xarxa)
            vec = cur.fetchall()
            conta_errors+=len(vec)
            for x in range (0,len(vec)):
                sql_1='select "source","target" from "GTC_Update"."UpdateGTC" where "id"='+str(vec[x][0])+';'
                cur.execute(sql_1)
                vec2 = cur.fetchall()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, 0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][0])+'),0) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR SQL_XARXA")

        #==============================================
        #    4. LINIES AMB MES DE DOS PUNTS I CAMP TARGET
        #==============================================

        sql_xarxa = 'select distinct(R.id) id,R.source Vertex, camp from (select S."the_geom",S."id",st_x(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_startpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr")) union '
        sql_xarxa +='select S."the_geom",S."id",st_x(st_endpoint(S."the_geom")),S."target", \'T\' camp from "GTC_Update"."UpdateGTC" S where (st_x(st_endpoint(S."the_geom")) not in (select st_x("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union '
        sql_xarxa +='select S."the_geom",S."id",st_y(st_startpoint(S."the_geom")),S."source",\'S\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_startpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )) union '
        sql_xarxa +='select S."the_geom",S."id",st_y(st_endpoint(S."the_geom")),S."target",\'T\' camp from "GTC_Update"."UpdateGTC" S where (st_y(st_endpoint(S."the_geom")) not in (select st_y("GTC_Update"."UpdateGTC_vertices_pgr"."the_geom") from "GTC_Update"."UpdateGTC_vertices_pgr" )))R where (ST_NPoints(R.the_geom)<>2 and R.camp=\'T\') order by R.id,R.source;'
        try:
            cur.execute(sql_xarxa)
            vec = cur.fetchall()
            conta_errors+=len(vec)
            for x in range (0,len(vec)):
                sql_1='select "source","target" from "GTC_Update"."UpdateGTC" where "id"='+str(vec[x][0])+';'
                cur.execute(sql_1)
                vec2 = cur.fetchall()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_RemovePoint(the_geom, ST_NPoints(the_geom) - 1) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()
                update='UPDATE "GTC_Update"."UpdateGTC" SET the_geom = ST_AddPoint(the_geom, (select "the_geom" from "GTC_Update"."UpdateGTC_vertices_pgr" where id='+str(vec2[0][1])+'),ST_NPoints(the_geom)) WHERE "id"='+str(vec[x][0])+';'
                cur.execute(update)
                conn.commit()

        except Exception as e:
            print (e.message, e.args)
            print ("ERROR SQL_XARXA")
        
        if conta_errors != 0:
            llista = "Errors trobats i reparats:"
            llista += (' ' + str(conta_errors) + '\n')
        else:
            llista = "No s'han detectat errors\n"
        textBox += llista
        self.dlg.text_info.setText(textBox)
        self.MouText()
        
        update = 'UPDATE "GTC_Update"."ControlActualitzacio" set modificant = false, modificat=true, "horaModificacio" = NULL, "usuariModificador" = NULL;'

        try:
            cur.execute(update)
            conn.commit()
            html = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;"><div style=\"align:center\"><span style=\"background:#00FF00;font-size:14pt\">GRAF VALIDAT!<\span><\div></body></html>'
            self.dlg.text_info.insertHtml(html)
            self.MouText()
        except Exception as e:
            print (e.message, e.args)
            print ("ERROR update Control (modificant,modificat, paraula clau, timestamp")

        
        self.barraEstat_connectat()
        
        
        
    def on_Change_ComboConn(self):
        """
        En el moment en que es modifica la opcio escollida 
        del combo o desplegable de les connexions,
        automàticament comprova si es pot establir
        connexió amb la bbdd seleccionada.
        """
        global aux
        global nomBD1
        global contra1
        global host1
        global port1
        global usuari1
        global schema
        global cur
        global conn
        s = QSettings()
        select = 'Selecciona connexió'
        nom_conn=self.dlg.comboConnexio.currentText()
        if nom_conn != select:
            aux = True
            s.beginGroup("PostgreSQL/connections/"+nom_conn)
            currentKeys = s.childKeys()
            
            nomBD1 = s.value("database", "" )
            contra1 = s.value("password", "" )
            host1 = s.value("host", "" )
            port1 = s.value("port", "" )
            usuari1 = s.value("username", "" )
            schema= 'public'
            
            self.barraEstat_connectant()
            self.dlg.lblEstatConn.setAutoFillBackground(True)
            QApplication.processEvents()

            #Connexio
            nomBD = nomBD1.encode('ascii','ignore')
            usuari = usuari1.encode('ascii','ignore')
            servidor = host1.encode('ascii','ignore')     
            contrasenya = contra1.encode('ascii','ignore')
            try:
                estructura = "dbname='"+ nomBD.decode("utf-8") + "' user='" + usuari.decode("utf-8") +"' host='" + servidor.decode("utf-8") +"' password='" + contrasenya.decode("utf-8") + "'"# schema='"+schema+"'"
                conn = psycopg2.connect(estructura)
                self.barraEstat_connectat()
                cur = conn.cursor()
                
            except:
                self.dlg.lblEstatConn.setStyleSheet('border:1px solid #000000; background-color: #ff7f7f')
                self.dlg.lblEstatConn.setText('Error: Hi ha algun camp erroni.')
                print ("I am unable to connect to the database")
        else:
            aux = False
            self.barraEstat_noConnectat()

    def MouText(self):
        newCursor=QTextCursor(self.dlg.text_info.document())
        newCursor.movePosition(QTextCursor.End)
        self.dlg.text_info.setTextCursor(newCursor)
    
    def barraEstat_processant(self):
        '''Aquesta funció canvia l'aparença de la barra inferior a "Processant"'''
        self.dlg.lblEstatConn.setStyleSheet('border:1px solid #000000; background-color: rgb(255, 125, 155)')
        self.dlg.lblEstatConn.setText("Processant...")
        QApplication.processEvents()
        
    def barraEstat_noConnectat(self):
        '''Aquesta funció canvia l'aparença de la barra inferior a "No connectat"'''
        self.dlg.lblEstatConn.setStyleSheet('border:1px solid #000000; background-color: #FFFFFF')
        self.dlg.lblEstatConn.setText('No connectat')
        QApplication.processEvents()
        
    def barraEstat_connectat(self):
        '''Aquesta funció canvia l'aparença de la barra inferior a "Connectat"'''
        self.dlg.lblEstatConn.setStyleSheet('border:1px solid #000000; background-color: #7fff7f')
        self.dlg.lblEstatConn.setText('Connectat')
        QApplication.processEvents()
        
    def barraEstat_connectant(self):
        '''Aquesta funció canvia l'aparença de la barra inferior a "Connectant"'''
        self.dlg.lblEstatConn.setStyleSheet('border:1px solid #000000; background-color: #ffff7f')
        self.dlg.lblEstatConn.setText('Connectant...')
        QApplication.processEvents()


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.estatInicial()
        self.dlg.show()
        conn=self.getConnections()
        self.populateComboBox(self.dlg.comboConnexio ,conn,'Selecciona connexió',True)

        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass