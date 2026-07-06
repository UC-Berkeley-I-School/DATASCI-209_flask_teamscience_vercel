from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def w209():
    file='nih_grant.png'
    file2='term_grants_60_prj_period.png'
    file3='dollar_breakdown.png'
    file4='region_termin_count.png'
    file5='region_termin_rates.png'
    return render_template('w209.html',file=file,file2=file2, 
                           file3=file3,file4=file4, file5=file5)

if __name__ == '__main__':
    app.run()
