import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class ShoppingInsightApi:
    
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.category_group = []
        self.url = 'https://openapi.naver.com/v1/datalab/shopping/categories'

    def add_category(self, name, param):
        """
        카테고리 추가
        """
        cat_dict = {
            'name':name,
            'param':[param]
        }

        self.category_group.append(cat_dict)

    def get_category_trend(self, startDate, endDate, timeUnit, device='pc', gender='f', ages=['20', '30']):
        """
        쇼핑인사이트 분야별 트렌드 조회
        """
        payload = {
            'startDate' : startDate,
            'endDate' : endDate,
            'timeUnit' : timeUnit,
            'category' : self.category_group,
            'device' : device,
            'gender' : gender,
            'ages' : ages
        }

        headers = {
            'X-Naver-Client-Id' : self.client_id,
            'X-Naver-Client-Secret' : self.client_secret
        }

        response = requests.post(self.url, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            df = pd.DataFrame(result['results'][0]['data'])[['period']]
            for i in range(len(self.category_group)):
                tmp = pd.DataFrame(result['results'][i]['data'])
                tmp = tmp.rename(columns={'ratio' : result['results'][i]['title']})
                df = pd.merge(df, tmp, how='left', on='period')
            
            df = df.rename(columns={'period' : '날짜'})
            df['날짜'] = pd.to_datetime(df['날짜'])
        else:
            print("Error Code : " + response.status_code)

        return df

    def plot_trend(self, df):
        """
        검색어 트렌드 그래프 출력
        """
        columns = df.columns[1:]
        n_col = len(columns)
        plt.figure(figsize=(12,6))
        plt.rc('font', family='Malgun Gothic')
        plt.title('쇼핑인사이트 분야별 트렌드 조회', size=20, weight='bold')
        for i in range(n_col):
            sns.lineplot(x=df['날짜'], y=df[columns[i]], label=columns[i])
        plt.ylabel("검색량")
        plt.legend(loc='upper right')
        
        plt.show()


# 본문
client_id = "A_5TeRCjyPtE8XqEOylQ"
client_secret = "IAElttsqBe"

startDate = '2022-08-01'
endDate = '2022-09-17'
timeUnit = 'week'
device = 'pc'
gender = 'f'
ages = ['20', '30']

res = ShoppingInsightApi(client_id, client_secret)
res.add_category('패션의류', '50000000')
res.add_category('화장품/미용', '50000002')
df = res.get_category_trend(startDate, endDate, timeUnit, device, gender, ages)
res.plot_trend(df)

