import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class SearchTrendApi():
    """
    네이버 데이터랩 오픈 API 컨트롤러 클래스
    """

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.keywordGroups = []
        self.url = "https://openapi.naver.com/v1/datalab/search"

    def add_keyword_groups(self, group_dict):
        """
        검색어 그룹 추가
        """
        keyword_group = {
            'groupName' : group_dict['groupName'],
            'keywords' : group_dict['keywords']
        }

        self.keywordGroups.append(keyword_group)
        print(f">>> Num of keywordGroups: {len(self.keywordGroups)}")

    def get_data(self,startDate, endDate,timeUnit, device, ages, gender):
        """
        요청 결과 반환
        """
        payload = {
            "startDate" : startDate,
            "endDate" : endDate,
            "timeUnit" : timeUnit,
            "keywordGroups" : self.keywordGroups,
            "device" : device,
            "ages" : ages,
            "gender" : gender
        }
        
        headers = {
            "X-Naver-Client-Id" : self.client_id,
            "X-Naver-Client-Secret" : self.client_secret,
            "Content-Type" : "application/json"
        }

        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            df = pd.DataFrame(result['results'][0]['data'])[['period']]
            for i in range(len(self.keywordGroups)):
                tmp = pd.DataFrame(result['results'][i]['data'])
                tmp = tmp.rename(columns={'ratio' : result['results'][i]['title']})
                df = pd.merge(df, tmp, how='left', on=['period'])

            df = df.rename(columns={'period' : '날짜'})
            df['날짜'] = pd.to_datetime(df['날짜'])
            #print(df.head())
        else:
            raise Exception("Error Code : " + str(response.status_code))

        return df

    def plot_trend(self, df):
        """
        검색어 트렌드 그래프 출력
        """
        columns = df.columns[1:]
        n_col = len(columns)

        plt.figure(figsize=(12,6))
        plt.rc('font', family='Malgun Gothic')
        plt.title('주 별 검색어 트렌드', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=df['날짜'], y=df[columns[i]], label=columns[i])
        plt.ylabel("검색량")
        plt.legend(loc='upper right')
        
        plt.show()

# 본문
# client_id = "A_5TeRCjyPtE8XqEOylQ"
# client_secret = "IAElttsqBe"

# keyword_group_set = {
#     'keyword_group_1': {'groupName': "애플", 'keywords': ["애플"," Apple","AAPL"]},
#     'keyword_group_2': {'groupName': "아마존", 'keywords': ["아마존"," Amazon","AMZN"]},
#     'keyword_group_3': {'groupName': "구글", 'keywords': ["구글"," Google","GOOGL"]},
#     'keyword_group_4': {'groupName': "테슬라", 'keywords': ["테슬라"," Tesla","TSLA"]},
#     'keyword_group_5': {'groupName': "페이스북", 'keywords': ["페이스북"," Facebook","FB"]}
# }

# res = SearchTrendApi(client_id, client_secret)
# res.add_keyword_groups(keyword_group_set['keyword_group_1'])
# res.add_keyword_groups(keyword_group_set['keyword_group_2'])
# res.add_keyword_groups(keyword_group_set['keyword_group_3'])
# res.add_keyword_groups(keyword_group_set['keyword_group_4'])
# res.add_keyword_groups(keyword_group_set['keyword_group_5'])

# startDate = "2022-01-01"
# endDate = "2022-08-31"
# timeUnit = "week"
# device = ""
# ages = []
# gender = ""

# df = res.get_data(startDate, endDate, timeUnit, device, ages, gender)
# res.plot_trend(df)
