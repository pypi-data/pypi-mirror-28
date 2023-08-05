# coding: utf8
import logging

import jinja2

from kalliope.neurons.uri import Uri

from kalliope.core.Models import Singleton
from six import with_metaclass

from kalliope.core.SynapseLauncher import SynapseLauncher
from kalliope.core.ConfigurationManager import BrainLoader, SettingLoader

logging.basicConfig()
logger = logging.getLogger("kalliope")
logger.setLevel(logging.DEBUG)

brain = BrainLoader().brain
settings = SettingLoader().settings
#
order = "met le chauffage a 16 degres"
# order = "remind me to call mom in three seconds"
SynapseLauncher.run_matching_synapse_from_order(order_to_process=order,
                                                brain=brain,
                                                settings=settings)

# data = "{\"id\": 0,\"jsonrpc\": \"2.0\", \"method\": \"interact::tryToReply\", \"params\": {\"apikey\": \"ISNOTMYPASSWORD\", \"query\": \"met le chauffage a {{valeur}} degres\"}}"
# url = "https://jsonplaceholder.typicode.com/posts"
#
# parameters = {
#     "data": data,
#     "url": url,
#     "method": "POST"
# }
#
# Uri(**parameters)

# dict_parameter = {
#     "valeur": 16
# }
#
# # json_sentence = "{\"id\": \"this is my {{ value }} sentence\"}}"
#
# print(jinja2.Template(data).render(dict_parameter))

