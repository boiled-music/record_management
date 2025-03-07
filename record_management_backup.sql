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
  `management_number` varchar(50) NOT NULL,
  `current_institution` varchar(100) DEFAULT NULL,
  `production_department` varchar(100) DEFAULT NULL,
  `storage_location` varchar(100) DEFAULT NULL,
  `shelf_location` varchar(100) DEFAULT NULL,
  `box_number` varchar(50) DEFAULT NULL,
  `production_year` int(11) DEFAULT NULL,
  `end_year` int(11) DEFAULT NULL,
  `preservation_period` int(11) DEFAULT NULL CHECK (`preservation_period` in (45,40,30,10,5,3,1,0)),
  `document_type` enum('?쇰컲湲곕줉臾?,'?쒖껌媛곴린濡앸Ъ','媛꾪뻾臾?,'?됱젙諛뺣Ъ') NOT NULL,
  `document_format` enum('臾몄꽌','移대뱶','???,'?꾨㈃','?꾨쫫','?⑤쾾','?뚯씠??,'媛꾪뻾臾?,'?됱젙諛뺣Ъ') NOT NULL,
  `quantity` int(11) DEFAULT 1,
  `folder_title` varchar(500) DEFAULT NULL,
  `additional_info` text DEFAULT NULL,
  `dual_preservation` tinyint(1) DEFAULT 0,
  `evaluation_status` varchar(50) DEFAULT NULL,
  `status_check` enum('1?깃툒','2?깃툒','3?깃툒','誘명솗??) DEFAULT '誘명솗??,
  `retrieval_priority` int(11) DEFAULT 0 CHECK (`retrieval_priority` in (1,2,3,0)),
  `notes` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `management_number` (`management_number`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `documents`
--

LOCK TABLES `documents` WRITE;
/*!40000 ALTER TABLE `documents` DISABLE KEYS */;
INSERT INTO `documents` VALUES (1,'GY00000001','湲고쉷?덉궛??,'湲고쉷媛먯궗??,'??湲곕줉愿','1-A-1','BX001',2001,2001,30,'?쇰컲湲곕줉臾?,'臾몄꽌',1,'媛쒕퀎怨듭떆吏媛寃곗젙痍⑥냼','',1,'蹂댁〈','1?깃툒',1,'','2025-02-10 14:19:50','2025-02-10 14:19:50'),(2,'GY00000002','?좎??뺣낫怨?,'吏?곴낵','??湲곕줉愿','15-A-5','',1987,1987,40,'?쇰컲湲곕줉臾?,'???,1,'?좎???λ?蹂몄엫?숇━','',1,'蹂댁〈','2?깃툒',1,'','2025-02-10 14:19:50','2025-02-10 14:19:50'),(3,'GY00000003','媛먯궗??,'湲고쉷媛먯궗??,'??湲곕줉愿','44-A-1','媛먯궗??29',2006,2006,5,'?쇰컲湲곕줉臾?,'臾몄꽌',3,'李멸껄??,'?섎즺 愿??踰뺤븞 ?ы븿',0,'?됯? 以?,'3?깃툒',3,'?κ린 蹂댁〈 ?꾩슂','2025-02-10 14:19:50','2025-02-10 14:19:50'),(4,'GY00000004','援??湲곕줉??,'?섍꼍遺','??湲곕줉愿','D-04','BX004',2000,2020,10,'?됱젙諛뺣Ъ','?꾨㈃',7,'?섍꼍 ?뺤콉 遺꾩꽍','?섍꼍 愿???곌뎄?먮즺',0,'蹂댁〈','誘명솗??,0,'?먭린 寃???꾩슂','2025-02-10 14:19:50','2025-02-10 14:19:50'),(5,'GY00000005','援??湲곕줉??,'援?넗援먰넻遺','??湲곕줉愿','E-05','BX005',1995,2015,5,'?쇰컲湲곕줉臾?,'?꾨쫫',2,'?꾩떆 怨꾪쉷 ?ㅺ퀎??,'嫄댁텞 ?ㅺ퀎 ?꾨쫫 ?ы븿',1,'蹂댁〈','1?깃툒',1,'?뱀닔 蹂닿? ?꾩슂','2025-02-10 14:19:50','2025-02-10 14:19:50');
/*!40000 ALTER TABLE `documents` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_uca1400_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER before_insert_documents
BEFORE INSERT ON documents
FOR EACH ROW
BEGIN
    DECLARE new_id INT;
    DECLARE new_management_number VARCHAR(50);

    
    SELECT COALESCE(MAX(id), 0) + 1 INTO new_id FROM documents;

    
    SET new_management_number = CONCAT('GY', LPAD(new_id, 8, '0'));

    
    SET NEW.management_number = new_management_number;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-12  0:41:55
