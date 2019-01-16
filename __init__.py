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
"""

def classFactory(iface):
    # load Vgi2ShpConverter class from file Vgi2ShpConverter
    from Vgi2ShpConverter.vgi2shpconverter import Vgi2ShpConverter
    return Vgi2ShpConverter(iface)
