# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Vgi2ShpConverter
                                 A QGIS plugin
 Vgi2Shp Converter, for Slovak users only
                             -------------------
        begin                : 2014-06-20
        copyright            : (C) 2014 by Ing.Olejar Milan, State Nature Conservancy, Slovakia
        email                : milan.olejar@sopsr.sk
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""

def classFactory(iface):
    # load Vgi2ShpConverter class from file Vgi2ShpConverter
    from vgi2shpconverter import Vgi2ShpConverter
    return Vgi2ShpConverter(iface)
