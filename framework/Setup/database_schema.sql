-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Apr 06, 2016 at 07:43 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";

--
-- Database: `db_scrapper`
--
DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_ScheduleRunNow`(
  IN Site_Id INT(10),
  IN Site VARCHAR(50),
   )
BEGIN
  IF ( SELECT EXISTS (SELECT 1 FROM Schedule WHERE SiteId = Site_Id  and Active = 0 )) THEN
    SELECT "Schedule Already active and running ";
  ELSE
    UPDATE Schedule SET Active = 0, UpdateDate = NULL where SiteId = Site_Id ;
    SELECT "Scheduled for run Successfully" ;
  END IF;
END$$


--
-- Procedures
--
CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddSchedule`(
  IN Site_Id INT(10),
  IN Start_Date VARCHAR(255),
  IN End_Date VARCHAR(255),
  IN IX_Code VARCHAR(255),
  IN Occ VARCHAR(255),
  IN Occ_Type VARCHAR(255),
  IN Is_Active VARCHAR(255),
  IN MsgOnSuccess VARCHAR(255),
  IN MsgOnFailure VARCHAR(255))
BEGIN
  IF ( SELECT EXISTS (SELECT 1 FROM Schedule WHERE IXCode = IX_Code)) THEN
    SELECT "Schedule Exists" Message;
  ELSE
    INSERT INTO Schedule (SiteId ,StartDate ,EndDate ,IXCode ,Occurance ,OccuranceType ,Active ,MessageTextOnSuccess ,MessageTextOnFailure)
    VALUES (Site_Id ,Start_Date ,End_Date ,IX_Code ,Occ ,Occ_Type ,Is_Active ,MsgOnSuccess ,MsgOnFailure );
    SELECT "Schedule Added Successfully" Message;
  END IF;
END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddScheduleLog`(
  IN Schedule_Id INT(10),
  IN Event_Name VARCHAR(255),
  IN Event_Exception_Message VARCHAR(2000))
BEGIN
  IF ( SELECT EXISTS (SELECT 1 FROM ScheduleLog WHERE ScheduleId = Schedule_Id AND Event = Event_Name AND EventExceptionMessage = Event_Exception_Message)) THEN
    SELECT "Schedule Log Exists" Message;
  ELSE
    INSERT INTO ScheduleLog (ScheduleId, Event, EventExceptionMessage)
    VALUES (Schedule_Id, Event_Name, Event_Exception_Message);
    SELECT "Schedule Logged" Message;
  END IF;
END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddSite`(IN Domain_Name VARCHAR(255), IN Sitemap_Url VARCHAR(255))
BEGIN
  IF ( SELECT EXISTS (SELECT 1 FROM Site WHERE DomainName = Domain_Name AND SitemapUrl = Sitemap_Url)) THEN
  SELECT 'Site Already Exists' Message;
  ELSE
  INSERT INTO Site (DomainName,SitemapUrl) VALUES (Domain_Name, Sitemap_Url);
  SELECT 'Site Added Successfully' Message;
  END IF;

END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddSiteLogin`(IN Site_Id INT, IN Key_Name VARCHAR(100), IN Key_Value VARCHAR(100))
BEGIN

  IF ( SELECT EXISTS (SELECT 1 FROM SiteLogin WHERE SiteId = Site_Id AND KeyName = Key_Name AND KeyValue = Key_Value)) THEN
    SELECT 'Site Login Already Exists' Message;
  ELSE
    INSERT INTO SiteLogin (SiteId, KeyName, KeyValue) VALUES (Site_Id, Key_Name, Key_Value);
    SELECT 'Site Login Added Successfully' Message;
  END IF;

END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddSiteScrapeKey`(
  IN Site_Id INT,
  IN Scrape_Scheme VARCHAR(100),
  IN Key_Name VARCHAR(100),
  IN Key_Alias VARCHAR(100),
  IN Key_DefaultValue VARCHAR(100)
)
BEGIN

  IF ( SELECT EXISTS (SELECT 1 FROM SiteScrapeKey WHERE SiteId = Site_Id AND KeyName = Key_Name AND KeyAlias = Key_Alias)) THEN
    SELECT "Site Scrape Key Already Exists" Message;
  ELSE
    INSERT INTO SiteScrapeKey (SiteId, ScrapeScheme, KeyName, KeyAlias, KeyDefaultValue)
    VALUES (Site_Id, Scrape_Scheme, Key_Name, Key_Alias, Key_DefaultValue);
    SELECT "Site Scrape Keys Added Successfully" Message;
  END IF;

END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_AddSiteScrapeUrl`(
  IN Site_Id INT,
  IN Url VARCHAR(400)
)
BEGIN

  IF ( SELECT EXISTS (SELECT 1 FROM SiteScrapeURL WHERE TRIM(URL) = TRIM(Url))) THEN
    SELECT "Site Scrape URL Exists" Message;
  ELSE
    INSERT INTO SiteScrapeURL (SiteId, URL) VALUES (Site_Id, Url);
    SELECT "Site Scrape URL(s) Added Successfully" Message;
  END IF;

END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_GetSite`(IN Site_Name VARCHAR(255))
BEGIN
  SELECT Id, DomainName FROM Site WHERE DomainName = Site_Name;
END$$

CREATE DEFINER=`db_scrapper`@`localhost` PROCEDURE `sp_ServerCheck`()
BEGIN
  SELECT 1 Message;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `ApplicationLog`
--

CREATE TABLE IF NOT EXISTS `ApplicationLog` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `Message` text NOT NULL,
  `Type` varchar(60) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Schedule`
--

CREATE TABLE IF NOT EXISTS `Schedule` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `IXCode` varchar(50) DEFAULT NULL,
  `SiteId` int(11) DEFAULT NULL,
  `StartDate` date DEFAULT NULL,
  `EndDate` date DEFAULT NULL,
  `Occurance` varchar(7) DEFAULT NULL,
  `OccuranceType` varchar(13) DEFAULT NULL,
  `Active` varchar(50) DEFAULT NULL,
  `MessageTextOnSuccess` varchar(50) DEFAULT 'Scrape Schedule Successfully Completed.',
  `MessageTextOnFailure` varchar(50) DEFAULT 'Scrape Schedule Failed.',
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;


-- --------------------------------------------------------
--
-- Table structure for table `ScheduleLog`
--

CREATE TABLE IF NOT EXISTS `ScheduleLog` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ScheduleId` int(11) DEFAULT NULL,
  `Event` varchar(255) DEFAULT NULL,
  `EventExceptionMessage` varchar(2000) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `ScheduleOutput`
--

CREATE TABLE IF NOT EXISTS `ScheduleOutput` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `ScheduleId` int(11) DEFAULT NULL,
  `OutputFile` varchar(255) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

-- --------------------------------------------------------

--
-- Table structure for table `ScheduleType`
--

CREATE TABLE IF NOT EXISTS `ScheduleType` (
  `Type` enum('Regular','Factory','','') NOT NULL,
  `CreateDate` datetime DEFAULT NULL,
  `CreateUser` int(11) NOT NULL,
  `UpdateDate` datetime NOT NULL,
  `UpdateUser` int(11) NOT NULL,
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `Site`
--

CREATE TABLE IF NOT EXISTS `Site` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `DomainName` varchar(50) DEFAULT NULL,
  `SitemapUrl` varchar(1000) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=12 ;


-- --------------------------------------------------------

--
-- Table structure for table `SiteLogin`
--

CREATE TABLE IF NOT EXISTS `SiteLogin` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `SiteId` int(11) DEFAULT NULL,
  `KeyName` varchar(50) DEFAULT NULL,
  `KeyValue` varchar(50) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17 ;


-- --------------------------------------------------------

--
-- Table structure for table `SiteScrapeKey`
--

CREATE TABLE IF NOT EXISTS `SiteScrapeKey` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `SiteId` int(11) DEFAULT NULL,
  `ScrapeScheme` varchar(50) DEFAULT NULL,
  `KeyName` varchar(50) DEFAULT NULL,
  `KeyAlias` varchar(50) DEFAULT NULL,
  `KeyDefaultValue` varchar(255) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;


-- --------------------------------------------------------

--
-- Table structure for table `SiteScrapeURL`
--

CREATE TABLE IF NOT EXISTS `SiteScrapeURL` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `SiteId` int(11) DEFAULT NULL,
  `URL` varchar(255) DEFAULT NULL,
  `CreateDate` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `CreateUser` varchar(50) DEFAULT 'sys',
  `UpdateDate` varchar(50) DEFAULT NULL,
  `UpdateUser` varchar(50) DEFAULT 'sys',
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=17442 

-- --------------------------------------------------------

--
-- Table structure for table `SiteTempURL`
--

CREATE TABLE IF NOT EXISTS `SiteTempURL` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `SiteId` int(11) NOT NULL,
  `URL` varchar(255) NOT NULL,
  `status` smallint(2) NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=215 ;


