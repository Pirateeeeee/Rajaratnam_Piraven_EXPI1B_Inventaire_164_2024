-- OM 2024.05.14
-- FICHIER MYSQL POUR FAIRE FONCTIONNER LES EXEMPLES
-- DE REQUETES MYSQL
-- Database: Rajaratnam_Piraven_EXPI1B_Inventaire_164_2024

-- Destruction de la BD si elle existe.
-- Pour être certain d'avoir la dernière version des données
DROP DATABASE IF EXISTS Rajaratnam_Piraven_EXPI1B_Inventaire_164_2024;
-- Création d'une nouvelle base de données
CREATE DATABASE IF NOT EXISTS Rajaratnam_Piraven_EXPI1B_Inventaire_164_2024;
-- Utilisation de cette base de données
USE Rajaratnam_Piraven_EXPI1B_Inventaire_164_2024;


-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_computer
DROP TABLE IF EXISTS `t_computer`;
CREATE TABLE IF NOT EXISTS `t_computer` (
  `idComputer` int NOT NULL AUTO_INCREMENT,
  `comHostname` varchar(255) DEFAULT NULL,
  `comIPAddress` varchar(15) DEFAULT NULL,
  `comOS` varchar(255) DEFAULT NULL,
  `comProcessor` varchar(255) DEFAULT NULL,
  `comRAM` int DEFAULT NULL,
  `idObject` int DEFAULT NULL,
  PRIMARY KEY (`idComputer`),
  KEY `idObject` (`idObject`),
  CONSTRAINT `t_computer_ibfk_1` FOREIGN KEY (`idObject`) REFERENCES `t_object` (`idObject`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_computer : ~5 rows (environ)
DELETE FROM `t_computer`;
INSERT INTO `t_computer` (`idComputer`, `comHostname`, `comIPAddress`, `comOS`, `comProcessor`, `comRAM`, `idObject`) VALUES
	(1, 'Computer1', '192.168.1.101', 'Windows 10', 'Intel Core i5', 16, 1),
	(2, 'Computer2', '192.168.1.102', 'Windows 11', 'AMD Ryzen 7', 32, 2),
	(3, 'Computer3', '192.168.1.103', 'Ubuntu 20.04', 'Intel Core i7', 8, 3),
	(4, 'Computer4', '192.168.1.104', 'macOS Catalina', 'Apple M1', 16, 4),
	(5, 'Computer5', '192.168.1.105', 'Windows 10', 'Intel Core i9', 64, 5);

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_note
DROP TABLE IF EXISTS `t_note`;
CREATE TABLE IF NOT EXISTS `t_note` (
  `idNote` int NOT NULL,
  `notContent` text,
  `notCreationDate` date DEFAULT NULL,
  `notPriority` int DEFAULT NULL,
  `notStatus` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idNote`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_note : ~5 rows (environ)
DELETE FROM `t_note`;
INSERT INTO `t_note` (`idNote`, `notContent`, `notCreationDate`, `notPriority`, `notStatus`) VALUES
	(1, 'Note content 1', '2024-03-28', 1, 'Pending'),
	(2, 'Note content 2', '2024-03-27', 2, 'Completed'),
	(3, 'Note content 3', '2024-03-26', 3, 'Pending'),
	(4, 'Note content 4', '2024-03-25', 1, 'Completed'),
	(5, 'Note content 5', '2024-03-24', 2, 'Pending');

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_object
DROP TABLE IF EXISTS `t_object`;
CREATE TABLE IF NOT EXISTS `t_object` (
  `idObject` int NOT NULL,
  `objInventoryNumber` varchar(255) DEFAULT NULL,
  `objSerialNumber` varchar(255) DEFAULT NULL,
  `objDateInService` date DEFAULT NULL,
  `objModel` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idObject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_object : ~5 rows (environ)
DELETE FROM `t_object`;
INSERT INTO `t_object` (`idObject`, `objInventoryNumber`, `objSerialNumber`, `objDateInService`, `objModel`) VALUES
	(1, 'INV123', 'SER456', '2020-01-01', 'Model A'),
	(2, 'INV234', 'SER567', '2019-12-31', 'Model B'),
	(3, 'INV345', 'SER678', '2020-02-01', 'Model C'),
	(4, 'INV456', 'SER789', '2020-03-01', 'Model D'),
	(5, 'INV567', 'SER890', '2020-04-01', 'Model E');

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_office
DROP TABLE IF EXISTS `t_office`;
CREATE TABLE IF NOT EXISTS `t_office` (
  `idOffice` int NOT NULL,
  `offName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idOffice`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_office : ~5 rows (environ)
DELETE FROM `t_office`;
INSERT INTO `t_office` (`idOffice`, `offName`) VALUES
	(1, 'Office A'),
	(2, 'Office B'),
	(3, 'Office C'),
	(4, 'Office D'),
	(5, 'Office E');

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_screen
DROP TABLE IF EXISTS `t_screen`;
CREATE TABLE IF NOT EXISTS `t_screen` (
  `idScreen` int NOT NULL,
  `scrInch` float DEFAULT NULL,
  `idObject` int DEFAULT NULL,
  PRIMARY KEY (`idScreen`),
  KEY `idObject` (`idObject`),
  CONSTRAINT `t_screen_ibfk_1` FOREIGN KEY (`idObject`) REFERENCES `t_object` (`idObject`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_screen : ~5 rows (environ)
DELETE FROM `t_screen`;
INSERT INTO `t_screen` (`idScreen`, `scrInch`, `idObject`) VALUES
	(1, 24, 1),
	(2, 27, 2),
	(3, 32, 3),
	(4, 22, 4),
	(5, 29, 5);

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_state
DROP TABLE IF EXISTS `t_state`;
CREATE TABLE IF NOT EXISTS `t_state` (
  `idState` int NOT NULL,
  `staName` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`idState`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_state : ~5 rows (environ)
DELETE FROM `t_state`;
INSERT INTO `t_state` (`idState`, `staName`) VALUES
	(1, 'State 1'),
	(2, 'State 2'),
	(3, 'State 3'),
	(4, 'State 4'),
	(5, 'State 5');

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_unit
DROP TABLE IF EXISTS `t_unit`;
CREATE TABLE IF NOT EXISTS `t_unit` (
  `idUnit` int NOT NULL,
  `uniName` varchar(255) DEFAULT NULL,
  `uniDescription` text,
  `uniResponsible` int DEFAULT NULL,
  PRIMARY KEY (`idUnit`),
  KEY `uniResponsible` (`uniResponsible`),
  CONSTRAINT `t_unit_ibfk_1` FOREIGN KEY (`uniResponsible`) REFERENCES `t_user` (`idUser`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_unit : ~5 rows (environ)
DELETE FROM `t_unit`;
INSERT INTO `t_unit` (`idUnit`, `uniName`, `uniDescription`, `uniResponsible`) VALUES
	(1, 'Unit 1', 'Description for Unit 1', 1),
	(2, 'Unit 2', 'Description for Unit 2', 2),
	(3, 'Unit 3', 'Description for Unit 3', 3),
	(4, 'Unit 4', 'Description for Unit 4', 4),
	(5, 'Unit 5', 'Description for Unit 5', 5);

-- Listage de la structure de table piraven_rajaratnam_mpdoficiel. t_user
DROP TABLE IF EXISTS `t_user`;
CREATE TABLE IF NOT EXISTS `t_user` (
  `idUser` int NOT NULL,
  `usrLastName` varchar(255) DEFAULT NULL,
  `usrFirstName` varchar(255) DEFAULT NULL,
  `usrEmailAddress` varchar(255) DEFAULT NULL,
  `usrPhoneNumber` varchar(15) DEFAULT NULL,
  `usrOccupiedPosition` varchar(255) DEFAULT NULL,
  `idOffice` int DEFAULT NULL,
  PRIMARY KEY (`idUser`),
  KEY `idOffice` (`idOffice`),
  CONSTRAINT `t_user_ibfk_1` FOREIGN KEY (`idOffice`) REFERENCES `t_office` (`idOffice`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Listage des données de la table piraven_rajaratnam_mpdoficiel.t_user : ~5 rows (environ)
DELETE FROM `t_user`;
INSERT INTO `t_user` (`idUser`, `usrLastName`, `usrFirstName`, `usrEmailAddress`, `usrPhoneNumber`, `usrOccupiedPosition`, `idOffice`) VALUES
	(1, 'Doe', 'John', 'john.doe@example.com', '123456789', 'Manager', 1),
	(2, 'Smith', 'Alice', 'alice.smith@example.com', '987654321', 'Developer', 2),
	(3, 'Johnson', 'Bob', 'bob.johnson@example.com', '456789123', 'Designer', 3),
	(4, 'Brown', 'Emma', 'emma.brown@example.com', '321654987', 'Analyst', 4),
	(5, 'Wilson', 'Mike', 'mike.wilson@example.com', '789123456', 'Engineer', 5);

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
