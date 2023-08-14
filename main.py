from pattern_ranker import *
log_path = dirname(__file__) + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_nezha.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()

if __name__ == '__main__':
    # normal_time1 = "2022-08-22 03:51"
    # path1 = dirname(__file__) +  "/rca_data/2022-08-22/2022-08-22-fault_list.json"

    # normal_time2 = "2022-08-23 17:00"
    # path2 = dirname(__file__) +  "/rca_data/2022-08-23/2022-08-23-fault_list.json"

    # ns = "hipster"

    # logger.info("------- OnlineBoutique Result at inner service level -------")
    # inject_list = [path1, path2]
    # normal_time_list = [normal_time1, normal_time2]
    # evaluation(normal_time_list, inject_list, ns)

    # logger.info("------- OnlineBoutique Result at service level -------")
    # inject_list = [path1, path2]
    # normal_time_list = [normal_time1, normal_time2]
    # evaluation_pod(normal_time_list, inject_list, ns)

    normal_time1 = "2023-01-29 08:50"
    path1 = dirname(__file__) +  "/rca_data/2023-01-29/2023-01-29-fault_list.json"

    normal_time2 = "2023-01-30 11:39"
    path2 = dirname(__file__) +  "/rca_data/2023-01-30/2023-01-30-fault_list.json"

    ns = "ts"

    inject_list = [path1, path2]
    normal_time_list = [normal_time1, normal_time2]

    logger.info("------- Trainticket Result at inner service level -------")
    evaluation(normal_time_list, inject_list, ns)

    logger.info("------- Trainticket Result at service level -------")
    evaluation_pod(normal_time_list, inject_list, ns)
