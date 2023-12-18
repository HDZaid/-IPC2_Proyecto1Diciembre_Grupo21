import xml.etree.ElementTree as ET

try:
    xml_file = open('lee.xml')
    #print(xml_file.read())
    if xml_file.readable():
        xml_data = ET.fromstring(xml_file.read())
        lst_plants = xml_data.findall('PLANT')
        #print(lst_plants.count())
        for plant in lst_plants:
            print(f"Nombre: :{plant.find('COMMON').text}")
    else:
        print(False)
    
except Exception as err:
    print("Error: ", err)
    
finally:
    xml_file.close()