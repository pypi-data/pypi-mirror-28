# GPXConverter
[![Build Status][Build-Badge]][Build-Badge-URL]
[![License][License-Badge]][License-Badge-URL]
## How to use

```
$pip install gpxconverter

$gpxconverter -i <input file> -o <output file>

```
*Note: 'csv' extension is not required for output filename.*

[Install pip if necessary](https://pip.pypa.io/en/latest/installing/)

## Output
It will extract waypoints information from input file to a csv file.

Waypoints will be saved as [output file]\_wpt.csv

Route will be saved as [output file]\_rte.csv

## XSD reference documents
GPX XSD is available at the below link.

[http://www.topografix.com/GPX/1/1](http://www.topografix.com/gpx/1/1/gpx.xsd)

[Build-Badge]:https://travis-ci.org/linusyoung/GPXConverter.svg?branch=master
[Build-Badge-URL]:https://travis-ci.org/linusyoung/GPXConverter
[License-Badge]: https://img.shields.io/badge/license-MIT-blue.svg
[License-Badge-URL]: ./LICENSE.txt
