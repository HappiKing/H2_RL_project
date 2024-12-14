# 강화학습을 이용한 수소 EMS 최적화 및 모니터링

이 프로젝트는 태양열 에너지와 그리드 전력 등을 활용하여 잉여 전력을 수소로 보관하고 다시 전력으로 변환하는 과정을 통해 그리드 비용을 저감하는 것을 목표로 둡니다.

## 주요 기능
- **그리드 비용 감소**: 잉여 태양광 발전량을 수소가스 형태로 변환하여 저장하고 다시 태양광 발전량이 부족할 경우 다시 전력으로 변환하여 사용함으로 그리드 비용을 절감
- **전력 장기 보관 가능**: 배터리 형태로 저장했을 때 보다 전력을 장기간 보관할 수 있음

## 파일 구조
```
.
├── LSTM
│   ├── 1extracted_data_10051700_10070340.csv
│   ├── 2020csv30T.csv
│   └── solarLSTM.ipynb
├── README.md
├── RL
│   ├── Data
│   │   ├── Power_Consumption_Data.csv
│   │   ├── Solar_Generation_Data.csv
│   │   └── costData.csv
│   ├── EMS_RL.ipynb
│   ├── EMS_RL_Hydrogen_backup.ipynb
│   ├── PV_LSTM
│   │   ├── 2020_30T.csv
│   │   ├── solarData.xlsx
│   │   └── solarLSTM.ipynb
│   ├── RL_test.ipynb
│   ├── Test
│   │   ├── OpenAI Custom Environment Reinforcement Learning.ipynb
│   │   ├── Power_Consumption_Data.csv
│   │   ├── Solar_Generation_Data.csv
│   │   └── costData.csv
│   └── pvLoadPriceData_test.mat
├── matlab_to_python(Batt)
│   ├── battNo.ipynb
│   ├── battSolarHuri.ipynb
│   ├── battSolarOptimiz.ipynb
│   ├── battSolarOptimize.m
│   ├── battSolar_RL.ipynb
│   └── pvLoadPriceData_test.mat
├── matlab_to_python(Hydrogen)
│   ├── 2020_load_data.csv
│   ├── HydroRL.ipynb
│   ├── HydroSolarHuri.ipynb
│   ├── RL_1year
│   │   ├── 2020_load_data.csv
│   │   ├── HydroRL_1year.ipynb
│   │   ├── action_table.csv
│   │   ├── cost_data copy.csv
│   │   ├── cost_data.csv
│   │   └── test.ipynb
│   ├── battNo.ipynb
│   ├── first_test
│   │   ├── best_cost_table.csv
│   │   ├── output.png
│   │   ├── output1.png
│   │   ├── output2.png
│   │   ├── output3.png
│   │   ├── output4.png
│   │   ├── total_action_data.csv
│   │   ├── total_cost_table.csv
│   │   └── worst_action_table.csv
│   ├── huri_1day_data
│   │   ├── Pgrid.csv
│   │   ├── Pload.csv
│   │   ├── Ppv.csv
│   │   └── soc.csv
│   ├── huri_1day_data.zip
│   ├── huri_1year_data
│   │   ├── Pgrid.csv
│   │   ├── Pload.csv
│   │   ├── Ppv.csv
│   │   └── soc.csv
│   ├── huri_1year_data.zip
│   ├── pvLoadPriceData_test.mat
│   └── save_point
│       ├── Grid.csv
│       ├── Ppv.csv
│       ├── load.csv
│       ├── soc.csv
│       └── total_cost_table.csv
├── 작품 코드
│   ├── jetson.py
│   ├── 부하 전처리
│   │   ├── load.ipynb
│   │   ├── 예제
│   │   │   ├── 2020_5E_load_cleaned.csv
│   │   │   └── test.ipynb
│   │   └── 예제.zip
│   ├── 과거 데이터 가져오기
│   │   ├── DB_set_2E.ipynb
│   │   ├── DB_set_4E.ipynb
│   │   └── DB_set_GR.ipynb
│   ├── 실시간 데이터 가져오기
│   │   ├── DB_E2.py
│   │   ├── DB_E4.py
│   │   └── DB_GR.py
│   ├── 해결해야 할 것
│   │   ├── DB_5E.py
│   │   ├── DB_set_5E.ipynb
│   │   ├── DB_set_H2Tank.ipynb
│   │   └── DB_set_Load.ipynb
│   ├── 강화학습(개별)
│   │   ├── 2020_load_data.csv
│   │   ├── 2공.csv
│   │   ├── 4공.csv
│   │   ├── 5공.csv
│   │   ├── HydroRL_E_2.ipynb
│   │   ├── HydroRL_E_4.ipynb
│   │   ├── HydroRL_E_5.ipynb
│   │   ├── HydroRL_E_GR.ipynb
│   │   └── 그린.csv
│   ├── 강화학습(전체)
│   │   ├── 2020_load_data.csv
│   │   ├── 2공.csv
│   │   ├── 4공.csv
│   │   ├── 5공.csv
│   │   ├── HydroRL_all.ipynb
│   │   ├── total_cost_table_all.csv
│   │   └── 그린.csv
│   └── 휴리스틱(전체)
│       ├── 2020_load_data.csv
│       ├── 2공.csv
│       ├── 4공.csv
│       ├── 5공 부하데이터.csv
│       ├── 5공.csv
│       ├── HydroSolarHuri.ipynb
│       └── 그린.csv
├── 에너지 수요-공급 분석을 위한 디지털트윈(EMS) 기반 서비스 모델.pdf
└── 신재생_에너지_최적_관리를_위한_강화학습_기반_EMS_시스템_설계.pdf
```

## 주요 파일 설명

### `matlab_to_python(Hydrogen)/HydroRL.ipynb`
- **목표**: Q-table 알고리즘을 사용하여 잉여 전력을 효율적으로 사용하여 그리드 전력 비용을 절감한다.
- **기능**: Q-table 알고리즘을 사용한 최적화 강화학습 알고리즘

### `matlab_to_python(Batt)/battSolarOptimiz.ipynb`
- **목표**: LP 최적화 알고리즘을 사용하여 잉여 전력을 효율적으로 사용하여 그리드 전력 비용을 절감한다.
- **기능**: LP 최적화 알고리즘

### `matlab_to_python(Batt)/battSolarHuri.ipynb`
- **목표**: 휴리스틱 최적화 알고리즘을 사용하여 잉여 전력을 효율적으로 사용하여 그리드 전력 비용을 절감한다.
- **기능**: 휴리스틱 최적화 알고리즘

# 결과
강화학습 기반의 신재생 에너지 최적 관리 시스템과 전통적인 휴리스틱 알고리즘의 성능을 비교한 결과 강화학습 기반 시스템의 전력 누적 비용은 9767.43원, 휴리스틱 알고리즘 기반 전력 누적 비용은 21707.59원으로 약 55% 절감 효과를 나타냈다.
