from lxml import etree as ET
# import model as m

DNX_NS = "http://www.exlibrisgroup.com/dps/dnx"
dnx_nsmap = {
    None: DNX_NS
}

# ET.register_namespace('', DNX_NS)

GENERAL_REP_CHARACTERISTICS = ['label', 'preservationType', 'usageType',
    'representationEntityType', 'contentType', 'contextType', 'hardwareUsed',
    'physicalCarrierMedia', 'derivedFromId', 'deliveryPriority',
    'orderingSequence', 'DigitalOriginal', 'RevisionNumber',
    'RepresentationCode', 'TaskID', 'RepresentationOriginalName',
    'UserDefinedA', 'UserDefinedB', 'UserDefinedC']

GRC = {'label': None, 'preservationType': None, 'usageType': None}


def _build_generic_section(section_name, keynames=None):
    section = ET.Element('section', id=section_name)
    record = ET.SubElement(section, 'record')
    for key in keynames:
        if keynames[key] != None:
            record_key = ET.SubElement(record, 'key', id=key)
            record_key.text = keynames[key]
    return section

def _build_generic_repeatable_section(section_name, allowed_keys, *args):
    section = ET.Element('section',
        id=section_name)
    # args = args[0]
    for arg in args:
        record = ET.SubElement(section, 'record')
        for key in arg.keys():
            if key in allowed_keys:
                record_key = ET.SubElement(record, 'key')
                record_key.attrib['id'] = key
                record_key.text = arg[key]
            else:
                raise ValueError("""\"{}\" is not a permitted key in {} 
                    record dictionary ( acceptable values are {} )
                    """.format(key, section_name, allowed_keys))
    return section

def build_generalIECharacteristics(submissionReason=None, status=None,
        statusDate=None, IEEntityType=None, UserDefinedA=None,
        UserDefinedB=None, UserDefinedC=None):
        # Note: statusDate is used by the system - not really for pre-ingest use
        
    return _build_generic_section('generalIECharacteristics', locals())


def build_generalRepCharacteristics(label=None, preservationType=None, 
        usageType=None, representationEntityType=None, contentType=None,
        contextType=None, hardwareUsed=None, physicalCarrierMedia=None,
        derivedFromId=None, deliveryPriority=None, orderingSequence=None,
        DigitalOriginal=None, RevisionNumber=None, RepresentationCode=None,
        TaskID=None, RepresentationOriginalName=None, UserDefinedA=None, 
        UserDefinedB=None, UserDefinedC=None):
        # Mandatory: preservationType, usageType(only "VIEW" supported)
    return _build_generic_section('generalRepCharacteristics', locals())



def build_generalFileCharacteristics(label=None, note=None,
        FileEntityType=None, compositionLevel=None, fileLocationType=None, 
        fileLocation=None, fileOriginalName=None,
        fileOriginalPath=None, fileOriginalID=None, fileExtension=None,
        fileMIMEType=None, fileSizeBytes=None, storageID=None, 
        streamRefId=None, formatLibraryId=None, riskLibraryIdentifiers=None,
        fileCreationDate=None, fileModificationDate=None):
        # Note: fileLocationType is used by the system - not really for pre-ingest use
        # Note: fileOriginalID is used by the system - not really for pre-ingest use
        # Note: fileExtension is used by the system - not really for pre-ingest use
        # Note: formatLibraryId is used by the system - not really for pre-ingest use
        # Note: riskLibraryIdentifiers is used by the system - not really for pre-ingest use
        # fileMIMEType can be submitted by user, or it will be set by system on ingest
        # fileSizeBytes can be submitted by user, or it will be set by system on ingest
        # Note: storageID and streamRefId currently not in use
    return _build_generic_section('generalFileCharacteristics', locals())


def build_objectCharacteristics(objectType=None, groupID=None):
    # parentID - set during loading stage
    # creationDate - set during loading stage
    # createdBy - set during loading stage
    # modificationDate - set in system, on committing new version
    # modifiedBy - set in system, on committing new version
    # owner - set in system during loading stage
    return _build_generic_section('objectCharacteristics', locals())

def build_cms(system=None, recordId=None):
    # mId = system-generated
    return _build_generic_section('CMS', locals())

def build_webHarvesting(primarySeedURL=None, WCTIdentifier=None,
        targetName=None, group=None, harvestDate=None, harvestTime=None):
    return _build_generic_section('webHarvesting', locals())

# internalIdentifier -- Not used for pre-ingest

def build_objectIdentifier(objectIdentifierType=None, 
            objectIdentifierValue=None):
    return _build_generic_section('objectIdentifier', locals())


def build_preservationLevel(preservationLevelValue=None, 
        preservationLevelRole=None, preservationLevelRationale=None,
        preservationLevelDateAssigned=None):
    return _build_generic_section('preservationLevel', locals())


def build_significantProperties(*args):
    allowed_keys = ['significantPropertiesType', 'significantPropertiesValue',
                    'significantProperiesExtension']
    return _build_generic_repeatable_section('significantProperties', 
        allowed_keys, *args)

def build_fileFixity(*args):
    allowed_keys = ['agent', 'fixityType', 'fixityValue']
    return _build_generic_repeatable_section('fileFixity', allowed_keys,
        *args)

def build_creatingApplication(creatingApplicationName=None,
        creatingApplicationVersion=None,
        dateCreatedByApplication=None,
        creatingApplicationExtension=None):
    return _build_generic_section('creatingApplication', locals())


def build_inhibitors(*args):
    allowed_keys = ['inhibitorType', 'inhibitorTarget', 'inhibitorKey']
    return _build_generic_repeatable_section('inhibitors', allowed_keys,
        *args)

def build_objectCharacteristicsExtension(objectCharacteristicsExtension=None):
    return _build_generic_section('objectCharacteristicsExtension', locals())


def build_environment(*args):
    allowed_keys = ['environmentCharacteristic', 'environmentPurpose',
        'environmentNote']
    return _build_generic_repeatable_section('environment', allowed_keys,
        *args)


def build_environmentDependencies(*args):
    allowed_keys = ['dependencyName', 'dependencyIdentifierValue1',
        'dependencyIdentifierValue1', 'dependencyIdentifierType2',
        'dependencyIdentifierType2', 'dependencyIdentifierValue3',
        'dependencyIdentifierType3']
    return _build_generic_repeatable_section('environmentDependencies', 
            allowed_keys, *args)

def build_environmentSoftware(*args):
    allowed_keys = ['softwareName', 'softwareVersion', 'softwareType',
        'softwareOtherInformation', 'softwareOtherInformation',
        'softwareDependancy']
    return _build_generic_repeatable_section('environmentSoftware',
            allowed_keys, *args)

def build_environmentSoftwareRegistry(*args):
    return _build_generic_repeatable_section('environmentSoftwareRegistry',
        ['registryId'], *args)

def build_environmentHardware(*args):
    allowed_keys = [
        'hardwareName', 
        'hardwareType',
        'hardwareOtherInformation'
        ]
    return _build_generic_repeatable_section('environmentHardware',
        allowed_keys, *args)

def build_envHardwareRegistry(*args):
    return _build_generic_repeatable_section('environmentSoftwareRegistry',
        ['registryId'], *args)

def build_environmentExtension(*args):
    return _build_generic_repeatable_section('environmentExtension',
        ['environmentExtension'], *args)

def build_signatureInformation(*args):
    allowed_keys = [
        'signatureInformationEncoding','signer','signatureMethod',
        'signatureValue', 'signatureValidationRules', 'signatureProperties',
        'keyInformation'
        ]
    return _build_generic_repeatable_section('signatureInformation',
        allowed_keys, *args)

def build_signatureInformationExtension(signatureInformationExtension=None):
    return _build_generic_section('signatureInformationExtension', locals())



def build_relationship(*args):
    allowed_keys = ['relationshipType', 'relationshipSubType',
        'relatedObjectIdentifierType1', 'relatedObjectIdentifierValue1',
        'relatedObjectSequence1', 'relatedObjectIdentfierType2',
        'relatedObjectIdentifierValue2', 'relatedObjectSequence2',
        'relatedObjectIdentifierType3', 'relatedObjectIdentifierValue3',
        'relatedObjectSequence3']
    return _build_generic_repeatable_section('relationship', allowed_keys,
        *args)


def build_linkingIEIdentifier(*args):
    allowed_keys = ['linkingIEIdentifierType', 'linkingIEIdentifierValue']
    return _build_generic_repeatable_section('linkingIEIdentifier',
        allowed_keys, *args)

def build_event(*args):
    allowed_keys = [
        'eventIdentifierType', 'eventIdentifierValue','eventType',
        'eventDescription', 'eventDateTime', 'eventOutcome1',
        'eventOutcomeDetail1', 'eventOutcomeDetailExtension1',
        'eventOutcome2', 'eventOutcomeDetail2',
        'eventOutcomeDetailExtension2', 'eventOutcome2',
        'eventOutcomeDetail2', 'eventOutcomeDetailExtension2',
        'linkingAgentIdentifierXMLID1', 'linkingAgentIdentifierType1',
        'linkingAgentIdentifierValue1', 'linkingAgentRole1',
        'linkingAgentIdentifierXMLID2', 'linkingAgentIdentifierType2',
        'linkingAgentIdentifierValue2', 'linkingAgentRole2',
        'linkingAgentIdentifierXMLID3', 'linkingAgentIdentifierType3',
        'linkingAgentIdentifierValue3', 'linkingAgentRole3']
    return _build_generic_repeatable_section('event', allowed_keys, *args)


def build_linkingRightsStatementIdentifier(*args):
    allowed_keys = ['linkingRightsStatementIdentifierType', 
        'linkingRightsStatementIdentifierValue']
    return _build_generic_repeatable_section(
            'linkingRightsStatementIdentifier',
            allowed_keys,
            *args)

def build_accessRightsPolicy(policyId=None, policyParameters=None,
        policyDescription=None):
    return _build_generic_section('accessRightsPolicy', locals())


def build_retentionPeriodPolicy(policyId=None, policyDescription=None):
    return _build_generic_section('retentionPeriodPolicy', locals())

def build_grantedRightsStatement(*args):
    allowed_keys = ['grantedRightsStatementIdentifier', 
        'grantedRightsStatementValue']
    return _build_generic_repeatable_section('grantedRightsStatement',
        allowed_keys, *args)


def build_collection(*args):
    allowed_keys = ['collectionID', 'collectionName', 'externalSystem',
        'externalRecordId', 'parentCollectionId']
    return _build_generic_repeatable_section('collection', allowed_keys,
        *args)


# generic builders for various DNX sections


def build_generic_amdSection(non_repeatable_keys, repeatable_keys, **kwargs):
    dnx = ET.Element('dnx', nsmap=dnx_nsmap)
    for key, value in kwargs.items():
        if key in non_repeatable_keys:
            if (value != None) and (len(value) == 1):
                # print("DEBUG: key={}, value={}".format(key, value))
                dnx.append(non_repeatable_keys[key](**value[0]))
            elif (value != None):
                raise ValueError("{} is non-repeatable, and may only" + 
                    " contain one dictionary of values")
        if (key in repeatable_keys) and (value != None):
            dnx.append(repeatable_keys[key](*value))
    return dnx

def build_ie_amdTech(**kwargs):
    non_repeatable_keys = {
        'generalIECharacteristics': build_generalIECharacteristics,
        'objectCharacteristics': build_objectCharacteristics,
        'CMS': build_cms,
        'objectIdentifier': build_objectIdentifier,
        'webHarvesting': build_webHarvesting
    }
    repeatable_keys = {}
    return build_generic_amdSection(non_repeatable_keys, repeatable_keys,
        **kwargs)

def build_rep_amdTech(**kwargs):
    non_repeatable_keys = {
        'generalRepCharacteristics': build_generalRepCharacteristics,
        'objectCharacteristics': build_objectCharacteristics
    }
    repeatable_keys = {}
    return build_generic_amdSection(non_repeatable_keys, repeatable_keys,
        **kwargs)

def build_file_amdTech(**kwargs):
    non_repeatable_keys = {
        'generalFileCharacteristics': build_generalFileCharacteristics,
        'objectCharacteristics': build_objectCharacteristics,
        'creatingApplication': build_creatingApplication,
        'signatureInformation': build_signatureInformation }
    repeatable_keys = {
        'fileFixity': build_fileFixity,
        'significantProperties': build_significantProperties,
        'inhibitors': build_inhibitors,
    'objectCharacteristicsExtension': build_objectCharacteristicsExtension,
        'environment': build_environment, 
        'environmentDependencies': build_environmentDependencies,
        'environmentSoftwareRegistry': build_environmentSoftwareRegistry,
        'environmentHardware': build_environmentHardware,
        'envHardwareRegistry': build_envHardwareRegistry,
        'environmentExtension': build_environmentExtension,
        'signatureInformationExtension': build_signatureInformationExtension,
        'relationship': build_relationship}
    return build_generic_amdSection(non_repeatable_keys,
                                    repeatable_keys,
                                    **kwargs)
    
def build_ie_amdRights(**kwargs):
    non_repeatable_keys = {'accessRightsPolicy': build_accessRightsPolicy}
    repeatable_keys = {}
    return build_generic_amdSection(non_repeatable_keys,
                                    repeatable_keys,
                                    **kwargs)

def build_ie_amdDigiprov(**kwargs):
    non_repeatable_keys = {}
    repeatable_keys = {'event': build_event}
    return build_generic_amdSection(non_repeatable_keys,
                                    repeatable_keys,
                                    **kwargs)