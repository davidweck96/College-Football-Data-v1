import cfbd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Configure API
config = cfbd.Configuration()
config.api_key['Authorization'] = '8om4vZLNAnCGJAIgUpd8ssn1to1r79RduXsVvdazw/z9xWMq+cfI3AR88yCVFkwj'
config.api_key_prefix['Authorization'] = 'Bearer'
api_config = cfbd.ApiClient(config)

#Call Teams API and get FBS Teams
teams_api = cfbd.TeamsApi(api_config)
teams = teams_api.get_fbs_teams()
teams[0]

#Put teams into dataframe and clean up columns
df = pd.DataFrame.from_records([t.to_dict() for t in teams])
df = pd.concat([df.drop('location', axis = 1), df['location'].apply(pd.Series)], axis = 1)
df['logo1'] = [df['logos'][i][0] for i in range(len(df))]
df['logo2'] = [df['logos'][i][1] for i in range(len(df))]
df.drop('logos', axis = 1, inplace = True)

df.columns
df.head()
df.tail()
df.describe()

#Call Records API and get SEC Records
records_api = cfbd.GamesApi(api_config)
sec_records = []

for i in range(1950,2022):
  sec_records.append(records_api.get_team_records(year=i, conference = 'SEC'))

sec_records[0]
