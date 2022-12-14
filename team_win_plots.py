import cfbd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
teams_df.rename(columns = {'school' : 'team'}, inplace = True)

teams_df.columns
teams_df.head()
teams_df.describe()

#Call Records API and get SEC Records
records_api = cfbd.GamesApi(api_config)
sec_records_df = pd.DataFrame()

#Put records into dataframe and clean columns
for i in range(1950,2022):
  record = records_api.get_team_records(year=i, conference = 'SEC')
  sec_record_df_temp = pd.DataFrame.from_records([r.to_dict() \
                                                  for r in record])
  sec_record_df_temp = sec_record_df_temp[['year', 'team', 'conference', 'division', 'total']]
  sec_record_df_temp = pd.concat([sec_record_df_temp.drop('total', axis = 1), \
                                 sec_record_df_temp['total'].apply(pd.Series)], axis = 1)
  sec_records_df = pd.concat([sec_records_df, sec_record_df_temp], axis = 0)

#Join SEC Records and team colors
team_info = teams_df[['team', 'mascot', 'color', 'alt_color']]  
sec_records_df2 = pd.merge(left = sec_records_df \
                         , right = team_info \
                         , how = 'left' \
                         , on = 'team')
sec_west_rec_df = sec_records_df2[sec_records_df2['division'] == 'West']
sec_east_rec_df = sec_records_df2[sec_records_df2['division'] == 'East']
    
#Creating East and West color palettes
west_colors = sec_west_rec_df[['team', 'color']].drop_duplicates()
west_col_dict = dict(zip(west_colors.team, west_colors.color))
east_colors = sec_east_rec_df[['team', 'color']].drop_duplicates()
east_col_dict = dict(zip(east_colors.team, east_colors.color))

#Plotting east and west wins through time
sns.set(rc={'figure.figsize':(14,8)})
sns.lineplot(data=sec_west_rec_df \
           , x = 'year' \
           , y = 'wins' \
           , hue = 'team' \
           , palette = west_col_dict)
plt.xlabel('Year')
plt.ylabel('Wins')
plt.legend(title='Team', loc='upper left', ncol=7)
plt.show()


sns.set(rc={'figure.figsize':(14,8)})
sns.lineplot(data=sec_east_rec_df \
           , x = 'year' \
           , y = 'wins' \
           , hue = 'team' \
           , palette = east_col_dict)
plt.xlabel('Year')
plt.ylabel('Wins')
plt.legend(title='Team', loc='upper left', ncol=7)
plt.show()
