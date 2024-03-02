from flask import *  
from flask_mail import *  
from random import *  
app = Flask(__name__)  
mail = Mail(app)  
app.config["MAIL_SERVER"]='smtp.gmail.com'  
app.config["MAIL_PORT"] = 465      
app.config["MAIL_USERNAME"] = 'krishnaoptima008@gmail.com'  
app.config['MAIL_PASSWORD'] = 'Kreshna@55555'  
app.config['MAIL_USE_TLS'] = False  
app.config['MAIL_USE_SSL'] = True  
mail = Mail(app)  
otp = randint(100000,999999)
print(otp)   
# @app.route('/')  
#  def index():  
#  return render_template("homepage.html")  
@app.route('/verify',methods = ["POST"])  
def verify():
    email = "kreshnaprassad55@gmail.com" 
    msg = Message('otp',sender = 'krishnaoptima008@gmail.com',recipients=[email] )
    print('test2otp:{}'.format(otp))
    print('aaaaaaaaaaaaaaaaaaaaaa')
    msg.body = str(otp)
    print('bbbbbbbbbbbbbbbbbbbbbbbb')
    #mail.send_message(msg)
    print('cccccccccccccccccccccccccccc')
    mail.send(msg)
    print('dddddddddddddddddddddddddddd')
    return "message sent" 
   
#  return render_template('verify.html')  
@app.route('/validate',methods=["POST"])   
def validate():
    user_otp = 873154
    print("",otp) 
    if otp == int(user_otp):
        return " Email  verification is  successful "
    return "failure, OTP does not match"

 
if __name__ == '__main__':
    app.run(debug = True)
    verify()


 