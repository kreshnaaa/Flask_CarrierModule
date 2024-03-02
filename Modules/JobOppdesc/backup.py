
from cgi import test
from re import A
from ssl import ALERT_DESCRIPTION_RECORD_OVERFLOW
from tokenize import Number
from numpy import number
from pymysql import NULL
from app import app, db, engine, app, session
import pandas as pd
from matplotlib import collections
#from config import DBConfig,cursor
from flask import Flask,render_template,request,jsonify
import json
from typing import OrderedDict
from db_models import TblJobDetails,create,TblApplicantDetails,update,TblAppliedJobs
from psycopg2 import DatabaseError, OperationalError, errors, NotSupportedError, Error, InternalError, ProgrammingError, InterfaceError, IntegrityError
from datetime import datetime

# from flask_mysqldb import MySQL
# import mysql.connector as msc


# @app.route('/jobopp/',methods = ['GET'])
# def jobapp():
#     try:   
#         if  request.method=="GET":
#              sql = 'SELECT job_position,job_id,job_location from job_positions_info where job_status_flag = 2'
#              joboverview = sql.fetchall(engine)
#              data_list = []
#              for row in joboverview:
#                 d = collections.OrderedDict()
#                 d['job_position'] =row[0]
#                 d['job_id']       =row[1]
#                 d['job_location'] =row[2]
#                 data_list.append(d)
#                 jsonData_list = json.dumps(data_list)
#         return jsonData_list            
#     except Exception as e:
#             print('Error! Unable to Display',str(e))
@app.route('/jobopp/',methods = ['GET'])
def jobopp():
    try:   
        if  request.method=="GET":
             sql = 'SELECT job_position,job_id,job_location,role_description from "JOB_DETAILS" where job_status_flag = 2'
             df = pd.read_sql_query(sql, engine)
             print(df)
             jsonData = df.to_dict('records')
        return jsonify(jsonData)            
    except Exception as e:
            print('Error! Unable to Display',str(e))

@app.route('/jobdesc/',methods = ['GET'])
def jobdesc():
    try:   
        if  request.method=="GET":
             sql = '''SELECT job_id, job_position, job_location, experience_required, 
             minimum_qualification, must_have_skills, good_to_have_skills, role_description, 
             job_status_flag from job where job_status_flag = "active"'''
             df = pd.read_sql_query(sql, engine)
             print(df)
             jsonData = df.to_dict('records')
        return jsonify(jsonData)            
    except Exception as e:
            print('Error! Unable to Display',str(e))

@app.route('/createjobold/', methods = ['POST'] )
def createjobold():
    try:
        print('createjob')
        request_data = request.get_json()
        jobtitle = request_data['jobtitle']
        joblocation = request_data['joblocation']
        experiencerange = request_data['experiencerange']
        musthaveskills = request_data['musthaveskills']
        goodtohaveskills = request_data['goodtohaveskills']
        jobdes_role_resp = request_data['jobdes_role_resp']
        eduqualification = request_data['eduqualification']
        creation_date = datetime.now().strftime('%Y-%m-%d')
        print('date:{}'.format(creation_date))
        jobstatus = 'active'
        print('test1')
        sql ='''insert into "JOB_DETAILS" (job_title,job_location,job_status,experience_range,must_have_skills,
                good_to_have_skills, job_desc_roles_resp,edu_qualification,job_created_date) 
                values('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(jobtitle,joblocation,jobstatus,experiencerange,musthaveskills,
                 goodtohaveskills,jobdes_role_resp,eduqualification,creation_date)
        print("sql:{}".format(sql))         
        status = engine.execute(sql)
        print("sts:{}".format(status))
        return jsonify("successful")
    except Exception as e:
        print('Error! Unable to Display', str(e))   

@app.route('/createjob/', methods = ['POST'] )
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

@app.route('/jobdetails/<int:Number>', methods = ['GET'])
def jobdetails(Number):
    #jobcode = {}.format(Number)
    try:
        if  request.method=="GET":
             sql = '''SELECT job_title,job_location,job_status,experience_range,must_have_skills,
                good_to_have_skills, job_desc_roles_resp,edu_qualification,job_created_date from "JOB_DETAILS"
                where job_code = {}'''.format(Number)
             df = pd.read_sql_query(sql, engine)
             print(df)
             jsonData = df.to_dict('records') 
        return jsonify(jsonData)               
    except Exception as e:
            print('Error! Unable to Display',str(e))
 

#using data frames
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

@app.route('/getAlljobs', methods = ['GET'])
def getllAlljobs():
    #jobcode = {}.format(Number)
    try:
        sql = '''SELECT * from "JOB_DETAILS where job_status = 'active'"   '''
        df = pd.read_sql_query(sql, engine)
        df['job_created_date'] = df['job_created_date'].apply(lambda x:datetime.strftime(x,'%Y-%m-%d'))
        #df.pop('job_created_date')
        #df = df[['edu_qualification','experience_range','good_to_have_skills']]
        #print(df)
        jsonData = df.to_dict('r') 
        return jsonify(jsonData)               
    except Exception as e:
            print('Error! Unable to Display',str(e))

# @app.route('/updateJob/<int:job_id>', methods = ['PUT'])
# def updateJob(job_id):
    
#     try:
#         request_data = request.get_json()
#         jobtitle = request_data['job_title']
#         joblocation = request_data['job_location']
#         experiencerange = request_data['experience_range']
#         musthaveskills = request_data['must_have_skills']
#         goodtohaveskills = request_data['good_to_have_skills']
#         jobdesroleresp = request_data['job_desc_roles_resp']
#         eduqualification = request_data['edu_qualification']
#         creation_date = datetime.now().strftime('%Y-%m-%d')
#         jobstatus = 'active'
#         sql = '''SELECT * from "JOB_DETAILS" where job_code = {}'''.format(job_id)
                
             
#         df = pd.read_sql_query(sql, engine)
#         df['job_status'] = 'inactive'
#         #df.to_sql('JOB_DETAILS',con = engine,index = False,if_exists= 'append')
#         sql = '''delete from "JOB_DETAILS" where job_code = {}
#                 '''.format(job_id)
#         engine.connect().execute(sql)     
#         #df.pop('job_code')
#         #df.to_sql("JOB_DETAILS",con = engine,index = False,if_exists= 'append')
#         df['job_title'] = jobtitle
#         df['job_location'] = joblocation
#         df['job_status'] = jobstatus
#         df['experience_range'] = experiencerange
#         df['must_have_skills'] = musthaveskills
#         df['good_to_have_skills'] = goodtohaveskills
#         df['job_desc_roles_resp'] = jobdesroleresp
#         df['edu_qualification'] = eduqualification
#         df['job_created_date'] = creation_date
#         df.to_sql("JOB_DETAILS",con = engine,index = False,if_exists= 'append')
#         #df.pop('job_created_date')
#         #df = df[['edu_qualification','experience_range','good_to_have_skills']]
#         #print(df)
#         #jsonData = df.to_dict('r') 
#         return jsonify("Successfully Updated")               
#     except Exception as e:
#         print('Error while updating',str(e))            


@app.route('/updateJobdetail/<int:job_id>', methods = ['PUT'])
def updateJobdetail(job_id):
    #jobcode = {}.format(Number)
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
        )                 # .where(job_code = job_id)
#                             # jobdetailobj.job_title = request_data['job_title']
#                         # jobdetailobj.job_location  = request_data['job_location']
#                         # jobdetailobj.experience_range = request_data['experience_range']
#                         # jobdetailobj.musthaveskills   = request_data['must_have_skills']
#                         # jobdetailobj.goodtohaveskills   = request_data['good_to_have_skills']
#                         # jobdetailobj.jobdesroleresp   = request_data['job_desc_roles_resp']
#                         # jobdetailobj.eduqualification = request_data['edu_qualification']
#                         # jobdetailobj.creation_date = datetime.now().strftime("%Y-%m-%d")
        session.commit()
#                         # for i in request_data:
#                         #     if 'job_title' in request_data:
#                         #         jobdetailobj.update(
#                         #         {
#                         #         TblJobDetails.job_title:request_data[i]

#                         #         }
#                         #     ) 
                                
        return jsonify("Successfully Updated")               
    except Exception as e:
        print('Error while updating',str(e))            

@app.route('/createapplication/<int:jobcode>', methods = ['POST'])
def createApplication(jobcode):
    try:

        request_data = request.get_json()
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
            #job_created_date = datetime.now().strftime("%Y-%m-%d"),
            #job_status = 'active'
        )
        create(appdetails)
        appdetails1 = TblAppliedJobs(
            job_code = jobcode,
            applied_on = datetime.now().strftime("%Y-%m-%d"),
            applicant_id = appdetails.applicant_id
            )
        create(appdetails1)   
        print('Job Creation Complete')
        #print('jobstatus:{}'.format(appdetails.job_status))
        #print('jobid:{}'.format(appdetails.job_code))
        print('applicantid:{}'.format(appdetails.applicant_id))
        print('Printing Jobid')
        return jsonify("successful inserted job details and the job id is :{}".format(jobcode))
    except Exception as e:
        print('Error while updating',str(e))





@app.route('/createapplicationold/<int:jobcode>', methods = ["POST"])
def createApplicationold(jobcode):
    try:
        
        request_data = request.get_json()
        firstname = request_data['first_name']
        lastname = request_data['last_name']
        gender = request_data['gender']
        emailid = request_data['email_id']
        mobileno = request_data['mobile_no']
        addressline1 = request_data['address_line1']
        addressline2 = request_data['address_line2']
        applicantcity = request_data['city']
        applicantpincode = request_data['pincode']
        applicantstate = request_data['applicant_state']
        applicantcountry = request_data['country']
        applied_date = datetime.now().strftime('%Y-%m-%d')
        print('date:{}'.format(applied_date))
        jobstatus = 'active'
        print('test1')
        sql ='''insert into "APPLICANT_DETAILS" (first_name,last_name,gender,email_id,
        mobile_no,address_line1,address_line2,city,pincode,applicant_state,country) 
        values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(firstname,lastname
        ,gender,emailid,mobileno,addressline1,addressline2,applicantcity,applicantpincode,applicantstate,
        applicantcountry)
        status = engine.execute(sql)
        
        sql2 = '''insert into "APPLIED_JOBS"(job_code,applied_on) values 
                  ('{}','{}')'''.format(jobcode,applied_date)        
        status2 = engine.execute(sql2)
        print("sts:{}".format(status2))
        # sql1 = '''insert into "APPLIED_JOBS"(applicant_id) where job_code = {} select applicant_id from "APPLICANT_DETAILS"
                    #  where mobile_no = {}'''.format(jobcode, mobileno)
        sql1 = '''UPDATE "APPLIED_JOBS" 
                   SET 
                   applicant_id = "APPLICANT_DETAILS".applicant_id
                   FROM "APPLICANT_DETAILS"  
                   WHERE "APPLIED_JOBS".job_code = {}
                   AND  
                   "APPLICANT_DETAILS".mobile_no ={}'''.format(jobcode,mobileno)             
        status1 = engine.execute(sql1)
        print("sts:{}".format(status))
        return jsonify("successful")
    except Exception as e:
        print('Error! Unable to Display', str(e)) 

@app.route('/getallapplications', methods = ['GET'])
def getAllapplications():
    try:
        sql = '''select ad.first_name as ad_fname, ad.last_name as ad_lname,aj.applied_on as aj_appdate,
        aj.application_status as aj_appstatus,jd.job_title  as jd_title,aj.job_code as jd_jcode,
        aj.document_path as aj_docpath     from "APPLICANT_DETAILS"  ad
        inner join "APPLIED_JOBS" aj ON ad.applicant_id = aj.applicant_id 
        inner join "JOB_DETAILS"  jd  ON aj.job_code =jd.job_code '''
        df = pd.read_sql_query(sql, engine)
        print(df)
        jsonData = df.to_dict('records') 
        return jsonify(jsonData)
    except Exception as e:
        print('Error while updating',str(e))

@app.route('/getapplicationdetails/<int:appno>', methods = ['GET'])
def getApplicationdetails(appno):
    try:
         print("a")              
    except Exception as e:
        print('Error! Unable to Display',str(e))

 
#without using dataframes
# @app.route('/jobdetails/<int:Number>',methods = ['GET'])
# def jobdetails(Number):
#     try:
#         sql = '''select job_title,job_location,job_status,experience_range,must_have_skills,good_to_have_skills,
#                  job_desc_roles_resp,edu_qualification from "JOB_DETAILS" where 
#                  job_code = {}'''.format(Number)
#         data = engine.execute(sql)         
#         details = data.fetchall()
#         for row in details:
#             jobtitle         = '{}'.format(row['job_title'])
#             joblocation      = '{}'.format(row['job_location'])
#             jobstatus        = '{}'.format(row['job_status'])
#             experiencerange  = '{}'.format(row['experience_range'])
#             musthaveskills   = '{}'.format(row['must_have_skills'])
#             goodtohaveskills = '{}'.format(row['good_to_have_skills'])
#             jobdescrolesresp = '{}'.format(row['job_desc_roles_resp'])
#             eduqualification = '{}'.format(row['edu_qualification'])
            



        # job_title varchar(100) NOT NULL,
        # job_location varchar(100) NOT NULL,
        # job_code int primary key ,
        # job_status int NOT NULL,
        # experience_range varchar(200) NOT NULL,
        # must_have_skills varchar(200) NOT NULL,
        # good_to_have_skills varchar(200)  NOT NULL,
        # job_desc_roles_resp varchar(2000)  NOT NULL,
        # edu_qualification varchar(400)  NOT NULL,
        # job_created_date date NOT NULL
        #     print(data)
    
# @app.route('/jobappsub/',methods = ['GET','POST'])
# def jobapp():
#     try:
#         data = request.get_json()
#         data['applicant_id'] = data['jobcode'] + data['applicantmobileno'] 
#         #tbldata = session.query(TblAppDetails).filter_by(applicant_id=data['applicant_id'])
#         tbldata = session.query(TblAppDetails).select(TblAppDetails).where(TblAppDetails.applicant_id == data['applicant_id'])
#         if  tbldata == NULL:
#             #print("\n create_employeedetails", data)
#             #response = {"status": 400, 'message': "Something went wrong. Please try again.", 'data': 0, "status_message": "error"}    
#             try:
#                 #applicant_details = TblAppDetails(
#                 session.query(TblAppDetails).insert().values( 
#                     applicant_fname          = data['first_name'],
#                     applicant_lname          = data['last_name'],
#                     applicant_emailid        = data['emailid'],
#                     applicant_mobileno       = data['mobileno'],
#                     applicant_addressline1   = data['addressline1'],
#                     applicant_addressline2   = data['addressline2'],
#                     applicant_city           = data['city'],
#                     applicant_pincode        = data['pincode'],
#                     applicant_state          = data['state'],
#                     applicant_country        = data['country'], 
#                     applicant_resume         = data['resume'],
#                     applicant_id             = data['applicant_id']
#                     )
#                 # response['message']= "Successfully created list master details!"
#                 # response['data'] = data['applicant_id']
#                 # response['status'] = 200
#                 # response['status_message'] = "success"
#             except Exception as e:
#                 print("\n Exception in create_applicantdetails ", e)
#                 # response['message']= "Eror during saving applicant details: " + str(e)
#             print("\n create_applicantdetails", data)
#             return jsonify(e)
#         else:
#             print('Application already submitted')
#     except DatabaseError as e :
#         print('Error while creating Application list data :',str(e))
#         return {
#                 'message': "DB Error",
#                 'status': 400,
#                 'Error': str(e),
#                 'data':0,
#             }, 400
#     except OperationalError as e:
#         print('Error while creating Application list data :',str(e))
#         return {
#                 'message': "Internal Server Error",
#                 'status': 500,
#                 'Error': str(e),
#                 'status_message': str(e),
#                 'data':0,
#             }, 500
#     except Exception as e:
#         print('Error while creating Application list data :',str(e))
#         return {
#                 'message': "Error while creating list data",
#                 'status': 404,
#                 'status_message': str(e),
#                 'Error': str(e),
#                 'data':0,
#             }, 404

            
    