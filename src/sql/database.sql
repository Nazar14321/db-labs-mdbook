USE lab5;

CREATE TABLE `Project` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `Team` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `project_id` INT NOT NULL,
  INDEX `idx_team_project` (`project_id`),
  CONSTRAINT `fk_team_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `User` (
  `id` CHAR(36) NOT NULL PRIMARY KEY
               DEFAULT (UUID()),
  `nickname` VARCHAR(255)   NOT NULL UNIQUE,
  `email`    VARCHAR(255)   NOT NULL UNIQUE,
  `password` TEXT NOT NULL,
  `photo` TEXT NULL,
  `team_id`  INT NOT NULL,
  INDEX `idx_user_team` (`team_id`),
  CONSTRAINT `fk_user_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Team` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `Role` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255)  NOT NULL,
  `description` TEXT,
  `project_id` INT NOT NULL,
  INDEX `idx_role_project` (`project_id`),
  CONSTRAINT `fk_role_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `User_Project` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id` CHAR(36) NOT NULL,
  `project_id` INT NOT NULL,
  `role_id` INT NULL,
  `team_id` INT NULL,
  INDEX `idx_up_user`    (`user_id`),
  INDEX `idx_up_project` (`project_id`),
  INDEX `idx_up_role`    (`role_id`),
  INDEX `idx_up_team`    (`team_id`),
  CONSTRAINT `fk_up_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_up_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_up_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `Role` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_up_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Team` (`id`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Task` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL,
  `description` TEXT,
  `startDate` TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deadlineDate` TIMESTAMP   NULL,
  `team_id` INT NOT NULL,
  INDEX `idx_task_team` (`team_id`),
  CONSTRAINT `fk_task_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Team` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Artifact` (
  `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `status`   VARCHAR(255) NOT NULL,
  `comment`  TEXT,
  `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `task_id`  INT NOT NULL,
  INDEX `idx_artifact_task` (`task_id`),
  CONSTRAINT `fk_artifact_task`
    FOREIGN KEY (`task_id`)
    REFERENCES `Task` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


-- 8) Дії
CREATE TABLE `Action` (
  `id`     INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `action` VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Role_Action` (
  `id` INT  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `role_id` INT  NOT NULL,
  `action_id` INT  NOT NULL,
  INDEX `idx_ra_role`   (`role_id`),
  INDEX `idx_ra_action` (`action_id`),
  CONSTRAINT `fk_ra_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `Role` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_ra_action`
    FOREIGN KEY (`action_id`)
    REFERENCES `Action` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Event` (
  `id`       INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id`  CHAR(36)NOT NULL,
  `role_id`  INT NOT NULL,
  `action`   VARCHAR(255) NOT NULL,
  `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX `idx_event_user` (`user_id`),
  INDEX `idx_event_role` (`role_id`),
  CONSTRAINT `fk_event_user`
    FOREIGN KEY (`user_id`)
    REFERENCES `User` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_event_role`
    FOREIGN KEY (`role_id`)
    REFERENCES `Role` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


INSERT INTO `Project` (`name`)
VALUES
  ('Project Alpha'),
  ('Project Beta'),
  ('Project Gamma');

INSERT INTO `Team` (`name`, `project_id`)
VALUES
  ('Alpha Team 1', 1),
  ('Alpha Team 2', 1),
  ('Beta Team 1', 2),
  ('Gamma Team 1', 3);


INSERT INTO `User` (`id`, `nickname`, `email`,`password`,`photo`,`team_id`)
VALUES
  (UUID(), 'alice','alice@example.com','pass123','https://example.com/photos/alice.jpg',1),
  (UUID(), 'bob','bob@example.com','qwerty',NULL,1),
  (UUID(), 'carol','carol@example.com','123456','https://example.com/photos/carol.png',2),
  (UUID(), 'david','david@example.com','password',NULL,3),
  (UUID(), 'eve','eve@example.com','evepass','https://example.com/photos/eve.jpeg',4);


INSERT INTO `Role` (`name`, `description`, `project_id`)
VALUES
  ('Developer', 'Writes code and implements features', 1),
  ('Tester', 'Performs QA and test cases', 1),
  ('Manager', 'Manages project and team', 2),
  ('DevOps', 'Maintains infrastructure and CI/CD', 3);



INSERT INTO `Action` (`action`)
VALUES
  ('CREATE_TASK'),
  ('UPDATE_TASK'),
  ('DELETE_TASK'),
  ('UPLOAD_ARTIFACT'),
  ('REVIEW_ARTIFACT');



INSERT INTO `Role_Action` (`role_id`, `action_id`)
VALUES
  -- Developer має право створювати, оновлювати таски, завантажувати артефакти
  (1, 1),  -- Developer → CREATE_TASK
  (1, 2),  -- Developer → UPDATE_TASK
  (1, 4),  -- Developer → UPLOAD_ARTIFACT

  -- Tester має право оновлювати таски, перевіряти артефакти
  (2, 2),  -- Tester → UPDATE_TASK
  (2, 5),  -- Tester → REVIEW_ARTIFACT

  -- Manager має право створювати, оновлювати, видаляти таски
  (3, 1),  -- Manager → CREATE_TASK
  (3, 2),  -- Manager → UPDATE_TASK
  (3, 3),  -- Manager → DELETE_TASK

  -- DevOps має право завантажувати артефакти
  (4, 4);  -- DevOps → UPLOAD_ARTIFACT


INSERT INTO `User_Project` (`user_id`,`project_id`, `role_id`, `team_id`)
SELECT u.`id`, 1 , 1, 1 FROM `User` u WHERE u.`nickname` = 'alice'
UNION ALL
SELECT u.`id`, 1, 2, 1 FROM `User` u WHERE u.`nickname` = 'bob'
UNION ALL
SELECT u.`id`, 1, 2, 2 
  FROM `User` u WHERE u.`nickname` = 'carol'
UNION ALL
SELECT u.`id`, 2, 3, 3 FROM `User` u WHERE u.`nickname` = 'david'
UNION ALL
SELECT u.`id`, 3, 4, 4 FROM `User` u WHERE u.`nickname` = 'eve';



INSERT INTO `Task` (`name`,         `description`,                 `startDate`,           `deadlineDate`,        `team_id`)
VALUES
  ('Design DB Schema', 'Спроектувати структуру БД', '2025-06-01 09:00:00', '2025-06-05 17:00:00', 1),
  ('Implement Auth',   'Реалізувати систему логінації', '2025-06-02 10:00:00', '2025-06-07 12:00:00', 1),
  ('Write Tests',      'Написати юніт‐тести', '2025-06-03 11:00:00', '2025-06-10 15:00:00', 2),
  ('Deploy to Staging','Розгорнути на стейджингу', '2025-06-04 14:00:00', '2025-06-08 18:00:00', 2),
  ('Beta Feature A',   'Розробка фічі для Beta', '2025-06-01 09:30:00', '2025-06-10 16:00:00', 3),
  ('Gamma Setup',      'Налаштувати середовище', '2025-06-05 08:00:00', NULL, 4);



INSERT INTO `Artifact` (`status`,`comment`,`datetime`,`task_id`)
VALUES
  ('CREATED','Перший варіант схеми','2025-06-02 13:00:00', 1),
  ('REVIEWED','Виправки зауважень','2025-06-04 10:30:00', 1),
  ('CREATED','Модуль аутентифікації','2025-06-03 16:45:00', 2),
  ('CREATED','Тести для Auth','2025-06-05 09:20:00', 3),
  ('CREATED','Скрипт деплою на стейджинг','2025-06-06 11:10:00', 4),
  ('CREATED','Feature A implementation','2025-06-07 14:55:00', 5),
  ('CREATED','Initial Gamma environment','2025-06-06 08:15:00', 6);



INSERT INTO `Event` (`user_id`, `role_id`, `action`, `datetime`)
SELECT u.`id`, 1 /* Developer */, 'CREATE_TASK', '2025-06-01 09:05:00' FROM `User` u WHERE u.`nickname` = 'alice'
UNION ALL
SELECT u.`id`, 1, 'UPLOAD_ARTIFACT', '2025-06-02 13:10:00' FROM `User` u WHERE u.`nickname` = 'alice'
UNION ALL
SELECT u.`id`, 2 , 'REVIEW_ARTIFACT', '2025-06-04 11:00:00' FROM `User` u WHERE u.`nickname` = 'bob'
UNION ALL
SELECT u.`id`, 3 , 'UPDATE_TASK', '2025-06-02 12:00:00' FROM `User` u WHERE u.`nickname` = 'david'
UNION ALL
SELECT u.`id`, 4 , 'UPLOAD_ARTIFACT', '2025-06-06 08:20:00' FROM `User` u WHERE u.`nickname` = 'eve';