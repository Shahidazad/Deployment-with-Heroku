from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy

# from send_mail import send_mail

app=Flask(__name__)  # Procfile for heroku understanding

ENV='prod'  # mode (production)

if ENV=='dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:S9822469692@a@localhost/lexus" # connect to data base
else:
    app.debug=False # production data base
    app.config['SQLALCHEMY_DATABASE_URI']='postgres://zdrifhkegvmklm:8f13e18b3e5af9d2440b687da5750d8dcafe5c502741e0874e16dcef8890e3c3@ec2-52-72-99-110.compute-1.amazonaws.com:5432/df8hkngb9tv6lf'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__='feedback'       # create table
    id=db.Column(db.Integer,primary_key=True)     # column details
    customer=db.Column(db.String(200),unique=True)
    dealer=db.Column(db.String(200))
    rating=db.Column(db.Integer)
    comments=db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit',methods=['POST'])
def submit():
    if request.method=='POST':  # get the data 
        customer=request.form['customer']
        dealer=request.form['dealer']
        rating=request.form['rating']
        comments=request.form['comments']
        # print(customer,dealer,rating,comments)
        if customer=='' or dealer=='':
            return render_template('index.html',message='please enter required field')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count()==0: # new feedback 
            data=Feedback(customer,dealer,rating,comments)
            db.session.add(data)
            db.session.commit()
            # send_mail(customer,dealer,rating,comments)
            return render_template('success.html')
        return render_template('index.html',message=' you submit feedback') # already submit feedback



if __name__=='__main__':
    app.run()