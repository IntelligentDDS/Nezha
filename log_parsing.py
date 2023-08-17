# -*- coding: utf-8 -*-
#!/usr/bin/env python
import pdb
from email import message
import os
import re
import json
import logging
import datetime
import pandas as pd

from log import Logger
from os.path import dirname
from drain3 import TemplateMiner
from drain3.file_persistence import FilePersistence
from drain3.template_miner_config import TemplateMinerConfig


log_path = dirname(__file__) + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_nezha.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()




def log_parsing(log, pod, log_template_miner,logrca=False):
    """
    func log_parsing
    parse log by drain3
    :parameter
        log - init log
        pod - podname
    :return
        cluster_id

    The output of drain3:
        change_type - indicates either if a new template was identified, an existing template was changed or message added to an existing cluster.
        cluster_id - Sequential ID of the cluster that the log belongs to.
        cluster_size- The size (message count) of the cluster that the log belongs to.
        cluster_count - Count clusters seen so far.
        template_mined- the last template of above cluster_id.
    """
    log_message, service = pod_to_service(log, pod)

    # logger.info(service + " Log message: " + log_message)

    if logrca:
        log_message = log_message + "_" + pod

    result = log_template_miner.add_log_message(log_message)

    if result["change_type"] != "none":
        result_json = json.dumps(result)
        # logger.info(service)
        logger.info(service + " Log Parings Result: " + result_json)

    return result['cluster_id']


def from_id_to_template(id,log_template_miner):
    """
    fun from_id_to_template: change template id to template content
    :parameter
        id - template id
    :return
        template - template content
    """
    # pdb.set_trace()
    # sorted_clusters = sorted(template_miner.drain.clusters,
    #                          key=lambda it: it.cluster_id, reverse=False)
    # id = int(id)
    for cluster in log_template_miner.drain.clusters:
        if cluster.cluster_id == id:
            # logger.info(cluster.get_template())
            return cluster.get_template()
    logger.error("Cannot find id %d 's template" % id)
    return ""


def pod_to_service(log, pod):
    """
    func pod_to_service
    regex service from pod name, regex logs message from log by json
    : parameter
        log - init log
        pod - podname
    : return
        log message
        service name
    """
    service = ""
    log_message = ""
    try:
        if re.search(r'adservice', pod):
            service = "adservice"
            # "{""log"":""TraceID: 00372df3bf20cf3eebd15423736e205b SpanID: 702371dc44d0f544 GetCartAsync called with userId=a009eb0b-68f6-48cd-9c7f-93ca74f1ddce\n"",""stream"":""stdout"",""time"":""2022-04-15T23:59:55.944837597Z""}"
            log_message = json.loads(log)['log']
        elif re.search(r'cartservice', pod):
            service = 'cartservice'
            log_message = json.loads(log)['log']
        elif re.search(r'checkoutservice', pod):
            service = 'checkoutservice'
            # "{""log"":""{\""message\"":\""TraceID: bc0149298d10ab94fd332037e32e68aa SpanID: 0137a7322c7d77fd PlaceOrder user_id=\\\""2ae2c9a6-6592-4ea3-8a36-f3d9af17d789\\\"" user_currency=\\\""USD\\\"" successfully\"",\""severity\"":\""info\"",\""timestamp\"":\""2022-04-15T23:59:15.187736033Z\""}\n"",""stream"":""stdout"",""time"":""2022-04-15T23:59:15.187788923Z""}"
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'currencyservice', pod):
            # "{""log"":""{\""severity\"":\""info\"",\""time\"":\""2022-04-15T23:59:43.066Z\"",\""pid\"":1,\""hostname\"":\""currencyservice-cf787dd48-nk84m\"",\""name\"":\""currencyservice-server\"",\""message\"":\""TraceID: 00ee170a2bdc4789137436834674f9ff SpanID: cc3cbbc725c08982 Conversion request successful\"",\""v\"":1}\n"",""stream"":""stdout"",""time"":""2022-04-15T23:59:43.066467543Z""}"
            service = 'currencyservice'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'emailservice', pod):
            service = 'emailservice'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'frontend', pod):
            service = 'frontend'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'paymentservice', pod):
            service = 'paymentservice'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'productcatalogservice', pod):
            service = 'productcatalogservice'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'recommendationservice', pod):
            service = 'recommendationservice'
            # "{""log"":""{\""timestamp\"": \""2022-04-15T23:59:43.076471Z\"", \""severity\"": \""INFO\"", \""name\"": \""recommendationservice-server\"", \""message\"": \""TraceID: 00ee170a2bdc4789137436834674f9ff SpanID: 6ed521e0cf0c7e67 List Recommendations product_ids=['0PUK6V6EV0', '1YMWWN1N4O', '9SIQT8TOJO', 'LS4PSXUNUM', 'L9ECAV7KIM']\""}\n"",""stream"":""stdout"",""time"":""2022-04-15T23:59:43.076629973Z""}"
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'shippingservice', pod):
            service = 'shippingservice'
            log_message = json.loads(json.loads(log)['log'])['message']
        elif re.search(r'alarm', pod):
            service = 'alarm'
            log_message = log
        elif re.search(r'ts-', pod):
            service = pod.rsplit('-', 1)[0]
            service = service.rsplit('-', 1)[0]
            # "{""log"":""TraceID: 00372df3bf20cf3eebd15423736e205b SpanID: 702371dc44d0f544 GetCartAsync called with userId=a009eb0b-68f6-48cd-9c7f-93ca74f1ddce\n"",""stream"":""stdout"",""time"":""2022-04-15T23:59:55.944837597Z""}"
            log_message = json.loads(log)['log']

            if len(re.findall(r"  (.+?#.+?) ", log_message)) > 0:
                log_message = re.findall(
                    r"  (.+?#.+?) ", log_message)[0]
            elif len(re.findall(r" (.+?#.+?) ", log_message)) > 0:
                log_message = re.findall(
                    r" (.+?#.+?) ", log_message)[0]
            else:
                logger.error(
                    "Regex failed: ", str(log_message))
        else:
            logger.fatal("Unknown pod %s" % (pod))

        return log_message.rstrip(), service

    except (Exception):
        # if json.loads failed, return log directly
        return log.rstrip(), service


if __name__ == '__main__':
    # 指定文件夹的路径
    for  i in range(0,4):
        ns = "hipster"
        config.load(dirname(__file__) + "/log_template/drain3_" + ns + ".ini")
        config.profiling_enabled = False

        path = dirname(__file__) + '/log_template/' + ns + ".bin"
        persistence = FilePersistence(path)
        template_miner = TemplateMiner(persistence, config=config)
        folder_path_list = ['./rca_data/2022-08-22/log','./rca_data/2022-08-23/log']

        for folder_path in folder_path_list:    
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    log_file = os.path.join(root, file) 
                    print(log_file)          
                    log_reader = pd.read_csv(log_file, index_col=False, usecols=[
                        'PodName', 'TimeUnixNano', 'Log'])
                    for i in range(1, len(log_reader['Log'])):
                        log_parsing(log=log_reader['Log'][i], pod=log_reader['PodName'][i], log_template_miner=template_miner)

        # ns = "ts"
        # config.load(dirname(__file__) + "/log_template/drain3_" + ns + ".ini")
        # config.profiling_enabled = False

        # path = dirname(__file__) + '/log_template/' + ns + ".bin"
        # persistence = FilePersistence(path)
        # template_miner = TemplateMiner(persistence, config=config)
        # folder_path_list = ['./rca_data/2023-01-29/log', './rca_data/2023-01-30/log']

        # for folder_path in folder_path_list:    
        #     for root, dirs, files in os.walk(folder_path):
        #         for file in files:
        #             log_file = os.path.join(root, file) 
        #             print(log_file)          
        #             log_reader = pd.read_csv(log_file, index_col=False, usecols=[
        #                 'PodName', 'TimeUnixNano', 'Log'])
        #             for i in range(1, len(log_reader['Log'])):
        #                 log_parsing(log=log_reader['Log'][i], pod=log_reader['PodName'][i], log_template_miner=template_miner)
    
