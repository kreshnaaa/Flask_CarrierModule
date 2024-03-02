
from cgi import test
from re import A
from ssl import ALERT_DESCRIPTION_RECORD_OVERFLOW
from tokenize import Number
# from numpy import number
# from pymysql import NULL
from app import app, db, engine, session,mail
import pandas as pd
# from matplotlib import collections
# from config import DBConfig,cursor
from flask import Flask,render_template,request,jsonify
import json
from typing import OrderedDict
from db_models import TblJobDetails,TblLookUptable,create,TblApplicantDetails,update,TblAppliedJobs,TblApplicantverif

from psycopg2 import DatabaseError, OperationalError, errors, NotSupportedError, Error, InternalError, ProgrammingError, InterfaceError, IntegrityError
from datetime import datetime, timedelta
from flask_mail import *  
from random import *
from twilio.rest import Client
from config import account_sid,auth_token




@app.route('/createjob', methods = ['POST'] )
def createjob():
    
    try:
        print('createjob')
        request_data = request.get_json()
        jobdetails = TblJobDetails(
            job_title = request_data['job_title'],
            job_location  = request_data['job_location'],
            experience_range = request_data['experience_range'],
            must_have_skills   = request_data['must_have_skills'],
            good_to_have_skills   = request_data['good_to_have_skills'],
            job_desc_roles_resp   = request_data['job_desc_roles_resp'],
            edu_qualification = request_data['edu_qualification'],
            job_created_date = datetime.now().strftime("%Y-%m-%d"),
            job_status = 'active'
        )
        create(jobdetails)
        print('Job Creation Complete')
        print('jobstatus:{}'.format(jobdetails.job_status))
        print('jobid:{}'.format(jobdetails.job_code))
        print('Printing Jobid')
        return jsonify("successful inserted job details and the job id is :{}".format(jobdetails.job_code))
    except Exception as e:
        print('Error! Unable to Display', str(e))   



@app.route('/jobdetailsbyid', methods = ['GET'])
def jobdetailsbyid():
    #jobcode = {}.format(Number)
    job_id= request.args.get('jobid')
    try:
        sql = '''SELECT job_title,job_location,job_status,experience_range,must_have_skills,
        good_to_have_skills, job_desc_roles_resp,edu_qualification,job_created_date from "JOB_DETAILS"
        where job_code = {}'''.format(job_id)
        df = pd.read_sql_query(sql, engine)
        print(df)
        jsonData = df.to_dict('records') 
        return jsonify(jsonData)               
    except Exception as e:
        print('Error! Unable to Display',str(e))

@app.route('/jobdetailsbyId', methods = ['GET'])
def jobdetailsbyId():
    #jobcode = {}.format(Number)
    job_id= request.args.get('jobid')
    print(job_id)
    try:
       jobrecord = session.query(TblJobDetails).get(job_id)
       jsonData = {
           'jobtitle' : jobrecord.job_title,
           'joblocation' : jobrecord.job_location,
           'jobstatus' : jobrecord.job_status,
           'experience'   : jobrecord.experience_range,
           'musthaveskills' : jobrecord.must_have_skills,
           'goodtohaveskils' : jobrecord.good_to_have_skills ,
           'jobdescroleresp' :  jobrecord.job_desc_roles_resp,
           'eduqualification' : jobrecord.edu_qualification,
           'jobcreateddate'   :  datetime.now().strftime("%Y-%m-%d")
            }
       return jsonify(jsonData)               
    except Exception as e:
        print('Error! Unable to Display',str(e)) 

              

@app.route('/getAlljobs', methods = ['GET'])
def  getAlljobs():
    #jobcode = {}.format(Number)
    try:
        sql = '''SELECT * from "JOB_DETAILS" where job_status = 'active' '''
        df = pd.read_sql_query(sql, engine)
        df['job_created_date'] = df['job_created_date'].apply(lambda x:datetime.strftime(x,'%Y-%m-%d'))
        #df.pop('job_created_date')
        #df = df[['edu_qualification','experience_range','good_to_have_skills']]
        #print(df)
        jsonData = df.to_dict('r') 
        return jsonify(jsonData)               
    except Exception as e:
            print('Error! Unable to Display',str(e))


@app.route('/updateJobdetail', methods = ['PUT'])
def updateJobdetail():
    #jobcode = {}.format(Number)
    job_id= request.args.get('jobid')
    try:
        request_data = request.get_json()
        session.query(TblJobDetails).filter_by(job_code = job_id).update(
        #session.query(TblJobDetails).first().update(    
        {
        TblJobDetails.job_title : request_data['job_title'],
        TblJobDetails.job_location  : request_data['job_location'],
        TblJobDetails.experience_range : request_data['experience_range'],
        TblJobDetails.must_have_skills   : request_data['must_have_skills'],
        TblJobDetails.good_to_have_skills   : request_data['good_to_have_skills'],
        TblJobDetails.job_desc_roles_resp   : request_data['job_desc_roles_resp'],
        TblJobDetails.edu_qualification : request_data['edu_qualification'],
        TblJobDetails.job_created_date : datetime.now().strftime("%Y-%m-%d")        
        }
        )  
                  
        session.commit()
        return jsonify("Successfully Updated")               
    except Exception as e:
        print('Error while updating',str(e))            

@app.route('/createapplication', methods = ['POST'])
def createApplication():
    jobcode= request.args.get('job_id')
    print(jobcode)
    try:        
        request_data = request.get_json()
        print(request_data)
        appdetails = TblApplicantDetails(
            first_name = request_data['first_name'],
            last_name = request_data['last_name'],
            gender  = request_data['gender'],
            email_id = request_data['email_id'],
            mobile_no = request_data['mobile_no'],
            address_line1 = request_data['address_line1'],
            address_line2 = request_data['address_line2'],
            city = request_data['city'],
            pincode = request_data['pincode'],
            applicant_state = request_data['applicant_state'],
            country = request_data['country'],
            document_name = request_data['document_name'],
            document_path = request_data['document_path']
        )
        create(appdetails)
        jobrecord = session.query(TblJobDetails).get(jobcode)
        appdetails1 = TblAppliedJobs(
               applied_on = datetime.now().strftime("%Y-%m-%d"),
               applicant_id = appdetails.applicant_id,
               applicant_name = appdetails.first_name + ' ' + appdetails.last_name,
               job_title = jobrecord.job_location,
               job_code =jobrecord.job_code
        )
             
       
        create(appdetails1)   
        print('Job Creation Complete')
        print('applicantid:{}'.format(appdetails.applicant_id))
        print('Printing Jobid')
        return jsonify("successful inserted job details and the job id is :{}".format(jobrecord.job_code))
    except Exception as e:
        print('Error while updating',str(e))


@app.route('/getallapplications', methods = ['GET'])
def getAllapplications():
    try:
       applicantrecord = session.query(TblAppliedJobs).all()
       jsonData = []
       for row in applicantrecord:
           app_dict = {
           'jobtitle' : row.job_title,
           'applicantid' : row.applicant_id,
           'applicantstatus' : row.application_status,
           'applicantname'   : row.applicant_name,
           'appliedon' : datetime.strftime(row.applied_on,"%Y-%m-%d"),
            }
           jsonData.append(app_dict)
       return jsonify(jsonData)
    except Exception as e:
        print('Error while updating',str(e))

@app.route('/getapplicationbyid', methods = ['GET'])
def getApplicationbyid():
    applicantid= request.args.get('applicantid')
    try:
       jobrecord = session.query(TblApplicantDetails).get(applicantid)
       jsonData = {
       'applicantid' : jobrecord.applicant_id,
       'firstname'   : jobrecord.first_name,
        'last_name'   : jobrecord.last_name,
        'gender'   : jobrecord.gender,
        'email_id'   : jobrecord.email_id,
        'address_line1'   : jobrecord.address_line1,
        'mobile_no'   : jobrecord.mobile_no,
        'address_line2'   : jobrecord.address_line2,
        'city'   : jobrecord.city,
        'applicant_state'   : jobrecord.applicant_state,   
        'country'   : jobrecord.country, 
        'pincode'   : jobrecord.pincode,
        'document_path'   : jobrecord.document_path,
        'document_name'   : jobrecord.document_name,  
        }         
       return jsonify(jsonData)    
    except Exception as e:
        print('Error! Unable to Display',str(e))

 
@app.route('/searchservice', methods=['GET'])
def searchservice():
    print(1111)
    attr_id=request.args.get('attrid')
    print(2222)
    try:
       attribute=session.query(TblLookUptable).filter_by(attribute_id=attr_id).all()
       locations=[]
       for r in attribute:
           jsonData={
               'lookupvid':r.value_id,
               'lookupvname':r.value_name
           }
           locations.append(jsonData)
           print('{}'.format(locations))
           return jsonify(locations)
           
    except Exception as e:
        print('Error!Unable to display',str(e))


@app.route('/getalllookups', methods = ['GET'])        
def getAlllookups():
    #attri_id = request.args.get('attri_id')
    print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    try:
        #lookuplistname = ['location','musthaveskills','educationqualification','jobtitle']
        lookuplistname = session.query(TblLookUptable.attribute_name).distinct().all()
        #listvalues = [lookuplistname[0] if len(lookuplistname)==1 else record for record in lookuplistname]
        print(lookuplistname)
        print(type(lookuplistname))
        # listvalues = [record[0] for record in lookuplistname]
        # print(listvalues)
        attribute = session.query(TblLookUptable).all()        
        print(type(attribute))
        # locations = [] 
        print("test1 {}".format(lookuplistname[0]))
        jobtitle = {}
        eduqualify ={}
        location = {}
        mustskills = {}
        #lookup = []
        for name in lookuplistname:
            print ("test4 {}".format(name))                      
            lookup = []            
            for x in attribute:
                print("test5 {}: {}".format(name[0],x.attribute_name))    
                if name[0] == x.attribute_name:
                    print("test6{}".format(name[0]))
                    jsonData = {
                        'lookupvid' : x.value_id,
                        'lookupvname': x.value_name,
                        }
                    lookup.append(jsonData)    
            print("test2 {}".format(name))
            if name[0] == 'jobtitle':
                jobtitle = lookup
            elif name[0] ==  'educationqualification':
                eduqualify = lookup
            elif name[0] == 'location':
                location = lookup
            elif name[0] == 'musthaveskills':
                mustskills = lookup        
            #['jobtitle', 'educationqualification', 'location', 'musthaveskills']
            #exec("{} = {}".format(name,lookup))   #dynamic statement
        print("test3 {}".format(name))
        return jsonify({'jobtitle' : jobtitle,
                        'eduqualify':eduqualify,
                        'location': location,
                        'mustskills':mustskills})
    except Exception as e:
        print('Error! Unable to Display',str(e)) 


@app.route('/jobdetailsbyIddel', methods = ['PUT'])
def jobdetailsbyIddel():
    #jobcode = {}.format(Number)
    job_id= request.args.get('jobid')
    try:
        # request_data = request.get_json()
        session.query(TblJobDetails).filter_by(job_code = job_id).update(
        #session.query(TblJobDetails).first().update(    
        {
        TblJobDetails.job_status :'inactive'         
        }
        )                    
        session.commit()
        return jsonify("Successfully Updated")               
    except Exception as e:
        print('Error while updating',str(e)) 


# ________________________________________________________________________________________
                                       
                                        # 1 #  
# _________________________________________________________________________________________


@app.route('/emailverify', methods = ['GET','POST'])
def emailVerify():
    try:
        otp = randint(100000,999999)
        print(otp)
        email = request.args.get("emailid","krishnaoptima008@gmail.com") 
        msg = Message('otp',sender = 'krishna_45@yahoo.com',recipients=[email])
        print('test2otp:{}'.format(otp))
        print('aaaaaaaaaaaaaaaaaaaaaa')
        msg.body = str(otp)
        print('bbbbbbbbbbbbbbbbbbbbbbbb')
        #mail.send_message(msg)
        print('cccccccccccccccccccccccccccc')
        mail.send(msg)
        #session.query(TblJobDetails)
        print('eeeeeeeeeeeeeeeeeeeeeeee')
        verifydetails = TblApplicantverif(
            applicant_emailid = email,
            applicant_emotp = otp,
            applicant_emotp_time = datetime.now() ,
            applicant_empotp_exptime = datetime.now() +timedelta(minutes =5)
        )
        create(verifydetails)
           #123456
        print('dddddddddddddddddddddd')
        #return jsonify({'msg' : msg})
        return " Otp sent successfully"
        #print('eeeeeeeeeeeeeeeeeee')
    except Exception as e:
        print(e)
     

@app.route('/emlvalidate',methods = ['GET','POST'])
def valiDate():
    try:
        user_mailid= request.args.get("emailid","kreshnaprassad55@gmail.com")
        #user_mailid = request_data['emailid']
        print('111111111111111')
        print(user_mailid)
        request_data = request.get_json()
        print('22222222222222')
        user_otp = request_data["otp"]

        appverify_details = session.query(TblApplicantverif).get(user_otp)
        print(appverify_details)
        print('333333333333')
        if  appverify_details != None:
            if user_otp == appverify_details.applicant_emotp:
                print('44444444444')
                if datetime.now() <= appverify_details.applicant_empotp_exptime:
                    print('555555555555')
                    session.query(TblApplicantverif).filter_by(applicant_emotp=user_otp).update(
                    {
                    TblApplicantverif.applicant_eml_verify_flag:True      
                    }
                    )  
                    session.commit()
                                      
                    return "Email verified successfully"

                    # print('{}'.format(jobdetails.job_status)) 
                else:
                    return "OTP expired"
        else:
            return "Invalid Otp"     
    except Exception as e:
            #print("Invalid Otp")
        print(e)

@app.route('/phoneverify', methods = ['GET','POST'])
def phoneVerify():
    try:
    # Find your Account SID and Auth Token at twilio.com/console   get_json()
    # and set the environment variables. See http://twil.io/secure
        print('2222222222')
        client = Client(account_sid, auth_token)
        print('333333333')
        # email = request.args.get("emailid","kreshnaprassad55@gmail.com")
        # request_data = request.t_json()
        # request_data = request.t_json()
        # pnumber = request_data['mobilenumber']
        pnumber=request.args.get("mbno",8500115263)
        print('4444444444')
        otp = randint(100000,999999)
        print('555555555')
        #print(pnumber.value)
        print('test2otp:{}'.format(otp))
        print(pnumber)
        message = client.messages \
            .create(
                from_='+13517771295',
                body='{}'.format(otp),
                to=['+91{}'.format(pnumber)]
            )
        print(6666666666666)
        verifydetails = TblApplicantverif(
            applicant_phoneno = pnumber,
            applicant_emotp=otp,
            applicant_potp = otp,
            # applicant_emotp_time=datetime.now(),
            applicant_potp_time = datetime.now() ,
            applicant_potp_exptime= datetime.now() +timedelta(minutes =5)
        )
        create(verifydetails)
        print(777777777777)    
        print(message.sid)
        return " Otp sent successfully"
            #print('eeeeeeeeeeeeeeeeeee')
    except Exception as e:
        print(e)

@app.route('/phonevalidate',methods = ['GET','POST'])
def phonevaliDate():
    try:
        user_pnumber= request.args.get("pnumber",7780669124)
        #user_mailid = request_data['emailid']
        print('111111111111111')
        print(user_pnumber)
        request_data = request.get_json()
        print('22222222222222')
        user_potp = request_data["otp"]

        appverify_details = session.query(TblApplicantverif).get(user_potp)
        print(appverify_details)
        print('333333333333')
        if  appverify_details != None:
            if user_potp == appverify_details.applicant_potp:
                print('44444444444')
                if datetime.now() <= appverify_details.applicant_potp_exptime:
                    print('555555555555')
                    session.query(TblApplicantverif).filter_by(applicant_potp=user_potp).update(
                    {
                    TblApplicantverif.applicant_pverify_flag:True      
                    }
                    )  
                    session.commit()
                                      
                    return "Phone verified successfully"

                    # print('{}'.format(jobdetails.job_status)) 
                else:
                    return "OTP expired"
        else:
            return "Invalid Otp"     
    except Exception as e:
            #print("Invalid Otp")
        print(e)