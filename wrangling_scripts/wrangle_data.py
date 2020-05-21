import pandas as pd
import plotly.graph_objs as go
import requests

# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
 
    # get the World Bank GDP API data for Japan, Korea, India, China and the United States
    import pandas as pd
    from collections import defaultdict

    payload = {'format': 'json', 'per_page': '5000', 'date':'1990:2100'}
    url = 'http://api.worldbank.org/v2/countries/us;cn;jp;kr;in/indicators/NY.GDP.MKTP.CD'
    r = requests.get(url, params=payload)

    data = defaultdict(list)
    for entry in r.json()[1]:
        if data[entry['country']['value']]:
            data[entry['country']['value']][0].append(int(entry['date']))
            data[entry['country']['value']][1].append(float(entry['value']))       
        else: 
            data[entry['country']['value']] = [[],[]] 

    pd_data = {}
    for country in data:
        pd_data[country] = pd.DataFrame({"year":data[country][0], "GDP":data[country][1]})
        pd_data[country] = pd_data[country].sort_values("year")[-21:]

    # first chart plots arable land from 1990 to 2015 in top 10 economies 
    # as a line chart
    
    graph_one = []    
    for country, df in pd_data.items():
      x_val = df.year.tolist()[-20:]
      y_val = (df.GDP / 1000000000).tolist()[-20:]
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )
        

    layout_one = dict(title = "20 years' GDP by Country",
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'GDP (in Billions)'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    
    recent_year = max(pd_data['China'].year)
    country_lst = []
    recent_GDP_lst = []
    for country, df in pd_data.items():
        country_lst.append(country)
        recent_GDP_lst.append(int(df[df.year==recent_year].GDP / 1000000000))
        
    graph_two.append(
      go.Bar(
      x = country_lst,
      y = recent_GDP_lst,
      )
    )

    layout_two = dict(title = 'Current GDP by Country (Year: {})'.format(recent_year),
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'GDP (in Billions)'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    for country, df in pd_data.items():
        gdps = (df.GDP / 1000000000).tolist()
        x_val = df.year.tolist()[-20:]
        y_val = [(y-x)/x*100 for x,y in zip(gdps[-21:-1], gdps[-20:] )]
        graph_three.append(
            go.Scatter(
                x = x_val,
                y = y_val,
                mode = 'lines+markers',
                name = country
            )
        )

    layout_three = dict(title = 'Year-to-year GDP Growth Rate',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'Year-to-year GDP Growth Rate (%)')
                       )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))

    return figures