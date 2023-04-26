import os
import csv
import articles_functions
import pandas as pd

def run():
    if os.path.exists("03_2023_nyt.csv"):
        df = pd.read_csv("03_2023_nyt.csv")

    else:
        response = articles_functions.get_api_archive(2023, 3)
        articles = articles_functions.get_response(response)
        df = articles_functions.parse_response(articles)
        df.to_csv("03_2023_nyt.csv",index= False, header=True)


    df['pub_date'] = df['pub_date'].apply(lambda x: x[0:10])

    df_by_key = articles_functions.order_by_key(df)
    df_finale = articles_functions.create_df_keys(df_by_key)
    return df_finale


if __name__=="__main__":
    print(run())