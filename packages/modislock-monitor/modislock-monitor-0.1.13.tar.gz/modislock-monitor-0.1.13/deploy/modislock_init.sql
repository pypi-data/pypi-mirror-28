-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema modislock
-- -----------------------------------------------------
-- Modis GmbH Lock
DROP SCHEMA IF EXISTS `modislock` ;

-- -----------------------------------------------------
-- Schema modislock
--
-- Modis GmbH Lock
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `modislock` DEFAULT CHARACTER SET utf8 ;
USE `modislock` ;

-- -----------------------------------------------------
-- Table `modislock`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`user` ;

CREATE TABLE IF NOT EXISTS `modislock`.`user` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `email` VARCHAR(50) NOT NULL,
  `password` VARCHAR(164) NULL,
  `is_admin` TINYINT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC))
ENGINE = InnoDB
AUTO_INCREMENT = 1;


-- -----------------------------------------------------
-- Table `modislock`.`pin_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`pin_key` ;

CREATE TABLE IF NOT EXISTS `modislock`.`pin_key` (
  `key` INT UNSIGNED NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1 COMMENT 'Main user entry and management table.',
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `fk_pincode_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`rfid_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`rfid_key` ;

CREATE TABLE IF NOT EXISTS `modislock`.`rfid_key` (
  `key` VARCHAR(128) NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `fk_rfid_code_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`host`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`host` ;

CREATE TABLE IF NOT EXISTS `modislock`.`host` (
  `idhost` INT NOT NULL,
  `serial_number` VARCHAR(45) NOT NULL,
  `host_name` VARCHAR(45) NOT NULL,
  `installation_date` DATE NOT NULL,
  `registered` TINYINT(1) NOT NULL,
  PRIMARY KEY (`idhost`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`controller`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`controller` ;

CREATE TABLE IF NOT EXISTS `modislock`.`controller` (
  `idcontroller` INT NOT NULL AUTO_INCREMENT,
  `uuid` VARCHAR(45) NULL,
  `software_version` VARCHAR(10) NULL,
  `name` VARCHAR(45) NOT NULL,
  `port` VARCHAR(45) NOT NULL,
  `baud_rate` INT NOT NULL DEFAULT 115200,
  `data_bits` TINYINT NOT NULL DEFAULT 8,
  `stop_bits` TINYINT NOT NULL DEFAULT 1,
  `host_idhost` INT NOT NULL,
  PRIMARY KEY (`idcontroller`),
  CONSTRAINT `fk_controller_host1`
    FOREIGN KEY (`host_idhost`)
    REFERENCES `modislock`.`host` (`idhost`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`door`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`door` ;

CREATE TABLE IF NOT EXISTS `modislock`.`door` (
  `iddoor` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `pin_num` INT NOT NULL DEFAULT 0,
  `alt_name` VARCHAR(45) NULL,
  `controller_idcontroller` INT NOT NULL,
  PRIMARY KEY (`iddoor`),
  CONSTRAINT `fk_door_controller1`
    FOREIGN KEY (`controller_idcontroller`)
    REFERENCES `modislock`.`controller` (`idcontroller`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`reader`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`reader` ;

CREATE TABLE IF NOT EXISTS `modislock`.`reader` (
  `idreader` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `status` ENUM('ACTIVE', 'INACTIVE') NOT NULL,
  `pin_num` INT NOT NULL DEFAULT 0,
  `alt_name` VARCHAR(45) NULL,
  `location` VARCHAR(45) NULL,
  `location_direction` ENUM('ENTRY', 'EXIT') NULL,
  `uuid` VARCHAR(45) NULL,
  `software_version` VARCHAR(10) NULL,
  `validation_count` INT NULL,
  `denied_count` INT NULL,
  `controller_address` INT NOT NULL,
  `controller_idcontroller` INT NOT NULL,
  `door_iddoor` INT NOT NULL,
  PRIMARY KEY (`idreader`),
  CONSTRAINT `fk_reader_controller1`
    FOREIGN KEY (`controller_idcontroller`)
    REFERENCES `modislock`.`controller` (`idcontroller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_reader_door1`
    FOREIGN KEY (`door_iddoor`)
    REFERENCES `modislock`.`door` (`iddoor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`events` ;

CREATE TABLE IF NOT EXISTS `modislock`.`events` (
  `id_event` INT NOT NULL AUTO_INCREMENT,
  `event_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `event_type` ENUM('USER_CREATED', 'ACCESS', 'DENIED') NOT NULL,
  `user_id` INT NOT NULL,
  `reader_idreader` INT NULL,
  PRIMARY KEY (`id_event`),
  CONSTRAINT `fk_timestamps_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_events_reader1`
    FOREIGN KEY (`reader_idreader`)
    REFERENCES `modislock`.`reader` (`idreader`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`otp_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`otp_key` ;

CREATE TABLE IF NOT EXISTS `modislock`.`otp_key` (
  `key` VARCHAR(16) NOT NULL COMMENT 'The id of the key is a unique number that is found on the serial number of the key. This is also known as the public name of the key.\n',
  `private_identity` VARCHAR(16) NOT NULL,
  `aeskey` VARCHAR(32) NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `counter` INT(11) NOT NULL DEFAULT 1,
  `time` INT NOT NULL,
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `remote_server` TINYINT(1) NULL DEFAULT 0,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `aeskey_UNIQUE` (`aeskey` ASC),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `fk_otp_key_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`u2f_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`u2f_key` ;

CREATE TABLE IF NOT EXISTS `modislock`.`u2f_key` (
  `key` INT UNSIGNED NOT NULL,
  `handle` VARCHAR(128) NOT NULL,
  `public_key` VARCHAR(128) NOT NULL,
  `counter` INT NOT NULL,
  `transports` ENUM('BT', 'BLE', 'NFC', 'USB') NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `handle_UNIQUE` (`handle` ASC),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `fk_u2f_key_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`alembic_version`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`alembic_version` ;

CREATE TABLE IF NOT EXISTS `modislock`.`alembic_version` (
  `idalembic_version` VARCHAR(32) NOT NULL)
ENGINE = MyISAM;


-- -----------------------------------------------------
-- Table `modislock`.`settings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`settings` ;

CREATE TABLE IF NOT EXISTS `modislock`.`settings` (
  `id_settings` INT NOT NULL AUTO_INCREMENT,
  `settings_name` VARCHAR(45) NOT NULL,
  `units` VARCHAR(45) NOT NULL,
  `settings_group_name` ENUM('WEB', 'READERS', 'MONITOR', 'RULES') NOT NULL,
  `host_idhost` INT NOT NULL,
  PRIMARY KEY (`id_settings`),
  UNIQUE INDEX `settings_name_UNIQUE` (`settings_name` ASC),
  CONSTRAINT `fk_settings_host1`
    FOREIGN KEY (`host_idhost`)
    REFERENCES `modislock`.`host` (`idhost`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`settings_values`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`settings_values` ;

CREATE TABLE IF NOT EXISTS `modislock`.`settings_values` (
  `id_values` INT NOT NULL AUTO_INCREMENT,
  `value` VARCHAR(45) NOT NULL,
  `settings_id_settings` INT NOT NULL,
  PRIMARY KEY (`id_values`, `settings_id_settings`),
  CONSTRAINT `fk_setting_values_settings1`
    FOREIGN KEY (`settings_id_settings`)
    REFERENCES `modislock`.`settings` (`id_settings`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`rules`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`rules` ;

CREATE TABLE IF NOT EXISTS `modislock`.`rules` (
  `id_rules` INT NOT NULL AUTO_INCREMENT,
  `days` TINYINT UNSIGNED NULL,
  `start_time` TIME NULL,
  `end_time` TIME NULL,
  `readers` TINYINT UNSIGNED NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id_rules`),
  CONSTRAINT `fk_rules_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`otp_cloud_service`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`otp_cloud_service` ;

CREATE TABLE IF NOT EXISTS `modislock`.`otp_cloud_service` (
  `cloud_id` INT NOT NULL AUTO_INCREMENT,
  `yubico_user_name` VARCHAR(45) NULL,
  `yubico_secret_key` VARCHAR(45) NULL,
  `otp_key_key` VARCHAR(16) NOT NULL,
  PRIMARY KEY (`cloud_id`, `otp_key_key`),
  CONSTRAINT `fk_otp_cloud_service_otp_key1`
    FOREIGN KEY (`otp_key_key`)
    REFERENCES `modislock`.`otp_key` (`key`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`totp_key`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`totp_key` ;

CREATE TABLE IF NOT EXISTS `modislock`.`totp_key` (
  `key` INT UNSIGNED NOT NULL,
  `secret` VARCHAR(16) NOT NULL,
  `period` TINYINT NOT NULL DEFAULT 30,
  `enabled` TINYINT(1) NOT NULL DEFAULT 1,
  `created_on` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`key`),
  UNIQUE INDEX `user_id_UNIQUE` (`user_id` ASC),
  CONSTRAINT `fk_totp_key_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`app_api`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`app_api` ;

CREATE TABLE IF NOT EXISTS `modislock`.`app_api` (
  `app_api_id` VARCHAR(25) NOT NULL,
  `app_secret` VARCHAR(128) NOT NULL,
  PRIMARY KEY (`app_api_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`app_api_access`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`app_api_access` ;

CREATE TABLE IF NOT EXISTS `modislock`.`app_api_access` (
  `token` VARCHAR(128) NOT NULL,
  `expires` TIMESTAMP NOT NULL,
  `app_api_app_api_id` VARCHAR(25) NOT NULL,
  PRIMARY KEY (`token`),
  CONSTRAINT `fk_app_api_access_app_api1`
    FOREIGN KEY (`app_api_app_api_id`)
    REFERENCES `modislock`.`app_api` (`app_api_id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`relay`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`relay` ;

CREATE TABLE IF NOT EXISTS `modislock`.`relay` (
  `idrelay` INT NOT NULL AUTO_INCREMENT,
  `type` ENUM('SOLID_STATE', 'MECHANICAL') NOT NULL,
  `enabled` TINYINT(1) NOT NULL DEFAULT 0,
  `position` TINYINT NOT NULL,
  `delay` INT NOT NULL DEFAULT 1500,
  `controller_idcontroller` INT NOT NULL,
  `door_iddoor` INT NULL,
  PRIMARY KEY (`idrelay`),
  CONSTRAINT `fk_relay_controller1`
    FOREIGN KEY (`controller_idcontroller`)
    REFERENCES `modislock`.`controller` (`idcontroller`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_relay_door1`
    FOREIGN KEY (`door_iddoor`)
    REFERENCES `modislock`.`door` (`iddoor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`reader_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`reader_status` ;

CREATE TABLE IF NOT EXISTS `modislock`.`reader_status` (
  `id_status` INT NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `temp` INT NOT NULL,
  `validation_count` INT NOT NULL,
  `denied_count` INT NOT NULL,
  `reader_idreader` INT NOT NULL,
  PRIMARY KEY (`id_status`))
ENGINE = MEMORY;


-- -----------------------------------------------------
-- Table `modislock`.`door_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`door_status` ;

CREATE TABLE IF NOT EXISTS `modislock`.`door_status` (
  `iddoor_status` INT NOT NULL AUTO_INCREMENT,
  `status` ENUM('ACTIVE', 'INACTIVE') NOT NULL DEFAULT 'INACTIVE',
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `door_iddoor` INT NOT NULL,
  PRIMARY KEY (`iddoor_status`))
ENGINE = MEMORY;


-- -----------------------------------------------------
-- Table `modislock`.`controller_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`controller_status` ;

CREATE TABLE IF NOT EXISTS `modislock`.`controller_status` (
  `idcontroller_status` INT NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `temp` INT NOT NULL DEFAULT 0,
  `validation_count` INT NOT NULL DEFAULT 0,
  `denied_count` INT NOT NULL DEFAULT 0,
  `controller_idcontroller` INT NOT NULL,
  PRIMARY KEY (`idcontroller_status`))
ENGINE = MEMORY;


-- -----------------------------------------------------
-- Table `modislock`.`host_sensors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`host_sensors` ;

CREATE TABLE IF NOT EXISTS `modislock`.`host_sensors` (
  `idhost_sensors` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `location` VARCHAR(45) NOT NULL,
  `host_idhost` INT NOT NULL,
  PRIMARY KEY (`idhost_sensors`),
  CONSTRAINT `fk_host_sensors_host1`
    FOREIGN KEY (`host_idhost`)
    REFERENCES `modislock`.`host` (`idhost`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`host_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`host_status` ;

CREATE TABLE IF NOT EXISTS `modislock`.`host_status` (
  `idhost_status` INT NOT NULL AUTO_INCREMENT,
  `reading` INT NOT NULL DEFAULT 0,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `host_sensors_idhost_sensors` INT NOT NULL,
  PRIMARY KEY (`idhost_status`))
ENGINE = MEMORY;

USE `modislock` ;

-- -----------------------------------------------------
-- Placeholder table for view `modislock`.`recent_24h_events`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `modislock`.`recent_24h_events` (`id_event` INT, `id` INT, `first_name` INT, `last_name` INT, `event_type` INT, `event_time` INT, `location` INT, `location_direction` INT);

-- -----------------------------------------------------
-- Placeholder table for view `modislock`.`recent_24h_denied_count`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `modislock`.`recent_24h_denied_count` (`denied_count` INT);

-- -----------------------------------------------------
-- Placeholder table for view `modislock`.`recent_24h_approved_count`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `modislock`.`recent_24h_approved_count` (`approved_count` INT);

-- -----------------------------------------------------
-- View `modislock`.`recent_24h_events`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `modislock`.`recent_24h_events` ;
DROP TABLE IF EXISTS `modislock`.`recent_24h_events`;
USE `modislock`;
CREATE  OR REPLACE VIEW `recent_24h_events` AS

SELECT events.id_event, user.id, user.first_name, user.last_name, events.event_type, events.event_time, reader.location, reader.location_direction
FROM user JOIN events ON user.id = events.user_id
JOIN reader ON events.reader_idreader = reader.idreader
WHERE events.event_time > DATE_SUB(NOW(), INTERVAL 24 HOUR)
ORDER BY events.event_time DESC;

-- -----------------------------------------------------
-- View `modislock`.`recent_24h_denied_count`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `modislock`.`recent_24h_denied_count` ;
DROP TABLE IF EXISTS `modislock`.`recent_24h_denied_count`;
USE `modislock`;
CREATE  OR REPLACE VIEW `recent_24h_denied_count` AS
SELECT COUNT(*) as denied_count
FROM events
WHERE events.event_type = "DENIED" && events.event_time > DATE_SUB(NOW(), INTERVAL 24 HOUR);

-- -----------------------------------------------------
-- View `modislock`.`recent_24h_approved_count`
-- -----------------------------------------------------
DROP VIEW IF EXISTS `modislock`.`recent_24h_approved_count` ;
DROP TABLE IF EXISTS `modislock`.`recent_24h_approved_count`;
USE `modislock`;
CREATE  OR REPLACE VIEW `recent_24h_approved_count` AS
SELECT COUNT(*) as approved_count
FROM events
WHERE events.event_type = "ACCESS" && events.event_time > DATE_SUB(NOW(), INTERVAL 24 HOUR);
USE `modislock`;

DELIMITER $$

USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`user_AFTER_INSERT` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`user_AFTER_INSERT` AFTER INSERT ON `user` FOR EACH ROW
BEGIN
INSERT INTO events (event_type, user_id) VALUES ('USER_CREATED', NEW.id);
END$$


USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`rfid_key_BEFORE_INSERT` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`rfid_key_BEFORE_INSERT` BEFORE INSERT ON `rfid_key` FOR EACH ROW
BEGIN
SET NEW.key = LOWER(NEW.key);
END$$


USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`rfid_key_BEFORE_UPDATE` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`rfid_key_BEFORE_UPDATE` BEFORE UPDATE ON `rfid_key` FOR EACH ROW
BEGIN
SET NEW.key = LOWER(NEW.key);
END$$


USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`reader_status_BEFORE_INSERT` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`reader_status_BEFORE_INSERT` BEFORE INSERT ON `reader_status` FOR EACH ROW
BEGIN
  SET @rowcount = (SELECT COUNT(*) FROM reader_status); 
    IF @rowcount > 1000 THEN
        DELETE FROM reader_status ORDER BY id_status LIMIT 1; 
    END IF;
END$$


USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`controller_status_BEFORE_INSERT` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`controller_status_BEFORE_INSERT` BEFORE INSERT ON `controller_status` FOR EACH ROW
BEGIN
    SET @rowcount = (SELECT COUNT(*) FROM controller_status); 
    IF @rowcount > 1000 THEN
        DELETE FROM controller_status ORDER BY idcontroller_status LIMIT 1; 
    END IF;
END$$


USE `modislock`$$
DROP TRIGGER IF EXISTS `modislock`.`host_status_BEFORE_INSERT` $$
USE `modislock`$$
CREATE DEFINER = CURRENT_USER TRIGGER `modislock`.`host_status_BEFORE_INSERT` BEFORE INSERT ON `host_status` FOR EACH ROW
BEGIN
  SET @rowcount = (SELECT COUNT(*) FROM host_status); 
    IF @rowcount > 1000 THEN
        DELETE FROM host_status ORDER BY idhost_status LIMIT 1; 
    END IF;
END$$


DELIMITER ;
SET SQL_MODE = '';
GRANT USAGE ON *.* TO modisweb;
 DROP USER modisweb;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'modisweb' IDENTIFIED BY 'l3j4lkjlskjd';

GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `modislock`.* TO 'modisweb';
SET SQL_MODE = '';
GRANT USAGE ON *.* TO modismon;
 DROP USER modismon;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'modismon' IDENTIFIED BY 'l3j4lkjlskjd';

GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `modislock`.* TO 'modismon';

-- -----------------------------------------------------
-- Data for table `modislock`.`user`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`user` (`id`, `first_name`, `last_name`, `email`, `password`, `is_admin`) VALUES (1, 'Modis', 'Admin', 'admin@modislab.com', 'pbkdf2:sha256:50000$zfgRyaz9$97aeec274328d9a27f73e6f9b6bbf549911c53c1e5b42b93134f514bc28a1c46', 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`pin_key`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`pin_key` (`key`, `enabled`, `created_on`, `user_id`) VALUES (4444, 1, DEFAULT, 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`host`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`host` (`idhost`, `serial_number`, `host_name`, `installation_date`, `registered`) VALUES (1, '0', 'modislock', '2017-01-01', false);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`controller`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`controller` (`idcontroller`, `uuid`, `software_version`, `name`, `port`, `baud_rate`, `data_bits`, `stop_bits`, `host_idhost`) VALUES (DEFAULT, NULL, NULL, 'ONBOARD', '/dev/ttyAMA0', 115200, 8, 1, 1);
INSERT INTO `modislock`.`controller` (`idcontroller`, `uuid`, `software_version`, `name`, `port`, `baud_rate`, `data_bits`, `stop_bits`, `host_idhost`) VALUES (DEFAULT, NULL, NULL, 'EXPANSION', '/dev/ttyAMA1', 115200, 8, 1, 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`door`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR1', 20, '', 1);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR2', 21, '', 1);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR3', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR4', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR5', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR6', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR7', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR8', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR9', 0, '', 2);
INSERT INTO `modislock`.`door` (`iddoor`, `name`, `pin_num`, `alt_name`, `controller_idcontroller`) VALUES (DEFAULT, 'DOOR10', 0, '', 2);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`reader`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (1, 'READER1', 1, 'INACTIVE', 17, '', NULL, NULL, '0', NULL, 0, 0, 1, 1, 1);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (2, 'READER2', 1, 'INACTIVE', 18, '', NULL, NULL, '0', NULL, 0, 0, 2, 1, 1);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (3, 'READER3', 1, 'INACTIVE', 27, '', NULL, NULL, '0', NULL, 0, 0, 3, 1, 2);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (4, 'READER4', 1, 'INACTIVE', 22, '', NULL, NULL, '0', NULL, 0, 0, 4, 1, 2);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (5, 'READER5', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 1, 2, 3);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (6, 'READER6', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 2, 2, 3);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (7, 'READER7', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 3, 2, 4);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (8, 'READER8', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 4, 2, 4);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (9, 'READER9', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 5, 2, 5);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (10, 'READER10', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 6, 2, 5);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (11, 'READER11', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 7, 2, 6);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (12, 'READER12', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 8, 2, 6);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (13, 'READER13', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 9, 2, 7);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (14, 'READER14', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 10, 2, 7);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (15, 'READER15', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 11, 2, 8);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (16, 'READER16', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 12, 2, 8);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (17, 'READER17', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 13, 2, 9);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (18, 'READER18', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 14, 2, 9);
INSERT INTO `modislock`.`reader` (`idreader`, `name`, `enabled`, `status`, `pin_num`, `alt_name`, `location`, `location_direction`, `uuid`, `software_version`, `validation_count`, `denied_count`, `controller_address`, `controller_idcontroller`, `door_iddoor`) VALUES (19, 'READER19', 0, 'INACTIVE', 0, '', NULL, NULL, '0', NULL, 0, 0, 15, 2, 10);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`alembic_version`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`alembic_version` (`idalembic_version`) VALUES ('3d8f34e83d23');

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`settings`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (1, 'PIN_PLACES', 'integer', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (6, 'GLOBAL_DAYS', 'integer', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (7, 'GLOBAL_START_TIME', 'time', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (8, 'GLOBAL_END_TIME', 'time', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (11, 'MONTHS_PRESERVED', 'integer', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (12, 'LAST_BACKUP', 'date', 'WEB', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (13, 'MAIL_SERVER', 'string', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (14, 'MAIL_PORT', 'integer', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (15, 'MAIL_USE_TLS', 'boolean', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (16, 'MAIL_USE_SSL', 'boolean', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (17, 'MAIL_USERNAME', 'string', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (18, 'MAIL_PASSWORD', 'string', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (19, 'MAIL_SENDER', 'string', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (20, 'NOTIFY_ON_DENIED', 'boolean', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (21, 'NOTIFY_ON_AFTER_HOURS', 'boolean', 'RULES', 1);
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`, `host_idhost`) VALUES (22, 'NOTIFY_ON_SYSTEM_ERROR', 'boolean', 'RULES', 1);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`settings_values`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (1, '4', 1);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (2, 'DISABLED', 2);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (3, 'DISABLED', 3);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (4, '1500', 4);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (5, '2000', 5);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (6, 'ENABLED', 9);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (7, 'ENABLED', 10);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (8, '1', 11);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (9, '2017-06-15 11:00:00', 12);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (10, 'smtp.gmail.com', 13);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (11, '465', 14);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (12, 'DISABLED', 15);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (13, 'ENABLED', 16);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (14, 'myusername', 17);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (15, 'mypassword', 18);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (16, 'modis_lock@myemail.net', 19);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (17, 'DISABLED', 20);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (18, 'DISABLED', 21);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (19, 'DISABLED', 22);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (20, 'ENABLED', 23);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (21, '0', 6);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (22, '09:00:00', 7);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (23, '18:00:00', 8);
INSERT INTO `modislock`.`settings_values` (`id_values`, `value`, `settings_id_settings`) VALUES (26, '0', 26);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`relay`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (1, 'MECHANICAL', 1, 1, 1500, 1, 1);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (2, 'MECHANICAL', 1, 2, 2500, 1, 2);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (3, 'SOLID_STATE', 1, 1, 1500, 1, 1);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (4, 'SOLID_STATE', 1, 2, 2500, 1, 2);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (5, 'MECHANICAL', 0, 1, 1000, 2, 3);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (6, 'MECHANICAL', 0, 2, 1000, 2, 4);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (7, 'MECHANICAL', 0, 3, 1000, 2, 5);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (8, 'MECHANICAL', 0, 4, 1000, 2, 6);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (9, 'MECHANICAL', 0, 5, 1000, 2, 7);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (10, 'MECHANICAL', 0, 6, 1000, 2, 8);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (11, 'MECHANICAL', 0, 7, 1000, 2, 9);
INSERT INTO `modislock`.`relay` (`idrelay`, `type`, `enabled`, `position`, `delay`, `controller_idcontroller`, `door_iddoor`) VALUES (12, 'MECHANICAL', 0, 8, 1000, 2, 10);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`host_sensors`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`host_sensors` (`idhost_sensors`, `name`, `location`, `host_idhost`) VALUES (1, 'Internal CPU', 'CPU', 1);
INSERT INTO `modislock`.`host_sensors` (`idhost_sensors`, `name`, `location`, `host_idhost`) VALUES (2, 'Case RTC', 'RTC', 1);

COMMIT;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- begin attached script 'script'
DELIMITER $$

DROP EVENT IF EXISTS `purge_old_records` $$

CREATE EVENT IF NOT EXISTS `purge_old_records` 
	ON SCHEDULE EVERY 1 DAY STARTS '2017-01-01 01:00:00' 
	DO BEGIN
        SET SQL_SAFE_UPDATES=0;

        SET @months := (SELECT value 
        FROM settings
        JOIN settings_values ON settings.id_settings = settings_values.settings_id_settings
        WHERE settings_name = 'MONTHS_PRESERVED');

        DELETE FROM events
        WHERE events.event_time < timestamp(DATE_SUB(NOW(), INTERVAL @months MONTH));

        SET SQL_SAFE_UPDATES=1;
	END $$

DELIMITER ;
-- end attached script 'script'
