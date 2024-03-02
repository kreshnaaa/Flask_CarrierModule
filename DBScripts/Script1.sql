insert into "JOB_DETAILS" (job_title,job_location,job_status,experience_range,must_have_skills,good_to_have_skills,
                           job_desc_roles_resp,edu_qualification,job_created_date) 
values('Python Developer','"Hyderabd"',2,'2 to 4 years','python, database, flask','github, aws, azure',
        'able to develop the scripts','bachelor of technology','2022-04-01')
        
alter table JOB_DETAILS alter column job_status type varchar(20)

ALTER TABLE table_name ADD PRIMARY KEY(JOB_CODE)
ALTER TABLE "JOB_DETAILS"   ADD  PRIMARY key(JOB_CODE)
ALTER TABLE "JOB_DETAILS"   add constraint   "JOB_DETAILS_pkey" primary key(JOB_CODE)                                     

ALTER TABLE "JOB_DETAILS" DROP primary key
ALTER TABLE "JOB_DETAILS" DROP CONSTRAINT job_code_pkey
ALTER TABLE "JOB_DETAILS" DROP CONSTRAINT "JOB_DETAILS_pkey"--_pkey
alter table "APPLIED_JOBS" ADD constraint "APPLIED_JOBS_job_code_fkey"

select * from "APPLIED_JOBS"
select * from "APPLICANT_DETAILS"
select * from "JOB_DETAILS"
update "JOB_DETAILS" set job_status = 'active' where job_code = 10 

delete from  "JOB_DETAILS" where JOB_CODE = 12
delete from "JOB_DETAILS" where job_location = 'Newzealand'
delete from "APPLICANT_DETAILS" where applicant_id =10
delete from "APPLIED_JOBS" where job_code = 10
delete from "APPLIED_JOBS" where applicant_id = 6

UPDATE "APPLIED_JOBS" --format schema.table_name
SET 
applicant_id = "APPLICANT_DETAILS".applicant_id
FROM "APPLICANT_DETAILS"  -- mention schema name
WHERE "APPLIED_JOBS".job_code =10
AND  
"APPLICANT_DETAILS".mobile_no = 9848032919

insert into "APPLIED_JOBS"(applicant_id where "APPLIED_JOBS".job_code =10) select applicant_id from "APPLICANT_DETAILS"
            where mobile_no = 9848032919 
 
insert into "APPLIED_JOBS"(applicant_id) select applicant_id from "APPLICANT_DETAILS"  where mobile_no = 123456



 alter table "APPLIED_JOBS" add CONSTRAINT "APPLIED_JOBS_pkey" PRIMARY KEY (job_code,applicant_id)  

 
 
 alter table "APPLIED_JOBS" add column job_title text;
alter table "APPLIED_JOBS" add column applicant_name text; 

alter table "APPLICANT_DETAILS" add column document_name text;
alter table "APPLICANT_DETAILS" add column document_path text;