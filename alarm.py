import csv
from itertools import product
import os
import re
import datetime
from os.path import dirname
from log import Logger
import logging
from yaml import FlowMappingEndToken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics
import numpy as np

log_path = dirname(__file__) + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_nezha.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()


metric_threshold_dir = "metric_threshold"


def get_svc(path):
    svc = path.rsplit('-', 1)[0]
    svc = svc.rsplit('-', 1)[0]

    return svc


def generate_threshold(metric_dir, trace_file):
    """
    fun generate_threshold: calculte mean and std for each metric of each servie
    write ruslt to metric_threshold_dir/service.csv
    :parameter
        metric_dir - metric dir in construction phase
    """
    metric_map = {}
    path_list = os.listdir(metric_dir)
    for path in path_list:
        if "metric" in path:
            svc = path.rsplit('-', 1)[0]
            svc = svc.rsplit('-', 1)[0]
            if svc in metric_map:
                metric_map[svc].append(os.path.join(metric_dir, path))
            else:
                metric_map[svc] = [os.path.join(metric_dir, path)]
    for svc in metric_map:
        frames = []

        # get pod name
        for path in path_list:
            if svc in path:
                pod_name = path.split("_")[0]
                print(pod_name)
                network_mean,  network_std = get_netwrok_metric(
                    trace_file=trace_file, pod_name=pod_name)
                break

        metric_threshold_file = metric_threshold_dir + "/" + svc + ".csv"
        for path in metric_map[svc]:
            frames.append(pd.read_csv(path, index_col=False, usecols=[
                'CpuUsageRate(%)', 'MemoryUsageRate(%)', 'SyscallRead', 'SyscallWrite']))
        # concat pods of the same service
        result = pd.concat(frames)
        with open(metric_threshold_file, 'w', newline='') as f:
            writer = csv.writer(f)
            header = ['CpuUsageRate(%)', 'MemoryUsageRate(%)', 'SyscallRead',
                      'SyscallWrite', 'NetworkP90(ms)']
            writer.writerow(header)
            mean_list = []
            std_list = []
            for metric in header:
                if metric == 'NetworkP90(ms)':
                    continue
                mean_list.append(np.mean(result[metric]))
                std_list.append(np.std(result[metric]))
            mean_list.append(network_mean)
            std_list.append(network_std)
            writer.writerow(mean_list)
            writer.writerow(std_list)


def get_netwrok_metric(trace_file, pod_name):
    """
    func get_netwrok_metric: use trace data to get netwrok metric
        :parameter
        time - to regex timestamp e.g, "2022-04-18 13:00"
        data_dir
        pod_name
        :return
        p90 netwrok latency
    """
    latency_list = []

    if "front" in pod_name:
        # front end dose not calculate netwrok latency
        return 10, 10

    pod_reader = pd.read_csv(
        trace_file, index_col='PodName', usecols=['TraceID', 'SpanID', 'ParentID', 'PodName', 'EndTimeUnixNano'])
    parent_span_reader = pd.read_csv(
        trace_file, index_col='SpanID', usecols=['TraceID', 'SpanID', 'ParentID', 'PodName', 'EndTimeUnixNano'])

    try:
        pod_spans = pod_reader.loc[[pod_name], [
            'SpanID', 'ParentID', 'PodName', 'EndTimeUnixNano']]
    except:
        service = pod_name.rsplit('-', 1)[0]
        service = service.rsplit('-', 1)[0]

        csv_file = dirname(__file__) +  "/metric_threshold/" + service + ".csv"
        pod_reader = pd.read_csv(csv_file, usecols=['NetworkP90(ms)'])
        # print("pod", pod_name, " not found in trace, return default ",
        #       float(pod_reader.iloc[0]))

        return float(pod_reader.iloc[0]), 0

    if len(pod_spans['SpanID']) > 0:
        # process span independentlt and order by timestamp
        for span_index in range(len(pod_spans['SpanID'])):
            # span event
            parent_id = pod_spans['ParentID'].iloc[span_index]
            pod_start_time = int(
                pod_spans['EndTimeUnixNano'].iloc[span_index])
            try:
                parent_pod_span = parent_span_reader.loc[[
                    parent_id], ['PodName', 'EndTimeUnixNano']]
                if len(parent_pod_span) > 0:
                    for parent_span_index in range(len(parent_pod_span['PodName'])):
                        parent_pod_name = parent_pod_span['PodName'].iloc[parent_span_index]
                        parent_end_time = int(
                            parent_pod_span['EndTimeUnixNano'].iloc[parent_span_index])

                    if str(parent_pod_name) != str(pod_name):
                        latency = (parent_end_time - pod_start_time) / \
                            1000000  # convert to microsecond
                        # if "contacts-service" in pod_name:
                        #     logger.info("%s, %s, %s, %s, %s" % (
                        #         pod_name, pod_spans['SpanID'].iloc[span_index], parent_pod_name, pod_spans['ParentID'].iloc[span_index], latency))
                        latency_list.append(latency)
            except:
                pass
    # logger.info("%s latency is %s" %(pod_name, np.percentile(latency_list, 90)))
    if len(latency_list) > 2:
        return np.percentile(latency_list, 90), statistics.stdev(latency_list)
    else:
        return 10, 10


def determine_alarm(pod, metric_type, metric_value, std_num, ns):
    """
    fun determine_alarm: determin whether violate 3-sgima
    :parameter
        pod - podname to find corrsponding metric threshold file
        metric_type - find correspding column
        metric_vault - compare with the history mean and std
        std_num - constrol std_num * std
    :return
        true - alarm
        false - no alarm
    """

    path_list = os.listdir(metric_threshold_dir)

    if metric_type == "CpuUsageRate(%)" or metric_type == 'MemoryUsageRate(%)':
        if metric_value > 80:
            return True
    else:

        if ns == "hipster":
            # for hipster
            if metric_value > 200:
                return True
        elif ns == "ts":
            # for ts
            if metric_value > 300:
                return True
    return False
    # for path in path_list:
    #     if re.search(path.split('.')[0], pod):
    #         hisory_metric = pd.read_csv(os.path.join(
    #             metric_threshold_dir, path), index_col=False, usecols=[metric_type])
    #         if metric_value > hisory_metric[metric_type][0] + std_num * hisory_metric[metric_type][1]:
    #             return True
    #         # elif metric_value < hisory_metric[metric_type][0] - std_num * hisory_metric[metric_type][1]:
    #         #     return True
    #         else:
    #             return False


def generate_alarm(metric_list, ns, std_num=6):
    """
    func generate_alarm:  generate alram of each pod at current miniute
    :parameter
        metric_list - metric list from get_metric_with_time

    :return
        alarm_list, e.g., [{'pod': 'cartservice-579f59597d-n69b4', 'alarm': [{'metric_type': 'CpuUsageRate(%)', 'alarm_flag': True}]}]
        [{
            pod:
            alarm: [
                {
                    metric_type: CpuUsageRate(%)
                    alarm_flag: True
                }
            ]
        }]
    """
    alarm_list = []
    for pod_metric in metric_list:
        alarm = {}
        for i in range(len(pod_metric['metrics'])):
            alarm_flag = determine_alarm(pod=pod_metric["pod"], metric_type=pod_metric['metrics'][i]["metric_type"],
                                         metric_value=pod_metric['metrics'][i]["metric_value"], std_num=std_num, ns=ns)
            if alarm_flag:
                # if exist alarm_flag equal to true, create map
                if "pod" not in alarm:
                    alarm = {"pod": pod_metric["pod"], "alarm": []}
                    alarm['alarm'].append(
                        {"metric_type": pod_metric['metrics'][i]["metric_type"], "alarm_flag": alarm_flag})

        if "pod" in alarm:
            alarm_list.append(alarm)

    return alarm_list


def get_metric_with_time(time, base_dir):
    """
    func get_metric_with_time: get metric list at determined miniute
    :parameter
        time - to regex timestamp e.g, "2022-04-18 13:00"
        product_metric_dir
    :return
        target_list - traget metrics
        [
            {
                pod:
                metrics: [
                    {
                        "metric_type":
                        "metric_value":
                    }
                ]
            }

        ]
    """
    date = time.split(' ')[0]
    hour_min = time.split(' ')[1]
    hour = hour_min.split(':')[0]
    min = hour_min.split(':')[1]
    trace_file = base_dir + "/" + date + "/trace/" + hour + "_" + min + "_trace.csv"

    metric_dir = base_dir + "/" + date + "/metric/"

    path_list = os.listdir(metric_dir)

    # metric_list = ['CpuUsageRate(%)', 'MemoryUsageRate(%)', 'SyscallRead',
    #                'SyscallWrite']
    metric_list = ['CpuUsageRate(%)', 'MemoryUsageRate(%)']
    target_list = []
    for path in path_list:
        if "metric" in path:
            metrics = pd.read_csv(os.path.join(metric_dir, path))
            # metrics = pd.read_csv(os.path.join(product_metric_dir, path), index_col=False, usecols=['TimeStamp', 'PodName', 'CpuUsageRate(%)', 'MemoryUsageRate(%)', 'SyscallRead', 'SyscallWrite', 'PodServerLatencyP90(s)', 'PodClientLatencyP90(s)'])
            for index in range(len(metrics['Time'])):
                # regex timestamp
                if re.search(time, metrics['Time'][index]):
                    target_metric = {
                        "pod": metrics['PodName'][index], "metrics": []}
                    for metric in metric_list:
                        target_metric["metrics"].append({
                            "metric_type": metric, "metric_value": metrics[metric][index]})
                    network_p90, _ = get_netwrok_metric(
                        trace_file=trace_file, pod_name=metrics['PodName'][index])
                    target_metric["metrics"].append(
                        {"metric_type": "NetworkP90(ms)", "metric_value": network_p90})
                    target_list.append(target_metric)

    # print(target_list)
    return target_list

