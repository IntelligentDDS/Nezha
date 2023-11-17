import datetime
from data_integrate import *

log_path = dirname(__file__) + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_nezha.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()


# def frequent_pattern_miner(event_sequences):
#     """
#     mining frequent pattern in event sequences (Discard)
#     input:
#         - event_sequences: event sequences belonging to the traces in time window, e.g., [[1,2,3],[2,3,4]]
#     output:
#         - pattern: frequent_pattern in the events, e.g.,  [['54', '29', '#SUP: 9'], ['54', '30', '#SUP: 9'], ['54', '32', '#SUP: 9']]
#     """
#     print(datetime.datetime.now())

#     spmf_path = dirname(__file__) + "/spmf"
#     spmf = Spmf("CM-SPAM", input_direct=event_sequences,
#                 output_filename="./spmf/SPAM.txt", arguments=[0.01, 2, 2], spmf_bin_location_dir=spmf_path, memory=8192)
#     spmf.run()
#     pattern = spmf.parse_output()
#     print(pattern)
#     print(datetime.datetime.now())
#     return pattern


# def frequent_graph_miner(file_name, topk=30):
#     """
#     mining frequent graph in event graph
#     input:
#         - file_name: input filename e.g.,
#     output:
#         - pattern_list: frequent_child_graph_list [{'support': '519', 'node1': '180', 'node2': '264'}]
#     """

#     # print(datetime.datetime.now())

#     spmf_path = dirname(__file__) + "/spmf"
#     spmf = Spmf("TKG", input_filename=file_name,
#                 output_filename="./spmf/tkg.txt", arguments=[topk, 2, False, False, True], spmf_bin_location_dir=spmf_path, memory=8192)
#     spmf.run()
#     pattern_result = spmf.parse_output()

#     # print(pattern_result)
#     # print(datetime.datetime.now())

#     pattern_list = []
#     for i in range(0, len(pattern_result), 6):
#         """ parse ['t # 29 * 519'], ['v 0 5'], ['v 1 265'], ['e 0 1 1'] """
#         support = pattern_result[i][0].split(' ')[-1]
#         node1 = pattern_result[i+1][0].split(' ')[-1]
#         node2 = pattern_result[i+2][0].split(' ')[-1]
#         pattern = {"support": support, "child_graph": node1 + "_" + node2}
#         pattern_list.append(pattern)

#     pattern_list.sort(key=lambda k: k['support'], reverse=True)

#     return pattern_list


# def generate_tkg_input(event_graphs):
#     """
#     generate_tkg_input:
#     :parameter
#         event_graphs - graph list
#     :return
#         file_name - tkg input filename

#     details see at https://www.philippe-fournier-viger.com/spmf/TKG.php
#     t # 0
#     v 0 10
#     v 1 11
#     e 0 1 20
#     """
#     file_name = dirname(__file__) + "/spmf/" + str(datetime.datetime.now().strftime(
#         '%Y-%m-%d')) + "_tkg_input.txt"
#     f = open(file_name, "w")

#     graph_number = 0
#     node_number = 0

#     for graph in event_graphs:
#         # write head
#         graph_head = "t # " + str(graph_number) + "\r\n"
#         f.write(graph_head)

#         node_map = {}
#         node_content = ""
#         edge_content = ""
#         for key in graph.adjacency_list.keys():
#             if key.event not in node_map:
#                 node_map[key.event] = node_number
#             node_content += "v " + \
#                 str(node_number) + " " + str(key.event) + "\r\n"
#             node_number += 1

#             for event in graph.adjacency_list[key]:
#                 if event.event not in node_map:
#                     node_map[event.event] = node_number
#                 node_content += "v " + \
#                     str(node_number) + " " + str(event.event) + "\r\n"
#                 node_number += 1

#                 edge_content += "e " + \
#                     str(node_map[key.event]) + " " + \
#                     str(node_map[event.event]) + " 1\r\n"

#         f.write(node_content)
#         f.write(edge_content)
#         graph_number += 1
#         f.write("\r\n")
#     f.close()

#     return file_name


def get_pattern_support(event_graphs):
    result_support_dict = {}
    total_pair = set()

    for event_graph in event_graphs:
        for key, value in event_graph.support_dict.items():
            if key in total_pair:
                result_support_dict[key] += value
            else:
                result_support_dict[key] = value
        total_pair = total_pair | event_graph.pair_set

    result_support_dict = dict(sorted(
        result_support_dict.items(), key=lambda x: x[1], reverse=True))

    return result_support_dict

