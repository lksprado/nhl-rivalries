import pandas as pd 

def model(allgames: str, top50: str, team: str ,output: str):
    """Generates top Rivalities + team of choice"""
    df1 = pd.read_csv(allgames)

    df2 = pd.read_csv(top50)

    df3 = df1.merge(df2, how='inner', left_on='game',right_on='fight')

    df3 = df3[['data','game']]

    filtro = (df1['game'].str.contains(team))

    df4 = df1.loc[filtro,:]

    df5 = pd.concat([df3, df4], ignore_index=True, sort=False)

    df5 = df5.drop_duplicates()

    df5.to_csv(output, index=False)

if __name__ == "__main__":
    model('data/all_games.csv', 'data/top50_fights.csv',"Oilers",'data/games_of_interest.csv' )
    


