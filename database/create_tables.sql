create table students
(
	student_uid uuid not null
		constraint student_pk
			primary key,
	name varchar not null,
	grade integer not null
);

comment on table students is 'table contains information for students';

alter table students owner to lernhelfer;

create unique index student_student_uid_uindex
	on students (student_uid);

create table subjects
(
	subject_id serial not null
		constraint subjects_pk
			primary key,
	subject_name varchar not null,
	description varchar
);

alter table subjects owner to lernhelfer;

create unique index subjects_subject_id_uindex
	on subjects (subject_id);

create table teachers
(
	teacher_uid uuid not null
		constraint teachers_pk
			primary key,
	name varchar not null,
	help_count integer default 0 not null,
	profile_image bytea
);

alter table teachers owner to lernhelfer;

create unique index teachers_teacher_uid_uindex
	on teachers (teacher_uid);

create table teachers_classes
(
	teacher_uid uuid not null
		constraint teachers_classes_teachers_teacher_uid_fk
			references teachers
				on delete cascade,
	class integer not null,
	constraint teachers_classes_pk
		primary key (teacher_uid, class)
);

alter table teachers_classes owner to lernhelfer;

create table teachers_reaches
(
	teacher_uid uuid not null
		constraint teacher_reaches_teachers_teacher_uid_fk
			references teachers
				on delete cascade,
	order_number integer not null,
	contact_type varchar not null,
	contact_reach varchar not null,
	constraint teacher_reaches_pk
		primary key (teacher_uid, order_number)
);

alter table teachers_reaches owner to lernhelfer;

create table topics
(
	topic_id integer not null
		constraint topics_pk
			primary key,
	topic_name varchar not null,
	description varchar,
	grade integer not null
);

alter table topics owner to lernhelfer;

create unique index topics_topic_id_uindex
	on topics (topic_id);

create table grades
(
	grade integer not null
		constraint grades_pk
			primary key,
	description varchar
);

alter table grades owner to lernhelfer;

create unique index grades_grade_uindex
	on grades (grade);

create table teachers_subjects_topics
(
	teacher_uid uuid not null
		constraint teachers_subjects_topics_teachers_teacher_uid_fk
			references teachers
				on delete cascade,
	subject_id integer not null
		constraint teachers_subjects_topics_subjects_subject_id_fk
			references subjects,
	topic_id integer not null
		constraint teachers_subjects_topics_topics_topic_id_fk
			references topics,
	constraint teachers_subjects_topics_pk
		primary key (teacher_uid, subject_id, topic_id)
);

alter table teachers_subjects_topics owner to lernhelfer;

create table learn_requests
(
	learn_request_id uuid not null
		constraint learn_requests_pk
			primary key,
	last_modification_date date default now() not null,
	student_uid uuid not null
		constraint learn_requests_students_student_uid_fk
			references students,
	subject_id integer not null
		constraint learn_requests_subjects_subject_id_fk
			references subjects,
	image bytea,
	question varchar,
	status varchar not null
);

alter table learn_requests owner to lernhelfer;

create unique index learn_requests_learn_request_id_uindex
	on learn_requests (learn_request_id);

create table learn_requests_topics
(
	learn_request_id uuid not null
		constraint learn_requests_topics_learn_requests_learn_request_id_fk
			references learn_requests
				on delete cascade,
	topic_id integer not null
		constraint learn_requests_topics_topics_topic_id_fk
			references topics,
	constraint learn_requests_topics_pk
		primary key (learn_request_id, topic_id)
);

alter table learn_requests_topics owner to lernhelfer;

create table help_offers
(
	help_offer_id uuid not null
		constraint help_offers_pk
			primary key,
	teacher_uid uuid not null
		constraint help_offers_teachers_teacher_uid_fk
			references teachers
				on delete cascade,
	learn_request_id uuid not null
		constraint help_offers_learn_requests_learn_request_id_fk
			references learn_requests
				on delete cascade,
	message varchar not null,
	status varchar not null
);

alter table help_offers owner to lernhelfer;

create unique index help_offers_help_offer_id_uindex
	on help_offers (help_offer_id);
