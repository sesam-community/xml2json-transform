# xml2json-transform

Transform string formatted XML into JSON.

## Endpoint

`http://localhost:5000/transform`.

## Environment variables

### Required

`SOURCE_PROPERTY` - where the string formatted XML resides

`TARGET_PROPERTY` - where to put the JSON result

### Optional

`LOG_LEVEL` - Default 'INFO'. Ref: https://docs.python.org/3/howto/logging.html#logging-levels

`PORT` - set this to override default port 5000.

## Example system config

```
{
  "_id": "xml2json-transform",
  "type": "system:microservice",
  "docker": {
    "environment": {
      "LOG_LEVEL": "INFO",
      "PORT": 5001,
      "SOURCE_PROPERTY": "xml-string",
      "TARGET_PROERTY": "json-result"
    },
    "image": "sesamcommunity/xml2json-transform:<version>",
    "port": 5001
  }
}
```

## Example pipe config

```
{
  "_id": "bg-ansatt-transformed",
  "type": "pipe",
  "source": {
    "type": "dataset",
    "dataset": "bg-ansatt"
  },
  "transform": {
    "type": "http",
    "system": "xml2json-transform",
    "url": "/transform"
  }
}
```

## Example input entity

```
{
    "_id": "1234",
    "xml-string": "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><PublishAnsattEntityRequest >    <Ansatt status='Aktiv'>        <PersonID name='PERSON.OBJECTID' idOwner='PUSER'>            <IdValue>123456</IdValue>        </PersonID>        <Personnavn>            <Fulltnavn>John Doe</Fulltnavn></Personnavn>        </Ansatt></PublishAnsattEntityRequest>",
}
```

## Example output entity

```
{
    "_id": "1234",
    "xml-string": "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><PublishAnsattEntityRequest >    <Ansatt status='Aktiv'>        <PersonID name='PERSON.OBJECTID' idOwner='PUSER'>            <IdValue>123456</IdValue>        </PersonID>        <Personnavn>            <Fulltnavn>John Doe</Fulltnavn></Personnavn>        </Ansatt></PublishAnsattEntityRequest>",
    "json-result": {
        "PublishAnsattEntityRequest": {
            "Ansatt": {
                "@status": "Aktiv",
                "PersonID": {
                    "@name": "PERSON.OBJECTID",
                    "@idOwner": "PUSER",
                    "IdValue": "123456"
                },
                "Personnavn": {
                    "Fulltnavn": "John Doe"
                }
            }
        }
    }
}
```
