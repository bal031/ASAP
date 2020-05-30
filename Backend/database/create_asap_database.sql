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
	`term_code` varchar(8) NOT NULL,
	PRIMARY KEY (`scheduleID`)
);

CREATE TABLE `class_event` (
	`section_id` INT(16) NOT NULL,
	`scheduleID` INT NOT NULL
);

CREATE TABLE `personal_event` (
	`name` varchar(255) NOT NULL,
	`day_code` varchar(4) NOT NULL,
	`start_time` TIME NOT NULL,
	`end_time` TIME NOT NULL,
	`scheduleID` INT NOT NULL
);

CREATE TABLE `course` (
	`courseID` INT NOT NULL AUTO_INCREMENT UNIQUE,
	`course_code` varchar(16) NOT NULL,
	`subject_code` varchar(16) NOT NULL,
	PRIMARY KEY (`courseID`)
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

ALTER TABLE `schedule` ADD CONSTRAINT `schedule_fk0` FOREIGN KEY (`userID`) REFERENCES `user`(`userID`);

ALTER TABLE `class_event` ADD CONSTRAINT `class_event_fk0` FOREIGN KEY (`scheduleID`) REFERENCES `schedule`(`scheduleID`);

ALTER TABLE `personal_event` ADD CONSTRAINT `personal_event_fk0` FOREIGN KEY (`scheduleID`) REFERENCES `schedule`(`scheduleID`);

ALTER TABLE `cape_review` ADD CONSTRAINT `cape_review_fk0` FOREIGN KEY (`courseID`) REFERENCES `course`(`courseID`);

ALTER TABLE `cape_review` ADD CONSTRAINT `cape_review_fk1` FOREIGN KEY (`professorID`) REFERENCES `professor`(`professorID`);