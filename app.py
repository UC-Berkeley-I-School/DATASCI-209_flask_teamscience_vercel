import pandas as pd
import altair as alt
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def w209():
    file='nih_grant.png'
    file2='term_grants_60_prj_period.png'
    file3='dollar_breakdown.png'
    file4='region_termin_count.png'
    file5='region_termin_rates.png'

    sector_status = pd.read_csv('data_files/sector_status.csv')

    sectors = alt.Chart(sector_status).mark_bar().encode(
    x=alt.X('pct:Q', axis=alt.Axis(format='%'), title='Share of Grants', stack='normalize'),
    y=alt.Y('org_sector:N', title='Sector'),
    color=alt.Color('detailed_status:N', title='Status'),
    tooltip=['org_sector', 'detailed_status', 'count', alt.Tooltip('pct:Q', format='.1%')]
)
    charts = {
        'sector_shares_of_grants': sectors.to_json()
    }
    
    return render_template('w209.html',file=file,file2=file2, 
                           file3=file3,file4=file4, file5=file5, charts=charts)

if __name__ == '__main__':
    app.run()
