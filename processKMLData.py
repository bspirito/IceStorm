from zipfile import ZipFile  # unzip KMZ to KML
from bs4 import BeautifulSoup
import re
from area import area


def processKMLData(filename):
    kmz = ZipFile(filename, 'r')
    total_area = 0
    total_area_in = 0
    total_area_out = 0
    total_area_in_tot = 0
    total_area_out_tot = 0
    with kmz.open('doc.kml') as kml_obj:  # Extract KMZ and save as KML
        soup = BeautifulSoup(kml_obj, 'html.parser')
    zPlaceMarks = getname_tags(soup, "Placemark|PlaceMark|placemark")
    print(filename)
    # Loop through each Placemark
    for i in range(0, len(zPlaceMarks)):
        # Get each set of Placemark data
        xdata = zPlaceMarks[i]

        # Get the name of the PlaceMark, CT18 or      CT81
        placemark_name = str(xdata.find('name')).strip('</name>')
        # print(placemark_name)

        # Get the multigeometry including both inner and outer boundaries if necessary
        # geo = str(xdata.find('multigeometry'))
        # print(geo)
        total_area_in = kml_getpolyinout(placemark=xdata, placemark_name=placemark_name, boundary='innerboundaryis')
        total_area_out = kml_getpolyinout(placemark=xdata, placemark_name=placemark_name, boundary='outerboundaryis')
        if total_area_in == None:
            total_area += total_area_out
        if total_area_out == None:
            total_area += total_area_in

    return total_area


def kml_getpolyinout(placemark, placemark_name, boundary):
    total_area = 0
    zBoundary = getname_tags(placemark, boundary)
    if zBoundary != []:
        for j in range(0, len(zBoundary)):
            zPaths = getname_tags(zBoundary[j], 'coordinates')  # Strip out the coordinates
            if len(zPaths) > 0:
                area_km2 = output_poly(placemark_name, zPaths)
            total_area += area_km2
        return total_area


def getname_tags(obj, keywords):
    xNode = ""
    xkeyword = keywords.split("|")
    for i in range(0, len(xkeyword)):
        if len(xNode) == 0:
            xNode = obj.findAll(xkeyword[i])
    return xNode


def output_poly(Pt_Name, line):
    vertices = str(line).split(' ')
    vertices = ArrayNotEmptyZ(vertices)
    if len(vertices) > 0:
        # print(Pt_Name, vertices)
        area_km2 = calculate_polygon(vertices)
    return area_km2


def ArrayNotEmptyZ(InArray):
    OArray = []
    s = ""
    for i in range(0, len(InArray)):
        s = ztrim(InArray[i])
        if len(s) > 1:
            OArray.append(s)
    return OArray


def ztrim(s):
    # non_decimal = re.compile(r'[^\d.]+')
    # s = non_decimal.sub('', s)
    # s = re.sub("[^0-9^.]", "", s)
    s = re.sub("[^0-9,.-]", "", s)  # strip all nonnumeric characters from string except comma and dot
    return s.replace("/^\s+|\s+$/g", "")


def calculate_polygon(vertices):
    # total_area = 0
    # Convert coordinate vertices (String) into list of floats
    newlist = []
    num_words = 1
    for coords in vertices:
        # print("Coordinate Set {} in {} Vertices: {}".format(num_words, len(vertices), coords))
        split_coords = coords.split(',')[:2]
        new_coords = []
        for item in split_coords:
            # Some values contain exponents
            item = f'{item:.16}'
            new_coords.append(float(item))
        newlist.append(new_coords)
        num_words += 1
    obj = {'type': 'Polygon',
           'coordinates': [newlist]}
    area_m2 = area(obj)
    area_km2 = area_m2 / 1e+6
    # print('AREA = {} m^2'.format(area_m2))
    # print('AREA = {} km^2'.format(area_km2))
    # total_area = total_area + area_km2
    return area_km2


if __name__ == "__main__":
    processKMLData("C:\\Users\\Brandon\\Documents\\IceStorm\\antarctic\\2020\\antarctic_line_2020001.kmz")