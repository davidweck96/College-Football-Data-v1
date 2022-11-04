import cfbd
import numpy as np
import pandas as pd
import seaborn as sns

#Configure API
config = cfbd.Configuration()
config.api_key['Authorization'] = '8om4vZLNAnCGJAIgUpd8ssn1to1r79RduXsVvdazw/z9xWMq+cfI3AR88yCVFkwj'
config.api_key_prefix['Authorization'] = 'Bearer'
api_config = cfbd.ApiClient(config)

#Call Stats API and get stats
stats_api = cfbd.StatsApi(api_config)
florida_stats = stats_api.get_team_season_stats(team = 'Florida')
florida_stats_df = pd.DataFrame().from_records(([t.to_dict() for t in florida_stats]))
florida_stats_df = florida_stats_df.pivot(index = ['season', 'team', 'conference'] \
                     , columns = 'stat_name' \
                     , values = 'stat_value')
    
florida_stats_df.info()
florida_stats_df.describe()
