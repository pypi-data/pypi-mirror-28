PPM_Common 
========================================================

Gives utilities to manage connexion to MongoDB database and Elasticsearch

You can install with pip:

    pip install PPM_Common

Example:

    >>> from PPM_Common import MongoConnexion
    >>> MongoConnexion(pathToConfigFile)

Configuration file looks like :

    {
      "mongodb": {
        "host": "127.0.0.1",
        "host_port": 27017
      },
      "elastic": {
        "host": "127.0.0.1",
        "host_port": 9200,
        "mode":"dev"
      }
    }
