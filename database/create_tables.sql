create table students
(
	student_uid uuid not null
		constraint student_pk
			primary key,
	name varchar not null,
	class integer not null
);

comment on table students is 'table contains information for students';

alter table students owner to lernhelfer;

create unique index student_student_uid_uindex
	on students (student_uid);

create table classes
(
	class integer not null
		constraint classes_pk
			primary key,
	description varchar
);

alter table classes owner to lernhelfer;

create unique index classes_class_uindex
	on classes (class);

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
	has_helped integer
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