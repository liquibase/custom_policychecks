--liquibase formatted sql
--changeset mikeo:indexgood
CREATE UNIQUE INDEX IDX_TITLE ON T_FILM (TITLE) TABLESPACE "INDEXES";
--rollback drop index IDX_TITLE

--changeset mikeo:indexbad
CREATE INDEX INDEX_DIRECTOR ON T_FILM (DIRECTOR);
--rollback drop index INDEX_DIRECTOR

--changeset mikeo:indexbad-2
CREATE UNIQUE INDEX IDX_USERS_TITLE ON T_FILM (TITLE) TABLESPACE "USERS";
--rollback drop index IDX_USERS_TITLE

--changeset mikeo:indexgood-2
CREATE INDEX INDEX_IDX_DIRECTOR ON T_FILM (DIRECTOR) TABLESPACE "INDEXES";
--rollback drop index INDEX_IDX_DIRECTOR

--changeset mikeo:indexbad-3
CREATE INDEX INDEX_DIRECTOR_BAD ON T_FILM (DIRECTOR) TABLESPACE "USERS";
--rollback drop index INDEX_DIRECTOR_BAD