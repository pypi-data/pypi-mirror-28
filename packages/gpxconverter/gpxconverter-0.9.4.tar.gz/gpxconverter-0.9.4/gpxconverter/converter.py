import xml.etree.ElementTree as et
import csv
import re
import os
import sys


def convert(i, o):
    inputfile = i[0]
    outputfile = o
    base_path = os.getcwd()
    xml_file = os.path.join(base_path, inputfile)
    if os.path.isfile(xml_file):
        _write_output(inputfile, outputfile, xml_file)
    else:
        print(inputfile +
              """ does not exist.Please check file name and try again!""")
        sys.exit()


def _write_output(inputfile, outputfile, xml_file):

    tree = et.parse(xml_file)
    root = tree.getroot()
    tags = []
    latlon_header = ['lat', 'lon']
    for child in root:
        child_tag = _get_tag(child)
        if child_tag != 'metadata':
            if child_tag not in tags:
                tags.append(child_tag)

    # row_count = 0  # count records
    ext_index = re.search(r'\.', inputfile[::-1])

    if outputfile:
        output_csv_file = outputfile
    else:
        output_csv_file = inputfile[: -(ext_index.start() + 1)]

    outputfiles = {}
    csv_headers = {}
    record_count = {}
    for tag in tags:
        outputfiles[tag] = output_csv_file + '_' + tag + '.csv'
        csv_headers[tag] = False
        record_count[tag] = 0

    for child in root:
        child_tag = _get_tag(child)
        if child_tag == 'wpt':
            waypoint = child
            elements = waypoint.getchildren()
            if not csv_headers['wpt']:
                with open(outputfiles[child_tag], 'w', newline='') as csv_file:
                    outputfile_header = latlon_header
                    wpt_header = _get_header(elements)
                    outputfile_header.extend(wpt_header)
                    writer = csv.DictWriter(csv_file, outputfile_header)
                    writer.writeheader()
                    csv_headers['wpt'] = True
            with open(outputfiles[child_tag], 'a', newline='') as csv_file:
                row_value = _parse_waypoints(waypoint, elements,
                                             outputfile_header)
                writer = csv.DictWriter(csv_file, outputfile_header)
                writer.writerow(row_value)

            record_count[child_tag] += 1
        elif child_tag == 'rte':
            route = child
            elements = route.getchildren()
            if not csv_headers['rte']:
                with open(outputfiles[child_tag], 'w') as csv_file:
                    rte_header = _get_header(elements)
                    outputfile_header = rte_header
                    for element in elements:
                        element_tag = _get_tag(element)
                        if element_tag == 'rtept':
                            waypoint_elements = element.getchildren()
                            rtept_header = _get_header(waypoint_elements,
                                                       'rtept')
                            break
                    waypoints_header = latlon_header
                    waypoints_header.extend(rtept_header)
                    outputfile_header.extend(waypoints_header)
                    writer = csv.DictWriter(csv_file, outputfile_header)
                    writer.writeheader()
                    csv_headers['rte'] = True
            with open(outputfiles[child_tag], 'a') as csv_file:
                # //TODO: return a list of dict of row values
                # write each
                record_count[tag] = _output_routes(
                                                   route, elements,
                                                   waypoints_header,
                                                   outputfile_header, csv_file)

    for tag in tags:
        print(outputfiles[tag] + ' is created with ' +
              str(record_count[tag]) + ' record(s).')


def _get_header(elements, header_type='wpt'):
    header = []
    for element in elements:
        element_tag = _get_tag(element)
        if element_tag != 'rtept':
            if header_type == 'wpt':
                header.append(element_tag)
            else:
                header.append(header_type + '_' + element_tag)

    return header


def _get_tag(element):
    return re.sub(r'^{.*?}', '', element.tag)


def _parse_waypoints(waypoint, elements, fieldnames):
    values = []
    values.append(waypoint.attrib['lat'])
    values.append(waypoint.attrib['lon'])

    for element in elements:
        elemnet_tag = _get_tag(element)
        if elemnet_tag == 'link':
            if element.text:
                link_value = '[' + element.text + ']'
            else:
                link_value = '[None]'
            link_value += '(' + element.attrib['href'] + ')'
            values.append(link_value)
        elif elemnet_tag == 'extensions':
            values.append('not support')
        else:
            values.append(element.text)
    return dict(zip(fieldnames, values))


# //TODO: return a list of dict values
def _output_routes(route, elements, waypoints_header, fieldnames, csv_file):
    values = []
    row_count = 0
    for element in elements:
        elemnet_tag = _get_tag(element)
        if elemnet_tag == 'link':
            if element.text:
                link_value = '[' + element.text + ']'
            else:
                link_value = '[None]'
            link_value += '(' + element.attrib['href'] + ')'
            values.append(link_value)
        elif elemnet_tag == 'extensions':
            values.append('not support')
        elif elemnet_tag == 'rtept':
            pass
        else:
            values.append(element.text)
    base_values = values
    for element in elements:
        elemnet_tag = _get_tag(element)
        if elemnet_tag == 'rtept':
            rtept_value = _parse_waypoints(element, element.getchildren(),
                                           waypoints_header)
            values = dict(zip(fieldnames, base_values))
            values.update(rtept_value)
            writer = csv.DictWriter(csv_file, fieldnames)
            writer.writerow(values)
            row_count += 1
    return row_count
