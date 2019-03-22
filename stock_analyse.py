from pandas.plotting import register_matplotlib_converters
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import matplotlib
import io
import base64
matplotlib.use('Agg')
register_matplotlib_converters()
engine = create_engine('sqlite:///stocks.db', echo=False)

def stock_info(symbols):
    big_df = pd.DataFrame()

    for symbol in symbols:
        # df = pd.DataFrame(columns=['Date'])

        df = pd.read_csv("stock_data/{}.us.txt".format(symbol), parse_dates= True, usecols=['Date','Close','Volume'], na_values=['nan'])
        #    print(" No such file")

        df['Date'] = pd.to_datetime(df['Date'])
        df.rename(columns={"Date":"Date",
                           "Close":symbol+"Close",
                           "Volume":symbol+"Volume",}, inplace=True)

        start_date = '2013-01-01'
        end_date = '2018-03-31'

        mask =(df['Date'] > start_date) & (df['Date'] <= end_date)
        df = df.loc[mask]

        df.set_index(['Date'], inplace=True)

        big_df = pd.concat([big_df, df], axis=1)

    print(big_df.head())

    ipo_dict = {}
    list_col = []
    list_ipo = []

    for symbol in symbols:
        column_name = symbol + "Close"
        list_col.append(column_name)

    # print('listcol is',list_col)

    for i in list_col:

        ipo_date = big_df[i].first_valid_index().date()

        if ipo_date > datetime.date(2013,1,3):
            comp_name = str(i.split("Close")[0])
            ipo_dict[comp_name] = ipo_date.strftime("%Y-%m-%d")

    for key in ipo_dict.keys():
        list_ipo.append(key + 'Close')
        list_ipo.append(key+'Volume')

    # print("ipo columns is", list_ipo)

    df_ipo = big_df[list_ipo]
    # Creating the table ipo_stocks

    create_table(df_ipo)


    return ipo_dict


def create_table(df):

    df = df.sort_values(by='Date', ascending=False)
    df.to_sql('ipo_stocks', con=engine, if_exists='replace')


def perf_graph(name):

    pd_sql = pd.read_sql_table('ipo_stocks', con=engine, index_col='Date')
    # mprint(pd_sql.head(5))
    list1 = [name+'Close', name+'Volume']
    fig = plt.figure(figsize=(10, 5))
    top = plt.subplot2grid((4, 4), (0, 0), rowspan=3, colspan=4)
    bottom = plt.subplot2grid((4, 4), (3, 0), rowspan=1, colspan=4)
    top.plot(pd_sql.index, pd_sql[list1[0]], label='Price')
    bottom.bar(pd_sql.index, pd_sql[list1[0]], label='Volume')

    # set the labels
    top.axes.get_xaxis().set_visible(False)
    top.set_title('Stock Performance')
    top.set_ylabel('Adj Closing Price')
    bottom.set_ylabel('Volume')
    plt.show()
    # fig.savefig('static/images/plot.png')  # saves the current figure into a pdf page
    bytes_image = io.BytesIO()
    fig.savefig(bytes_image, format='png')
    bytes_image.seek(0)
    graph_url = base64.b64encode(bytes_image.getvalue()).decode()
    plt.close()
    return 'data:image/png;base64,{}'.format(graph_url)

# symbols=['TSLA','ze','SNAP','FIT', 'MSFT']
# dict1 = stock_info(symbols)
# print(dict1)
# perf_graph()
# print_table()




