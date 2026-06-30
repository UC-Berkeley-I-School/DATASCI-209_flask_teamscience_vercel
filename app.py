from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def w209():
    file='about9.jpg'
    file2='term_grants_60_prj_period.png'
    file3='dollar_breakdown.png'
    return render_template('w209.html',file=file,file2=file2, file3=file3)

if __name__ == '__main__':
    app.run()
