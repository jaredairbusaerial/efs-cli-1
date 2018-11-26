import arcgis
import csv
import time
import pandas as pd
import click
from arcgis.features import FeatureLayerCollection
from tqdm import tqdm
from pyproj import Proj, transform

@click.command()
@click.argument('fs_url')
@click.option('--waittime', default=-1.0,
            help='Wait time to call get attachment api for a specific feature object Id')
@click.argument('output', type=click.File('w'),default='-',required=False)
def cli(fs_url,output,waittime):
    """Process the Fire Structure Damage ESRI Feature Service to generate CSV file with location, structure status and attachments Web URLs"""
  # fs_url = 'https://services1.arcgis.com/jUJYIo9tSA7EHvfZ/ArcGIS/rest/services/Camp2018_DINS_Public_View_Pictures/FeatureServer'
    flc = FeatureLayerCollection(fs_url)
    fl = flc.layers[0]
    rs = fl.query(where='1=1')
    writer = csv.writer(output, lineterminator='\n')
    writer.writerow(['Damage','Structure Type','Lat','Lon','Photol','Photo2','Photo3'])
    for feature in tqdm(rs.features):
        aId = None
        aUrl = None
        objId = feature.attributes['OBJECTID']
        attachs = fl.attachments.get_list(objId)
        aUrl1 = "None"
        aUrl2 = "None"
        aUrl3 = "None"
        if (len(attachs) > 0):
            aId = attachs[0]['id']
            aUrl1 = fs_url + '/0/' + str(objId) + '/attachments/' + str(aId)
        if (len(attachs) > 1):
            aId = attachs[1]['id']
            aUrl2 = fs_url + '/0/' + str(objId) + '/attachments/' + str(aId)
        if (len(attachs) > 2):
            aId = attachs[2]['id']
            aUrl3 = fs_url + '/0/' + str(objId) + '/attachments/' + str(aId)
        lon,lat = transform(Proj(init='epsg:3857'), Proj(init='epsg:4326'), feature.geometry['x'], feature.geometry['y'])
        tup =feature.attributes['DAMAGE'],feature.attributes['STRUCTURETYPE'],lat,lon,aUrl1,aUrl2,aUrl3
        if (waittime > 0):
            time.sleep(waittime)
        writer.writerow(tup)

