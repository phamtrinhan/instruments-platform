import requests
from typing import Any, Optional

import dlt
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import (
    RESTAPIConfig,
    check_connection,
    rest_api_resources,
    rest_api_source,
)

def pokemon_source():
    return rest_api_source(
        config={
            "client": {
                "base_url": "https://pokeapi.co/api/v2/",
                # If you leave out the paginator, it will be inferred from the API:
                # "paginator": "json_link",
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "limit": 1000,
                    },
                },      
                "write_disposition": "replace", # Setting the write disposition to `replace`

            },
            "resources": [
                {
                    "name": "pokemonlist",
                    "endpoint": {
                        "path": "pokemon",
                        "params": {
                            "offset": 0,
                            "limit": 0   
                        }
                    },
                    "primary_key": "name",
                },
                {
                    "name": "pokemons",
                    "endpoint": {
                        "path": "pokemon/{pokemon_name}",
                        "params": {
                            "pokemon_name": {
                                "type": "resolve",
                                "resource": "pokemonlist",
                                "field": "name"
                            }
                        }
                    }
                }
            ],
        },
        parallelized=True
    )

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="rest_api_pokemon",
        destination='filesystem',
        dataset_name="pokemon_dataset",
    )
    load_info = pipeline.run(pokemon_source())
    print(load_info)

