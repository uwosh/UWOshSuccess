I think that these are the original peoplesoft database queries that were used to build the vocabularies in this folder.

UWOshSubjects:
select s1.subject from ps_subject_tbl s1 where eff_status = 'A' and effdt = (select max(effdt) from ps_subject_tbl s2 where s1.subject = s2.subject) order by s1.subject;

UWOshSemesters:
select strm, descr, descrshort from ps_term_val_tbl where strm >= '0630' and strm < '9999' order by strm

UWOshBuildings:
select bldg_cd, descrshort from ps_bldg_tbl p1 where p1.eff_status = 'A' and p1.effdt = (select max(effdt) from ps_bldg_tbl p2 where p1.bldg_cd = p2.bldg_cd and p2.eff_status = 'A');
