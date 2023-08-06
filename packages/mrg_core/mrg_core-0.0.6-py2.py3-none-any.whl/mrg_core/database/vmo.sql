    -- MySQL dump 10.13  Distrib 5.6.26, for Win64 (x86_64)
--
-- Host: localhost    Database: vmo
-- ------------------------------------------------------
-- Server version	5.6.26-log

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
-- Table structure for table `cam_camera`
--

DROP TABLE IF EXISTS `cam_camera`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_camera` (
  `camera_code` varchar(255) NOT NULL,
  `brand` longtext,
  `model` longtext,
  `chip` longtext,
  `pixels_x` int(11) DEFAULT NULL,
  `pixels_y` int(11) DEFAULT NULL,
  `pixelsize_x` decimal(20,10) DEFAULT NULL,
  `pixelsize_y` decimal(20,10) DEFAULT NULL,
  `interlaced_flag` tinyint(4) DEFAULT NULL,
  `bitdepth` int(11) DEFAULT NULL,
  `sensitivity` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`camera_code`),
  KEY `cam_camera_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_camera_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_digitizer`
--

DROP TABLE IF EXISTS `cam_digitizer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_digitizer` (
  `digitizer_code` varchar(255) NOT NULL,
  `brand` longtext,
  `model` longtext,
  `chip` longtext,
  `bitdepth` int(11) DEFAULT NULL,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`digitizer_code`),
  KEY `cam_digitizer_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_digitizer_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_intensifier`
--

DROP TABLE IF EXISTS `cam_intensifier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_intensifier` (
  `intensifier_code` varchar(255) NOT NULL,
  `brand` longtext,
  `model` longtext,
  `generation` longtext,
  `resolution` decimal(20,10) DEFAULT NULL,
  `dynamic_range` decimal(20,10) DEFAULT NULL,
  `input_diameter` decimal(20,10) DEFAULT NULL,
  `output_diameter` decimal(20,10) DEFAULT NULL,
  `photocathode` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`intensifier_code`),
  KEY `cam_intensifier_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_intensifier_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_lens`
--

DROP TABLE IF EXISTS `cam_lens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_lens` (
  `lens_code` varchar(255) NOT NULL,
  `brand` longtext,
  `model` longtext,
  `aperture` decimal(20,10) DEFAULT NULL,
  `focal_length` decimal(20,10) DEFAULT NULL,
  `lens_type` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`lens_code`),
  KEY `cam_lens_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_lens_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_meteor`
--

DROP TABLE IF EXISTS `cam_meteor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_meteor` (
  `meteor_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `period_code` varchar(255) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `shower_code` longtext,
  `exposures` smallint(6) DEFAULT NULL,
  `duration` decimal(20,10) DEFAULT NULL,
  `mag` decimal(20,10) DEFAULT NULL,
  `speed` decimal(20,10) DEFAULT NULL,
  `in_fov` longtext,
  `begin_ra` decimal(20,10) DEFAULT NULL,
  `begin_dec` decimal(20,10) DEFAULT NULL,
  `end_ra` decimal(20,10) DEFAULT NULL,
  `end_dec` decimal(20,10) DEFAULT NULL,
  `comments` longtext,
  `e_duration` decimal(20,10) DEFAULT NULL,
  `e_mag` decimal(20,10) DEFAULT NULL,
  `e_speed` decimal(20,10) DEFAULT NULL,
  `e_begin_ra` decimal(20,10) DEFAULT NULL,
  `e_begin_dec` decimal(20,10) DEFAULT NULL,
  `cov_begin` decimal(20,10) DEFAULT NULL,
  `e_end_ra` decimal(20,10) DEFAULT NULL,
  `e_end_dec` decimal(20,10) DEFAULT NULL,
  `cov_end` decimal(20,10) DEFAULT NULL,
  `shower_code_original` longtext,
  PRIMARY KEY (`meteor_code`),
  KEY `cam_meteor_entry_code_fkey` (`entry_code`),
  KEY `cam_meteor_period_code_fkey` (`period_code`),
  CONSTRAINT `cam_meteor_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `cam_session` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cam_meteor_meteor_code_fkey` FOREIGN KEY (`meteor_code`) REFERENCES `meteor` (`meteor_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cam_meteor_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `cam_period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_period`
--

DROP TABLE IF EXISTS `cam_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_period` (
  `period_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `start` datetime DEFAULT NULL,
  `stop` datetime DEFAULT NULL,
  `teff` decimal(20,10) DEFAULT NULL,
  `lm` decimal(20,10) DEFAULT NULL,
  `fov_alt` decimal(20,10) DEFAULT NULL,
  `fov_az` decimal(20,10) DEFAULT NULL,
  `fov_rotation` decimal(20,10) DEFAULT NULL,
  `fov_guided_flag` tinyint(4) DEFAULT NULL,
  `fov_obstruction` decimal(20,10) DEFAULT NULL,
  `e_teff` decimal(20,10) DEFAULT NULL,
  `e_lm` decimal(20,10) DEFAULT NULL,
  `e_fov_obstruction` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`period_code`),
  KEY `cam_period_entry_code_fkey` (`entry_code`),
  CONSTRAINT `cam_period_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `cam_session` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cam_period_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_pos`
--

DROP TABLE IF EXISTS `cam_pos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_pos` (
  `meteor_code` varchar(255) NOT NULL,
  `pos_no` smallint(6) NOT NULL,
  `time` datetime(3) DEFAULT NULL,
  `mag` decimal(20,10) DEFAULT NULL,
  `pos_x` decimal(20,10) DEFAULT NULL,
  `pos_y` decimal(20,10) DEFAULT NULL,
  `pos_ra` decimal(20,10) DEFAULT NULL,
  `pos_dec` decimal(20,10) DEFAULT NULL,
  `correction_flag` tinyint(4) DEFAULT NULL,
  `outlier_flag` tinyint(4) DEFAULT NULL,
  `saturation_flag` tinyint(4) DEFAULT NULL,
  `e_time` decimal(20,10) DEFAULT NULL,
  `e_mag` decimal(20,10) DEFAULT NULL,
  `e_pos_x` decimal(20,10) DEFAULT NULL,
  `e_pos_y` decimal(20,10) DEFAULT NULL,
  `e_pos_ra` decimal(20,10) DEFAULT NULL,
  `e_pos_dec` decimal(20,10) DEFAULT NULL,
  `cov_ra_dec` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`meteor_code`,`pos_no`),
  CONSTRAINT `cam_pos_meteor_code_fkey` FOREIGN KEY (`meteor_code`) REFERENCES `cam_meteor` (`meteor_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_pos_file`
--

DROP TABLE IF EXISTS `cam_pos_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_pos_file` (
  `meteor_code` varchar(255) NOT NULL,
  `pos_no` smallint(6) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`meteor_code`,`pos_no`,`path`),
  KEY `cam_pos_file_path_fkey` (`path`),
  CONSTRAINT `cam_pos_file_meteor_code_fkey` FOREIGN KEY (`meteor_code`, `pos_no`) REFERENCES `cam_pos` (`meteor_code`, `pos_no`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cam_pos_file_path_fkey` FOREIGN KEY (`path`) REFERENCES `files` (`path`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_prism`
--

DROP TABLE IF EXISTS `cam_prism`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_prism` (
  `prism_code` varchar(255) NOT NULL,
  `type_name` longtext,
  `brand` longtext,
  `model` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`prism_code`),
  KEY `cam_prism_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_prism_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_session`
--

DROP TABLE IF EXISTS `cam_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_session` (
  `entry_code` varchar(255) NOT NULL,
  `system_code` varchar(255) DEFAULT NULL,
  `location_code` varchar(255) DEFAULT NULL,
  `observer_code` varchar(255) DEFAULT NULL,
  `version` datetime DEFAULT NULL,
  `software_code` varchar(255) DEFAULT NULL,
  `shower_cat_code` varchar(4) DEFAULT NULL,
  `camera_code` varchar(255) DEFAULT NULL,
  `prism_code` varchar(255) DEFAULT NULL,
  `lens_code` varchar(255) DEFAULT NULL,
  `intensifier_code` varchar(255) DEFAULT NULL,
  `relay_lens_code` varchar(255) DEFAULT NULL,
  `digitizer_code` varchar(255) DEFAULT NULL,
  `gain` longtext,
  `storage` longtext,
  `interlaced_flag` tinyint(4) DEFAULT NULL,
  `interlaced_order` longtext,
  `exposure_time` decimal(20,10) DEFAULT NULL,
  `sampling_interval` decimal(20,10) DEFAULT NULL,
  `shutter_flag` tinyint(4) DEFAULT NULL,
  `shutter_frequency` decimal(20,10) DEFAULT NULL,
  `shutter_description` longtext,
  `fov_vertical` decimal(20,10) DEFAULT NULL,
  `image_scale` decimal(20,10) DEFAULT NULL,
  `effective_x` int(11) DEFAULT NULL,
  `effective_y` int(11) DEFAULT NULL,
  `depth` int(11) DEFAULT NULL,
  `saturation_value` int(11) DEFAULT NULL,
  `color_flag` tinyint(4) DEFAULT NULL,
  `e_time` decimal(20,10) DEFAULT NULL,
  `e_astrometry` decimal(20,10) DEFAULT NULL,
  `comments` longtext,
  PRIMARY KEY (`entry_code`),
  KEY `cam_session_camera_code_fkey` (`camera_code`),
  KEY `cam_session_digitizer_code_fkey` (`digitizer_code`),
  KEY `cam_session_intensifier_code_fkey` (`intensifier_code`),
  KEY `cam_session_lens_code_fkey` (`lens_code`),
  KEY `cam_session_location_code_fkey` (`location_code`),
  KEY `cam_session_observer_code_fkey` (`observer_code`),
  KEY `cam_session_prism_code_fkey` (`prism_code`),
  KEY `cam_session_relay_lens_code_fkey` (`relay_lens_code`),
  KEY `cam_session_shower_cat_code_fkey` (`shower_cat_code`),
  KEY `cam_session_software_code_fkey` (`software_code`),
  KEY `cam_session_system_code_fkey` (`system_code`),
  CONSTRAINT `cam_session_camera_code_fkey` FOREIGN KEY (`camera_code`) REFERENCES `cam_camera` (`camera_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_digitizer_code_fkey` FOREIGN KEY (`digitizer_code`) REFERENCES `cam_digitizer` (`digitizer_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `cam_session_intensifier_code_fkey` FOREIGN KEY (`intensifier_code`) REFERENCES `cam_intensifier` (`intensifier_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_lens_code_fkey` FOREIGN KEY (`lens_code`) REFERENCES `cam_lens` (`lens_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_location_code_fkey` FOREIGN KEY (`location_code`) REFERENCES `location` (`location_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_prism_code_fkey` FOREIGN KEY (`prism_code`) REFERENCES `cam_prism` (`prism_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_relay_lens_code_fkey` FOREIGN KEY (`relay_lens_code`) REFERENCES `cam_lens` (`lens_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_shower_cat_code_fkey` FOREIGN KEY (`shower_cat_code`) REFERENCES `shower_catalog` (`catalog_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_software_code_fkey` FOREIGN KEY (`software_code`) REFERENCES `cam_software` (`software_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `cam_session_system_code_fkey` FOREIGN KEY (`system_code`) REFERENCES `cam_system` (`system_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_software`
--

DROP TABLE IF EXISTS `cam_software`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_software` (
  `software_code` varchar(255) NOT NULL,
  `name` longtext,
  `star_catalog` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`software_code`),
  KEY `cam_software_observer_code_fkey` (`observer_code`),
  CONSTRAINT `cam_software_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cam_system`
--

DROP TABLE IF EXISTS `cam_system`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `cam_system` (
  `system_code` varchar(255) NOT NULL,
  `name` longtext,
  `system_type` longtext,
  `contact_code` varchar(255) DEFAULT NULL,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  `active_start` date DEFAULT NULL,
  `active_stop` date DEFAULT NULL,
  PRIMARY KEY (`system_code`),
  KEY `cam_system_contact_code_fkey` (`contact_code`),
  CONSTRAINT `cam_system_contact_code_fkey` FOREIGN KEY (`contact_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orb`
--

DROP TABLE IF EXISTS `orb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orb` (
  `orbit_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) DEFAULT NULL,
  `method_code` varchar(255) DEFAULT NULL,
  `error_iterations` int(11) DEFAULT NULL,
  `shower_code` varchar(255) DEFAULT NULL,
  `time` datetime(3) DEFAULT NULL,
  `q` decimal(30,15) DEFAULT NULL,
  `a` decimal(30,15) DEFAULT NULL,
  `e` decimal(30,15) DEFAULT NULL,
  `i` decimal(30,15) DEFAULT NULL,
  `omega` decimal(30,15) DEFAULT NULL,
  `node` decimal(30,15) DEFAULT NULL,
  `m0` decimal(30,15) DEFAULT NULL,
  `t0` decimal(30,15) DEFAULT NULL,
  `mag_abs` decimal(30,15) DEFAULT NULL,
  `mass` decimal(35,15) DEFAULT NULL,
  `vel_obs` decimal(30,15) DEFAULT NULL,
  `vel_inf` decimal(30,15) DEFAULT NULL,
  `vel_geo` decimal(30,15) DEFAULT NULL,
  `vel_helio` decimal(30,15) DEFAULT NULL,
  `height_begin` decimal(30,15) DEFAULT NULL,
  `height_max` decimal(30,15) DEFAULT NULL,
  `height_end` decimal(30,15) DEFAULT NULL,
  `rad_obs_ra` decimal(30,15) DEFAULT NULL,
  `rad_obs_dec` decimal(30,15) DEFAULT NULL,
  `rad_geo_ra` decimal(30,15) DEFAULT NULL,
  `rad_geo_dec` decimal(30,15) DEFAULT NULL,
  `z` decimal(30,15) DEFAULT NULL,
  `conv_max` decimal(30,15) DEFAULT NULL,
  `meteors` int(11) DEFAULT NULL,
  `in_fov` longtext,
  `quality_code` longtext,
  `correction_code` longtext,
  `comments` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  `d_time` decimal(30,15) DEFAULT NULL,
  `d_q` decimal(30,15) DEFAULT NULL,
  `d_a` decimal(30,15) DEFAULT NULL,
  `d_e` decimal(30,15) DEFAULT NULL,
  `d_i` decimal(30,15) DEFAULT NULL,
  `d_omega` decimal(30,15) DEFAULT NULL,
  `d_node` decimal(30,15) DEFAULT NULL,
  `d_m0` decimal(30,15) DEFAULT NULL,
  `d_t0` decimal(30,15) DEFAULT NULL,
  `d_mag_abs` decimal(30,15) DEFAULT NULL,
  `d_mass` decimal(35,15) DEFAULT NULL,
  `d_vel_obs` decimal(30,15) DEFAULT NULL,
  `d_vel_inf` decimal(30,15) DEFAULT NULL,
  `d_vel_geo` decimal(30,15) DEFAULT NULL,
  `d_vel_helio` decimal(30,15) DEFAULT NULL,
  `d_height_begin` decimal(30,15) DEFAULT NULL,
  `d_height_max` decimal(30,15) DEFAULT NULL,
  `d_height_end` decimal(30,15) DEFAULT NULL,
  `d_rad_obs_ra` decimal(30,15) DEFAULT NULL,
  `d_rad_obs_dec` decimal(30,15) DEFAULT NULL,
  `d_rad_geo_ra` decimal(30,15) DEFAULT NULL,
  `d_rad_geo_dec` decimal(30,15) DEFAULT NULL,
  `d_z` decimal(30,15) DEFAULT NULL,
  PRIMARY KEY (`orbit_code`),
  KEY `orb_entry_code_fkey` (`entry_code`),
  KEY `orb_method_code_fkey` (`method_code`),
  KEY `orb_shower_code_fkey` (`shower_code`),
  CONSTRAINT `orb_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orb_method_code_fkey` FOREIGN KEY (`method_code`) REFERENCES `orb_method` (`method_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `orb_orbit_code_fkey` FOREIGN KEY (`orbit_code`) REFERENCES `meteor` (`meteor_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `orb_shower_code_fkey` FOREIGN KEY (`shower_code`) REFERENCES `shower` (`shower_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orb_method`
--

DROP TABLE IF EXISTS `orb_method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orb_method` (
  `method_code` varchar(255) NOT NULL,
  `name` longtext,
  `mass_method` longtext,
  `comments` longtext,
  PRIMARY KEY (`method_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `orb_traject`
--

DROP TABLE IF EXISTS `orb_traject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orb_traject` (
  `orbit_code` varchar(255) NOT NULL,
  `pos_no` int(11) NOT NULL,
  `time` datetime(3) DEFAULT NULL,
  `lon` decimal(30,15) DEFAULT NULL,
  `lat` decimal(30,15) DEFAULT NULL,
  `height` decimal(30,15) DEFAULT NULL,
  `mag_abs` decimal(30,15) DEFAULT NULL,
  `vel` decimal(30,15) DEFAULT NULL,
  `d_time` decimal(30,15) DEFAULT NULL,
  `d_lon` decimal(30,15) DEFAULT NULL,
  `d_lat` decimal(30,15) DEFAULT NULL,
  `d_height` decimal(30,15) DEFAULT NULL,
  `d_mag_abs` decimal(30,15) DEFAULT NULL,
  `d_vel` decimal(30,15) DEFAULT NULL,
  `meteor_code` varchar(255) DEFAULT NULL,
  `meteor_pos_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`orbit_code`,`pos_no`),
  KEY `orb_traject_meteor_code_fkey` (`meteor_code`),
  CONSTRAINT `orb_traject_meteor_code_fkey` FOREIGN KEY (`meteor_code`) REFERENCES `meteor` (`meteor_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `orb_traject_orbit_code_fkey` FOREIGN KEY (`orbit_code`) REFERENCES `orb` (`orbit_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metrecflux`
--

DROP TABLE IF EXISTS `metrecflux`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metrecflux` (
  `filename` varchar(255) NOT NULL,
  `station` longtext,
  `shower` varchar(4) NOT NULL,
  `time` datetime(3) NOT NULL,
  `sollong` float DEFAULT NULL,
  `teff` float DEFAULT NULL,
  `lmstar` float DEFAULT NULL,
  `alt` float DEFAULT NULL,
  `dist` float DEFAULT NULL,
  `vel` float DEFAULT NULL,
  `mlalt` float DEFAULT NULL,
  `lmmet` float DEFAULT NULL,
  `eca` float DEFAULT NULL,
  `met` int(11) DEFAULT NULL,
  `mag` longtext,
  PRIMARY KEY (`filename`,`shower`,`time`),
  KEY `metrecflux_time_idx` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metrecflux_meta`
--

DROP TABLE IF EXISTS `metrecflux_meta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metrecflux_meta` (
  `filename` varchar(255) NOT NULL,
  `format` longtext,
  `observer_firstname` longtext,
  `observer_middlename` longtext,
  `observer_lastname` longtext,
  `observer_code` longtext,
  `reporter_firstname` longtext,
  `reporter_middlename` longtext,
  `reporter_lastname` longtext,
  `site_name` longtext,
  `site_country` longtext,
  `site_code` longtext,
  `site_lon` double DEFAULT NULL,
  `site_lat` double DEFAULT NULL,
  `site_height` float DEFAULT NULL,
  `camera_name` longtext,
  `camera_type` longtext,
  `camera_nominallm` float DEFAULT NULL,
  `camera_intensifier` longtext,
  `lens_type` longtext,
  `lens_focallength` float DEFAULT NULL,
  `lens_fstop` float DEFAULT NULL,
  `fov_alt` float DEFAULT NULL,
  `fov_az` float DEFAULT NULL,
  `fov_sqdeg` float DEFAULT NULL,
  `fov_sqkm` float DEFAULT NULL,
  PRIMARY KEY (`filename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `metrecflux_stations`
--

DROP TABLE IF EXISTS `metrecflux_stations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `metrecflux_stations` (
  `station` longtext,
  `observer` longtext,
  `country` longtext,
  `is_intensified` tinyint(4) DEFAULT NULL,
  `focallength` decimal(20,10) DEFAULT NULL,
  `fstop` decimal(20,10) DEFAULT NULL,
  `sqkm` double DEFAULT NULL,
  `alt` double DEFAULT NULL,
  `az` double DEFAULT NULL,
  `lon` double DEFAULT NULL,
  `lat` double DEFAULT NULL,
  `nights` bigint(20) DEFAULT NULL,
  `lm` double DEFAULT NULL,
  `nspo` bigint(20) DEFAULT NULL,
  `teff` double DEFAULT NULL,
  `eff` decimal(20,10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `country_code` varchar(4) NOT NULL,
  `name` longtext,
  PRIMARY KEY (`country_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entry`
--

DROP TABLE IF EXISTS `entry`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry` (
  `entry_code` varchar(255) NOT NULL,
  `prefix` longtext NOT NULL,
  `prefix_no` smallint(6) NOT NULL,
  `section_code` longtext,
  `start` datetime(3) DEFAULT NULL,
  `stop` datetime(3) DEFAULT NULL,
  `reporter_code` varchar(255) DEFAULT NULL,
  `source_code` varchar(255) DEFAULT NULL,
  `status_code` varchar(255) DEFAULT NULL,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  `directory` longtext,
  PRIMARY KEY (`entry_code`),
  UNIQUE KEY `entry_prefix_key` (`prefix`(255),`prefix_no`),
  KEY `entry_reporter_code_fkey` (`reporter_code`),
  KEY `entry_source_code_fkey` (`source_code`),
  KEY `entry_status_code_fkey` (`status_code`),
  CONSTRAINT `entry_reporter_code_fkey` FOREIGN KEY (`reporter_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `entry_source_code_fkey` FOREIGN KEY (`source_code`) REFERENCES `entry_source` (`source_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `entry_status_code_fkey` FOREIGN KEY (`status_code`) REFERENCES `entry_status` (`status_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entry_file`
--

DROP TABLE IF EXISTS `entry_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry_file` (
  `entry_code` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`entry_code`,`path`),
  KEY `entry_file_path_fkey` (`path`),
  CONSTRAINT `entry_file_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `entry_file_path_fkey` FOREIGN KEY (`path`) REFERENCES `files` (`path`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entry_source`
--

DROP TABLE IF EXISTS `entry_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry_source` (
  `source_code` varchar(255) NOT NULL,
  `description` longtext,
  `reference` longtext,
  `url` longtext,
  PRIMARY KEY (`source_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `entry_status`
--

DROP TABLE IF EXISTS `entry_status`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entry_status` (
  `status_code` varchar(255) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`status_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `files`
--

DROP TABLE IF EXISTS `files`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `files` (
  `path` varchar(255) NOT NULL,
  `comments` longtext,
  `file_type` longtext,
  `observer_code` varchar(255) DEFAULT NULL,
  `time_created` datetime DEFAULT NULL,
  PRIMARY KEY (`path`),
  KEY `files_owner` (`observer_code`),
  CONSTRAINT `files_owner` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `location_code` varchar(255) NOT NULL,
  `name` longtext,
  `country_code` varchar(4) DEFAULT NULL,
  `lon` decimal(20,10) DEFAULT NULL,
  `lat` decimal(20,10) DEFAULT NULL,
  `height` decimal(20,10) DEFAULT NULL,
  `uncertainty` decimal(20,10) DEFAULT NULL,
  `comments` longtext,
  `tex_name` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  `observer_code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`location_code`),
  KEY `location_country_code_key` (`country_code`),
  KEY `fkey_location_observer` (`observer_code`),
  CONSTRAINT `fkey_location_observer` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `location_country_code_fkey` FOREIGN KEY (`country_code`) REFERENCES `country` (`country_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_changes`
--

DROP TABLE IF EXISTS `log_changes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_changes` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `username` longtext,
  `action` longtext,
  `tablename` longtext,
  `key1` longtext,
  `key2` longtext,
  `before` longtext,
  `after` longtext,
  `comments` longtext,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10217 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `log_messages`
--

DROP TABLE IF EXISTS `log_messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log_messages` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `timestamp` datetime DEFAULT NULL,
  `module` longtext,
  `message_type` longtext,
  `message` longtext,
  `username` longtext,
  `hostname` longtext,
  `uri` longtext,
  `referer` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6036 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meteor`
--

DROP TABLE IF EXISTS `meteor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meteor` (
  `meteor_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `meteor_number` int(11) NOT NULL,
  PRIMARY KEY (`meteor_code`),
  UNIQUE KEY `meteor_entry_code_key` (`entry_code`,`meteor_number`),
  CONSTRAINT `meteor_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `meteor_file`
--

DROP TABLE IF EXISTS `meteor_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `meteor_file` (
  `meteor_code` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`meteor_code`,`path`),
  KEY `meteor_file_path_fkey` (`path`),
  CONSTRAINT `meteor_file_meteor_code_fkey` FOREIGN KEY (`meteor_code`) REFERENCES `meteor` (`meteor_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `meteor_file_path_fkey` FOREIGN KEY (`path`) REFERENCES `files` (`path`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `observer`
--

DROP TABLE IF EXISTS `observer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `observer` (
  `observer_code` varchar(255) NOT NULL,
  `first_name` longtext,
  `last_name` longtext,
  `address1` longtext,
  `address2` longtext,
  `address3` longtext,
  `postal_code` longtext,
  `city` longtext,
  `country_code` varchar(4) DEFAULT NULL,
  `birth_year` smallint(6) DEFAULT NULL,
  `email` longtext,
  `url` longtext,
  `affiliation` longtext,
  `comments` longtext,
  `tex_first_name` longtext,
  `tex_last_name` longtext,
  `time_created` datetime DEFAULT NULL,
  `time_updated` datetime DEFAULT NULL,
  PRIMARY KEY (`observer_code`),
  KEY `observer_country_code_fkey` (`country_code`),
  CONSTRAINT `observer_country_code_fkey` FOREIGN KEY (`country_code`) REFERENCES `country` (`country_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `period`
--

DROP TABLE IF EXISTS `period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period` (
  `period_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `period_number` int(11) NOT NULL,
  PRIMARY KEY (`period_code`),
  UNIQUE KEY `period_entry_code_key` (`entry_code`,`period_number`),
  CONSTRAINT `period_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `period_file`
--

DROP TABLE IF EXISTS `period_file`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `period_file` (
  `period_code` varchar(255) NOT NULL,
  `path` varchar(255) NOT NULL,
  PRIMARY KEY (`period_code`,`path`),
  KEY `period_file_path_fkey` (`path`),
  CONSTRAINT `period_file_path_fkey` FOREIGN KEY (`path`) REFERENCES `files` (`path`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `period_file_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shower`
--

DROP TABLE IF EXISTS `shower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shower` (
  `shower_code` varchar(255) NOT NULL,
  `iau_number` smallint(6) DEFAULT NULL,
  `name` longtext,
  `parent` longtext,
  `tex_name` longtext,
  `unofficial_codes` longtext,
  `unofficial_names` longtext,
  `comments` longtext,
  PRIMARY KEY (`shower_code`),
  UNIQUE KEY `shower_iau_number_key` (`iau_number`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shower_catalog`
--

DROP TABLE IF EXISTS `shower_catalog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shower_catalog` (
  `catalog_code` varchar(4) NOT NULL,
  `description` longtext,
  `imo_start` date DEFAULT NULL,
  `imo_stop` date DEFAULT NULL,
  PRIMARY KEY (`catalog_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shower_info`
--

DROP TABLE IF EXISTS `shower_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shower_info` (
  `catalog_code` varchar(4) NOT NULL,
  `shower_code` varchar(255) NOT NULL,
  `activity` varchar(255) NOT NULL,
  `legacy_code` longtext,
  `legacy_name` longtext,
  `date_begin` date DEFAULT NULL,
  `date_end` date DEFAULT NULL,
  `date_max` date DEFAULT NULL,
  `sollon_max` decimal(20,10) DEFAULT NULL,
  `ra_max` decimal(20,10) DEFAULT NULL,
  `dec_max` decimal(20,10) DEFAULT NULL,
  `ra_drift` decimal(20,10) DEFAULT NULL,
  `dec_drift` decimal(20,10) DEFAULT NULL,
  `zhr_max` decimal(20,10) DEFAULT NULL,
  `var_flag` tinyint(4) DEFAULT NULL,
  `v_g` decimal(20,10) DEFAULT NULL,
  `v_inf` decimal(20,10) DEFAULT NULL,
  `mdi` decimal(20,10) DEFAULT NULL,
  `dfp` decimal(20,10) DEFAULT NULL,
  `dt` decimal(20,10) DEFAULT NULL,
  `comments` longtext,
  PRIMARY KEY (`catalog_code`,`shower_code`,`activity`),
  KEY `shower_info_shower_code_fkey` (`shower_code`),
  CONSTRAINT `shower_info_catalog_code_fkey` FOREIGN KEY (`catalog_code`) REFERENCES `shower_catalog` (`catalog_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `shower_info_shower_code_fkey` FOREIGN KEY (`shower_code`) REFERENCES `shower` (`shower_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `shower_radiant`
--

DROP TABLE IF EXISTS `shower_radiant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shower_radiant` (
  `catalog_code` varchar(4) NOT NULL,
  `shower_code` varchar(255) NOT NULL,
  `sollon` decimal(30,15) NOT NULL,
  `radiant_ra` decimal(20,10) NOT NULL,
  `radiant_dec` decimal(20,10) NOT NULL,
  PRIMARY KEY (`catalog_code`,`shower_code`,`sollon`),
  KEY `shower_radiant_shower_code_fkey` (`shower_code`),
  CONSTRAINT `shower_radiant_catalog_code_fkey` FOREIGN KEY (`catalog_code`) REFERENCES `shower_catalog` (`catalog_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `shower_radiant_shower_code_fkey` FOREIGN KEY (`shower_code`) REFERENCES `shower` (`shower_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_magnitude_bin`
--

DROP TABLE IF EXISTS `vis_magnitude_bin`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_magnitude_bin` (
  `period_code` varchar(255) NOT NULL,
  `magnitude` smallint(6) NOT NULL,
  `number` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`period_code`,`magnitude`),
  CONSTRAINT `vis_magnitude_bin_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `vis_magnitude_period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_magnitude_period`
--

DROP TABLE IF EXISTS `vis_magnitude_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_magnitude_period` (
  `period_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `shower_code` varchar(255) DEFAULT NULL,
  `start` datetime(3) DEFAULT NULL,
  `stop` datetime(3) DEFAULT NULL,
  `lm` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`period_code`),
  KEY `vis_magnitude_period_entry_code_fkey` (`entry_code`),
  KEY `vis_magnitude_period_shower_code_fkey` (`shower_code`),
  CONSTRAINT `vis_magnitude_period_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `vis_session` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vis_magnitude_period_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vis_magnitude_period_shower_code_fkey` FOREIGN KEY (`shower_code`) REFERENCES `shower` (`shower_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_rate_period`
--

DROP TABLE IF EXISTS `vis_rate_period`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_rate_period` (
  `period_code` varchar(255) NOT NULL,
  `entry_code` varchar(255) NOT NULL,
  `start` datetime(3) DEFAULT NULL,
  `stop` datetime(3) DEFAULT NULL,
  `fov_ra` decimal(20,10) DEFAULT NULL,
  `fov_dec` decimal(20,10) DEFAULT NULL,
  `teff` decimal(20,10) DEFAULT NULL,
  `fov_obstruction` decimal(20,10) DEFAULT NULL,
  `lm` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`period_code`),
  KEY `vis_rate_period_entry_code_fkey` (`entry_code`),
  CONSTRAINT `vis_rate_period_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `vis_session` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vis_rate_period_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_rate_shower`
--

DROP TABLE IF EXISTS `vis_rate_shower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_rate_shower` (
  `period_code` varchar(255) NOT NULL,
  `shower_code` varchar(4) NOT NULL,
  `method` longtext,
  `number` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`period_code`,`shower_code`),
  CONSTRAINT `vis_rate_shower_period_code_fkey` FOREIGN KEY (`period_code`) REFERENCES `vis_rate_period` (`period_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_session`
--

DROP TABLE IF EXISTS `vis_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_session` (
  `entry_code` varchar(255) NOT NULL,
  `observer_code` varchar(255) DEFAULT NULL,
  `location_code` varchar(255) DEFAULT NULL,
  `timezone_local` longtext,
  `copy_email` longtext,
  `comments` longtext,
  PRIMARY KEY (`entry_code`),
  KEY `vis_session_location_code_fkey` (`location_code`),
  KEY `vis_session_observer_code_fkey` (`observer_code`),
  CONSTRAINT `vis_session_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `entry` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `vis_session_location_code_fkey` FOREIGN KEY (`location_code`) REFERENCES `location` (`location_code`) ON DELETE NO ACTION ON UPDATE CASCADE,
  CONSTRAINT `vis_session_observer_code_fkey` FOREIGN KEY (`observer_code`) REFERENCES `observer` (`observer_code`) ON DELETE NO ACTION ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_session_shower`
--

DROP TABLE IF EXISTS `vis_session_shower`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_session_shower` (
  `entry_code` varchar(255) NOT NULL,
  `shower_code` varchar(4) NOT NULL,
  `nr` smallint(6) DEFAULT NULL,
  `catalog_ra` decimal(20,10) DEFAULT NULL,
  `catalog_dec` decimal(20,10) DEFAULT NULL,
  PRIMARY KEY (`entry_code`,`shower_code`),
  CONSTRAINT `vis_session_shower_entry_code_fkey` FOREIGN KEY (`entry_code`) REFERENCES `vis_session` (`entry_code`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `vis_temp`
--

DROP TABLE IF EXISTS `vis_temp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `vis_temp` (
  `reporter_code` varchar(255) NOT NULL,
  `form_data` longtext,
  `time_created` datetime DEFAULT NULL,
  PRIMARY KEY (`reporter_code`)
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

-- Dump completed on 2016-06-22  9:25:53
