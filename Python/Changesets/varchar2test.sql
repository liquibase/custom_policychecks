--liquibase formatted sql
--changeset mikeo:goodchange
CREATE TABLE "T_MIKE_RATING" 
   ("TITLE" VARCHAR2(50 CHAR), 
	"DIRECTOR" VARCHAR2(30 CHAR), 
	"RATING" NUMBER(*,0) DEFAULT 3
   );
--rollback drop table T_MIKE_RATING;

--changeset mikeo:badchange
CREATE TABLE "T_MIKEBAD_RATING" 
   ("TITLE" VARCHAR2(50), 
	"DIRECTOR" VARCHAR2(30), 
	"RATING" NUMBER(*,0) DEFAULT 3
   );
--rollback drop table T_MIKEBAD_RATING;