-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: jumpserver
-- ------------------------------------------------------
-- Server version	5.1.73

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
-- Table structure for table `jasset_assetservice`
--

DROP TABLE IF EXISTS `jasset_assetservice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jasset_assetservice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  `comment` varchar(160) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jasset_assetservice`
--

LOCK TABLES `jasset_assetservice` WRITE;
/*!40000 ALTER TABLE `jasset_assetservice` DISABLE KEYS */;
INSERT INTO `jasset_assetservice` VALUES (1,'mysql',NULL),(2,'mongodb',NULL),(3,'ldap',NULL),(4,'redis',NULL),(5,'db2',NULL),(6,'apache',NULL),(7,'nginx',NULL),(8,'git',NULL),(9,'gerrit',NULL),(10,'tfs',NULL),(11,'zabbix',NULL),(12,'jenkins',NULL),(13,'rtx',NULL),(14,'erm',NULL),(15,'rocketmq',NULL),(16,'gcache',NULL),(17,'jira',NULL),(18,'wiki',NULL),(19,'svn',NULL),(20,'bugfree',NULL),(21,'seafile',NULL),(22,'samba',NULL),(23,'project',NULL),(24,'rabbitMQ',NULL),(25,'ftp',NULL),(26,'erlang',NULL),(27,'端点app',NULL),(28,'tomcat',NULL),(29,'Hadoop',NULL),(30,'Tair',NULL),(31,'java',NULL),(32,'zookeeper',NULL),(33,'oracle',NULL),(34,'Dubble',NULL);
/*!40000 ALTER TABLE `jasset_assetservice` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-01-20 16:07:35
