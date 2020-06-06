

CREATE TABLE `candidate` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '	',
  `exam_config_id` int(11) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `password_hash` varchar(45) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `exam_owner_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1

CREATE TABLE `candidate_exam` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_questions_id` int(11) DEFAULT NULL,
  `provided_answer` varchar(45) DEFAULT NULL,
  `candidate_id` int(11) DEFAULT NULL,
  `exam_config_id` int(11) DEFAULT NULL,
  `current_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1

CREATE TABLE `exam_config` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `exam_owner_id` int(11) DEFAULT NULL,
  `random_question` tinyint(1) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `end_time` datetime DEFAULT NULL,
  `duration_minute` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `exam_title` varchar(45) DEFAULT NULL,
  `exam_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1

CREATE TABLE `exam_questions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` varchar(512) DEFAULT NULL,
  `choice1` varchar(128) DEFAULT NULL,
  `choice2` varchar(128) DEFAULT NULL,
  `choice3` varchar(128) DEFAULT NULL,
  `choice4` varchar(128) DEFAULT NULL,
  `choice5` varchar(128) DEFAULT NULL,
  `correct_answer` varchar(45) DEFAULT NULL,
  `exam_owner_id` int(11) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `is_multiple_choice` tinyint(4) DEFAULT NULL,
  `exam_config_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `activation_link` varchar(45) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1


SELECT ce.id, ce.exam_questions_id, ce.candidate_id, ce.exam_config_id, ce.is_choice1_correct, ce.is_choice2_correct, ce.is_choice3_correct, ce.is_choice4_correct, ce.is_choice5_correct,
eq.question, eq.choice1, eq.choice2, eq.choice3, eq.choice4, eq.choice5, eq.is_multiple_choice, eq.negative_marks, eq.positive_marks
FROM candidate_exam ce inner join exam_questions eq on ce.exam_questions_id = eq.id 
WHERE ce.candidate_id=13 and ce.exam_config_id=12;

    result = session_candidate_exam_app.execute(
        'SELECT ce.id, ce.exam_questions_id, ce.candidate_id, ce.exam_config_id, ce.is_choice1_correct, ce.is_choice2_correct, ce.is_choice3_correct, ce.is_choice4_correct, ce.is_choice5_correct,\
        eq.question, eq.choice1, eq.choice2, eq.choice3, eq.choice4, eq.choice5, eq.is_multiple_choice, eq.negative_marks, eq.positive_marks\
        FROM candidate_exam ce inner join exam_questions eq on ce.exam_questions_id = eq.id \
        WHERE ce.candidate_id=:val1 and ce.exam_config_id=:val2 ORDER BY ce.id DESC LIMIT offset, row_count',
        {'val1': candidate_id, 'val2': exam_config_id}).paginate(page,per_page,error_out=False)

SELECT ce.id, ce.exam_questions_id, ce.candidate_id, ce.exam_config_id, ce.is_choice1_correct, ce.is_choice2_correct, ce.is_choice3_correct, ce.is_choice4_correct, ce.is_choice5_correct,
eq.question, eq.choice1, eq.choice2, eq.choice3, eq.choice4, eq.choice5, eq.is_multiple_choice, eq.negative_marks, eq.positive_marks
FROM candidate_exam ce inner join exam_questions eq on ce.exam_questions_id = eq.id 
WHERE ce.candidate_id=13 and ce.exam_config_id=12 ORDER BY ce.id DESC LIMIT offset, row_count;

pip install flask-marshmallow
pip install Flask-Mail
pip install requests
