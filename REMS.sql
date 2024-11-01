-- MySQL dump 10.13  Distrib 8.0.36, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: systestrems
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `leasecontract`
--

DROP TABLE IF EXISTS `leasecontract`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leasecontract` (
  `contract_id` int NOT NULL AUTO_INCREMENT,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `property_id` int DEFAULT NULL,
  `owner_id` int DEFAULT NULL,
  `tenant_id` int DEFAULT NULL,
  PRIMARY KEY (`contract_id`),
  KEY `owner_id` (`owner_id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `leasecontract_ibfk_1` (`property_id`),
  CONSTRAINT `leasecontract_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `property` (`property_id`) ON DELETE CASCADE,
  CONSTRAINT `leasecontract_ibfk_2` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`owner_id`),
  CONSTRAINT `leasecontract_ibfk_3` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`tenant_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leasecontract`
--

LOCK TABLES `leasecontract` WRITE;
/*!40000 ALTER TABLE `leasecontract` DISABLE KEYS */;
INSERT INTO `leasecontract` VALUES (1,'2024-04-01','2024-08-31',1,1,1),(3,'2024-05-30','2024-11-30',1,2,1),(4,'2024-02-10','2024-09-10',1,2,1),(5,'2024-04-30','2025-01-30',1,2,1),(6,'2024-04-30','2025-01-30',1,2,1),(7,'2024-01-30','2024-11-30',1,2,1),(8,'2024-01-11','2024-09-11',1,1,2),(9,'2024-03-11','2024-08-11',1,2,1);
/*!40000 ALTER TABLE `leasecontract` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `owner`
--

DROP TABLE IF EXISTS `owner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `owner` (
  `owner_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`owner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `owner`
--

LOCK TABLES `owner` WRITE;
/*!40000 ALTER TABLE `owner` DISABLE KEYS */;
INSERT INTO `owner` VALUES (1,'Carol White','555-1234','carol@example.com'),(2,'David Brown','456-789-0123','david@example.com');
/*!40000 ALTER TABLE `owner` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `payment_id` int NOT NULL AUTO_INCREMENT,
  `contract_id` int DEFAULT NULL,
  `date` date NOT NULL,
  `is_paid` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`payment_id`),
  KEY `payments_ibfk_1` (`contract_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`contract_id`) REFERENCES `leasecontract` (`contract_id`)
) ENGINE=InnoDB AUTO_INCREMENT=278 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (207,1,'2024-04-01',0),(208,1,'2024-05-01',0),(209,1,'2024-06-01',0),(210,1,'2024-07-01',0),(211,1,'2024-08-01',0),(212,5,'2024-04-01',0),(213,5,'2024-05-01',0),(214,5,'2024-06-01',0),(215,5,'2024-07-01',0),(216,5,'2024-08-01',0),(217,5,'2024-09-01',0),(218,5,'2024-10-01',0),(219,5,'2024-11-01',0),(220,5,'2024-12-01',0),(221,5,'2025-01-01',0),(222,6,'2024-04-30',0),(223,6,'2024-05-30',0),(224,6,'2024-06-30',0),(225,6,'2024-07-30',0),(226,6,'2024-08-30',0),(227,6,'2024-09-30',0),(228,6,'2024-10-30',0),(229,6,'2024-11-30',0),(230,6,'2024-12-30',0),(231,6,'2025-01-30',0),(234,9,'2024-03-11',1),(235,9,'2024-04-11',1),(236,9,'2024-05-11',1),(237,9,'2024-06-11',0),(238,9,'2024-07-11',0),(239,9,'2024-08-11',0);
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `property`
--

DROP TABLE IF EXISTS `property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `property` (
  `property_id` int NOT NULL AUTO_INCREMENT,
  `address` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `owner_id` int DEFAULT NULL,
  PRIMARY KEY (`property_id`),
  KEY `owner_id` (`owner_id`),
  CONSTRAINT `property_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `owner` (`owner_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `property`
--

LOCK TABLES `property` WRITE;
/*!40000 ALTER TABLE `property` DISABLE KEYS */;
INSERT INTO `property` VALUES (1,'123 Main St',1600.00,1),(2,'456 Oak Dr',1800.00,2);
/*!40000 ALTER TABLE `property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertytype`
--

DROP TABLE IF EXISTS `propertytype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertytype` (
  `type_id` int NOT NULL,
  `type_name` varchar(50) NOT NULL,
  PRIMARY KEY (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertytype`
--

LOCK TABLES `propertytype` WRITE;
/*!40000 ALTER TABLE `propertytype` DISABLE KEYS */;
INSERT INTO `propertytype` VALUES (1,'Apartment'),(2,'House');
/*!40000 ALTER TABLE `propertytype` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `propertytypelist`
--

DROP TABLE IF EXISTS `propertytypelist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `propertytypelist` (
  `property_id` int NOT NULL,
  `type_id` int NOT NULL,
  PRIMARY KEY (`property_id`,`type_id`),
  KEY `type_id` (`type_id`),
  CONSTRAINT `propertytypelist_ibfk_2` FOREIGN KEY (`type_id`) REFERENCES `propertytype` (`type_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `propertytypelist`
--

LOCK TABLES `propertytypelist` WRITE;
/*!40000 ALTER TABLE `propertytypelist` DISABLE KEYS */;
INSERT INTO `propertytypelist` VALUES (1,1),(2,2);
/*!40000 ALTER TABLE `propertytypelist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reporting`
--

DROP TABLE IF EXISTS `reporting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reporting` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `property_id` int DEFAULT NULL,
  `quarter` varchar(10) NOT NULL,
  `contract_count` int DEFAULT NULL,
  `total_income` decimal(10,2) DEFAULT NULL,
  `debt` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`report_id`),
  KEY `reporting_ibfk_1` (`property_id`),
  CONSTRAINT `reporting_ibfk_1` FOREIGN KEY (`property_id`) REFERENCES `property` (`property_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reporting`
--

LOCK TABLES `reporting` WRITE;
/*!40000 ALTER TABLE `reporting` DISABLE KEYS */;
INSERT INTO `reporting` VALUES (3,1,'Q2',1,0.00,4500.00),(4,1,'Q3',1,0.00,3000.00);
/*!40000 ALTER TABLE `reporting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant`
--

DROP TABLE IF EXISTS `tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tenant` (
  `tenant_id` int NOT NULL,
  `name` varchar(100) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`tenant_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tenant`
--

LOCK TABLES `tenant` WRITE;
/*!40000 ALTER TABLE `tenant` DISABLE KEYS */;
INSERT INTO `tenant` VALUES (1,'Alice Johnson','555-5678','alice@example.com'),(2,'Bob','234-567-8901','bob@example.com');
/*!40000 ALTER TABLE `tenant` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-02  0:09:18
