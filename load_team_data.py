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
teams_df = pd.DataFrame.from_records([t.to_dict() for t in teams])
teams_df = pd.concat([teams_df.drop('location', axis = 1), teams_df['location'].apply(pd.Series)], axis = 1)
teams_df['logo1'] = [teams_df['logos'][i][0] for i in range(len(teams_df))]
teams_df['logo2'] = [teams_df['logos'][i][1] for i in range(len(teams_df))]
teams_df.drop('logos', axis = 1, inplace = True)

teams_df.columns
teams_df.head()
teams_df.describe()

#Call Records API and get SEC Records
records_api = cfbd.GamesApi(api_config)
sec_records_df = pd.DataFrame()

for i in range(1950,2022):
  record = records_api.get_team_records(year=i, conference = 'SEC')
  sec_record_df_temp = pd.DataFrame.from_records([r.to_dict() \
                                                  for r in record])
  sec_record_df_temp = sec_record_df_temp[['year', 'team', 'conference', 'division', 'total']]
  sec_record_df_temp = pd.concat([sec_record_df_temp.drop('total', axis = 1), \
                                 sec_record_df_temp['total'].apply(pd.Series)], axis = 1)



