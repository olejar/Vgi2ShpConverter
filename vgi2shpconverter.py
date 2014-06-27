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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from vgi2shpconverterdialog import Vgi2ShpConverterDialog
import os.path

# zaciatok
def divideline(dataline):
    global section, s_mark
    section = []
    s_mark = 0
    while dataline <> '':
        endsubsection = dataline.find(' ')
        if endsubsection <> -1:
            subsection = dataline[:endsubsection]
            section.append(subsection)
            dataline = dataline[endsubsection+1:].strip()
        else:
            subsection = dataline[:len(dataline)]
            section.append(subsection)
            dataline = ''
        if (section[0] == "&L" or section[0] == "P"):
            if subsection[:2] == 'S=':
                s_mark = 1

def calculate_max(x,y,calculate_object):
    if x < globals()["xmin_"+calculate_object]:
        globals()["xmin_"+calculate_object] = x
    if x > globals()["xmax_"+calculate_object]:
        globals()["xmax_"+calculate_object] = x
    if y < globals()["ymin_"+calculate_object]:
        globals()["ymin_"+calculate_object] = y
    if y > globals()["ymax_"+calculate_object]:
        globals()["ymax_"+calculate_object] = y

def codepage_conv(char):
    global char852
    char1250=ord(char)
    if char1250 == 129:
        char1250 = 252
    elif char1250 == 130:
        char1250 = 233
    elif char1250 == 132:
        char1250 = 228
    elif char1250 == 133:
        char1250 = 249
    elif char1250 == 138:
        char1250 = 213
    elif char1250 == 139:
        char1250 = 245
    elif char1250 == 142:
        char1250 = 196
    elif char1250 == 144:
        char1250 = 201
    elif char1250 == 145:
        char1250 = 197
    elif char1250 == 146:
        char1250 = 229
    elif char1250 == 147:
        char1250 = 244
    elif char1250 == 148:
        char1250 = 246
    elif char1250 == 149:
        char1250 = 188
    elif char1250 == 150:
        char1250 = 190
    elif char1250 == 153:
        char1250 = 214
    elif char1250 == 154:
        char1250 = 220
    elif char1250 == 155:
        char1250 = 141
    elif char1250 == 156:
        char1250 = 157
    elif char1250 == 159:
        char1250 = 232
    elif char1250 == 160:
        char1250 = 225
    elif char1250 == 161:
        char1250 = 237
    elif char1250 == 162:
        char1250 = 243
    elif char1250 == 163:
        char1250 = 250
    elif char1250 == 166:
        char1250 = 142
    elif char1250 == 167:
        char1250 = 158
    elif char1250 == 172:
        char1250 = 200
    elif char1250 == 181:
        char1250 = 193
    elif char1250 == 183:
        char1250 = 204
    elif char1250 == 210:
        char1250 = 207
    elif char1250 == 212:
        char1250 = 239
    elif char1250 == 213:
        char1250 = 210
    elif char1250 == 214:
        char1250 = 205
    elif char1250 == 216:
        char1250 = 236
    elif char1250 == 222:
        char1250 = 217
    elif char1250 == 224:
        char1250 = 211
    elif char1250 == 226:
        char1250 = 212
    elif char1250 == 229:
        char1250 = 242
    elif char1250 == 230:
        char1250 = 138
    elif char1250 == 231:
        char1250 = 154
    elif char1250 == 232:
        char1250 = 192
    elif char1250 == 233:
        char1250 = 218
    elif char1250 == 234:
        char1250 = 224
    elif char1250 == 235:
        char1250 = 219
    elif char1250 == 236:
        char1250 = 253
    elif char1250 == 237:
        char1250 = 221
    elif char1250 == 252:
        char1250 = 216
    elif char1250 == 253:
        char1250 = 248
    char852 = chr(char1250)  

def znacky_text(mark):
    global marktext
    if mark == "S1":
      marktext = "bod trigonometrickej siete"
    elif mark == "S2":
      marktext = "bod trigonometrickej siete - pod vodou"
    elif mark == "S3":
      marktext = "bod nivelačnej siete"
    elif mark == "S4":
      marktext = "bod technickej nivelácie"
    elif mark == "S5":
      marktext = "medzník na vlastnícko-užívateľskej hranici"
    elif mark == "S22":
      marktext = "slučka pri bode"
    elif mark == "S23":
      marktext = "slučka"
    elif mark == "S28":
      marktext = "chmeľnice"
    elif mark == "S29":
      marktext = "vinice"
    elif mark == "S30":
      marktext = "záhrada"
    elif mark == "S31":
      marktext = "ovocný sad"
    elif mark == "S32":
      marktext = "lúka"
    elif mark == "S34":
      marktext = "lesná pôda bez rozlíšenia"
    elif mark == "S40":
      marktext = "park, okrasná záhrada"
    elif mark == "S41":
      marktext = "cintorín"
    elif mark == "S42":
      marktext = "neplodná pôda"
    elif mark == "S44":
      marktext = "nehnuteľná kultúrna pamiatka"
    elif mark == "S45":
      marktext = "budova murovaná"
    elif mark == "S46":
      marktext = "budova drevená"
    elif mark == "S50":
      marktext = "kostol, kaplnka, kríž"
    elif mark == "S51":
      marktext = "kostol, kaplnka, kríž"
    elif mark == "S52":
      marktext = "synagóga"
    elif mark == "S53":
      marktext = "stred predmetu malého rozsahu"
    elif mark == "S54":
      marktext = "predmet malého rozsahu"
    elif mark == "S55":
      marktext = "predmet malého rozsahu bez rozlíšenia"
    elif mark == "S67":
      marktext = "most, lávka, priepustok"
    elif mark == "S68":
      marktext = "most, lávka, priepustok"
    elif mark == "S69":
      marktext = "most, lávka, priepustok"
    elif mark == "S70":
      marktext = "most, lávka, priepustok"
    elif mark == "S71":
      marktext = "most, lávka, priepustok"
    elif mark == "S72":
      marktext = "most, lávka, priepustok"
    elif mark == "S108":
      marktext = "kovový, betónový, drevený stožiar"
    elif mark == "S109":
      marktext = "priehradový stožiar"
    elif mark == "S111":
      marktext = "stožiar vysielacej veže"
    elif mark == "S201":
      marktext = "elektráreň, spínacia stanica"
    elif mark == "S226":
      marktext = "povrchová ťažba bez rozlíšenia"
    elif mark == "S231":
      marktext = "ústie štôly, úklonnej jamy"
    elif mark == "S238":
      marktext = "vodný tok"
    elif mark == "S239":
      marktext = "vodná nádrž"
    elif mark == "S240":
      marktext = "močiar"
    elif mark == "S247":
      marktext = "studňa, studnička"
    elif mark == "S253":
      marktext = "vodotrysk, fontána"
    elif mark == "S254":
      marktext = "malý vodotrysk, fontána"
    elif mark == "S260":
      marktext = "tansformátor"
    elif mark == "S431":
      marktext = "dvor, ostatná stavebná plocha"
    elif mark == "S432":
      marktext = "cesta, komunikácia"
    elif mark == "S433":
      marktext = "chodník, komunikácia pre peších"
    elif mark == "S434":
      marktext = "slučka zmenšená o tretinu"
    elif mark == "S435":
      marktext = "ostatná plocha"
    elif mark == "S436":
      marktext = "transformátor na stožiari"
    elif mark == "S479":
      marktext = "orná pôda"
    elif mark == "S488":
      marktext = "smerová šípka k parcelnému číslu"
    elif mark == "S489":
      marktext = "smerová šípka k parcelnému číslu"
    else:
      marktext = "bez popisu"
    marktext = marktext.decode("utf8").encode("cp1250")

def calculate_object():
    #KLADPAR
    global number_of_object_kladpar
    global xmin_kladpar, xmax_kladpar, ymin_kladpar, ymax_kladpar
    global kladparik, uovik
    #ZAPPAR
    global number_of_object_zappar
    global xmin_zappar, xmax_zappar, ymin_zappar, ymax_zappar
    global zapparik
    #LINIE
    global number_of_object_linie
    global xmin_linie, xmax_linie, ymin_linie, ymax_linie
    global linijik
    #ZUOB
    global number_of_object_zuob
    global xmin_zuob, xmax_zuob, ymin_zuob, ymax_zuob
    global zuobik
    #KATUZ
    global number_of_object_katuz
    global xmin_katuz, xmax_katuz, ymin_katuz, ymax_katuz
    global katuzik
    #TARCHY
    global number_of_object_tarchy
    global xmin_tarchy, xmax_tarchy, ymin_tarchy, ymax_tarchy
    global tarchik
    #POPIS
    global number_of_object_popis
    global xmin_popis, xmax_popis, ymin_popis, ymax_popis
    global popisik
    #ZNACKY
    global number_of_object_znacky
    global xmin_znacky, xmax_znacky, ymin_znacky, ymax_znacky
    global znacik
    #POLYGON
    global number_of_object_polygon
    global xmin_polygon, xmax_polygon, ymin_polygon, ymax_polygon
    global polygonik
    f = open(files,'r')
    kladparik = uovik = zapparik = linijik = zuobik = katuzik = tarchik = popisik = znacik = polygonik = 0
    global_object = ['kladpar','zappar','linie','zuob','katuz','tarchy','popis','znacky','polygon']
    for i_global_object in global_object:
        globals()["number_of_object_"+i_global_object] = 0
        globals()["xmin_"+i_global_object] = globals()["ymin_"+i_global_object] = 0
        globals()["xmax_"+i_global_object] = globals()["ymax_"+i_global_object] = -9999999
    #Calculate objects
    prechod = 1
    s = f.readline()
    divideline(s.strip())
    while section[0] <> '&K':
        if (section[1] == 'KLADPAR' or section[1] == 'UOV'):
            if section[1] == 'KLADPAR':
                if kladparik == 0:
                    kladparik = 1
            elif section[1] == 'UOV':
                if uovik == 0:
                    uovik = 1
            number_of_object_kladpar += 1
            s = f.readline()
            divideline(s.strip())
            while section[0] <> '&O':
                if section[0] == '&K':
                    break
                if (section[0] == '&L'):
                    if s_mark == 0:
                        x1 = -1 * float(section[2])
                        y1 = -1 * float(section[3])
                        calculate_max(x1,y1,'kladpar')
                #ZNACKY IN KLADPAR
                    elif s_mark == 1:
                        if znacik == 0:
                            znacik = 1
                        if (section[1] == 'P'):
                            number_of_object_znacky += 1
                            x1 = -1 * float(section[2])
                            y1 = -1 * float(section[3])
                            calculate_max(x1,y1,'znacky')
                elif (section[0] == 'P'):
                    if s_mark == 1:
                        if znacik == 0:
                            znacik = 1
                        number_of_object_znacky += 1
                        x1 = -1 * float(section[1])
                        y1 = -1 * float(section[2])
                        calculate_max(x1,y1,'znacky')
                #ZNACKY IN KLADPAR
                elif (section[0] == 'L'or section[0] == 'C'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'kladpar')
                elif (section[0] == 'R'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'kladpar')
                    s = f.readline()
                    divideline(s.strip())
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'kladpar')
                elif (section[0][:1] == 'N'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'kladpar')
                s = f.readline()
                divideline(s.strip())
            if (section[0] == '&K' or not (section[1][:5] == 'OBVOD:')):
                prechod = 0
        elif (section[1] == 'ZAPPAR' or section[1] == 'LINIE' or section[1] == 'ZUOB' or section[1] == 'KATUZ' or section[1] == 'TARCHY'):
            if section[1] == 'ZAPPAR':
                if zapparik == 0:
                    zapparik = 1
                number_of_object_zappar += 1
                objekt = 'zappar'
            elif section[1] == 'LINIE':
                if linijik == 0:
                    linijik = 1
                number_of_object_linie += 1
                objekt = 'linie'
            elif section[1] == 'ZUOB':
                if zuobik == 0:
                    zuobik = 1
                number_of_object_zuob += 1
                objekt = 'zuob'
            elif section[1] == 'KATUZ':
                if katuzik == 0:
                    katuzik = 1
                number_of_object_katuz += 1
                objekt = 'katuz'
            elif section[1] == 'TARCHY':
                if tarchik == 0:
                    tarchik = 1
                number_of_object_tarchy += 1
                objekt = 'tarchy'
            s = f.readline()
            divideline(s.strip())
            prvy = 1
            while section[0] <> '&O':
                if section[0] == '&K':
                    break
                if prvy == 0:
                    s = f.readline()
                    divideline(s.strip())
                if (section[0] == '&A'):
                    if prvy == 1:
                        s = f.readline()
                        divideline(s.strip())
                if (section[0] == '&L'):
                    if prvy == 1:
                        prvy = 0
                    x1 = -1 * float(section[2])
                    y1 = -1 * float(section[3])
                    calculate_max(x1,y1,objekt)
                elif (section[0] == 'L' or section[0] == 'C'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,objekt)
                elif (section[0] == 'R'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,objekt)
                    s = f.readline()
                    divideline(s.strip())
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,objekt)
                elif (section[0][:1] == 'N' or section[0] == 'P'):
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,objekt)
            if (section[0] == '&K' or not (section[1][:5] == 'OBVOD')):
                prechod = 0
        elif section[1] == 'POPIS':
            if popisik == 0:
                popisik = 1
            s = f.readline()
            divideline(s.strip())
            while section[0] <> '&O':
                if section[0] == '&K':
                    break
                elif (section[0] == '&T'):
                    number_of_object_popis += 1
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'popis')
                s = f.readline()
                divideline(s.strip())
                if prechod == 1:
                    prechod = 0
        elif section[1] == 'ZNACKY':
            if znacik == 0:
                znacik = 1
            s = f.readline()
            divideline(s.strip())
            while section[0] <> '&O':
                if section[0] == '&K':
                    break
                elif (section[0] == '&L' and section[1] == 'P' and s_mark == 1):
                    number_of_object_znacky += 1
                    x1 = -1 * float(section[2])
                    y1 = -1 * float(section[3])
                    calculate_max(x1,y1,'znacky')
                elif (section[0] == 'P' and s_mark == 1):
                    number_of_object_znacky += 1
                    x1 = -1 * float(section[1])
                    y1 = -1 * float(section[2])
                    calculate_max(x1,y1,'znacky')
                s = f.readline()
                divideline(s.strip())
                if prechod == 1:
                    prechod = 0
        elif section[1] == 'POLYGON':
            s = f.readline()
            divideline(s.strip())
            while section[0] <> '&O':
                if section[0] == '&K':
                    break
                elif (section[0] == '&L' and section[1] == 'P' and s_mark == 1):
                    if polygonik == 0:
                        polygonik = 1
                    number_of_object_polygon += 1
                    x1 = -1 * float(section[2])
                    y1 = -1 * float(section[3])
                    calculate_max(x1,y1,'polygon')
                s = f.readline()
                divideline(s.strip())
                if prechod == 1:
                    prechod = 0
        if prechod == 1:
            s = f.readline()
            divideline(s.strip())
        else:
            prechod = 1
    f.close()

def array(array_table):
    import struct
    for i_array_table in array_table:
        b32_42=struct.pack('>11s',i_array_table[0])
        f_dbf.write(b32_42)
        b43=struct.pack('>1s',i_array_table[1])
        f_dbf.write(b43)
        b44_47=struct.pack('>i',0)
        f_dbf.write(b44_47)
        b48_49=struct.pack('>2b',i_array_table[2],0)
        f_dbf.write(b48_49)
        b50_63=struct.pack('>14b',0,0,0,0,0,0,0,0,0,0,0,0,0,0)
        f_dbf.write(b50_63)

def header(header_object):
    global f_dbf
    import struct
    from time import localtime
    time = localtime()
    year = time[0] - 1900
    month = time[1]
    day = time[2]
    #SHP
    f=open(file_dir+file_name+'_'+header_object+'.shp','wb')
    #Main File Header
    #Integer, Big
    b00_27=struct.pack('>7i',9994,0,0,0,0,0,0)
    f.write(b00_27)
    if (header_object == 'kladpar' or header_object == 'uov'):
        #Integer, Little
        b28_35=struct.pack('<2i',1000,5)
        f.write(b28_35)
    elif (header_object == 'zappar' or header_object == 'linie' or header_object == 'zuob' or header_object == 'katuz' or header_object == 'tarchy'):
        #Integer, Little
        b28_35=struct.pack('<2i',1000,3)
        f.write(b28_35)
    elif (header_object == 'popis' or header_object == 'znacky' or header_object == 'polygon'):
        #Integer, Little
        b28_35=struct.pack('<2i',1000,1)
        f.write(b28_35)
    #Double, Little
    if (header_object == 'kladpar' or header_object == 'uov'):
        b36_99=struct.pack('<8d',xmin_kladpar,ymin_kladpar,xmax_kladpar,ymax_kladpar,0,0,0,0)
    else:
        b36_99=struct.pack('<8d',globals()["xmin_"+header_object],globals()["ymin_"+header_object],globals()["xmax_"+header_object],globals()["ymax_"+header_object],0,0,0,0)
    f.write(b36_99)
    f.close()
    #SHX
    f=open(file_dir+file_name+'_'+header_object+'.shx','wb')
    #Index File Header
    #Integer, Big
    if (header_object == 'kladpar' or header_object == 'uov'):
        b00_27=struct.pack('>7i',9994,0,0,0,0,0,(100+8*number_of_object_kladpar)/2)
    else:
        b00_27=struct.pack('>7i',9994,0,0,0,0,0,(100+8*globals()["number_of_object_"+header_object])/2)
    f.write(b00_27)
    f.write(b28_35)
    f.write(b36_99)
    f.close()
    #DBF
    f_dbf=open(file_dir+file_name+'_'+header_object+'.dbf','wb')
    #DBF File Header
    #Integer, Big
    b00_03=struct.pack('>4b',3,year,month,day)
    f_dbf.write(b00_03)
    #Integer, Little
    if (header_object == 'kladpar' or header_object == 'uov'):
        b04_11=struct.pack('<i2h',number_of_object_kladpar,289,67)
    elif header_object == 'zappar':
        b04_11=struct.pack('<i2h',number_of_object_zappar,97,17)
    elif header_object == 'linie':
        b04_11=struct.pack('<i2h',number_of_object_linie,161,120)
    elif header_object == 'zuob':
        b04_11=struct.pack('<i2h',number_of_object_zuob,161,120)
    elif header_object == 'katuz':
        b04_11=struct.pack('<i2h',number_of_object_katuz,161,123)
    elif header_object == 'tarchy':
        b04_11=struct.pack('<i2h',number_of_object_tarchy,97,17)
    elif header_object == 'popis':
        b04_11=struct.pack('<i2h',number_of_object_popis,129,117)
    elif header_object == 'znacky':
        b04_11=struct.pack('<i2h',number_of_object_znacky,161,122)
    elif header_object == 'polygon':
        b04_11=struct.pack('<i2h',number_of_object_polygon,193,130)
    f_dbf.write(b04_11)
    #Integer, Big
    b12_15=struct.pack('>4b',0,0,0,0)
    f_dbf.write(b12_15)
    b16_27=struct.pack('>12b',0,0,0,0,0,0,0,0,0,0,0,0)
    f_dbf.write(b16_27)
    b28_31=struct.pack('>4b',0,87,0,0)
    f_dbf.write(b28_31)
    #Field Descriptor Array Table
    array([['Objekt','C',6],['Vrstva','C',10]])
    if (header_object == 'kladpar' or header_object == 'uov'):
        array([['Parcis','C',12],['CPA','N',12],['Parcela','C',12],['KU','C',6],['DRP','C',2],['LV','C',6]])
    elif header_object == 'linie':
        array([['Linie','C',3],['Popis','C',100]])
    elif header_object == 'zuob':
        array([['ZUOB','C',3],['Obec','C',100]])
    elif header_object == 'katuz':
        array([['KU','C',6],['HKU','C',100]])
    elif header_object == 'popis':
        array([['Popis','C',100]])
    elif header_object == 'znacky':
        array([['Znacky','C',5],['Popis','C',100]])
    elif header_object == 'polygon':
        array([['Bod','C',8],['Znacky','C',5],['Popis','C',100]])
    #End DBF File Header
    b64=struct.pack('>b',13)
    f_dbf.write(b64)
    f_dbf.close()
    #PRJ
    f=open(file_dir+file_name+'_'+header_object+'.prj','wb')
    b00_15=struct.pack('>16s','PROJCS["S-JTSK_K')
    f.write(b00_15)
    b00_15=struct.pack('>16s','rovak_East_North')
    f.write(b00_15)
    b00_15=struct.pack('>16s','",GEOGCS["GCS_S_')
    f.write(b00_15)
    b00_15=struct.pack('>16s','JTSK",DATUM["D_S')
    f.write(b00_15)
    b00_15=struct.pack('>16s','_JTSK",SPHEROID[')
    f.write(b00_15)
    b00_15=struct.pack('>16s','"Bessel_1841",63')
    f.write(b00_15)
    b00_15=struct.pack('>16s','77397.155,299.15')
    f.write(b00_15)
    b00_15=struct.pack('>16s','28128]],PRIMEM["')
    f.write(b00_15)
    b00_15=struct.pack('>16s','Greenwich",0.0],')
    f.write(b00_15)
    b00_15=struct.pack('>16s','UNIT["Degree",0.')
    f.write(b00_15)
    b00_15=struct.pack('>16s','0174532925199433')
    f.write(b00_15)
    b00_15=struct.pack('>16s',']],PROJECTION["K')
    f.write(b00_15)
    b00_15=struct.pack('>16s','rovak"],PARAMETE')
    f.write(b00_15)
    b00_15=struct.pack('>16s','R["False_Easting')
    f.write(b00_15)
    b00_15=struct.pack('>16s','",0.0],PARAMETER')
    f.write(b00_15)
    b00_15=struct.pack('>16s','["False_Northing')
    f.write(b00_15)
    b00_15=struct.pack('>16s','",0.0],PARAMETER')
    f.write(b00_15)
    b00_15=struct.pack('>16s','["Pseudo_Standar')
    f.write(b00_15)
    b00_15=struct.pack('>16s','d_Parallel_1",78')
    f.write(b00_15)
    b00_15=struct.pack('>16s','.5],PARAMETER["S')
    f.write(b00_15)
    b00_15=struct.pack('>16s','cale_Factor",0.9')
    f.write(b00_15)
    b00_15=struct.pack('>16s','999],PARAMETER["')
    f.write(b00_15)
    b00_15=struct.pack('>16s','Azimuth",30.2881')
    f.write(b00_15)
    b00_15=struct.pack('>16s','3975277778],PARA')
    f.write(b00_15)
    b00_15=struct.pack('>16s','METER["Longitude')
    f.write(b00_15)
    b00_15=struct.pack('>16s','_Of_Center",24.8')
    f.write(b00_15)
    b00_15=struct.pack('>16s','3333333333333],P')
    f.write(b00_15)
    b00_15=struct.pack('>16s','ARAMETER["Latitu')
    f.write(b00_15)
    b00_15=struct.pack('>16s','de_Of_Center",49')
    f.write(b00_15)
    b00_15=struct.pack('>16s','.5],PARAMETER["X')
    f.write(b00_15)
    b00_15=struct.pack('>16s','_Scale",-1.0],PA')
    f.write(b00_15)
    b00_15=struct.pack('>16s','RAMETER["Y_Scale')
    f.write(b00_15)
    b00_15=struct.pack('>16s','",1.0],PARAMETER')
    f.write(b00_15)
    b00_15=struct.pack('>16s','["XY_Plane_Rotat')
    f.write(b00_15)
    b00_15=struct.pack('>16s','ion",90.0],UNIT[')
    f.write(b00_15)
    b00_15=struct.pack('>13s','"Meter",1.0]]')
    f.write(b00_15)
    f.close()

def record(record_object):
    import struct
    #SHP
    f=open(file_dir+file_name+'_'+record_object+'.shp','ab')
    #Main File Record Header
    if (record_object == 'kladpar' or record_object == 'uov'):
        #Integer, Big
        b00_07=struct.pack('>2i',record_kladpar,(44+number_of_parts*4+i_x_y_record*16)/2)
        f.write(b00_07)
        #Polygon Record Contents
        #Integer, Little
        b00_03=struct.pack('<i',5)
        f.write(b00_03)
    elif (record_object == 'zappar' or record_object == 'linie' or record_object == 'zuob' or record_object == 'katuz' or record_object == 'tarchy'):
        #Integer, Big
        b00_07=struct.pack('>2i',globals()["record_"+record_object],(44+number_of_parts*4+i_x_y_record*16)/2)
        f.write(b00_07)
        #Polygon Record Contents
        #Integer, Little
        b00_03=struct.pack('<i',3)
        f.write(b00_03)
    elif (record_object == 'popis' or record_object == 'znacky' or record_object == 'polygon'):
        #Integer, Big
        b00_07=struct.pack('>2i',globals()["record_"+record_object],10)
        f.write(b00_07)
        #Polygon Record Contents
        #Integer, Little
        b00_03=struct.pack('<i',1)
        f.write(b00_03)
    if (record_object == 'kladpar' or record_object == 'uov' or record_object == 'zappar' or record_object == 'linie' or record_object == 'zuob' or record_object == 'katuz' or record_object == 'tarchy'):
        #Double, Little
        if (record_object == 'kladpar' or record_object == 'uov'):
            b04_35=struct.pack('<4d',xmin_polygon,ymin_polygon,xmax_polygon,ymax_polygon)
        else:
            b04_35=struct.pack('<4d',xmin_polyline,ymin_polyline,xmax_polyline,ymax_polyline)
        f.write(b04_35)
        #Integer, Little
        b36_43=struct.pack('<2i',number_of_parts,i_x_y_record)
        f.write(b36_43)
        b44_47=struct.pack('<i',0)
        f.write(b44_47)
        while parts:
            b_part = parts[0]
            parts.remove(b_part)
            b48_51=struct.pack('i',b_part)
            f.write(b48_51)
        #Point Record Contents
        #Double, Little
        while x_y_record:
            xcoord = x_y_record[0][0]
            ycoord = x_y_record[0][1]
            x_y_record.remove([xcoord,ycoord])
            b48_63=struct.pack('<2d',xcoord,ycoord)
            f.write(b48_63)
    elif (record_object == 'popis' or record_object == 'znacky' or record_object == 'polygon'):
        #Double, Little
        xcoord = globals()["x_y_record_"+record_object][0][0]
        ycoord = globals()["x_y_record_"+record_object][0][1]
        b04_19=struct.pack('<2d',xcoord,ycoord)
        f.write(b04_19)
    f.close()
    #SHX
    f=open(file_dir+file_name+'_'+record_object+'.shx','ab')
    if (record_object == 'kladpar' or record_object == 'uov'):
        global c_length_kladpar
        #Index Record
        #Integer, Big
        if record_kladpar == 1:
            b00_07 = struct.pack('>2i',50,(44+number_of_parts*4+i_x_y_record*16)/2)
            f.write(b00_07)
            c_length_kladpar = 50 + (52+number_of_parts*4+i_x_y_record*16)/2
        else:
            b00_07 = struct.pack('>2i',c_length_kladpar,(44+number_of_parts*4+i_x_y_record*16)/2)
            f.write(b00_07)     
            c_length_kladpar += (52+number_of_parts*4+i_x_y_record*16)/2
    elif (record_object == 'zappar' or record_object == 'linie' or record_object == 'zuob' or record_object == 'katuz' or record_object == 'tarchy'):
        #Index Record
        #Integer, Big
        if globals()["record_"+record_object] == 1:
            b00_07 = struct.pack('>2i',50,(44+number_of_parts*4+i_x_y_record*16)/2)
            f.write(b00_07)
            globals()["c_length_"+record_object] = 50 + (52+number_of_parts*4+i_x_y_record*16)/2
        else:
            b00_07 = struct.pack('>2i',globals()["c_length_"+record_object],(44+number_of_parts*4+i_x_y_record*16)/2)
            f.write(b00_07)
            globals()["c_length_"+record_object] += (52+number_of_parts*4+i_x_y_record*16)/2
    elif (record_object == 'popis' or record_object == 'znacky' or record_object == 'polygon'):
        #Index Record
        #Integer, Big
        if globals()["record_"+record_object] == 1:
            b00_07 = struct.pack('>2i',50,10)
            f.write(b00_07)
            globals()["c_length_"+record_object] = 50 + 14
        else:
            b00_07 = struct.pack('>2i',globals()["c_length_"+record_object],10)
            f.write(b00_07)     
            globals()["c_length_"+record_object] += 14
    f.close()
    #DBF
    f=open(file_dir+file_name+'_'+record_object+'.dbf','ab')
    #Table Records
    b65=struct.pack('s',' ')
    f.write(b65)
    b66_71=struct.pack('6s',objekt)
    f.write(b66_71)
    b72_81=struct.pack('10s',vrstva)
    f.write(b72_81)
    if (record_object == 'kladpar' or record_object == 'uov'):
        b82_93=struct.pack('12s',parcis)
        f.write(b82_93)
        b94_105=struct.pack('12s',cpa)
        f.write(b94_105)
        b106_117=struct.pack('12s',parcela)
        f.write(b106_117)
        b118_123=struct.pack('6s',ku)
        f.write(b118_123)
        b124_129=struct.pack('2s',dp)
        f.write(b124_129)
        b130_135=struct.pack('6s',lv)
        f.write(b130_135)
    elif record_object == 'linie':
        b82_84=struct.pack('3s',linie)
        f.write(b82_84)
        b85_184=struct.pack('100s',popis)
        f.write(b85_184)
    elif record_object == 'zuob':
        b82_84=struct.pack('3s',zuob)
        f.write(b82_84)
        b85_184=struct.pack('100s',obec)
        f.write(b85_184)
    elif record_object == 'katuz':
        b82_87=struct.pack('6s',kataster)
        f.write(b82_87)
        b88_187=struct.pack('100s',hku)
        f.write(b88_187)
    elif record_object == 'popis':
        b82_181=struct.pack('100s',popis)
        f.write(b82_181)
    elif record_object == 'znacky':
        b82_86=struct.pack('5s',znacky)
        f.write(b82_86)
        b87_186=struct.pack('100s',popis)
        f.write(b87_186)
    elif record_object == 'polygon':
        b82_89=struct.pack('8s',bod)
        f.write(b82_89)
        b90_94=struct.pack('5s',znacky)
        f.write(b90_94)
        b95_194=struct.pack('100s',popis)
        f.write(b95_194)

def end(end_object):
    import struct
    f=open(file_dir+file_name+'_'+end_object+'.dbf','ab')
    #End Of File
    b_end=struct.pack('>b',26)
    f.write(b_end)
    f.close()

def prechod_arc(x,y):
    global i_x_y_record, n_i_x_y_record
    global x_y_record, n_x_y_record
    if n_prechod == 0:
        if calculate == 0:
            x_y_record += [[x, y]]
        i_x_y_record += 1
    elif n_prechod > 0:    
        if calculate == 0:
            n_x_y_record[n_prechod-1].append([x, y])
        n_i_x_y_record[n_prechod-1] += 1

def point_arc(uhol, xs, ys, radius):
    from math import sin, cos, pi
    if ((uhol >= 0) and (uhol < 90)):
        uhlik = (pi/180)*(90-uhol)
        x0 = xs + (radius * cos(uhlik))
        y0 = ys + (radius * sin(uhlik))
    else:
        uhlik = (pi/180)*(450-uhol)
        x0 = xs + (radius * cos(uhlik))
        y0 = ys + (radius * sin(uhlik))
    prechod_arc(x0,y0)

def compute_arc(clock, start, finis, xs, ys, radius, x1, y1, x3, y3):
    step = 1
    if clock:
        if (start > finis):
            prechod_arc(x1,y1)
            uhol = start + step
            while uhol <= 360:
                point_arc(uhol,xs,ys,radius)
                uhol += step
            uhol -= 360
            while uhol < finis:
                point_arc(uhol,xs,ys,radius)
                uhol += step
            if uhol >= finis:
                prechod_arc(x3,y3)
        else:
            prechod_arc(x1,y1)
            uhol = start + step
            while uhol < finis:
                point_arc(uhol,xs,ys,radius)
                uhol += step
            if uhol >= finis:
                prechod_arc(x3,y3)
    else:
        if (start < finis):
            prechod_arc(x1,y1)
            uhol = start - step
            while uhol >= 0:
                point_arc(uhol,xs,ys,radius)
                uhol -= step
            uhol += 360
            while uhol > finis:
                point_arc(uhol,xs,ys,radius)
                uhol -= step
            if uhol <= finis:
                prechod_arc(x3,y3)
        else:
            prechod_arc(x1,y1)
            uhol = start - step
            while uhol > finis:
                point_arc(uhol,xs,ys,radius)
                uhol -= step
            if uhol <= finis:
                prechod_arc(x3,y3)

def arc(x1, x2, x3, y1, y2, y3, xx1, xx2, xx3, yy1, yy2, yy3):
    from math import sqrt, asin, degrees
    ka = (yy2-yy1)/(xx2-xx1)
    kb = (yy3-yy2)/(xx3-xx2)
    xs = (ka*kb*(yy1-yy3)+kb*(xx1+xx2)-ka*(xx2+xx3))/(2*(kb-ka))
    ys = ((xx1-xx3)+ka*(yy1+yy2)-kb*(yy2+yy3))/(2*(ka-kb))
    radius = sqrt((x1-xs)**2+(y1-ys)**2)
    rozx = x1 - xs
    rozy = y1 - ys
    if rozx >= 0:
        start = 90 - degrees(asin(rozy/radius))
    else:
        start = 270 + degrees(asin(rozy/radius))
    radius = sqrt((x2-xs)**2+(y2-ys)**2)
    rozx = x2 - xs
    rozy = y2 - ys
    if rozx >= 0:
        inner = 90 - degrees(asin(rozy/radius))
    else:
        inner = 270 + degrees(asin(rozy/radius))
    radius = sqrt((x3-xs)**2+(y3-ys)**2)
    rozx = x3 - xs
    rozy = y3 - ys
    if rozx >= 0:
        finis = 90 - degrees(asin(rozy/radius))
    else:
        finis = 270 + degrees(asin(rozy/radius))
    if ((start < inner) and (inner < finis)):
        clock = 1
    elif ((start > inner) and (inner > finis)):
        clock = 0
    elif  ((start < inner) and (inner > finis)):
        if start > finis:
            clock = 1
        else:
            clock = 0
    elif  ((start > inner) and (inner < finis)):
        if start > finis:
            clock = 1
        else:
            clock = 0
    compute_arc(clock,start,finis,xs,ys,radius,x1,y1,x3,y3)

def func_polygon(polygon_object):
    global record_kladpar, number_of_parts, parts, objekt, vrstva, parcis, cpa, parcela, dp, lv, prechod, n_prechod
    global i_x_y_record, x_y_record, n_i_x_y_record, n_x_y_record
    global xmin_polygon, xmax_polygon, ymin_polygon, ymax_polygon
    #ZNACKY IN KLADPAR
    global record_znacky, znacky, popis
    global x_y_record_znacky
    #ZNACKY IN KLADPAR
    xmin_polygon = ymin_polygon = 0
    xmax_polygon = ymax_polygon = -9999999
    vrstva = section[1]
    objekt = section[2]
    parcis = ''
    cpa = '0'
    parcela = ''
    dp = '0'
    lv = '0'
    #ZNACKY IN KLADPAR
    znacky = ''
    popis = ''
    #ZNACKY IN KLADPAR
    number_of_parts = 1
    parts = []
    i_x_y_record = 0
    x_y_record = []
    n_prechod = 0
    n_x_y_record = []
    n_i_x_y_record = []
    n_prenos_x_y_record = []
    n_prenos_i_x_y_record = []
    nclr_x_y_record = []
    nclr_x_y_pred_record = []
    record_kladpar += 1
    s = f_global.readline()
    divideline(s.strip())
    while section[0] <> '&O':
        if section[0] == '&K':
            break
        if section[0] == '&A':
            if section[1][:7] == 'PARCIS=':
                parcis = section[1][7:]
            elif (section[1][:3] == 'KN=' or section[1][:3] == 'UO='):
                parcis = section[1][3:]
            elif (section[1][:3] == 'DP=' or section[1][:4] == 'KUL='):
                if section[1][:3] == 'DP=':
                    dp = section[1][3:]
                elif section[1][:4] == 'KUL=':
                    dp = section[1][4:]
            elif section[1][:3] == 'LV=':
                lv = section[1][3:]
            if parcis.find('-') == -1:
                if len(parcis)-(parcis.find('.')+1) == 3:
                    cpa = (parcis[:parcis.find('.')]+parcis[(parcis.find('.')+1):]+'0')
                if len(parcis)-(parcis.find('.')+1) == 4:
                    cpa = (parcis[:parcis.find('.')]+parcis[(parcis.find('.')+1):])
            else:
                cpa = '0'
        if (section[0] == '&L'):
            if s_mark == 0:
                xl = -1 * float(section[2])
                yl = -1 * float(section[3])
                x1 = xl
                y1 = yl
                calculate_max(x1,y1,'polygon')
                x_y_record += [[xl, yl]]
                i_x_y_record += 1
        #ZNACKY IN KLADPAR
            elif s_mark == 1:
                znacky = ''
                popis = ''
                record_znacky += 1
                for i_znacky in section[4:]:
                    if i_znacky[:2] == "S=":
                        znacky = 'S' + i_znacky[2:]
                        znacky_text(znacky)
                        popis = marktext
                x_y_record_znacky = []
                xl = -1 * float(section[2])
                yl = -1 * float(section[3])
                x1 = xl
                y1 = yl
                x_y_record_znacky += [[xl, yl]]
                record('znacky')
        elif (section[0] == 'P' and s_mark == 1):
            znacky = ''
            popis = ''
            record_znacky += 1
            for i_znacky in section[3:]:
                if i_znacky[:2] == "S=":
                    znacky = 'S' + i_znacky[2:]
                    znacky_text(znacky)
                    popis = marktext
            x_y_record_znacky = []
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            x_y_record_znacky += [[xl, yl]]
            record('znacky')
        #ZNACKY IN KLADPAR
        elif (section[0] == 'L' or section[0] == 'C'):
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            calculate_max(x1,y1,'polygon')
            prechod_arc(x1,y1)
        elif (section[0] == 'R'):
            x2 = -1 * float(section[1])
            y2 = -1 * float(section[2])
            calculate_max(x2,y2,'polygon')
            s = f_global.readline()
            divideline(s.strip())
            x3 = -1 * float(section[1])
            y3 = -1 * float(section[2])
            calculate_max(x3,y3,'polygon')
            if (x1 == x2 == x3):
                x_y_record += [[x2, y2]]
                x_y_record += [[x3, y3]]
                i_x_y_record += 2
            elif ((x1 == x2) or (x2 == x3)):
                if (x1 == x2):
                    arc(x1,x2,x3,y1,y2,y3,x1,x3,x2,y1,y3,y2)
                elif (x2 == x3):
                    arc(x1,x2,x3,y1,y2,y3,x3,x1,x2,y3,y1,y2)
            elif round((y1-y2)/(x1-x2),4) <> round((y2-y3)/(x2-x3),4):
                arc(x1,x2,x3,y1,y2,y3,x1,x2,x3,y1,y2,y3)
            else:
                x_y_record += [[x2, y2]]
                x_y_record += [[x3, y3]]
                i_x_y_record += 2
            x1 = x3
            y1 = y3
        elif (section[0][:1] == 'N'):
            x_pred = x1
            y_pred = y1
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            calculate_max(x1,y1,'polygon')
            nclr_x_y_record += [[x1,y1]]
            nclr_x_y_pred_record += [[x_pred,y_pred]]
            if len(nclr_x_y_record) > 1:
                if ((nclr_x_y_pred_record[len(nclr_x_y_pred_record)-1][0] == nclr_x_y_record[len(nclr_x_y_record)-2][0]) and (nclr_x_y_pred_record[len(nclr_x_y_pred_record)-1][1] == nclr_x_y_record[len(nclr_x_y_record)-2][1])):
                    n_prechod -= 1
                    for i in n_x_y_record[n_prechod]:
                        n_prenos_x_y_record.append(i)
                    n_prenos_i_x_y_record.append(n_i_x_y_record[n_prechod])
                    n_x_y_record.pop()
                    n_i_x_y_record.pop()
                    nclr_x_y_record.pop(len(nclr_x_y_record)-2)
                    nclr_x_y_pred_record.pop()
                    if ((nclr_x_y_pred_record[len(nclr_x_y_pred_record)-1][0] == x1) and (nclr_x_y_pred_record[len(nclr_x_y_pred_record)-1][1] == y1)):
                        nclr_x_y_record.pop()
                        nclr_x_y_pred_record.pop()
                    else:
                        n_prechod += 1
                        number_of_parts += 1
                        n_x_y_record.append([[xl, yl]])
                        n_i_x_y_record.append(1)
                else:
                    n_prechod += 1
                    number_of_parts += 1
                    n_x_y_record.append([[xl, yl]])
                    n_i_x_y_record.append(1)
            else:
                n_prechod += 1
                number_of_parts += 1
                n_x_y_record.append([[xl, yl]])
                n_i_x_y_record.append(1)
        elif section[0] == '&T':
            parcela = section[3][1:(len(section[3])-1)]
        s = f_global.readline()
        divideline(s.strip())
    # NL nema par - start
    if len(nclr_x_y_record) <> 0:
        number_of_parts -= len(nclr_x_y_record)
        for i in nclr_x_y_record:
            n_i_x_y_record[0] -= 1
            n_x_y_record[0].remove(i)
            while len(n_x_y_record) > 0:
                i_index = x_y_record.index(nclr_x_y_pred_record[0])+1
                while len(n_x_y_record[0]) > 0:
                    x_y_record.insert(i_index,n_x_y_record[0][0])
                    n_x_y_record[0].pop(0)
                    i_index += 1
                n_x_y_record.pop(0)
                nclr_x_y_record.pop(0)
                nclr_x_y_pred_record.pop(0)
            while len(n_i_x_y_record) > 0:
                i_x_y_record += n_i_x_y_record[0]
                n_i_x_y_record.pop(0)
    # NL nema par - koniec
    for i in n_prenos_x_y_record:
        x_y_record.append(i)
    for i in n_prenos_i_x_y_record:
        parts.append(i)
    i = 0
    while i < number_of_parts-1:
        i_x_y_record_in_parts = parts[i]
        parts[i] = i_x_y_record
        i_x_y_record += i_x_y_record_in_parts
        i += 1
    if (section[0] == '&K' or not (section[1][:5] == 'OBVOD:')):
        prechod = 0
    if polygon_object == 'kladpar':
        record('kladpar')
    elif polygon_object == 'uov':
        record('uov')

def func_polyline(polyline_object):
    global xmin_polyline, xmax_polyline, ymin_polyline, ymax_polyline
    if polyline_object == 'zappar':
        global record_zappar, number_of_parts, parts, objekt, vrstva
        global prechod, i_x_y_record, x_y_record, n_prechod
        record_zappar += 1
    elif polyline_object == 'linie':
        global record_linie, number_of_parts, parts, objekt, vrstva, linie, popis
        global prechod, i_x_y_record, x_y_record, n_prechod
        record_linie += 1
        linie = ''
        popis = ''
    elif polyline_object == 'zuob':
        global record_zuob, number_of_parts, parts, objekt, vrstva, zuob, obec
        global prechod, i_x_y_record, x_y_record, n_prechod
        record_zuob += 1
        zuob = ''
        obec = ''
    elif polyline_object == 'katuz':
        global record_katuz, number_of_parts, parts, objekt, vrstva, kataster, hku
        global prechod, i_x_y_record, x_y_record, n_prechod
        record_katuz += 1
        kataster = ''
        hku = ''
    if polyline_object == 'tarchy':
        global record_tarchy, number_of_parts, parts, objekt, vrstva
        global prechod, i_x_y_record, x_y_record, n_prechod
        record_tarchy += 1
    xmin_polyline = ymin_polyline = 0
    xmax_polyline = ymax_polyline = -9999999
    vrstva = section[1]
    objekt = section[2]
    number_of_parts = 1
    parts = []
    i_x_y_record = 0
    x_y_record = []
    n_prechod = 0
    prvy = 1
    s = f_global.readline()
    divideline(s.strip())
    while section[0] <> '&O':
        if section[0] == '&K':
            break
        if prvy == 0:
            s = f_global.readline()
            divideline(s.strip())
        if (section[0] == '&A'):
            if polyline_object == 'linie':
                if (section[1][:3] == 'INT' or section[1][:3] == 'HCU' or section[1][:3] == 'HOP' or section[1][:3] == 'HTO'):
                    linie = section[1][:3]
                    popis = section[1][4:]
                    for i_popis in section[2:]:
                        popis = popis + ' ' + i_popis
            elif polyline_object == 'zuob':
                if section[1][:4] == 'ZUOB':
                    zuob = section[1][5:]
                elif section[1][:4] == 'OBEC':
                    obec = section[1][5:]
                    for i_obec in section[2:]:
                        obec = obec + ' ' + i_obec
            elif polyline_object == 'katuz':
                if section[1][:2] == 'KU':
                    kataster = section[1][3:]
                elif section[1][:3] == 'HKU':
                    hku = section[1][4:]
                    for i_hku in section[2:]:
                        hku = hku + ' ' + i_hku
            if prvy == 1:
                s = f_global.readline()
                divideline(s.strip())
        if (section[0] == '&L'):
            if prvy == 0:
                parts += [i_x_y_record]
                number_of_parts += 1
            else:
                prvy = 0
            xl = -1 * float(section[2])
            yl = -1 * float(section[3])
            x1 = xl
            y1 = yl
            calculate_max(x1,y1,'polyline')
            x_y_record += [[xl, yl]]
            i_x_y_record += 1
        elif (section[0] == 'L' or section[0] == 'C'):
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            calculate_max(x1,y1,'polyline')
            x_y_record += [[x1, y1]]
            i_x_y_record += 1
        elif (section[0] == 'R'):
            x2 = -1 * float(section[1])
            y2 = -1 * float(section[2])
            calculate_max(x2,y2,'polyline')
            s = f_global.readline()
            divideline(s.strip())
            x3 = -1 * float(section[1])
            y3 = -1 * float(section[2])
            calculate_max(x3,y3,'polyline')
            if (x1 == x2 == x3):
                x_y_record += [[x2, y2]]
                x_y_record += [[x3, y3]]
                i_x_y_record += 2
            elif ((x1 == x2) or (x2 == x3)):
                if (x1 == x2):
                    arc(x1,x2,x3,y1,y2,y3,x1,x3,x2,y1,y3,y2)
                elif (x2 == x3):
                    arc(x1,x2,x3,y1,y2,y3,x3,x1,x2,y3,y1,y1)
            elif round((y1-y2)/(x1-x2),4) <> round((y2-y3)/(x2-x3),4):
                arc(x1,x2,x3,y1,y2,y3,x1,x2,x3,y1,y2,y3)
            else:
                x_y_record += [[x2, y2]]
                x_y_record += [[x3, y3]]
                i_x_y_record += 2
            x1 = x3
            y1 = y3
        elif (section[0][:1] == 'N' or section[0] == 'P'):
            parts += [i_x_y_record]
            number_of_parts += 1
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            calculate_max(x1,y1,'polyline')
            x_y_record += [[xl, yl]]
            i_x_y_record += 1
    if (section[0] == '&K' or not (section[1][:5] == 'OBVOD:')):
        prechod = 0
    record(polyline_object)

def func_popis():
    global record_popis, objekt, vrstva, popis, prechod
    global x_y_record_popis
    vrstva = section[1]
    objekt = section[2]
    popis = ''
    s = f_global.readline()
    divideline(s.strip())
    while section[0] <> '&O':
        if section[0] == '&K':
            break
        elif (section[0] == '&T'):
            popis = ''
            record_popis += 1
            for i_popis in section[3:]:
                if i_popis == "":
                    continue
                if popis == "":
                    if i_popis == "'":
                        popis = i_popis
                    else:
                        if not i_popis[-1] == "'":
                            popis = i_popis + " "
                        else:
                            popis = i_popis
                            popis = popis[1:-1]
                            break
                else:
                    if not i_popis[-1] == "'":
                        popis += (i_popis + " ")
                    else:
                        popis += i_popis
                        popis = popis[1:-1]
                        break
            for i_popis_char in popis:
                codepage_conv(i_popis_char)
                if i_popis_char <> char852:
                    popis = popis.replace(i_popis_char,char852,1)
            x_y_record_popis = []
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            x_y_record_popis += [[xl, yl]]
            record('popis')
        s = f_global.readline()
        divideline(s.strip())
        if prechod == 1:
            prechod = 0

def func_znacky():
    global record_znacky, objekt, vrstva, znacky, popis, prechod
    global x_y_record_znacky
    vrstva = section[1]
    objekt = section[2]
    znacky = ''
    popis = ''
    s = f_global.readline()
    divideline(s.strip())
    while section[0] <> '&O':
        if section[0] == '&K':
            break
        elif (section[0] == '&L' and section[1] == 'P' and s_mark == 1):
            znacky = ''
            popis = ''
            record_znacky += 1
            for i_znacky in section[4:]:
                if i_znacky[:2] == "S=":
                    znacky = 'S' + i_znacky[2:]
                    znacky_text(znacky)
                    popis = marktext
            x_y_record_znacky = []
            xl = -1 * float(section[2])
            yl = -1 * float(section[3])
            x1 = xl
            y1 = yl
            x_y_record_znacky += [[xl, yl]]
            record('znacky')
        elif (section[0] == 'P' and s_mark == 1):
            znacky = ''
            popis = ''
            record_znacky += 1
            for i_znacky in section[3:]:
                if i_znacky[:2] == "S=":
                    znacky = 'S' + i_znacky[2:]
                    znacky_text(znacky)
                    popis = marktext
            x_y_record_znacky = []
            xl = -1 * float(section[1])
            yl = -1 * float(section[2])
            x1 = xl
            y1 = yl
            x_y_record_znacky += [[xl, yl]]
            record('znacky')
        s = f_global.readline()
        divideline(s.strip())
        if prechod == 1:
            prechod = 0

def func_polyg():    
    global record_polygon, record_popis, objekt, vrstva, bod, znacky, popis, prechod
    global x_y_record_polygon
    vrstva = section[1]
    objekt = section[2]
    bod = ''
    znacky = ''
    popis = ''
    s = f_global.readline()
    divideline(s.strip())
    while section[0] <> '&O':
        if section[0] == '&K':
            break
        elif (section[0] == '&L' and section[1] == 'P' and s_mark == 1):
            record_polygon += 1
            for i_polygon in section[4:]:
                if i_polygon[:2] == "S=":
                    znacky = 'S' + i_polygon[2:]
                    znacky_text(znacky)
                    popis = marktext
                elif i_polygon[:2] == "C=":
                    bod = i_polygon[2:]
            x_y_record_polygon = []
            xl = -1 * float(section[2])
            yl = -1 * float(section[3])
            x1 = xl
            y1 = yl
            x_y_record_polygon += [[xl, yl]]
            record('polygon')
        s = f_global.readline()
        divideline(s.strip())
        if prechod == 1:
            prechod = 0
# koniec

class Vgi2ShpConverter:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'vgi2shpconverter_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = Vgi2ShpConverterDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/vgi2shpconverter/icon.png"),
            u"Vgi2Shp", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&Vgi2Shp", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&Vgi2Shp", self.action)
        self.iface.removeToolBarIcon(self.action)

    def select_files(self):
        global calculate
        global files, f_global, file_name, file_ext, file_dir, ku
        global record_kladpar, record_zappar, record_linie, record_zuob, record_katuz, record_tarchy, record_popis, record_znacky, record_polygon, prechod
        from PyQt4 import QtGui
        file_part = ''
        file_part = QtGui.QFileDialog.getOpenFileName(None, u'Vyberte VGI súbor', os.getcwd(), 'VGI File *.vgi')
        if file_part <> '':
            self.dlg.setEnabled(False)
            self.dlg.repaint()
            files = file_part
            file_name = files[files.rfind('/')+1:files.find('.')]
            file_ext = files[files.find('.')+1:]
            file_dir = files[:files.rfind('/')+1]
            ku = str(file_name[2:8])
            calculate = 1
            calculate_object()
            calculate = 0
            if kladparik == 1:
                header('kladpar')
                record_kladpar = 0
            if uovik == 1:
                header('uov')
                record_kladpar = 0
            if zapparik == 1:
                header('zappar')
                record_zappar = 0
            if linijik == 1:
                header('linie')
                record_linie = 0
            if zuobik == 1:
                header('zuob')
                record_zuob = 0
            if katuzik == 1:
                header('katuz')
                record_katuz = 0
            if tarchik == 1:
                header('tarchy')
                record_tarchy = 0
            if popisik == 1:
                header('popis')
                record_popis = 0
            if znacik == 1:
                header('znacky')
                record_znacky = 0
            if polygonik == 1:
                header('polygon')
                record_polygon = 0
            f_global = open(files,'r')
            prechod = 1
            s = f_global.readline()
            divideline(s.strip())
            while section[0] <> '&K':
                if kladparik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'KLADPAR':
                            func_polygon('kladpar')
                if uovik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'UOV':
                            func_polygon('uov')
                if zapparik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'ZAPPAR':
                            func_polyline('zappar')
                if linijik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'LINIE':
                            func_polyline('linie')
                if zuobik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'ZUOB':
                            func_polyline('zuob')
                if katuzik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'KATUZ':
                            func_polyline('katuz')
                if tarchik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'TARCHY':
                            func_polyline('tarchy')
                if popisik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'POPIS':
                            func_popis()
                if znacik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'ZNACKY':
                            func_znacky()
                if polygonik == 1:
                    if section[0] <> '&K':
                        if section[1] == 'POLYGON':
                            func_polyg()
                if prechod == 1:
                    s = f_global.readline()
                    divideline(s.strip())
                else:
                    prechod = 1
            if kladparik == 1:
                end('kladpar')
            if uovik == 1:
                end('uov')
            if zapparik == 1:
                end('zappar')
            if linijik == 1:
                end('linie')
            if zuobik == 1:
                end('zuob')
            if katuzik == 1:
                end('katuz')
            if tarchik == 1:
                end('tarchy')
            if popisik == 1:
                end('popis')
            if znacik == 1:
                end('znacky')
            if polygonik == 1:
                end('polygon')
            f_global.close()
            self.dlg.setEnabled(True)
            self.dlg.repaint()

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        while result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)
            self.dlg.show()
            self.select_files()
            # self.dlg.hide()
            result = self.dlg.exec_()
