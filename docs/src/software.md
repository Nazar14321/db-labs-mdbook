# Реалізація інформаційного та програмного забезпечення

## SQL-скрипт для створення на початкового наповнення бази даних

```sql


CREATE TABLE `Project` (
  `id`   INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name` VARCHAR(255) NOT NULL
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `Team` (
  `id`         INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name`       VARCHAR(255) NOT NULL,
  `project_id` INT         NOT NULL,
  INDEX `idx_team_project` (`project_id`),
  CONSTRAINT `fk_team_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `User` (
  `id`       CHAR(36)       NOT NULL PRIMARY KEY
               DEFAULT (UUID()),
  `nickname` VARCHAR(255)   NOT NULL UNIQUE,
  `email`    VARCHAR(255)   NOT NULL UNIQUE,
  `password` TEXT           NOT NULL,
  `photo`    TEXT           NULL,
  `team_id`  INT            NOT NULL,
  INDEX `idx_user_team` (`team_id`),
  CONSTRAINT `fk_user_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Team` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `Role` (
  `id`          INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name`        VARCHAR(255)  NOT NULL,
  `description` TEXT,
  `project_id`  INT           NOT NULL,
  INDEX `idx_role_project` (`project_id`),
  CONSTRAINT `fk_role_project`
    FOREIGN KEY (`project_id`)
    REFERENCES `Project` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;



CREATE TABLE `User_Project` (
  `id`         INT    NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id`    CHAR(36) NOT NULL,
  `project_id` INT      NOT NULL,
  `role_id`    INT      NULL,
  `team_id`    INT      NULL,
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
  `id`           INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `name`         VARCHAR(255) NOT NULL,
  `description`  TEXT,
  `startDate`    TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `deadlineDate` TIMESTAMP   NULL,
  `team_id`      INT         NOT NULL,
  INDEX `idx_task_team` (`team_id`),
  CONSTRAINT `fk_task_team`
    FOREIGN KEY (`team_id`)
    REFERENCES `Team` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Artifact` (
  `id`       INT       NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `status`   VARCHAR(255) NOT NULL,
  `comment`  TEXT,
  `datetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `task_id`  INT       NOT NULL,
  INDEX `idx_artifact_task` (`task_id`),
  CONSTRAINT `fk_artifact_task`
    FOREIGN KEY (`task_id`)
    REFERENCES `Task` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Action` (
  `id`     INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `action` VARCHAR(255) NOT NULL UNIQUE
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;


CREATE TABLE `Role_Action` (
  `id`        INT  NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `role_id`   INT  NOT NULL,
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
  `id`       INT         NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `user_id`  CHAR(36)    NOT NULL,
  `role_id`  INT         NOT NULL,
  `action`   VARCHAR(255) NOT NULL,
  `datetime` TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
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

```



