-- MySQL dump 10.13  Distrib 5.5.48, for Linux (x86_64)
--
-- Host: localhost    Database: hsn_mail_mdb
-- ------------------------------------------------------
-- Server version	5.5.48

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
-- Table structure for table `PKKND`
--

DROP TABLE IF EXISTS `PKKND`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PKKND` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `IDNR` int(11) DEFAULT NULL,
  `IDNRP` int(11) DEFAULT NULL,
  `GAKTNRP` varchar(8) DEFAULT NULL,
  `PKTYPE` int(11) DEFAULT NULL,
  `EINDAGPK` int(11) DEFAULT NULL,
  `EINMNDPK` int(11) DEFAULT NULL,
  `EINJARPK` int(11) DEFAULT NULL,
  `CTRDGP` int(11) DEFAULT NULL,
  `CTRMDP` int(11) DEFAULT NULL,
  `CTRJRP` int(11) DEFAULT NULL,
  `CTRPARP` varchar(1) DEFAULT NULL,
  `GZNVRMP` varchar(50) DEFAULT NULL,
  `ANMPERP` varchar(50) DEFAULT NULL,
  `TUSPERP` varchar(10) DEFAULT NULL,
  `VNM1PERP` varchar(20) DEFAULT NULL,
  `VNM2PERP` varchar(20) DEFAULT NULL,
  `VNM3PERP` varchar(30) DEFAULT NULL,
  `GDGPERP` int(11) DEFAULT NULL,
  `GMDPERP` int(11) DEFAULT NULL,
  `GJRPERP` int(11) DEFAULT NULL,
  `GDGPERPCR` int(11) DEFAULT NULL,
  `GMDPERPCR` int(11) DEFAULT NULL,
  `GJRPERPCR` int(11) DEFAULT NULL,
  `GPLPERP` varchar(50) DEFAULT NULL,
  `NATPERP` varchar(40) DEFAULT NULL,
  `GDSPERP` varchar(20) DEFAULT NULL,
  `GSLPERP` varchar(1) DEFAULT NULL,
  `ANMVDRP` varchar(50) DEFAULT NULL,
  `TUSVDRP` varchar(10) DEFAULT NULL,
  `VNM1VDRP` varchar(20) DEFAULT NULL,
  `VNM2VDRP` varchar(20) DEFAULT NULL,
  `VNM3VDRP` varchar(30) DEFAULT NULL,
  `GDGVDRP` int(11) DEFAULT NULL,
  `GMDVDRP` int(11) DEFAULT NULL,
  `GJRVDRP` int(11) DEFAULT NULL,
  `GDGVDRPCR` int(11) DEFAULT NULL,
  `GMDVDRPCR` int(11) DEFAULT NULL,
  `GJRVDRPCR` int(11) DEFAULT NULL,
  `GPLVDRP` varchar(50) DEFAULT NULL,
  `ANMMDRP` varchar(50) DEFAULT NULL,
  `TUSMDRP` varchar(10) DEFAULT NULL,
  `VNM1MDRP` varchar(20) DEFAULT NULL,
  `VNM2MDRP` varchar(20) DEFAULT NULL,
  `VNM3MDRP` varchar(30) DEFAULT NULL,
  `GDGMDRP` int(11) DEFAULT NULL,
  `GMDMDRP` int(11) DEFAULT NULL,
  `GJRMDRP` int(11) DEFAULT NULL,
  `GDGMDRPCR` int(11) DEFAULT NULL,
  `GMDMDRPCR` int(11) DEFAULT NULL,
  `GJRMDRPCR` int(11) DEFAULT NULL,
  `GPLMDRP` varchar(50) DEFAULT NULL,
  `ODGPERP` int(11) DEFAULT NULL,
  `OMDPERP` int(11) DEFAULT NULL,
  `OJRPERP` int(11) DEFAULT NULL,
  `OPLPERP` varchar(50) DEFAULT NULL,
  `OAKPERP` varchar(10) DEFAULT NULL,
  `ODOPERP` varchar(50) DEFAULT NULL,
  `GEGPERP` varchar(1) DEFAULT NULL,
  `GEGVDRP` varchar(1) DEFAULT NULL,
  `GEGMDRP` varchar(1) DEFAULT NULL,
  `PROBLMP` varchar(1) DEFAULT NULL,
  `PSBDGP` int(11) DEFAULT NULL,
  `PSBMDP` int(11) DEFAULT NULL,
  `PSBJRP` int(11) DEFAULT NULL,
  `PSBNRP` varchar(10) DEFAULT NULL,
  `OPDRNR` varchar(3) DEFAULT NULL,
  `DATUM` datetime DEFAULT NULL,
  `INIT` varchar(3) DEFAULT NULL,
  `VERSIE` varchar(5) DEFAULT NULL,
  `ONDRZKO` varchar(3) DEFAULT NULL,
  `OPDRNRO` varchar(3) DEFAULT NULL,
  `DATUMO` datetime DEFAULT NULL,
  `INITO` varchar(3) DEFAULT NULL,
  `VERSIEO` varchar(5) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `IDNR` (`IDNR`),
  KEY `IDNRP` (`IDNRP`)
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

-- Dump completed on 2016-03-11 13:40:01
