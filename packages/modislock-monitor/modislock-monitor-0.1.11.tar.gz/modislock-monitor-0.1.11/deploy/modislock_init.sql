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
-- Table `modislock`.`settings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`settings` ;

CREATE TABLE IF NOT EXISTS `modislock`.`settings` (
  `id_settings` INT NOT NULL AUTO_INCREMENT,
  `settings_name` VARCHAR(45) NOT NULL,
  `units` VARCHAR(45) NOT NULL,
  `settings_group_name` ENUM('WEB', 'READERS', 'MONITOR', 'RULES') NOT NULL,
  PRIMARY KEY (`id_settings`),
  UNIQUE INDEX `settings_name_UNIQUE` (`settings_name` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`reader_settings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`reader_settings` ;

CREATE TABLE IF NOT EXISTS `modislock`.`reader_settings` (
  `id_reader` INT NOT NULL,
  `location_name` VARCHAR(20) NOT NULL,
  `alt_name` VARCHAR(20) NULL,
  `location_direction` ENUM('NONE', 'EXIT', 'ENTRY') NOT NULL,
  `settings_id_settings` INT NOT NULL,
  PRIMARY KEY (`id_reader`),
  CONSTRAINT `fk_reader_settings_settings1`
    FOREIGN KEY (`settings_id_settings`)
    REFERENCES `modislock`.`settings` (`id_settings`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0;


-- -----------------------------------------------------
-- Table `modislock`.`events`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`events` ;

CREATE TABLE IF NOT EXISTS `modislock`.`events` (
  `id_event` INT NOT NULL AUTO_INCREMENT,
  `event_time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `event_type` ENUM('USER_CREATED', 'ACCESS', 'DENIED') NOT NULL,
  `user_id` INT NOT NULL,
  `reader_settings_id_reader` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_event`),
  CONSTRAINT `fk_timestamps_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `modislock`.`user` (`id`)
    ON DELETE CASCADE
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_events_reader_settings1`
    FOREIGN KEY (`reader_settings_id_reader`)
    REFERENCES `modislock`.`reader_settings` (`id_reader`)
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
-- Table `modislock`.`locations`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`locations` ;

CREATE TABLE IF NOT EXISTS `modislock`.`locations` (
  `id_locations` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `reader_settings_id_reader` INT NULL,
  PRIMARY KEY (`id_locations`),
  CONSTRAINT `fk_locations_reader_settings1`
    FOREIGN KEY (`reader_settings_id_reader`)
    REFERENCES `modislock`.`reader_settings` (`id_reader`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 0;


-- -----------------------------------------------------
-- Table `modislock`.`sensors`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`sensors` ;

CREATE TABLE IF NOT EXISTS `modislock`.`sensors` (
  `id_sensors` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `units` VARCHAR(45) NOT NULL,
  `locations_id_locations` INT NOT NULL,
  PRIMARY KEY (`id_sensors`),
  UNIQUE INDEX `name_UNIQUE` (`name` ASC),
  CONSTRAINT `fk_sensors_locations1`
    FOREIGN KEY (`locations_id_locations`)
    REFERENCES `modislock`.`locations` (`id_locations`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`readings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`readings` ;

CREATE TABLE IF NOT EXISTS `modislock`.`readings` (
  `id_readings` INT NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `value` VARCHAR(10) NOT NULL,
  `sensors_id_sensors` INT NOT NULL,
  PRIMARY KEY (`id_readings`))
ENGINE = MEMORY;


-- -----------------------------------------------------
-- Table `modislock`.`settings_values`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`settings_values` ;

CREATE TABLE IF NOT EXISTS `modislock`.`settings_values` (
  `id_values` INT NOT NULL AUTO_INCREMENT,
  `value` VARCHAR(45) NOT NULL,
  `settings_id_settings` INT NOT NULL,
  PRIMARY KEY (`id_values`),
  CONSTRAINT `fk_setting_values_settings1`
    FOREIGN KEY (`settings_id_settings`)
    REFERENCES `modislock`.`settings` (`id_settings`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `modislock`.`reader_status`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`reader_status` ;

CREATE TABLE IF NOT EXISTS `modislock`.`reader_status` (
  `id_status` INT NOT NULL AUTO_INCREMENT,
  `status` ENUM('DISCONNECTED', 'CONNECTED', 'ERROR') NOT NULL,
  `updated_on` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `reader_id_reader` INT NOT NULL,
  PRIMARY KEY (`id_status`))
ENGINE = MEMORY;


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
-- Table `modislock`.`static_readings`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `modislock`.`static_readings` ;

CREATE TABLE IF NOT EXISTS `modislock`.`static_readings` (
  `id_static_readings` INT NOT NULL AUTO_INCREMENT,
  `timestamp` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `value` VARCHAR(10) NOT NULL,
  `sensors_id_sensors` INT NOT NULL,
  PRIMARY KEY (`id_static_readings`))
ENGINE = MEMORY;

USE `modislock` ;

-- -----------------------------------------------------
-- procedure add_reading
-- -----------------------------------------------------

USE `modislock`;
DROP procedure IF EXISTS `modislock`.`add_reading`;

DELIMITER $$
USE `modislock`$$
CREATE PROCEDURE `add_reading`
(
    ReadValue VARCHAR(10),
    SensorID INT
)
add_reading:BEGIN

    DECLARE KeepLimit, DeleteLimit, MaxID INT;
    SET DeleteLimit = 250;
    Set KeepLimit = 200;

    INSERT INTO readings (readings.value, readings.sensors_id_sensors)
    VALUES (ReadValue, SensorID);

    SELECT MAX(id_readings) 
    INTO MaxID 
    FROM readings;
    IF MOD(MaxID, DeleteLimit) > 0 THEN
        LEAVE add_reading;
    END IF;

    DROP TABLE IF EXISTS readings_window;
    CREATE TEMPORARY TABLE readings_window
    (id_readings INT NOT NULL PRIMARY KEY) ENGINE=MEMORY;

    SET @sqlstmt= CONCAT('INSERT INTO reading_window ',
        'SELECT id_readings FROM readings ORDER BY id_readings DESC LIMIT ', KeepLimit);
    PREPARE st FROM @sqlstmt; EXECUTE st; DEALLOCATE PREPARE st;

    SELECT *
    FROM readings
    ORDER BY id;
    
    SELECT SLEEP(10);
    DELETE A.* 
    FROM readings A LEFT JOIN readings_window B USING (id_readings);

    SELECT *
    FROM readings
    ORDER BY id_readings;
    DROP TABLE IF EXISTS readings_window;

END $$$$

DELIMITER ;
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


DELIMITER ;
SET SQL_MODE = '';
GRANT USAGE ON *.* TO modisweb;
 DROP USER modisweb;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'modisweb' IDENTIFIED BY 'l3j4lkjlskjd';

GRANT SELECT, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `modislock`.* TO 'modisweb';
GRANT EXECUTE ON `modislock`.* TO 'modisweb';
SET SQL_MODE = '';
GRANT USAGE ON *.* TO modismon;
 DROP USER modismon;
SET SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';
CREATE USER 'modismon' IDENTIFIED BY 'l3j4lkjlskjd';

GRANT SELECT, CREATE, INSERT, TRIGGER, UPDATE, DELETE ON TABLE `modislock`.* TO 'modismon';
GRANT EXECUTE ON `modislock`.* TO 'modismon';
GRANT CREATE ON modislock.* TO 'modismon';

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
-- Data for table `modislock`.`settings`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (1, 'PIN_PLACES', 'integer', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (2, 'OUTPUT_1', 'boolean', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (3, 'OUTPUT_2', 'boolean', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (4, 'RELAY_1_DELAY', 'integer', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (5, 'RELAY_2_DELAY', 'integer', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (6, 'GLOBAL_DAYS', 'integer', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (7, 'GLOBAL_START_TIME', 'time', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (8, 'GLOBAL_END_TIME', 'time', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (9, 'RELAY_1_ENABLED', 'boolean', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (10, 'RELAY_2_ENABLED', 'boolean', 'MONITOR');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (11, 'MONTHS_PRESERVED', 'integer', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (12, 'LAST_BACKUP', 'date', 'WEB');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (13, 'MAIL_SERVER', 'string', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (14, 'MAIL_PORT', 'integer', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (15, 'MAIL_USE_TLS', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (16, 'MAIL_USE_SSL', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (17, 'MAIL_USERNAME', 'string', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (18, 'MAIL_PASSWORD', 'string', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (19, 'MAIL_SENDER', 'string', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (20, 'NOTIFY_ON_DENIED', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (21, 'NOTIFY_ON_AFTER_HOURS', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (22, 'NOTIFY_ON_SYSTEM_ERROR', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (23, 'REGISTRATION', 'boolean', 'RULES');
INSERT INTO `modislock`.`settings` (`id_settings`, `settings_name`, `units`, `settings_group_name`) VALUES (26, 'SERIAL_NUMBER', 'string', 'WEB');

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`reader_settings`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`reader_settings` (`id_reader`, `location_name`, `alt_name`, `location_direction`, `settings_id_settings`) VALUES (0, 'HOST', NULL, 'NONE', 0);
INSERT INTO `modislock`.`reader_settings` (`id_reader`, `location_name`, `alt_name`, `location_direction`, `settings_id_settings`) VALUES (1, 'READER 1', NULL, 'ENTRY', 9);
INSERT INTO `modislock`.`reader_settings` (`id_reader`, `location_name`, `alt_name`, `location_direction`, `settings_id_settings`) VALUES (2, 'READER 2', NULL, 'EXIT', 10);
INSERT INTO `modislock`.`reader_settings` (`id_reader`, `location_name`, `alt_name`, `location_direction`, `settings_id_settings`) VALUES (3, 'READER 3', NULL, 'ENTRY', 9);
INSERT INTO `modislock`.`reader_settings` (`id_reader`, `location_name`, `alt_name`, `location_direction`, `settings_id_settings`) VALUES (4, 'READER 4', NULL, 'EXIT', 10);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`alembic_version`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`alembic_version` (`idalembic_version`) VALUES ('3d8f34e83d23');

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`locations`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (1, 'HOST_CONTROLLER', NULL);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (2, 'READER1', 1);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (3, 'READER2', 2);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (4, 'READER3', 3);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (5, 'READER4', 4);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (6, 'HOST', NULL);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (7, 'DOOR1', NULL);
INSERT INTO `modislock`.`locations` (`id_locations`, `name`, `reader_settings_id_reader`) VALUES (8, 'DOOR2', NULL);

COMMIT;


-- -----------------------------------------------------
-- Data for table `modislock`.`sensors`
-- -----------------------------------------------------
START TRANSACTION;
USE `modislock`;
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_HOST_CPU', 'float', 6);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_CONTROLLER_CPU', 'float', 1);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_READER1', 'float', 2);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_READER2', 'float', 3);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_READER3', 'float', 4);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_READER4', 'float', 5);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'VALIDATION_COUNT_READER1', 'integer', 2);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'VALIDATION_COUNT_READER2', 'integer', 3);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'VALIDATION_COUNT_READER3', 'integer', 4);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'VALIDATION_COUNT_READER4', 'integer', 5);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DENIED_COUNT_READER1', 'integer', 2);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DENIED_COUNT_READER2', 'integer', 3);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DENIED_COUNT_READER3', 'integer', 4);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DENIED_COUNT_READER4', 'integer', 5);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'VALIDATION_COUNT_CONTROLLER', 'integer', 1);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DENIED_COUNT_CONTROLLER', 'integer', 1);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'TEMP_HOST_CASE', 'integer', 6);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DOOR1_STATUS', 'string', 7);
INSERT INTO `modislock`.`sensors` (`id_sensors`, `name`, `units`, `locations_id_locations`) VALUES (DEFAULT, 'DOOR2_STATUS', 'string', 8);

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


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
-- begin attached script 'script'
DELIMITER $$

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
