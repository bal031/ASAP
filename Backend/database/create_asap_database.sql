/*
 * Use this script to create the asap-databse. 
 * NOTE: Make sure there is no database in the server called 'asap_database'.
 *       You can delete such a database by typing `DROP DATABASE asap_database`,
 *       but this will delete all data in that database, so cautious.
 *
 * TO USE:
 * 1. Be in the directory with this file. 
 * 2. Log into the mysql server with root.
 * 3. type `source create_asap_database.sql`
 */
CREATE DATABASE asap_database;
USE asap_database;

CREATE TABLE `user` (
	`userID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`create_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`email` varchar(255) NOT NULL,
	`google_id` varchar(255) NOT NULL,
	PRIMARY KEY (`userID`)
);

CREATE TABLE `schedule` (
	`scheduleID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`userID` INT NOT NULL,
	`name` varchar(255) NOT NULL,
	`term_quarter` varchar(2) NOT NULL,
	`term_year` varchar(4) NOT NULL,
	PRIMARY KEY (`scheduleID`)
);

CREATE TABLE `class_schedule_event` (
	`scheduleID` INT NOT NULL,
	`sectionID` INT NOT NULL
);

CREATE TABLE `personal_event` (
	`end` DATETIME NOT NULL,
	`name` varchar(255) NOT NULL,
	`start` DATETIME NOT NULL,
	`scheduleID` INT NOT NULL
);

CREATE TABLE `course` (
	`courseID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`course_code` varchar(16) NOT NULL,
	`subject_code` varchar(16) NOT NULL,
	PRIMARY KEY (`courseID`)
);

CREATE TABLE `current_class_section` (
	`sectionID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`instruction_type` varchar(8) NOT NULL,
	`section_code` varchar(32) NOT NULL,
	`term_code` varchar(8) NOT NULL,
	`professorID` INT NOT NULL,
	`courseID` INT NOT NULL,
	PRIMARY KEY (`sectionID`)
);

CREATE TABLE `current_section_meeting` (
	`day_code` varchar(4) NOT NULL,
	`end_time` TIME NOT NULL,
	`start_time` TIME NOT NULL,
	`roomID` INT,
	`sectionID` INT NOT NULL
);

CREATE TABLE `current_additional_meeting` (
	`meeting_date` DATE NOT NULL,
	`meeting_type` varchar(16) NOT NULL,
	`start_time` TIME NOT NULL,
	`end_time` TIME NOT NULL,
	`roomID` INT,
	`sectionID` INT NOT NULL
);

CREATE TABLE `professor` (
	`professorID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`name` varchar(255) NOT NULL,
	PRIMARY KEY (`professorID`)
);

CREATE TABLE `cape_review` (
	`courseID` INT NOT NULL,
	`professorID` INT NOT NULL,
	`expected_grade` FLOAT NOT NULL,
	`hours_per_week` FLOAT NOT NULL,
	`received_grade` FLOAT NOT NULL,
	`recommend_course` FLOAT NOT NULL,
	`recommend_professor` FLOAT NOT NULL,
	`response_rate` FLOAT NOT NULL,
	`term_code` varchar(8) NOT NULL
);

CREATE TABLE `room` (
	`roomID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`room_code` varchar(32) NOT NULL DEFAULT 'TBA',
	`building_code` varchar(32) NOT NULL DEFAULT 'TBA',
	PRIMARY KEY (`roomID`)
);

ALTER TABLE `schedule` ADD CONSTRAINT `schedule_fk0` FOREIGN KEY (`userID`) REFERENCES `user`(`userID`);

ALTER TABLE `class_schedule_event` ADD CONSTRAINT `class_schedule_event_fk0` FOREIGN KEY (`scheduleID`) REFERENCES `schedule`(`scheduleID`);

ALTER TABLE `class_schedule_event` ADD CONSTRAINT `class_schedule_event_fk1` FOREIGN KEY (`sectionID`) REFERENCES `current_class_section`(`sectionID`);

ALTER TABLE `personal_event` ADD CONSTRAINT `personal_event_fk0` FOREIGN KEY (`scheduleID`) REFERENCES `schedule`(`scheduleID`);

ALTER TABLE `current_class_section` ADD CONSTRAINT `current_class_section_fk0` FOREIGN KEY (`professorID`) REFERENCES `professor`(`professorID`);

ALTER TABLE `current_class_section` ADD CONSTRAINT `current_class_section_fk1` FOREIGN KEY (`courseID`) REFERENCES `course`(`courseID`);

ALTER TABLE `current_section_meeting` ADD CONSTRAINT `current_section_meeting_fk0` FOREIGN KEY (`roomID`) REFERENCES `room`(`roomID`);

ALTER TABLE `current_section_meeting` ADD CONSTRAINT `current_section_meeting_fk1` FOREIGN KEY (`sectionID`) REFERENCES `current_class_section`(`sectionID`);

ALTER TABLE `current_additional_meeting` ADD CONSTRAINT `current_additional_meeting_fk0` FOREIGN KEY (`roomID`) REFERENCES `room`(`roomID`);

ALTER TABLE `current_additional_meeting` ADD CONSTRAINT `current_additional_meeting_fk1` FOREIGN KEY (`sectionID`) REFERENCES `current_class_section`(`sectionID`);

ALTER TABLE `cape_review` ADD CONSTRAINT `cape_review_fk0` FOREIGN KEY (`courseID`) REFERENCES `course`(`courseID`);

ALTER TABLE `cape_review` ADD CONSTRAINT `cape_review_fk1` FOREIGN KEY (`professorID`) REFERENCES `professor`(`professorID`);