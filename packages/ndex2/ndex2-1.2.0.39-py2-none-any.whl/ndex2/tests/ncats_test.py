import unittest

from ndex2.niceCXNetwork import NiceCXNetwork
from ndex2.cx.aspects.NodeElement import NodeElement
from ndex2.cx.aspects.EdgeElement import EdgeElement
from ndex2.cx.aspects.NodeAttributesElement import NodeAttributesElement
from ndex2.cx.aspects.EdgeAttributesElement import EdgeAttributesElement
from ndex2.cx.aspects import ATTRIBUTE_DATA_TYPE
import ndex2.client as nc
import networkx as nx
import pandas as pd
import os
import ndex2
import cPickle

path_this = os.path.dirname(os.path.abspath(__file__))

my_username = 'scratch'
my_password = 'scratch'
my_server = 'http://dev.ndexbio.org'

path_this = os.path.dirname(os.path.abspath(__file__))

class TestNcats(unittest.TestCase):
    @unittest.skip("Temporary skipping")
    def test_ncats(self):
        G = nx.Graph()
        G.add_node('ABC', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('DEF', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('GHI', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('JKL', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('MNO', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('PQR', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})
        G.add_node('XYZ', attr_dict={'Alpha': '1.234', 'Beta': '9.876'})

        G.add_edge('ABC', 'DEF', attr_dict={'weight': '0.4321'})
        G.add_edge('DEF', 'GHI', attr_dict={'weight': '0.4321'})
        G.add_edge('GHI', 'JKL', attr_dict={'weight': '0.4321'})
        G.add_edge('DEF', 'JKL', attr_dict={'weight': '0.4321'})
        G.add_edge('JKL', 'MNO', attr_dict={'weight': '0.4321'})
        G.add_edge('DEF', 'MNO', attr_dict={'weight': '0.4321'})
        G.add_edge('MNO', 'XYZ', attr_dict={'weight': '0.4321'})
        G.add_edge('DEF', 'PQR', attr_dict={'weight': '0.4321'})

        niceCx = ndex2.create_nice_cx_from_networkx(G)

        niceCx.set_name('NCATS TEMP2')

        upload_message = niceCx.upload_to(my_server, my_username, my_password)

    #import cPickle
    @unittest.skip("Temporary skipping")
    def test_ncats3(self):
        path_to_network = os.path.join(path_this, 'tmp.pkl')
        with open(path_to_network, 'rb') as f:
            tmp2 = cPickle.load(f)
            tmp2.subnetwork_id = 1
            tmp2.upload_to('http://dev.ndexbio.org', 'scratch', 'scratch')
            print 'test'



    @unittest.skip("Temporary skipping")
    def test_ncats2(self):
        niceCx_from_server = ndex2.create_nice_cx_from_server(server='public.ndexbio.org',
        uuid= 'c0e70804-d848-11e6-86b1-0ac135e8bacf') # '8948691b-f4c8-11e7-adc1-0ac135e8bacf')#
        print(niceCx_from_server.get_summary())

        for k, v in niceCx_from_server.nodeAttributes.items():
            for na in v:
                val_type = na.get_data_type()
                if na.get_data_type() == ATTRIBUTE_DATA_TYPE.FLOAT:
                    value = na.get_values()
                    na.set_values(str(value))
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.INTEGER:
                    value = na.get_values()
                    na.set_values(str(value))
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.DOUBLE:
                    value = na.get_values()
                    na.set_values(str(value))
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.LIST_OF_FLOAT:
                    values = na.get_values()
                    na.set_data_type(ATTRIBUTE_DATA_TYPE.STRING)
                    na.set_values("")
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.LIST_OF_INTEGER:
                    values = na.get_values()
                    na.set_data_type(ATTRIBUTE_DATA_TYPE.STRING)
                    na.set_values("")
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.LIST_OF_DOUBLE:
                    values = na.get_values()
                    na.set_data_type(ATTRIBUTE_DATA_TYPE.STRING)
                    na.set_values("")
                elif na.get_data_type() == ATTRIBUTE_DATA_TYPE.LIST_OF_STRING:
                    values = na.get_values()
                    na.set_data_type(ATTRIBUTE_DATA_TYPE.STRING)
                    na.set_values("")
                elif na.get_data_type() == None:
                    value = na.get_values()
                    na.set_values(str(value))
                else:
                    value = na.get_values()
                    na.set_values(str(value))

                print(k)

        niceCx_from_server.upload_to(my_server, my_username, my_password)

    @unittest.skip("Temporary skipping")
    def test_ncats4(self):
        net_client = nc.Ndex2(host='public.ndexbio.org', username='scratch', password='scratch')
        net_set = net_client.get_network_set('0f06f419-68c1-11e7-961c-0ac135e8bacf')
        if net_set.get('networks'):
            for ns in net_set.get('networks'):
                niceCx_from_server = ndex2.create_nice_cx_from_server(server='public.ndexbio.org',
                    uuid=ns)
                #found_network = net_client.get_network_summary(ns)
                print(niceCx_from_server)

    #@unittest.skip("Temporary skipping")
    def test_ncats5(self):

        path_to_network = os.path.join(path_this, 't8d1.csv')

        with open(path_to_network, 'rU') as tsvfile:
            header = [h.strip() for h in tsvfile.readline().split(',')]

            df = pd.read_csv(tsvfile, delimiter=',', engine='python', names=header)

            niceCx = ndex2.create_nice_cx_from_pandas(df, source_field='Gene1', target_field='Gene2',
                                                      source_node_attr=['score'], target_node_attr=['score'], edge_attr=['score'])

            upload_message = niceCx.upload_to(my_server, my_username, my_password)

            print(niceCx)

