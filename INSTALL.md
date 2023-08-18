# Quick Start

### 1.1 Requirements 

- Python3.6 is recommended to run the anomaly detection. Otherwise, any python3 version should be fine.
- Git is also needed.

### 1.2 Setup

download `Nezha`  first by  `git clone git@github.com:IntelligentDDS/Nezha.git` 

`python3.6 -m pip install -r requirements.txt` to install the dependency for Nezha

### 1.3 Running  Nezha

#### 1.3.1 Localize OnlineBoutique at service level


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

#### 1.3.2 Localize OnlineBoutique at inner service level

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

#### 1.3.3 Localize Trainticket at service level

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

#### 1.3.4 Localize Trainticket at inner service level

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