from pattern_ranker import *
import argparse

log_path = dirname(__file__) + '/log/' + str(datetime.datetime.now().strftime(
    '%Y-%m-%d')) + '_nezha.log'
logger = Logger(log_path, logging.DEBUG, __name__).getlog()


def get_miner(ns):
    template_indir = dirname(__file__) + '/log_template'
    config = TemplateMinerConfig()
    config.load(dirname(__file__) + "/log_template/drain3_" + ns + ".ini")
    config.profiling_enabled = False

    path = dirname(__file__) + '/log_template/' + ns + ".bin"
    persistence = FilePersistence(path)
    template_miner = TemplateMiner(persistence, config=config)

    return template_miner

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Nezha')

    parser.add_argument('--ns', default="hipster", help='namespace')
    parser.add_argument('--level', default="service", help='service-level or inner-service level')

    args = parser.parse_args()
    ns = args.ns
    level = args.level

    if ns == "hipster":
        normal_time1 = "2022-08-22 03:51"
        path1 = dirname(__file__) +  "/rca_data/2022-08-22/2022-08-22-fault_list.json"

        normal_time2 = "2022-08-23 17:00"
        path2 = dirname(__file__) +  "/rca_data/2022-08-23/2022-08-23-fault_list.json"

        log_template_miner = get_miner(ns)
        inject_list = [path1, path2]
        normal_time_list = [normal_time1, normal_time2]
        if level=="service":
            logger.info("------- OnlineBoutique Result at service level -------")
            evaluation_pod(normal_time_list, inject_list, ns,log_template_miner)
        else:
            logger.info("------- OnlineBoutique Result at inner service level -------")
            evaluation(normal_time_list, inject_list, ns,log_template_miner)

    elif ns == "ts":
        normal_time1 = "2023-01-29 08:50"
        path1 = dirname(__file__) +  "/rca_data/2023-01-29/2023-01-29-fault_list.json"

        normal_time2 = "2023-01-30 11:39"
        path2 = dirname(__file__) +  "/rca_data/2023-01-30/2023-01-30-fault_list.json"

        log_template_miner = get_miner(ns)
        inject_list = [path1, path2]
        normal_time_list = [normal_time1, normal_time2]

        if level=="service":
            logger.info("------- Trainticket Result at service level -------")
            evaluation_pod(normal_time_list, inject_list, ns,log_template_miner)
        else:
            logger.info("------- Trainticket Result at inner service level -------")
            evaluation(normal_time_list, inject_list, ns,log_template_miner)

    else:
        logger.info("Unknown namespace")
