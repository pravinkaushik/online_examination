-- test.candidate definition

CREATE TABLE `candidate` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '	',
  `exam_config_id` int DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password_hash` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `exam_owner_id` int DEFAULT NULL,
  `c_name` varchar(100) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

-- test.candidate_exam definition

CREATE TABLE `candidate_exam` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exam_questions_id` int DEFAULT NULL,
  `candidate_id` int DEFAULT NULL,
  `exam_config_id` int DEFAULT NULL,
  `current_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_choice1_selected` tinyint DEFAULT NULL,
  `is_choice2_selected` tinyint DEFAULT NULL,
  `is_choice3_selected` tinyint DEFAULT NULL,
  `is_choice4_selected` tinyint DEFAULT NULL,
  `is_choice5_selected` tinyint DEFAULT NULL,
  `answer` mediumtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=138 DEFAULT CHARSET=latin1;

-- test.exam_config definition

CREATE TABLE `exam_config` (
  `id` int NOT NULL AUTO_INCREMENT,
  `exam_owner_id` int DEFAULT NULL,
  `random_question` tinyint(1) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_minute` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `exam_title` varchar(45) DEFAULT NULL,
  `exam_name` varchar(45) DEFAULT NULL,
  `time_zone` varchar(100) DEFAULT NULL,
  `question_per_page` smallint DEFAULT NULL,
  `total_question` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;

-- test.exam_questions definition

CREATE TABLE `exam_questions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `question` mediumtext,
  `choice1` mediumtext,
  `choice2` mediumtext,
  `choice3` mediumtext,
  `choice4` mediumtext,
  `choice5` mediumtext,
  `exam_owner_id` int DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `question_type` tinyint DEFAULT NULL,
  `exam_config_id` int DEFAULT NULL,
  `negative_marks` smallint DEFAULT NULL,
  `positive_marks` smallint DEFAULT NULL,
  `is_choice1_correct` tinyint DEFAULT NULL,
  `is_choice2_correct` tinyint DEFAULT NULL,
  `is_choice3_correct` tinyint DEFAULT NULL,
  `is_choice4_correct` tinyint DEFAULT NULL,
  `is_choice5_correct` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=latin1;

-- test.`user` definition

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activation_link` varchar(45) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  `is_social_login` tinyint DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;


-- pip install flask-marshmallow
-- pip install Flask-Mail
-- pip install requests
-- pip install Flask-Mail
-- pip install flasgger

CREATE OR REPLACE
ALGORITHM = UNDEFINED VIEW `RESULT_LIST_VIEW` AS
SELECT ce.candidate_id, cand.c_name, cand.email, cand.start_time, cand.end_time, ce.exam_config_id, eq.question_type, eq.id,
CASE
	WHEN eq.question_type = 3 THEN IFNULL(ce.subjective_mark,0)
	WHEN IFNULL(ce.is_choice1_selected,0) = eq.is_choice1_correct AND IFNULL(ce.is_choice2_selected,0) = eq.is_choice2_correct
		AND IFNULL(ce.is_choice3_selected,0) = eq.is_choice3_correct AND IFNULL(ce.is_choice4_selected,0) = eq.is_choice4_correct 
		AND IFNULL(ce.is_choice5_selected,0) = eq.is_choice5_correct THEN eq.positive_marks	
    ELSE 0
END AS positive_marks,
CASE
	WHEN eq.question_type != 3 THEN 0
    WHEN IFNULL(ce.is_choice1_selected,0) != eq.is_choice1_correct OR IFNULL(ce.is_choice2_selected,0) != eq.is_choice2_correct
		OR IFNULL(ce.is_choice3_selected,0) != eq.is_choice3_correct OR IFNULL(ce.is_choice4_selected,0) != eq.is_choice4_correct 
		OR IFNULL(ce.is_choice5_selected,0) != eq.is_choice5_correct THEN eq.negative_marks 
    ELSE 0
END AS negative_marks
FROM exam_questions eq inner join candidate_exam ce on ce.exam_questions_id = eq.id 
	inner join candidate cand on cand.id = ce.candidate_id;
	
SELECT candidate_id, c_name, email, start_time, end_time, exam_config_id, SUM(positive_marks) AS total_pos, SUM(negative_marks) AS total_neg from RESULT_LIST_VIEW where exam_config_id=12 group by candidate_id, exam_config_id;

