-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: record_management_db
-- ------------------------------------------------------
-- Server version	11.6.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `documents`
--

DROP TABLE IF EXISTS `documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `documents` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `management_number` varchar(50) DEFAULT NULL,
  `current_institution` varchar(100) DEFAULT NULL,
  `production_institution` varchar(100) DEFAULT NULL,
  `storage_info` varchar(100) DEFAULT NULL,
  `box_number` varchar(50) DEFAULT NULL,
  `production_year` int(11) DEFAULT NULL,
  `end_year` int(11) DEFAULT NULL,
  `preservation_period` int(11) DEFAULT NULL,
  `document_type` varchar(50) DEFAULT NULL,
  `document_form` varchar(50) DEFAULT NULL,
  `quantity` int(11) DEFAULT NULL,
  `folder_title` varchar(100) DEFAULT NULL,
  `additional_info` text DEFAULT NULL,
  `dual_preservation` tinyint(1) DEFAULT NULL,
  `status_check` varchar(50) DEFAULT NULL,
  `evacuation_priority` int(11) DEFAULT NULL,
  `notes` text DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,'GY0000001','기획예산실','기획감사실','1서고-1-A-1','BX-001',1999,2000,30,'일반기록물','문서',1,'프로젝트 계획서','중요한 문서',1,'정상',1,'특이사항 없음');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;
