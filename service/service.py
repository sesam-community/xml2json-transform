import datetime
import json
import os
import sys
import xmltodict
from flask import Flask, request, Response
from sesamutils.flask import serve
from sesamutils import sesam_logger
from sesamutils import VariablesConfig

# Activate logging
logger = sesam_logger("xml2json-transform")

# Fetch env.vars
required_env_vars = [
    "SOURCE_PROPERTY",  # where the XML resides
    "TARGET_PROPERTY"   # where the transformed JSON will be put
]
optional_env_vars = ["LOG_LEVEL", "PORT"]

env_vars = VariablesConfig(required_env_vars, optional_env_vars=optional_env_vars)

port = int(os.getenv("PORT", 5000))

# Check that all required env.vars are supplied
if not env_vars.validate():
    sys.exit(1)


# Start the service
app = Flask(__name__)


def xml_to_json(xml):
    """Transform xml to json"""

    logger.debug("-> xml_to_json()")

    xml_as_dict = xmltodict.parse(xml)
    xml_as_json = json.dumps(xml_as_dict)

    logger.debug("<- xml_to_json()")

    return xml_as_json


@app.route('/transform', methods=['POST'])
def receiver():

    logger.debug(datetime.datetime.now())

    source_property = env_vars.SOURCE_PROPERTY
    target_property = env_vars.TARGET_PROPERTY

    logger.debug(f'source_property: {source_property}')
    logger.debug(f'target_property: {target_property}')

    entities = request.get_json()

    logger.debug(f'source entities: {entities}')
    logger.debug(f'entities type: {type(entities)}')

    for entity in entities:
        logger.debug(f'entity type: {type(entity)}')
        json_data = xml_to_json(entity[source_property])
        entity[target_property] = json.loads(json_data)

    logger.debug(f'result entities: {entities}')

    return Response(json.dumps(entities), mimetype='application/json')


if __name__ == "__main__":
    serve(app, port=port)
