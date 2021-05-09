import pycountry
import pycountry_convert as pc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns

class country_utils():
    def __init__(self):
        self.d = {}
    
    def get_dic(self):
        return self.d
    
    def get_country_details(self,country):
        """Returns country code(alpha_3) and continent"""
        try:
            country_obj = pycountry.countries.get(name=country)
            if country_obj is None:
                c = pycountry.countries.search_fuzzy(country)
                country_obj = c[0]
            continent_code = pc.country_alpha2_to_continent_code(country_obj.alpha_2)
            continent = pc.convert_continent_code_to_continent_name(continent_code)
            return country_obj.alpha_3, continent
        
        except:
            if 'Congo' in country:
                country = 'Congo'
            elif country == 'Diamond Princess' or country == 'Laos' or country == 'MS Zaandam'\
            or country == 'Holy See' or country == 'Timor-Leste':
                return country, country
            elif country == 'Korea, South' or country == 'South Korea':
                country = 'Korea, Republic of'
            elif country == 'Taiwan*':
                country = 'Taiwan'
            elif country == 'Burma':
                country = 'Myanmar'
            elif country == 'West Bank and Gaza':
                country = 'Gaza'
            else:
                return country, country
            country_obj = pycountry.countries.search_fuzzy(country)
            continent_code = pc.country_alpha2_to_continent_code(country_obj[0].alpha_2)
            continent = pc.convert_continent_code_to_continent_name(continent_code)
            return country_obj[0].alpha_3, continent
    
    def get_iso3(self, country):
        return self.d[country]['code']
    def get_continent(self,country):
        return self.d[country]['continent']

    def add_values(self,country):
        self.d[country] = {}
        self.d[country]['code'],self.d[country]['continent'] = self.get_country_details(country)

    def fetch_iso3(self,country):
        if country in self.d.keys():
            return self.get_iso3(country)
        else:
            self.add_values(country)
            return self.get_iso3(country)
        
    def fetch_continent(self,country):
        if country in self.d.keys():
            return self.get_continent(country)
        else:
            self.add_values(country)
            return self.get_continent(country)


us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}


def add_daily_measures(df):
    df.loc[0,'Daily Cases'] = df.loc[0,'ConfirmedCases']
    df.loc[0,'Daily Deaths'] = df.loc[0,'Fatalities']
    for i in range(1,len(df)):
        df.loc[i,'Daily Cases'] = df.loc[i,'ConfirmedCases'] - df.loc[i-1,'ConfirmedCases']
        df.loc[i,'Daily Deaths'] = df.loc[i,'Fatalities'] - df.loc[i-1,'Fatalities']
    #Make the first row as 0 because we don't know the previous value
    df.loc[0,'Daily Cases'] = 0
    df.loc[0,'Daily Deaths'] = 0
    return df


def draw_graph(df, x, y1, y2, title, days=7):
    colors = dict(case = '#4285F4', death = '#EA4335')
    df['cases_roll_avg'] = df[y1].rolling(days).mean()
    df['deaths_roll_avg'] = df[y2].rolling(days).mean()

    fig = make_subplots(specs = [[{'secondary_y':True}]])
    fig.add_trace(go.Scatter(name = 'Daily Cases', x = df[x], y = df[y1], mode='lines',
                            line = dict(width = 0.5, color=colors['case'])),
                 secondary_y = False)

    fig.add_trace(go.Scatter(name = 'Daily Deaths', x = df[x], y=df[y2], mode = 'lines',
                            line = dict(width = 0.5, color = colors['death'])),
                 secondary_y = True)
    fig.add_trace(go.Scatter(name = 'Cases: <br>'+str(days)+'day rolling avg',
                            x = df[x], y = df['cases_roll_avg'], mode = 'lines',
                            line = dict(width=3, color = colors['case'])),
                  secondary_y = False
                            )
    fig.add_trace(go.Scatter(name = 'Deaths:<br>'+str(days)+'day rolling avg',
                            x = df[x], y = df['deaths_roll_avg'], mode = 'lines',
                            line = dict(width = 3, color = colors['death'])),
                 secondary_y = True)
    fig.update_yaxes(title_text = 'Cases', title_font = dict(color = colors['case']), secondary_y = False,
                    nticks = 5, tickfont = dict(color = colors['case']), linewidth = 2, linecolor = 'black',
                    gridcolor = 'darkgray',zeroline = False)
    fig.update_yaxes(title_text = 'Deaths', title_font = dict(color = colors['death']), secondary_y = True,
                    nticks = 5, tickfont = dict(color = colors['death']), linewidth = 2, linecolor = 'black',
                    gridcolor = 'darkgray', zeroline = False)
    fig.update_layout(title = title, height = 400, width = 700, 
                     margin = dict(l=0,r=0,t=60,b=30),hovermode='x',
                      legend=dict(x=0.01,y=0.99,bordercolor='black',borderwidth=1,bgcolor='#EED8E4',
                                  font=dict(family='arial',size=10)),
                     xaxis=dict(mirror=True,linewidth=2,linecolor='black',gridcolor='darkgray'),
                     plot_bgcolor='rgb(255,255,255)')
    return fig

def draw_with_rolling_avg(df, x_date, y1_cases, y2_death, title_text = '', days = 7, figsize=(23,12)):
    df['cases_roll_avg'] = df[y1_cases].rolling(days).mean()
    df['deaths_roll_avg'] = df[y2_death].rolling(days).mean()
    fig, ax = plt.subplots(figsize=figsize)
    label_text1 = f'{days}-day rolling avg Cases'
    sns.lineplot(x=df[x_date], y = df[y1_cases], ax = ax, lw = 0.3, color = '#4285F4', label='Daily Cases', legend=False)
    sns.lineplot(x=df[x_date], y = df['cases_roll_avg'], ax = ax, lw = 3, color = '#4285F4', label=label_text1, legend=False)
    ax2 = ax.twinx()
    label_text2 = f'{days}-day rolling avg Death'
    sns.lineplot(x=df[x_date], y = df[y2_death], ax = ax2, lw = 0.3, color = '#EA4335', label='Daily Death', legend=False)
    sns.lineplot(x=df[x_date], y = df['deaths_roll_avg'], ax = ax2, lw = 3, color = '#EA4335', label=label_text2, legend=False)
    if title_text == '':
        title_text = f'Daily Cases & Death\nwith {days}-Day Rolling Averages'
    ax.set_title(title_text, fontsize = 20)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    return fig