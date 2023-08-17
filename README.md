# Nezha

This repository is the basic implementation of our publication in `FSE'23` conference paper `Nezha: Interpretable Fine-Grained Root Causes Analysis for Microservices on Multi-Modal Observability Data`

## Description

`Nezha` is an interpretable and fine-grained RCA approach that pinpoints root causes at the code region and resource type level by incorporative analysis of multimodal data. `Nezha` transforms heterogeneous multi-modal data into a homogeneous event representation and extracts event patterns by constructing and mining event graphs. The core idea of `Nezha` is to compare event patterns in the fault-free phase with those in the fault-suffering phase to localize root causes in an interpretable way. 

## Quick Start

### Requirements 

- Python3.6 is recommended to run the anomaly detection. Otherwise, any python3 version should be fine.
- Git is also needed.

### Setup
`python3 -m pip install -r requirements.txt` to install the dependency for Nezha


### Running  Nezha

#### OnlineBoutique at service level


```
python3.6 ./main.py --ns hipster --level service 

pattern_ranker.py:622: -------- hipster Fault numbuer : 56-------
pattern_ranker.py:623: --------AS@1 Result-------
pattern_ranker.py:624: 92.857143 %
pattern_ranker.py:625: --------AS@3 Result-------
pattern_ranker.py:626: 96.428571 %
pattern_ranker.py:627: --------AS@5 Result-------
pattern_ranker.py:628: 96.428571 %
```

#### OnlineBoutique at inner service level

```
python3.6 ./main.py --ns hipster --level inner

pattern_ranker.py:622: -------- hipster Fault numbuer : 56-------
pattern_ranker.py:623: --------AIS@1 Result-------
pattern_ranker.py:624: 92.857143 %
pattern_ranker.py:625: --------AIS@3 Result-------
pattern_ranker.py:626: 96.428571 %
pattern_ranker.py:627: --------AIS@5 Result-------
pattern_ranker.py:628: 96.428571 %
```

#### Trainticket at service level

```
python3.6 ./main.py --ns ts --level service

pattern_ranker.py:622: -------- ts Fault numbuer : 45-------
pattern_ranker.py:623: --------AS@1 Result-------
pattern_ranker.py:624: 86.666667 %
pattern_ranker.py:625: --------AS@3 Result-------
pattern_ranker.py:626: 97.777778 %
pattern_ranker.py:627: --------AS@5 Result-------
pattern_ranker.py:628: 97.777778 %
```

#### Trainticket at inner service level

```
python3.6 ./main.py --ns ts --level inner

pattern_ranker.py:622: -------- ts Fault numbuer : 45-------
pattern_ranker.py:623: --------AIS@1 Result-------
pattern_ranker.py:624: 86.666667 %
pattern_ranker.py:625: --------AIS@3 Result-------
pattern_ranker.py:626: 97.777778 %
pattern_ranker.py:627: --------AIS@5 Result-------
pattern_ranker.py:628: 97.777778 %
```

The details of service level results and inner-service level results will be printed and recorded in `./log`

## Dataset 

[2022-08-22](./rca_data/2022-08-22/) and [2022-08-23](./rca_data/2022-08-23/) is the fault-suffering dataset of OnlineBoutique


[2023-01-29](./rca_data/2023-01-29/) and [2023-01-30](./rca_data/2023-01-30/) is the fault-suffering dataset of Trainticket

### Fault-free data

[construct_data](./construct_data/)  is the data of fault-free phase 

[root_cause_hipster.json](./construct_data/root_cause_hipster.json) is the inner-servie level label of root causes in OnlineBoutique

[root_cause_ts.json](./construct_data/root_cause_ts.json) is the inner-servie level label of root causes in Trainticket

As an example,

```
    "checkoutservice": {
        "return": "Start charge card_Charge successfully",
        "exception": "Start charge card_Charge successfully",
        "network_delay": "NetworkP90(ms)",
        "cpu_contention": "CpuUsageRate(%)",
        "cpu_consumed": "CpuUsageRate(%)"
    },
```

The label of `checkoutservice` means that the label `return` fault of `checkoutservice` is core regions between log statement contains  `Start charge card` and `Charge successfully`. 


### Fault-suffering Data

[rca_data](./rca_data/) is the data of fault-suffering phase

[2022-08-22-fault_list](./rca_data/2022-08-22-fault_list) and [2022-08-23-fault_list](./rca_data/2022-08-23-fault_list) is the servie level label of root causes in OnlineBoutique

[2023-01-29-fault_list](./rca_data/2022-01-29-fault_list) and [2022-01-30-fault_list](./rca_data/2022-01-30-fault_list) is the servie level label of root causes in TrainTicket


## Project Structure
```
.
├── LICENSE
├── README.md
├── construct_data
│   ├── 2022-08-22
│   │   ├── log
│   │   ├── metric
│   │   ├── trace
│   │   └── traceid
│   ├── 2022-08-23
│   ├── 2023-01-29
│   ├── 2023-01-30
│   ├── root_cause_hipster.json: label at inner-service level for hipster
│   └── root_cause_ts.json: label at inner-service level for ts
├── rca_data
│   ├── 2022-08-22
│   │   ├── log
│   │   ├── metric
│   │   ├── trace
│   │   ├── traceid
│   │   └── 2022-08-22-fault_list.json: label at service level
│   ├── 2022-08-23
│   ├── 2023-01-29
│   └── 2023-01-30
├── log: RCA result
├── log_template: drain3 config 
├── alarm.py: generate alarm 
├── data_integrate.py: transform metric, log, and trace to event graph 
├── log_parsing.py: parsing logs
├── log.py: record logs
├── pattern_miner.py: mine patterns from event graph
├── pattern_ranker.py: rank suspicious patterns
├── main.py: running nezha
└── requirements.txt

```

## Reference
Please cite our FSE'23 paper if you find this work is helpful. 
```
@inproceedings{nezha,
  title={Nezha: Interpretable Fine-Grained Root Causes Analysis for Microservices on Multi-Modal Observability Data},
  author={Yu, Guangba and Chen, Pengfei and Li, Yufeng and Chen, Hongyang and Li, Xiaoyun and Zheng, Zibin},
  booktitle={ESEC/FSE 2023},
  pages={},
  year={2023},
  organization={ACM}
}
```