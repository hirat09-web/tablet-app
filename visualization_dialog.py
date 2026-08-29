# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QWidget,
    QHBoxLayout
)

from PyQt5.QtGui import (
    QFont,
    QColor,
    QPixmap
)

from qgis.PyQt.QtWidgets import QAbstractItemView

from qgis.utils import iface

from qgis.core import (
    Qgis,
    QgsProject,
    QgsRasterLayer,
    QgsVectorLayer,
    QgsLineSymbol,
    QgsFillSymbol,
    QgsSingleSymbolRenderer,
    QgsPalLayerSettings,
    QgsTextFormat,
    QgsVectorLayerSimpleLabeling
)

import os
import tempfile
import processing

from .visualization_dialog_ui import Ui_VisualizationDialog


class VisualizationDialog(QDialog, Ui_VisualizationDialog):

    VECTOR_LAYERS = [
        "Land cover",
        "Land cover change",
        "Deforestation",
        "Recovery potential",
        "Burning area"
    ]

    RASTER_LAYERS = [
        "Forest carbon stock",
        "Forest degradation",
        "Fire risk",
        "Water Resources"
    ]

    def __init__(
            self,
            selected_district_name=None,
            selected_province_name=None,
            parent=None
    ):

        super().__init__(parent)

        self.setupUi(self)

        self.selected_district_name = selected_district_name
        self.selected_province_name = selected_province_name

        # ---------------------------------------------------
        # ListWidget 複数選択
        # ---------------------------------------------------
        self.lstMap.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        self.lstDisplay.setSelectionMode(
            QAbstractItemView.ExtendedSelection
        )

        # ---------------------------------------------------
        # Background
        # ---------------------------------------------------
        self.comboBackground.addItems([
            "",
            "OpenStreetMap",
            "ESRI Satellite"
        ])

        self.comboBackground.currentTextChanged.connect(
            self.load_basemap
        )

        # ---------------------------------------------------
        # CheckBox Signals
        # ---------------------------------------------------
        self.chkRoad.stateChanged.connect(
            self.toggle_roads_layer
        )

        self.chkWatershed2km2.stateChanged.connect(
            self.toggle_watershed_2km_layer
        )

        self.chkWatershed10km2.stateChanged.connect(
            self.toggle_watershed_10km_layer
        )

        self.checkPlaceName.stateChanged.connect(
            self.toggle_place_name_layer
        )

        self.chkDEM.stateChanged.connect(
            self.toggle_dem_layer
        )

        self.chkContour.stateChanged.connect(
            self.toggle_dem_layer
        )

        self.chkRiver.stateChanged.connect(
            self.toggle_river_layer
        )

        self.chkRiverName.stateChanged.connect(
            self.toggle_river_labels
        )

        # ---------------------------------------------------
        # DEM Transparency
        # ---------------------------------------------------
        self.dem_layer = None

        self.transparencySlider.setMinimum(0)
        self.transparencySlider.setMaximum(100)
        self.transparencySlider.setValue(100)

        self.transparencySlider.valueChanged.connect(
            self.change_dem_opacity
        )

        # ---------------------------------------------------
        # Map Items
        # ---------------------------------------------------
        self.map_items = [
            "Land cover",
            "Land cover change",
            "Forest carbon stock",
            "Deforestation",
            "Forest degradation",
            "Recovery potential",
            "Burning area",
            "Fire risk",
            "Water Resources"
        ]

        self.populate_lstMap()

        # ---------------------------------------------------
        # Buttons
        # ---------------------------------------------------
        self.psbRight.clicked.connect(
            self.move_right
        )

        self.psbLeft.clicked.connect(
            self.move_left
        )

        self.psbUpper.clicked.connect(
            self.move_up
        )

        self.psbLower.clicked.connect(
            self.move_down
        )

        self.btnShowLayers.clicked.connect(
            self.load_selected_layers
        )

        # ---------------------------------------------------
        # Initial Display
        # ---------------------------------------------------
        self.load_district_boundaries()

    # =======================================================
    # Utility
    # =======================================================
    def refresh_canvas(self):

        iface.mapCanvas().refresh()

    def raise_overlay_layers(self):

        root = QgsProject.instance().layerTreeRoot()

        overlay_names = [
            "District Boundaries",
            "Watershed 2km2",
            "Watershed 10km2",
            "River",
            "Contour",
            "Place Name"
        ]

        for layer_name in overlay_names:

            layers = QgsProject.instance().mapLayersByName(
                layer_name
            )

            if not layers:
                continue

            layer = layers[0]

            node = root.findLayer(layer.id())

            if node:

                cloned = node.clone()

                root.insertChildNode(
                    0,
                    cloned
                )

                parent = node.parent()

                parent.removeChildNode(node)

    # =======================================================
    # Background
    # =======================================================
    def add_xyz_layer(self, name, url):

        for layer in QgsProject.instance().mapLayersByName(name):
            QgsProject.instance().removeMapLayer(layer.id())

        uri = f"type=xyz&url={url}"

        layer = QgsRasterLayer(
            uri,
            name,
            "wms"
        )

        if not layer.isValid():
            return

        QgsProject.instance().addMapLayer(layer)

        self.raise_overlay_layers()

        iface.setActiveLayer(layer)

        self.refresh_canvas()

    def load_basemap(self, text):

        for layer_name in [
            "OpenStreetMap",
            "ESRI Satellite"
        ]:

            for layer in QgsProject.instance().mapLayersByName(
                    layer_name
            ):

                QgsProject.instance().removeMapLayer(
                    layer.id()
                )

        if text == "OpenStreetMap":

            self.add_xyz_layer(
                "OpenStreetMap",
                "https://tile.openstreetmap.org/{z}/{x}/{y}.png"
            )

        elif text == "ESRI Satellite":

            self.add_xyz_layer(
                "ESRI Satellite",
                "https://services.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
            )

    # =======================================================
    # District Boundary
    # =======================================================
    def load_district_boundaries(self):

        for layer in QgsProject.instance().mapLayersByName(
                "District Boundaries"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        shp_path = os.path.join(
            os.path.dirname(__file__),
            "data",
            "shapefiles",
            "district_boundaries.shp"
        )

        layer = QgsVectorLayer(
            shp_path,
            "District Boundaries",
            "ogr"
        )

        if not layer.isValid():
            return

        if self.selected_district_name:

            layer.setSubsetString(
                f'"district" = \'{self.selected_district_name}\''
            )

        symbol = QgsFillSymbol.createSimple({
            'color': '0,0,0,0',
            'outline_color': 'red',
            'outline_width': '0.6'
        })

        layer.setRenderer(
            QgsSingleSymbolRenderer(symbol)
        )

        layer.setReadOnly(True)

        QgsProject.instance().addMapLayer(
            layer,
            addToLegend=True
        )

        self.refresh_canvas()

    # =======================================================
    # Roads
    # =======================================================
    def toggle_roads_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "OSM Roads"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if self.chkRoad.isChecked():

            gpkg_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "roads",
                "hotosm_per_roads_lines_gpkg.gpkg"
            )

            layer = QgsVectorLayer(
                gpkg_path,
                "OSM Roads",
                "ogr"
            )

            if layer.isValid():

                symbol = QgsLineSymbol.createSimple({
                    'color': 'white',
                    'width': '0.8'
                })

                layer.setRenderer(
                    QgsSingleSymbolRenderer(symbol)
                )

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # Watershed 2km2
    # =======================================================
    def toggle_watershed_2km_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "Watershed 2km2"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if (
                self.chkWatershed2km2.isChecked()
                and
                self.selected_district_name
        ):

            district = self.selected_district_name

            gpkg_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "watershed",
                f"basin_{district}_2km2.gpkg"
            )

            layer = QgsVectorLayer(
                gpkg_path,
                "Watershed 2km2",
                "ogr"
            )

            if layer.isValid():

                symbol = QgsFillSymbol.createSimple({
                    'color': '0,0,0,0',
                    'outline_color': 'cyan',
                    'outline_width': '0.5',
                    'outline_style': 'dash'
                })

                layer.setRenderer(
                    QgsSingleSymbolRenderer(symbol)
                )

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # Watershed 10km2
    # =======================================================
    def toggle_watershed_10km_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "Watershed 10km2"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if (
                self.chkWatershed10km2.isChecked()
                and
                self.selected_district_name
        ):

            district = self.selected_district_name

            gpkg_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "watershed",
                f"basin_{district}_10km2.gpkg"
            )

            layer = QgsVectorLayer(
                gpkg_path,
                "Watershed 10km2",
                "ogr"
            )

            if layer.isValid():

                symbol = QgsFillSymbol.createSimple({
                    'color': '0,0,0,0',
                    'outline_color': 'yellow',
                    'outline_width': '0.7',
                    'outline_style': 'solid'
                })

                layer.setRenderer(
                    QgsSingleSymbolRenderer(symbol)
                )

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # Place Name
    # =======================================================
    def toggle_place_name_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "Place Name"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if self.checkPlaceName.isChecked():

            shp_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "placename",
                "Place_name.shp"
            )

            layer = QgsVectorLayer(
                shp_path,
                "Place Name",
                "ogr"
            )

            if layer.isValid():

                settings = QgsPalLayerSettings()

                settings.fieldName = "name"
                settings.enabled = True

                text_format = QgsTextFormat()

                text_format.setFont(
                    QFont("Arial", 10)
                )

                text_format.setSize(10)

                text_format.setColor(
                    QColor("black")
                )

                settings.setFormat(text_format)

                layer.setLabeling(
                    QgsVectorLayerSimpleLabeling(settings)
                )

                layer.setLabelsEnabled(True)

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # DEM
    # =======================================================
    def toggle_dem_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "DEM"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if (
                self.chkDEM.isChecked()
                and
                self.selected_province_name
        ):

            dem_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "dem",
                f"DEM_{self.selected_province_name}.tif"
            )

            layer = QgsRasterLayer(
                dem_path,
                "DEM"
            )

            self.dem_layer = layer

            if layer.isValid():

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                if self.chkContour.isChecked():

                    self.add_contour_layer(layer)

        self.refresh_canvas()

    def change_dem_opacity(self, value):

        if self.dem_layer:

            self.dem_layer.renderer().setOpacity(
                value / 100.0
            )

            self.dem_layer.triggerRepaint()

    def add_contour_layer(self, dem_layer):

        contour_output_path = os.path.join(
            tempfile.gettempdir(),
            'contour.shp'
        )

        processing.run(
            "gdal:contour",
            {
                'INPUT': dem_layer.source(),
                'BAND': 1,
                'INTERVAL': 200,
                'FIELD_NAME': 'ELEV',
                'CREATE_3D': False,
                'IGNORE_NODATA': False,
                'NODATA': None,
                'OFFSET': 0,
                'OUTPUT': contour_output_path
            }
        )

        layer = QgsVectorLayer(
            contour_output_path,
            "Contour",
            "ogr"
        )

        if layer.isValid():

            QgsProject.instance().addMapLayer(
                layer,
                addToLegend=True
            )

        self.refresh_canvas()

    # =======================================================
    # River
    # =======================================================
    def toggle_river_layer(self):

        for layer in QgsProject.instance().mapLayersByName(
                "River"
        ):

            QgsProject.instance().removeMapLayer(
                layer.id()
            )

        if (
                self.chkRiver.isChecked()
                and
                self.selected_district_name
        ):

            shp_path = os.path.join(
                os.path.dirname(__file__),
                "data",
                "river",
                f"{self.selected_district_name.replace(' ', '_')}_River.shp"
            )

            layer = QgsVectorLayer(
                shp_path,
                "River",
                "ogr"
            )

            if layer.isValid():

                symbol = QgsLineSymbol.createSimple({
                    'color': 'blue',
                    'width': '0.6'
                })

                layer.setRenderer(
                    QgsSingleSymbolRenderer(symbol)
                )

                QgsProject.instance().addMapLayer(
                    layer,
                    addToLegend=True
                )

                if self.chkRiverName.isChecked():

                    self.toggle_river_labels()

                self.raise_overlay_layers()

        self.refresh_canvas()

    def toggle_river_labels(self):

        river_layers = QgsProject.instance().mapLayersByName(
            "River"
        )

        if not river_layers:
            return

        river_layer = river_layers[0]

        if self.chkRiverName.isChecked():

            settings = QgsPalLayerSettings()

            settings.fieldName = "NOM"

            settings.enabled = True

            text_format = QgsTextFormat()

            text_format.setFont(
                QFont("Arial", 12)
            )

            text_format.setSize(12)

            text_format.setColor(
                QColor("black")
            )

            from qgis.core import QgsTextBufferSettings

            buffer = QgsTextBufferSettings()

            buffer.setEnabled(True)

            buffer.setSize(1)

            buffer.setColor(
                QColor("white")
            )

            text_format.setBuffer(buffer)

            settings.setFormat(text_format)

            river_layer.setLabeling(
                QgsVectorLayerSimpleLabeling(settings)
            )

            river_layer.setLabelsEnabled(True)

        else:

            river_layer.setLabelsEnabled(False)

        river_layer.triggerRepaint()

        iface.layerTreeView().refreshLayerSymbology(
            river_layer.id()
        )

        self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # Map List
    # =======================================================
    def populate_lstMap(self):

        self.lstMap.clear()

        for item in self.map_items:

            self.lstMap.addItem(item)

    def move_right(self):

        selected_items = self.lstMap.selectedItems()

        for item in selected_items:

            text = item.text()

            self.lstDisplay.addItem(text)

            row = self.lstMap.row(item)

            self.lstMap.takeItem(row)

    def move_left(self):

        selected_items = self.lstDisplay.selectedItems()

        for item in selected_items:

            text = item.text()

            self.lstMap.addItem(text)

            row = self.lstDisplay.row(item)

            self.lstDisplay.takeItem(row)

    def move_up(self):

        current_row = self.lstDisplay.currentRow()

        if current_row <= 0:
            return

        item = self.lstDisplay.takeItem(current_row)

        self.lstDisplay.insertItem(
            current_row - 1,
            item
        )

        self.lstDisplay.setCurrentItem(item)

    def move_down(self):

        current_row = self.lstDisplay.currentRow()

        if current_row < 0:
            return

        if current_row >= self.lstDisplay.count() - 1:
            return

        item = self.lstDisplay.takeItem(current_row)

        self.lstDisplay.insertItem(
            current_row + 1,
            item
        )

        self.lstDisplay.setCurrentItem(item)

    # =======================================================
    # Load Selected Layers
    # =======================================================
    def load_selected_layers(self):

        district = self.selected_district_name

        if not district:
            return

        base_path = os.path.join(
            os.path.dirname(__file__),
            "data"
        )

        # 逆順で追加（上にしたいものを上へ）
        for i in reversed(range(self.lstDisplay.count())):

            item_name = self.lstDisplay.item(i).text()

            file_name = (
                f"{item_name.replace(' ', '_')}_{district}"
            )

            layer_folder = os.path.join(
                base_path,
                item_name.replace(' ', '_')
            )

            # ---------------------------------------------------
            # Vector
            # ---------------------------------------------------
            if item_name in self.VECTOR_LAYERS:

                layer_name = (
                    item_name.replace(' ', '_').lower()
                )

                file_name = (
                    f"{layer_name}_{district}"
                )

                file_path = os.path.join(
                    layer_folder,
                    file_name + ".gpkg"
                )

                for layer in QgsProject.instance().mapLayersByName(
                        item_name
                ):
                    QgsProject.instance().removeMapLayer(
                        layer.id()
                    )

                if os.path.exists(file_path):

                    uri = (
                        f"{file_path}"
                        f"|layername={layer_name}"
                    )

                    layer = QgsVectorLayer(
                        uri,
                        item_name,
                        "ogr"
                    )

                    if layer.isValid():

                        # ---------------------------------
                        # QML Style
                        # ---------------------------------
                        qml_path = os.path.join(
                            os.path.dirname(__file__),
                            "styles",
                            "Landcover.qml"
                        )

                        if os.path.exists(qml_path):
                            layer.loadNamedStyle(qml_path)

                            layer.triggerRepaint()

                        QgsProject.instance().addMapLayer(
                            layer,
                            addToLegend=True
                        )

            # ---------------------------------------------------
            # Raster
            # ---------------------------------------------------
            elif item_name in self.RASTER_LAYERS:

                file_path = os.path.join(
                    layer_folder,
                    file_name + ".tif"
                )

                for layer in QgsProject.instance().mapLayersByName(
                        item_name
                ):

                    QgsProject.instance().removeMapLayer(
                        layer.id()
                    )

                if os.path.exists(file_path):

                    layer = QgsRasterLayer(
                        file_path,
                        item_name
                    )

                    if layer.isValid():

                        QgsProject.instance().addMapLayer(
                            layer,
                            addToLegend=True
                        )

        self.raise_overlay_layers()

        self.refresh_canvas()

    # =======================================================
    # Close Event
    # =======================================================
    def closeEvent(self, event):

        layers_to_remove = [
            "OpenStreetMap",
            "ESRI Satellite",
            "District Boundaries",
            "OSM Roads",
            "Watershed 2km2",
            "Watershed 10km2",
            "Place Name",
            "DEM",
            "Contour",
            "River"
        ]

        for i in range(self.lstDisplay.count()):

            layers_to_remove.append(
                self.lstDisplay.item(i).text()
            )

        for layer_name in layers_to_remove:

            layers = QgsProject.instance().mapLayersByName(
                layer_name
            )

            for layer in layers:

                QgsProject.instance().removeMapLayer(
                    layer.id()
                )

        self.refresh_canvas()

        event.accept()