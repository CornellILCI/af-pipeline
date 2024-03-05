import json

import pytest
from af.pipeline.data_reader.models import ApiResponse

_table_response_body = json.loads("""{
"@context": [
    "https://brapi.org/jsonld/context/metadata.jsonld"
],
"metadata": {
    "datafiles": [
    {
        "fileDescription": "This is an Excel data file",
        "fileMD5Hash": "c2365e900c81a89cf74d83dab60df146",
        "fileName": "datafile.xlsx",
        "fileSize": 4398,
        "fileType": "application/vnd.ms-excel",
        "fileURL": "https://wiki.brapi.org/examples/datafile.xlsx"
    }
    ],
    "pagination": {
    "currentPage": 0,
    "pageSize": 1000,
    "totalCount": 10,
    "totalPages": 1
    },
    "status": [
    {
        "message": "Request accepted, response successful",
        "messageType": "INFO"
    }
    ]
},
"result": {
    "data": [
    [
        "f3a8a3db",
        "Plant Alpha",
        "0fe3e48b",
        "2017 Plant Study",
        "06307ec0",
        "A0043001",
        "76.50106681",
        "42.44409301",
        "2017",
        "Field_1",
        "Plot_11",
        "SubPlot_111",
        "Plant_1111",
        "Pot_1111",
        "Block_11",
        "Entry_11",
        "Rep_11",
        "25.3",
        "3",
        "50.75"
    ],
    [
        "05d1b011",
        "Plant Beta",
        "0fe3e48b",
        "2017 Plant Study",
        "59d435cd",
        "A0043002",
        "76.50106683",
        "42.44409301",
        "2017",
        "Field_1",
        "Plot_11",
        "SubPlot_112",
        "Plant_1122",
        "Pot_1122",
        "Block_11",
        "Entry_11",
        "Rep_12",
        "27.9",
        "1",
        "45.345"
    ],
    [
        "67e2d87c",
        "Plant Gamma",
        "0fe3e48b",
        "2017 Plant Study",
        "06307ec0",
        "A0043001",
        "76.50106681",
        "42.44409356",
        "2017",
        "Field_1",
        "Plot_12",
        "SubPlot_123",
        "Plant_1233",
        "Pot_1233",
        "Block_12",
        "Entry_12",
        "Rep_11",
        "25.5",
        "3",
        "50.76"
    ],
    [
        "d98d0d4c",
        "Plant Epsilon",
        "0fe3e48b",
        "2017 Plant Study",
        "59d435cd",
        "A0043002",
        "76.50106683",
        "42.44409356",
        "2017",
        "Field_1",
        "Plot_12",
        "SubPlot_124",
        "Plant_1244",
        "Pot_1244",
        "Block_12",
        "Entry_12",
        "Rep_12",
        "28.9",
        "0",
        "46.5"
    ]
    ],
    "headerRow": [
    "observationUnitDbId",
    "observationUnitName",
    "studyDbId",
    "studyName",
    "germplasmDbId",
    "germplasmName",
    "positionCoordinateX",
    "positionCoordinateY",
    "year",
    "field",
    "plot",
    "sub-plot",
    "plant",
    "pot",
    "block",
    "entry",
    "rep"
    ],
    "observationVariables": [
    {
        "observationVariableDbId": "367aa1a9",
        "observationVariableName": "Plant height"
    },
    {
        "observationVariableDbId": "2acb934c",
        "observationVariableName": "Carotenoid"
    },
    {
        "observationVariableDbId": "85a21ce1",
        "observationVariableName": "Root color"
    },
    {
        "observationVariableDbId": "46f590e5",
        "observationVariableName": "Virus severity"
    }
    ]
}
}
"""
    )


@pytest.fixture
def brapi_observation_table_api_response_1():
    return ApiResponse(
        http_status=200,
        body=_table_response_body,
        is_success=True
    )
    