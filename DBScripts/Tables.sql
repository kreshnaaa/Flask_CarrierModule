
--create  table for job details

drop table "JOB_DETAILS" CASCADE;
CREATE TABLE public."JOB_DETAILS" (
	job_title varchar(100) ,
	job_location varchar(100) ,
	job_code int primary key generated by default as identity ,
	job_status varchar(20) ,
	experience_range varchar(200) ,
	must_have_skills varchar(200) ,
	good_to_have_skills varchar(200)  ,
	job_desc_roles_resp varchar(2000)  ,
	edu_qualification varchar(400)  ,
	job_created_date date 
	);

--create table for applicant details
drop table "APPLICANT_DETAILS" CASCADE
CREATE TABLE public."APPLICANT_DETAILS"(
     applicant_id int primary key generated by default as identity , 
     first_name varchar(100) ,
     last_name varchar(100) ,
     gender varchar(20) ,
     email_id varchar(100) ,
     mobile_no bigint ,
     address_line1 varchar(200) ,
     address_line2 varchar(200) ,
     city varchar(100) ,
     pincode int ,
     applicant_state varchar(100) ,
     country varchar(100) 
);

--create table for applied_jobs
drop table "APPLIED_JOBS" CASCADE;
CREATE TABLE public."APPLIED_JOBS"(
    job_code int REFERENCES "JOB_DETAILS"(job_code),--REFERENCES JOB_DETAILS(job_code),
    applicant_id int REFERENCES "APPLICANT_DETAILS"(applicant_id),--  REFERENCES applicant_details(applicant_id),
    applied_on	date ,
    document_name varchar(50) ,
    document_path varchar(400) ,
    application_status	int ,
    reason_for_rejection varchar(500)
)
   
    --app_applicant_id bigint FOREIGN KEY REFERENCES applicant_details(applicant_id)
alter table "JOB_DETAILS" alter column job_status type varchar(20)--create  table for job details

-- drop table "JOB_DETAILS" CASCADE;
-- CREATE TABLE public."JOB_DETAILS" (
-- 	job_title varchar(100) ,
-- 	job_location varchar(100) ,
-- 	job_code int primary key generated by default as identity ,
-- 	job_status int ,
-- 	experience_range varchar(200) ,
-- 	must_have_skills varchar(200) ,
-- 	good_to_have_skills varchar(200)  ,
-- 	job_desc_roles_resp varchar(2000)  ,
-- 	edu_qualification varchar(400)  ,
-- 	job_created_date date 
-- 	);

-- --create table for applicant details
-- drop table "APPLICANT_DETAILS" CASCADE
-- CREATE TABLE public."APPLICANT_DETAILS"(
--      applicant_id int primary key , 
--      first_name varchar(100) ,
--      last_name varchar(100) ,
--      gender varchar(20) ,
--      email_id varchar(100) ,
--      mobile_no bigint ,
--      address_line1 varchar(200) ,
--      address_line2 varchar(200) ,
--      city varchar(100) ,
--      pincode int ,
--      applicant_state varchar(100) ,
--      country varchar(100) 
-- );

-- --create table for applied_jobs
-- drop table "APPLIED_JOBS" CASCADE;
-- CREATE TABLE public."APPLIED_JOBS"(
--     job_code int REFERENCES "JOB_DETAILS"(job_code),--REFERENCES JOB_DETAILS(job_code),
--     applicant_id int REFERENCES "APPLICANT_DETAILS"(applicant_id),--  REFERENCES applicant_details(applicant_id),
--     applied_on	date ,
--     document_name varchar(50) ,
--     document_path varchar(400) ,
--     application_status	int ,
--     reason_for_rejection varchar(500)
-- )
   
--     --app_applicant_id bigint FOREIGN KEY REFERENCES applicant_details(applicant_id)
