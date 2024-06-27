-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema nomadnirvana
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema nomadnirvana
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `nomadnirvana` DEFAULT CHARACTER SET utf8 ;
USE `nomadnirvana` ;

-- -----------------------------------------------------
-- Table `nomadnirvana`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nomadnirvana`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(60) NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nomadnirvana`.`vacations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nomadnirvana`.`vacations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `country` VARCHAR(45) NULL,
  `city` VARCHAR(45) NULL,
  `date` DATE NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_vacations_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_vacations_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `nomadnirvana`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nomadnirvana`.`inspiration`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nomadnirvana`.`inspiration` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `link` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vacation_id` INT NOT NULL,
  `vacation_user_id` INT NOT NULL,
  `edited_link` TEXT NULL,
  PRIMARY KEY (`id`, `vacation_id`, `vacation_user_id`),
  INDEX `fk_inspiration_vacations1_idx` (`vacation_id` ASC, `vacation_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_inspiration_vacations1`
    FOREIGN KEY (`vacation_id` , `vacation_user_id`)
    REFERENCES `nomadnirvana`.`vacations` (`id` , `user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nomadnirvana`.`itinerarys`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nomadnirvana`.`itinerarys` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `day` DATE NULL,
  `time` TIME NULL,
  `address` VARCHAR(100) NULL,
  `description` TEXT NULL,
  `notes` TEXT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vacation_id` INT NOT NULL,
  `vacation_user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_itinerarys_vacations1_idx` (`vacation_id` ASC, `vacation_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_itinerarys_vacations1`
    FOREIGN KEY (`vacation_id` , `vacation_user_id`)
    REFERENCES `nomadnirvana`.`vacations` (`id` , `user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `nomadnirvana`.`packing_list_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `nomadnirvana`.`packing_list_items` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category` VARCHAR(45) NULL,
  `name` VARCHAR(45) NULL,
  `quantity` INT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `vacation_id` INT NOT NULL,
  `vacation_user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_packing_list_items_vacations1_idx` (`vacation_id` ASC, `vacation_user_id` ASC) VISIBLE,
  CONSTRAINT `fk_packing_list_items_vacations1`
    FOREIGN KEY (`vacation_id` , `vacation_user_id`)
    REFERENCES `nomadnirvana`.`vacations` (`id` , `user_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
