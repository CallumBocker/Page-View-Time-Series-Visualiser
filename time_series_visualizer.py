import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df.set_index('date')

# Clean data
index_clean = df[(df['value'] < df['value'].quantile(0.025)) | (df['value'] > df['value'].quantile(0.975))].index
df = df.drop(index_clean)


def draw_line_plot():
    # Draw line plot
    df.date = pd.to_datetime(df.date)

    plt.figure(figsize=(12,4))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=180))
    plt.gcf().autofmt_xdate()

    plt.plot(df.date, df.value, color='red', linewidth=.5)
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    plt.xticks(rotation=0)

    plt.show()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.set_index(df.date)
    df_bar = df_bar.groupby(pd.Grouper(freq='M'))['value'].mean()
    df_bar = df_bar.to_frame()
    df_bar = df_bar.reset_index(level=0)
    df_bar['Years'] = pd.DatetimeIndex(df_bar.date).year
    df_bar['Months'] = pd.DatetimeIndex(df_bar.date).month_name()
    df_bar.rename(columns={'value': 'Average Page Views'}, inplace=True)

    # Draw bar plot
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

    sns.barplot(data=df_bar, x='Years', y='Average Page Views', hue='Months', hue_order=months)

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, axes = plt.subplots(1, 2, figsize=(20, 4))

    sns.boxplot(data=df_box, x='year', y='value', ax=axes[0]).set(title='Year-wise Box Plot (Trend)', ylabel='Page Views', xlabel='Year')

    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    sns.boxplot(data=df_box, x='month', y='value', ax=axes[1], order=months).set(title='Month-wise Box Plot (Seasonality)', ylabel='Page Views', xlabel='Month')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
