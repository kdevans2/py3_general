# ---------------------------------------------------------------------------
# generalARC.py
# Kirk Evans 5/18 TetraTech EC
# Commonly used utility functions related to ARCGIS Pro
#
# Known limitations: python 3
# ---------------------------------------------------------------------------
import arcpy, os, csv

# ---------------------------------------------------------------------------
# general
def message(string):
    print(string)
    arcpy.AddMessage(string)

def warning(string):
    print(string)
    arcpy.AddWarning(string)
    
def error(string):
    print(string)
    arcpy.AddError(string)
    
def DeleteIntermediatesARC(lstDel, bolVerbose = True):
    ''' Delete list of files using arcpy '''
    print('\tDeleting intermediates...')
    for f in lstDel:
        try:
            arcpy.Delete_management(f)
        except Exception:
            if bolVerbose:
                print(f + ' delete failed, skipping.')

# ---------------------------------------------------------------------------
# Raster related
# all raster related arcgis functions now found in:
#   N:\code\kdevans\python3\modules\rasterARCUtility.py
# Keep moved rasterARCUtility functions and classes visible to generalARC
from rasterARCUtility import *

# ---------------------------------------------------------------------------
# Table related   
def Table2CSV(strPathFC, strPathCSV, lstFields = None):
    ''' Export feature class table to CSV text
        Lame work around for failing arcpy.CopyRows function.
        lstFields: optional list of output fields. Default is all fields except
            the geometry field
    '''
    if lstFields is None:
        lstFields = [f.name for f in arcpy.ListFields(strPathFC) if f.type != 'Shape']

    with arcpy.da.SearchCursor(strPathFC, lstFields) as rows:
        with open(strPathCSV, 'wb') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',')
            spamwriter.writerow(lstFields)
            for row in rows:
                spamwriter.writerow(row)
                

def addfieldtype(strTable,strField):
    ''' Return field type as used as addfield keyword. '''
    dictFieldType = {"String":"Text",
                     "Integer":"Long",
                     "SmallInteger":"Short",
                     "OID":"OID",
                     "Geometry":"Geometry",
                     "Single":"Float",
                     "Double":"Double",
                     "Date":"Date",
                     "Blob":"Blob"}

    fld = arcpy.ListFields(strTable, strField)
    if fld:
        strtype = dictFieldType[fld[0].type]
        return strtype
    else:
        raise Exception('field: ' + strField + ' not found')
    

# ---------------------------------------------------------------------------
# Misc
def VertexCount(feat):
    ''' Return vertex count of feature class feat. '''
    with arcpy.da.SearchCursor(feat, ("Shape@", )) as rows:
        lstCounts = [row[0].pointCount for row in rows]
    return sum(lstCounts)


def NonFalse(feat, field):
    ''' Return count of non false evaluations in a field and a total count. '''
    with arcpy.da.SearchCursor(feat, (field, )) as rows:
        i, j = 0, 0
        for row in rows:
            j += 1
            if row[0]:
                i += 1
    return i, j

                
def Topo(strPathFC, strPathFDS, strPathTopo, BoolValidate = None):
    ''' Create a no gaps/no overlaps topology for a feature class.
        creates requisite featuredataset if needed.
        optionally validates topology.
        Returns the location of the new featureclass in the featuredataset.
    '''
    if BoolValidate is None:
        BoolValidate = True

    if os.path.dirname(strPathFC):
        strFC = os.path.basename(strPathFC)
    strGDB, strFDS = os.path.split(strPathFDS)
    strPathFDS_FC = strPathFDS + os.sep + strFC

    if not arcpy.Exists(strPathTopo):
        print('\tCreate FDS and add FC...')
        sr = arcpy.Describe(strPathFC).spatialreference
        if not arcpy.Exists(strPathFDS):
            arcpy.CreateFeatureDataset_management(strGDB, strFDS, sr)
        
        if not arcpy.Exists(strPathFDS_FC):
            arcpy.CopyFeatures_management(strPathFC, strPathFDS_FC)

        print('\tCreate topology and add rules...')
        arcpy.CreateTopology_management(strPathFDS, os.path.basename(strPathTopo))

        arcpy.AddFeatureClassToTopology_management(strPathTopo, strPathFDS_FC, 1)
        arcpy.AddRuleToTopology_management(strPathTopo, 'Must Not Have Gaps (Area)', strPathFDS_FC)
        arcpy.AddRuleToTopology_management(strPathTopo, 'Must Not Overlap (Area)', strPathFDS_FC)

    if BoolValidate:
        print('\tValidate...')
        arcpy.ValidateTopology_management(strPathTopo)

    return strPathFDS_FC
