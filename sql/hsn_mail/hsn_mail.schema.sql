-- MySQL dump 10.14  Distrib 5.5.44-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: hsn_mail
-- ------------------------------------------------------
-- Server version	5.5.44-MariaDB

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
-- Table structure for table `Archief_gemeente`
--

DROP TABLE IF EXISTS `Archief_gemeente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Archief_gemeente` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Gemnr` int(11) DEFAULT NULL,
  `Provnr` int(11) DEFAULT NULL,
  `Gemnaam` varchar(50) DEFAULT NULL,
  `Archiefnaam` varchar(254) DEFAULT NULL,
  `Gemeente_met_archief` varchar(255) DEFAULT NULL,
  `Bezoekadres` varchar(254) DEFAULT NULL,
  `Postadres` varchar(254) DEFAULT NULL,
  `Postcode` varchar(254) DEFAULT NULL,
  `Plaats` varchar(254) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `HSN_BEHEER`
--

DROP TABLE IF EXISTS `HSN_BEHEER`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HSN_BEHEER` (
  `Idnr` int(11) NOT NULL AUTO_INCREMENT,
  `Ovldag` int(11) DEFAULT '0',
  `Ovlmnd` int(11) DEFAULT '0',
  `Ovljaar` int(11) DEFAULT '0',
  `Fase_A` int(11) DEFAULT '0',
  `Fase_B` int(11) DEFAULT '0',
  `Fase_C_D` int(11) DEFAULT '0',
  `OvlPlaats` varchar(50) DEFAULT NULL,
  `Mail_type` varchar(1) DEFAULT NULL,
  `Invoerstatus` varchar(1) DEFAULT NULL,
  `Randomgetal` int(11) DEFAULT '0',
  `Releasestatus` varchar(1) DEFAULT NULL,
  PRIMARY KEY (`Idnr`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `HSN_IDMUT`
--

DROP TABLE IF EXISTS `HSN_IDMUT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HSN_IDMUT` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IDNR` int(11) DEFAULT NULL,
  `ID_Origin` int(11) DEFAULT NULL,
  `Source` varchar(100) DEFAULT NULL,
  `Valid_day` int(11) DEFAULT NULL,
  `Valid_month` int(11) DEFAULT NULL,
  `Valid_year` int(11) DEFAULT NULL,
  `RP_family` varchar(50) DEFAULT NULL,
  `RP_prefix` varchar(255) DEFAULT NULL,
  `RP_firstname` varchar(50) DEFAULT NULL,
  `RP_B_DAY` int(11) DEFAULT NULL,
  `RP_B_MONTH` int(11) DEFAULT NULL,
  `RP_B_YEAR` int(11) DEFAULT NULL,
  `RP_B_PLACE` varchar(30) DEFAULT NULL,
  `RP_B_SEX` varchar(1) DEFAULT NULL,
  `Remarks` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Id` (`Id`),
  KEY `IDNR` (`IDNR`),
  KEY `ID_Origin` (`ID_Origin`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `HSN_KWYT`
--

DROP TABLE IF EXISTS `HSN_KWYT`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `HSN_KWYT` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Idnr` int(11) DEFAULT '0',
  `Idvolgnr` int(11) DEFAULT '0',
  `Startdag` int(11) DEFAULT '0',
  `Startmaand` int(11) DEFAULT '0',
  `Startjaar` int(11) DEFAULT '0',
  `Eindedag` int(11) DEFAULT '0',
  `Eindemaand` int(11) DEFAULT '0',
  `Eindejaar` int(11) DEFAULT '0',
  `gevonden` varchar(1) DEFAULT NULL,
  `reden` tinyint(3) unsigned DEFAULT '0',
  `locatie` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `MAIL`
--

DROP TABLE IF EXISTS `MAIL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `MAIL` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Idnr` int(11) DEFAULT '0',
  `Briefnr` int(11) DEFAULT NULL,
  `Aard` varchar(1) DEFAULT NULL,
  `Datum` varchar(12) DEFAULT NULL,
  `Periode` varchar(20) DEFAULT NULL,
  `Gemnr` int(11) DEFAULT '0',
  `Naamgem` varchar(50) DEFAULT NULL,
  `Status` int(11) DEFAULT '0',
  `Printdatum` varchar(15) DEFAULT NULL,
  `Printen` tinyint(1) DEFAULT NULL,
  `Ontvdat` varchar(15) DEFAULT NULL,
  `Opmerk` longtext,
  `Opident` varchar(150) DEFAULT NULL,
  `Oppartner` varchar(150) DEFAULT NULL,
  `OpVader` varchar(100) DEFAULT NULL,
  `Opmoeder` varchar(100) DEFAULT NULL,
  `Type` varchar(50) DEFAULT NULL,
  `InfoOuders` tinyint(1) DEFAULT NULL,
  `InfoPartner` tinyint(1) DEFAULT NULL,
  `InfoReis` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_faseA`
--

DROP TABLE IF EXISTS `Tekst_faseA`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_faseA` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `fase_A` int(11) DEFAULT '0',
  `fase_A text` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_faseB`
--

DROP TABLE IF EXISTS `Tekst_faseB`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_faseB` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `fase_B` int(11) DEFAULT '0',
  `fase_B text` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_faseC_D`
--

DROP TABLE IF EXISTS `Tekst_faseC_D`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_faseC_D` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `fase_C_D` int(11) DEFAULT '0',
  `fase_C_D text` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_gevonden`
--

DROP TABLE IF EXISTS `Tekst_gevonden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_gevonden` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `gevonden` varchar(50) DEFAULT NULL,
  `text-gevonden` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_reden`
--

DROP TABLE IF EXISTS `Tekst_reden`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_reden` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `reden` int(11) DEFAULT '0',
  `reden_text` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `Tekst_voortgang`
--

DROP TABLE IF EXISTS `Tekst_voortgang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tekst_voortgang` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Invoerstatus` varchar(1) DEFAULT NULL,
  `Invoerstatustekst` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Id`),
  KEY `Id` (`Id`)
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

-- Dump completed on 2016-03-16 14:12:21
