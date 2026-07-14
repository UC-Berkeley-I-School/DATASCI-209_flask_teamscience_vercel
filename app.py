import pandas as pd
import altair as alt
from vega_datasets import data as vega_data
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def w209():
    file='nih_grant.png'
    file2='term_grants_60_prj_period.png'
    file3='dollar_breakdown.png'
    file4='region_termin_count.png'
    file5='region_termin_rates.png'

#------------------Teresa's Interactuve Graphs-------------------------------------------------
    sector_status = pd.read_csv('data_files/sector_status.csv')

    sectors = alt.Chart(sector_status).mark_bar().encode(
    x=alt.X('pct:Q', axis=alt.Axis(format='%'), title='Share of Grants', stack='normalize'),
    y=alt.Y('org_sector:N', title='Sector'),
    color=alt.Color('detailed_status:N', title='Status'),
    tooltip=['org_sector', 'detailed_status', 'count', alt.Tooltip('pct:Q', format='.1%')])
    # Load US states topojson
    states = alt.topo_feature(vega_data.us_10m.url, 'states')

    # FIPS code → state abbreviation lookup
    fips_to_state = {
        1:'AL',2:'AK',4:'AZ',5:'AR',6:'CA',8:'CO',9:'CT',10:'DE',
        11:'DC',12:'FL',13:'GA',15:'HI',16:'ID',17:'IL',18:'IN',
        19:'IA',20:'KS',21:'KY',22:'LA',23:'ME',24:'MD',25:'MA',
        26:'MI',27:'MN',28:'MS',29:'MO',30:'MT',31:'NE',32:'NV',
        33:'NH',34:'NJ',35:'NM',36:'NY',37:'NC',38:'ND',39:'OH',
        40:'OK',41:'OR',42:'PA',44:'RI',45:'SC',46:'SD',47:'TN',
        48:'TX',49:'UT',50:'VT',51:'VA',53:'WA',54:'WV',55:'WI',56:'WY'
    }

    northeast = {'CT','ME','MA','NH','RI','VT','NJ','NY','PA'}
    midwest   = {'IL','IN','MI','OH','WI','IA','KS','MN','MO','NE','ND','SD'}
    south     = {'DE','FL','GA','MD','NC','SC','VA','DC','WV','AL','KY','MS','TN','AR','LA','OK','TX'}
    west      = {'AZ','CO','ID','MT','NV','NM','UT','WY','AK','CA','HI','OR','WA'}

    def get_region(state):
        if state in northeast: return 'Northeast'
        if state in midwest:   return 'Midwest'
        if state in south:     return 'South'
        if state in west:      return 'West'
        return 'Other'

    # Build a lookup dataframe with FIPS + region + termination rate
    reg_rates = {
        'Northeast': 0.483,
        'Midwest':   0.308,
        'South':     0.950,
        'West':      0.926
    }

    state_df = pd.DataFrame([
        {'id': fips, 'state': abbr, 'region': get_region(abbr),
        'rate': reg_rates.get(get_region(abbr), None)}
        for fips, abbr in fips_to_state.items()
    ])

    region_map = alt.Chart(states).mark_geoshape().transform_lookup(
        lookup='id',
        from_=alt.LookupData(state_df, 'id', ['region', 'rate'])
    ).encode(
        color=alt.Color('rate:Q',
            scale=alt.Scale(scheme='reds'),
            title='Termination Rate'
        ),
        tooltip=['region:N', alt.Tooltip('rate:Q', format='.1%')]
    ).project('albersUsa').properties(
        title='NIH Grant Termination Rate by Region',
        width=600,
        height=400
    )
    charts = {
        'sector_shares_of_grants': sectors.to_json(),
        'regions_on_map': region_map.to_json()
    }
   
    hist='termination_histogram.png'
    scatter='termination_scatter.png'
    bar='termination_bar.png'

    return render_template('w209.html',file=file,file2=file2, 
                           file3=file3,file4=file4, file5=file5, hist=hist,scatter=scatter, charts=charts,bar=bar)

if __name__ == '__main__':
    app.run()
