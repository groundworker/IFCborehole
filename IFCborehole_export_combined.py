# -*- coding: utf-8 -*-
"""
@author:Andreas Sorgatz-Wenzel
"""

import random
import string
import math
import time
import pandas as pd


# randomString() by pynative.com: generate a random string of letters a. digits
def randomString(stringLength=22):
    rS = string.ascii_letters + string.digits
    return ''.join(random.choice(rS) for i in range(stringLength))


def read_csv(filename):
    dataframe = pd.read_csv(filename, delimiter=';')
    return dataframe


# Punkte für Kreis-Polyline definieren
def circlepoints(n_points=12):
    position_data = []
    for index in range(0, n_points):
        alpha = (index*2/n_points*math.pi)
        x = round(math.sin(alpha), 4)
        y = round(math.cos(alpha), 4)
        position = [x, y]
        position_data.append(position)
    return position_data


file_in = "borehole_data.csv"
file_out = open("Modell_Aufschuesse_kombiniert.ifc", "w")

data = read_csv(file_in)

data_stammid = []
empty_column = data['HAUPTGEMENGTEIL'].isnull()
data_X = ""
data_G = ""
data_S = ""
data_U = ""
data_T = ""
data_H = ""
num = 0
radius = 3.0
BoreholeAdress={}

file_out.write("ISO-10303-21;\n HEADER;\nFILE_DESCRIPTION(( 'ViewDefinition [CoordinationView_V2.0]'),'2;1');\n")
file_out.write("FILE_NAME('Bohrungen','"+str(time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime()))+"',('Andreas, Sorgatz-Wenzel'),(''),'','','');\n")
file_out.write("FILE_SCHEMA(('IFC2X3'));\nENDSEC;\n")

file_out.write("DATA;\n")
file_out.write("#100= IFCPROJECT('"+str(randomString(22))+"',#110,'Projekt',$,$,$,$,(#201),#301);\n")
file_out.write("#110= IFCOWNERHISTORY(#111,#115,$,.NOCHANGE.,$,$,$,$);\n")

file_out.write("#111= IFCPERSONANDORGANIZATION(#112,#113,$);\n")
file_out.write("#112= IFCPERSON($,'BIM-Modellierer',$,$,$,$,$,$);\n")
file_out.write("#113= IFCORGANIZATION($,'Geotechnik',$,$,$);\n")
file_out.write("#115= IFCAPPLICATION(#113,'0.3','Skript',$);\n")
file_out.write("#116= IFCSITE('"+str(randomString(22))+"',$,'Baugrund',$,$,#118,$,$,.ELEMENT.,(0,0,0,0),(0,0,0,0),0.,$,$);\n")
file_out.write("#117= IFCRELAGGREGATES('"+str(randomString(22))+"',$,$,$,#100,(#116));\n")
file_out.write("#118= IFCLOCALPLACEMENT($,#120);\n")
file_out.write("#119= IFCCARTESIANPOINT((0.,0.,0.));\n")
file_out.write("#120= IFCAXIS2PLACEMENT3D(#119,$,$);\n")

file_out.write("#201= IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.0E-5,#210,$);\n")
file_out.write("#202= IFCGEOMETRICREPRESENTATIONSUBCONTEXT('Body','Model',*,*,*,*,#201,$,.MODEL_VIEW.,$);\n")
file_out.write("#210= IFCAXIS2PLACEMENT3D(#901,$,$);\n")

file_out.write("#301= IFCUNITASSIGNMENT((#311,#312));\n")
file_out.write("#311= IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);\n")
file_out.write("#312= IFCCONVERSIONBASEDUNIT(#313,.PLANEANGLEUNIT.,'degree',#314);\n")
file_out.write("#313= IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);\n")
file_out.write("#314= IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453293),#315);\n")
file_out.write("#315= IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);\n")

file_out.write("#500= IFCBUILDING('"+str(randomString(22))+"',$,'Baugrundaufschluesse',$,$,#118,$,$,.ELEMENT.,$,$,$);\n")
file_out.write("#519= IFCRELAGGREGATES('"+str(randomString(22))+"',$,$,$,#116,(#500));\n")
file_out.write("#520= IFCBUILDINGSTOREY('"+str(randomString(22))+"',#110,'Ebene Aufschluesse',$,'Ebene:Ebene',#118,$,'borehole-Storey',.ELEMENT.,.0);\n")
file_out.write("#521= IFCBUILDINGSTOREY('"+str(randomString(22))+"',#110,'Ebene Punkte',$,'Ebene:Ebene',#118,$,'point-Storey',.ELEMENT.,.0);\n")
file_out.write("#530= IFCRELAGGREGATES('"+str(randomString(22))+"',#110,$,$,#500,(#520));\n")
file_out.write("#531= IFCRELAGGREGATES('"+str(randomString(22))+"',#110,$,$,#500,(#521));\n")

file_out.write("#801= IFCPRESENTATIONSTYLEASSIGNMENT((#802));\n")
file_out.write("#802= IFCSURFACESTYLE($,.POSITIVE.,(#804));\n")
file_out.write("#803= IFCCOLOURRGB($,0.,0.,0.);\n")
file_out.write("#804= IFCSURFACESTYLESHADING(#803);\n")

file_out.write("#901= IFCCARTESIANPOINT((0.,0.,0.));\n")
file_out.write("#902= IFCDIRECTION((1.,0.,0.));\n")
file_out.write("#903= IFCDIRECTION((0.,1.,0.));\n")
file_out.write("#904= IFCDIRECTION((0.,0.,1.));\n")
file_out.write("#905= IFCDIRECTION((-1.,0.,0.));\n")
file_out.write("#906= IFCDIRECTION((0.,-1.,0.));\n")
file_out.write("#907= IFCDIRECTION((0.,0.,-1.));\n")
file_out.write("#908= IFCCIRCLEPROFILEDEF(.AREA.,$,$,"+str(radius)+");\n")

i = 10  # Startnummer für >10XX
for j, row in enumerate(data['ID_STAMMDATEN']):
    ok = float(data['ANSATZHOEHE_NN'][j])-float(data['OBERE_TIEFE'][j])
    uk = float(data['ANSATZHOEHE_NN'][j])-float(data['UNTERE_TIEFE'][j])
    laenge_abschnitt = float(data['UNTERE_TIEFE'][j])-float(data['OBERE_TIEFE'][j])
    RW = data['X_ETRS89'][j]
    HW = data['Y_ETRS89'][j]

    file_out.write("#"+str(i)+"00= IFCBUILDINGELEMENTPROXY('"+str(randomString(22))+"',4,'"+str(data['ID_STAMMDATEN'][j])+"','Cylinder Extrusion',$,#"+str(i)+"01,#"+str(i)+"10,$,$);\n")
    file_out.write("#"+str(i)+"01= IFCLOCALPLACEMENT($,#"+str(i)+"02);\n")
    file_out.write("#"+str(i)+"02= IFCAXIS2PLACEMENT3D(#"+str(i)+"03,$,$);\n")
    file_out.write("#"+str(i)+"03= IFCCARTESIANPOINT((.0,.0,.0));\n")
    file_out.write("#"+str(i)+"10= IFCPRODUCTDEFINITIONSHAPE($,$,(#"+str(i)+"30));\n")

    file_out.write("#"+str(i)+"30= IFCSHAPEREPRESENTATION(#202,'Body','SweptSolid',(#"+str(i)+"31));\n")        
    file_out.write("#"+str(i)+"31= IFCEXTRUDEDAREASOLID(#908,#"+str(i)+"35,#907,"+str(laenge_abschnitt)+");\n")
    file_out.write("#"+str(i)+"35= IFCAXIS2PLACEMENT3D(#"+str(i)+"36,$,$);\n")        
    file_out.write("#"+str(i)+"36= IFCCARTESIANPOINT(("+str(RW)+","+str(HW)+","+str(ok)+"));\n")
    
    file_out.write("#"+str(i)+"40= IFCPROPERTYSET('"+str(randomString(22))+"',$,'HH_Baugrund_Attribute',$,(#"+str(i)+"41,#"+str(i)+"42,#"+str(i)+"43,#"+str(i)+"44,#"+str(i)+"45,#"+str(i)+"46,#"+str(i)+"47,#"+str(i)+"48,#"+str(i)+"49));\n")
    file_out.write("#"+str(i)+"41= IFCPROPERTYSINGLEVALUE('_Schichtnummer',$,IFCLABEL('"+str(data['ID_STAMMDATEN'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"42= IFCPROPERTYSINGLEVALUE('_Hauptbestandteil',$,IFCLABEL('"+str(data['HAUPTGEMENGTEIL'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"43= IFCPROPERTYSINGLEVALUE('_Nebenbestandteil/Bemerkung',$,IFCLABEL('"+str(data['NEBENGEMENGTEIL'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"44= IFCPROPERTYSINGLEVALUE('_Stratigraphie',$,IFCLABEL('"+str(data['STRATIGRAPHIE'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"45= IFCPROPERTYSINGLEVALUE('_Farbe',$,IFCLABEL('"+str(data['FARBE'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"46= IFCPROPERTYSINGLEVALUE('_Aufschlussbereich_OK',$,IFCLABEL('"+str(data['OBERE_TIEFE'][j])+"'),$);\n")  
    file_out.write("#"+str(i)+"47= IFCPROPERTYSINGLEVALUE('_Aufschlussbereich_UK',$,IFCLABEL('"+str(data['UNTERE_TIEFE'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"48= IFCPROPERTYSINGLEVALUE('_Genese',$,IFCLABEL('"+str(data['GENESE'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"49= IFCPROPERTYSINGLEVALUE('_Aufschlussnummer',$,IFCLABEL('"+str(data['ID_SCHICHTDATEN'][j])+"'),$);\n")
    file_out.write("#"+str(i)+"50= IFCRELDEFINESBYPROPERTIES('"+str(randomString(22))+"',$,$,$,(#"+str(i)+"00),#"+str(i)+"40);\n")

    kontroll = True
    if empty_column[j]:
        data_column = ""
    else:
        data_column = str(data['HAUPTGEMENGTEIL'][j])
    if "X" in data_column and kontroll is True:
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,0.25,0.25,0.25);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")  
        data_X=str(data_X)+",#"+str(i)+"30"
        kontroll = False
    if "G" in data_column and kontroll is True:
        data_G=str(data_G)+",#"+str(i)+"30"
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,1.,1.,0.);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")
        kontroll = False
    if "S" in data_column and kontroll is True:
        data_S=str(data_S)+",#"+str(i)+"30"
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,0.76,0.70,0.50);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")
        kontroll = False               
    if "U" in data_column and kontroll is True:
        data_U=str(data_U)+",#"+str(i)+"30"
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,0.53,0.85,0.46);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")
        kontroll = False               
    if "T" in data_column and kontroll is True:
        data_T=str(data_T)+",#"+str(i)+"30"
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,0.29,0.21,0.49);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")
        kontroll = False
    if "H" in data_column and kontroll is True:
        data_H=str(data_H)+",#"+str(i)+"30"
        file_out.write("#"+str(i)+"55= IFCCOLOURRGB($,0.55,0.27,0.07);\n") 
        file_out.write("#"+str(i)+"56= IFCSURFACESTYLERENDERING(#"+str(i)+"55,$,$,$,$,$,$,$,.FLAT.);\n") 
        file_out.write("#"+str(i)+"57= IFCSURFACESTYLE($,.BOTH.,(#"+str(i)+"56));\n") 
        file_out.write("#"+str(i)+"58= IFCPRESENTATIONSTYLEASSIGNMENT((#"+str(i)+"57));\n") 
        file_out.write("#"+str(i)+"59= IFCSTYLEDITEM(#"+str(i)+"31,(#"+str(i)+"58),$);\n")
        kontroll = False            

    if data['ID_STAMMDATEN'][j] not in data_stammid:
        data_stammid.append(data['ID_STAMMDATEN'][j])

        file_out.write("#"+str(i)+"07= IFCBUILDINGELEMENTPROXY('"+str(randomString(22))+"',4,'"+str(data['ID_STAMMDATEN'][j])+"',$,$,#"+str(i)+"71,$,$,$);\n")
        file_out.write("#"+str(i)+"08= IFCRELCONTAINEDINSPATIALSTRUCTURE('"+str(randomString(22))+"',110,$,$,(#"+str(i)+"07),#520);\n")
        BoreholeAdress[str(data['ID_STAMMDATEN'][j])] ="#"+str(i)+"07"
        file_out.write("#"+str(i)+"71= IFCLOCALPLACEMENT($,#"+str(i)+"02);\n")
        file_out.write("#"+str(i)+"72= IFCAXIS2PLACEMENT3D(#"+str(i)+"03,$,$);\n")
        file_out.write("#"+str(i)+"73= IFCCARTESIANPOINT((.0,.0,.0));\n")

        data_point = ""
        i_pointid = 10
        for i_point in circlepoints():
            i_pointid += 1
            file_out.write("#"+str(i)+str(i_pointid)+"= IFCCARTESIANPOINT(("+str(float(RW)+radius*i_point[0])+","+str(float(HW)+radius*i_point[1])+","+str(data['ANSATZHOEHE_NN'][j])+"));\n")
            if i_pointid == 11:
                data_point="#"+str(i)+str(i_pointid)
            else:
                data_point=str(data_point)+",#"+str(i)+str(i_pointid)

        file_out.write("#"+str(i)+"60= IFCPROPERTYSET('"+str(randomString(22))+"',$,'HH_Baugrundaufschluesse_Attribute',$,(#"+str(i)+"61,#"+str(i)+"62,#"+str(i)+"63,#"+str(i)+"64,#"+str(i)+"65));\n")
        file_out.write("#"+str(i)+"61= IFCPROPERTYSINGLEVALUE('_Aufschlussnummer',$,IFCLABEL('Pkt-"+str(data['ID_STAMMDATEN'][j])+"'),$);\n")
        file_out.write("#"+str(i)+"62= IFCPROPERTYSINGLEVALUE('_Aufschlussart',$,IFCLABEL('"+str(data['ARCHIVKURZBEZEICHNUNG'][j])+"'),$);\n")
        file_out.write("#"+str(i)+"63= IFCPROPERTYSINGLEVALUE('_Hoehe_Ansatzpunkt',$,IFCLABEL('"+str(data['ANSATZHOEHE_NN'][j])+"'),$);\n")
        file_out.write("#"+str(i)+"64= IFCPROPERTYSINGLEVALUE('_Laenge_Baugrundaufschluss',$,IFCLABEL('"+str(data['ENDTEUFE'][j])+"'),$);\n")
        file_out.write("#"+str(i)+"65= IFCPROPERTYSINGLEVALUE('_Aufschlussdatum',$,IFCLABEL('"+str(data['BOHRDATUM'][j])+"'),$);\n")
        file_out.write("#"+str(i)+"69= IFCRELDEFINESBYPROPERTIES('"+str(randomString(22))+"',$,$,$,(#"+str(i)+"07),#"+str(i)+"60);\n")

    id_borehole = int(data['ID_STAMMDATEN'][j])
    file_out.write("#"+str(i)+"09= IFCRELAGGREGATES('"+str(randomString(22))+"',#110,$,$,"+str(BoreholeAdress[str(id_borehole)])+",(#"+str(i)+"00));\n")
    i = i+1

file_out.write("ENDSEC;\n")
file_out.write("END-ISO-10303-21;")

file_out.close()
