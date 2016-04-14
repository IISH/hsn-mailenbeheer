-- MySQL dump 10.14  Distrib 5.5.44-MariaDB, for Linux (x86_64)
--
-- Host: node-030    Database: links_general
-- ------------------------------------------------------
-- Server version	5.5.25a

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `HSNRP`
--

DROP TABLE IF EXISTS `HSNRP`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HSNRP` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IDNR` int(11) DEFAULT NULL,
  `ID_origin` int(11) DEFAULT NULL,
  `Project` varchar(255) DEFAULT NULL,
  `Gemnr` int(11) DEFAULT NULL,
  `Valid_day` int(11) DEFAULT NULL,
  `Valid_month` int(11) DEFAULT NULL,
  `Valid_year` int(11) DEFAULT NULL,
  `RP_family` varchar(60) DEFAULT NULL,
  `RP_prefix` varchar(255) DEFAULT NULL,
  `RP_firstname` varchar(255) DEFAULT NULL,
  `RP_B_DAY` int(11) DEFAULT NULL,
  `RP_B_MONTH` int(11) DEFAULT NULL,
  `RP_B_YEAR` int(11) DEFAULT NULL,
  `RP_B_SEX` varchar(1) DEFAULT NULL,
  `RP_B_PLACE` varchar(50) DEFAULT NULL,
  `RP_B_PROV` int(11) DEFAULT NULL,
  `RP_B_COH` int(11) DEFAULT NULL,
  `MO_family` varchar(60) DEFAULT NULL,
  `MO_prefix` varchar(255) DEFAULT NULL,
  `MO_firstname` varchar(255) DEFAULT NULL,
  `FA_family` varchar(60) DEFAULT NULL,
  `FA_prefix` varchar(255) DEFAULT NULL,
  `FA_firstname` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Id` (`Id`),
  KEY `ID_origin` (`ID_origin`),
  KEY `IDNR` (`IDNR`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-03-14 15:11:43
