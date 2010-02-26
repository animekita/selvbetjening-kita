-- MySQL dump 10.11
--
-- Host: localhost    Database: 9_vanilla
-- ------------------------------------------------------
-- Server version	5.0.45-Debian_1-log

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
-- Table structure for table `LUM_Attachment`
--

DROP TABLE IF EXISTS `LUM_Attachment`;
CREATE TABLE `LUM_Attachment` (
  `AttachmentID` int(11) NOT NULL auto_increment,
  `UserID` int(11) NOT NULL default '0',
  `DiscussionID` int(11) NOT NULL default '0',
  `CommentID` int(11) NOT NULL default '0',
  `Title` varchar(200) NOT NULL default '',
  `Description` text NOT NULL,
  `Name` varchar(200) NOT NULL default '',
  `Path` text NOT NULL,
  `Size` int(11) NOT NULL default '0',
  `MimeType` varchar(200) NOT NULL default '',
  `DateCreated` datetime NOT NULL default '0000-00-00 00:00:00',
  `DateModified` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`AttachmentID`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Table structure for table `LUM_Category`
--

DROP TABLE IF EXISTS `LUM_Category`;
CREATE TABLE `LUM_Category` (
  `CategoryID` int(2) NOT NULL auto_increment,
  `Name` varchar(100) NOT NULL default '',
  `Description` text,
  `Priority` int(11) NOT NULL default '0',
  PRIMARY KEY  (`CategoryID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_CategoryBlock`
--

DROP TABLE IF EXISTS `LUM_CategoryBlock`;
CREATE TABLE `LUM_CategoryBlock` (
  `CategoryID` int(11) NOT NULL default '0',
  `UserID` int(11) NOT NULL default '0',
  `Blocked` enum('1','0') NOT NULL default '1',
  PRIMARY KEY  (`CategoryID`,`UserID`),
  KEY `cat_block_user` (`UserID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_CategoryRoleBlock`
--

DROP TABLE IF EXISTS `LUM_CategoryRoleBlock`;
CREATE TABLE `LUM_CategoryRoleBlock` (
  `CategoryID` int(11) NOT NULL default '0',
  `RoleID` int(11) NOT NULL default '0',
  `Blocked` enum('1','0') NOT NULL default '0',
  KEY `cat_roleblock_cat` (`CategoryID`),
  KEY `cat_roleblock_role` (`RoleID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_Comment`
--

DROP TABLE IF EXISTS `LUM_Comment`;
CREATE TABLE `LUM_Comment` (
  `CommentID` int(8) NOT NULL auto_increment,
  `DiscussionID` int(8) NOT NULL default '0',
  `AuthUserID` int(10) NOT NULL default '0',
  `DateCreated` datetime default NULL,
  `EditUserID` int(10) default NULL,
  `DateEdited` datetime default NULL,
  `WhisperUserID` int(11) default NULL,
  `Body` text,
  `FormatType` varchar(20) default NULL,
  `Deleted` enum('1','0') NOT NULL default '0',
  `DateDeleted` datetime default NULL,
  `DeleteUserID` int(10) NOT NULL default '0',
  `RemoteIp` varchar(100) default '',
  PRIMARY KEY  (`CommentID`,`DiscussionID`),
  KEY `comment_user` (`AuthUserID`),
  KEY `comment_whisper` (`WhisperUserID`),
  KEY `comment_discussion` (`DiscussionID`)
) ENGINE=MyISAM AUTO_INCREMENT=1612 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_Discussion`
--

DROP TABLE IF EXISTS `LUM_Discussion`;
CREATE TABLE `LUM_Discussion` (
  `DiscussionID` int(8) NOT NULL auto_increment,
  `AuthUserID` int(10) NOT NULL default '0',
  `WhisperUserID` int(11) NOT NULL default '0',
  `FirstCommentID` int(11) NOT NULL default '0',
  `LastUserID` int(11) NOT NULL default '0',
  `Active` enum('1','0') NOT NULL default '1',
  `Closed` enum('1','0') NOT NULL default '0',
  `Sticky` enum('1','0') NOT NULL default '0',
  `Sink` enum('1','0') NOT NULL default '0',
  `Name` varchar(100) NOT NULL default '',
  `DateCreated` datetime NOT NULL default '0000-00-00 00:00:00',
  `DateLastActive` datetime NOT NULL default '0000-00-00 00:00:00',
  `CountComments` int(4) NOT NULL default '1',
  `CategoryID` int(11) default NULL,
  `WhisperToLastUserID` int(11) default NULL,
  `WhisperFromLastUserID` int(11) default NULL,
  `DateLastWhisper` datetime default NULL,
  `TotalWhisperCount` int(11) NOT NULL default '0',
  PRIMARY KEY  (`DiscussionID`),
  KEY `discussion_user` (`AuthUserID`),
  KEY `discussion_whisperuser` (`WhisperUserID`),
  KEY `discussion_first` (`FirstCommentID`),
  KEY `discussion_last` (`LastUserID`),
  KEY `discussion_category` (`CategoryID`),
  KEY `discussion_dateactive` (`DateLastActive`)
) ENGINE=MyISAM AUTO_INCREMENT=78 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_DiscussionUserWhisperFrom`
--

DROP TABLE IF EXISTS `LUM_DiscussionUserWhisperFrom`;
CREATE TABLE `LUM_DiscussionUserWhisperFrom` (
  `DiscussionID` int(11) NOT NULL default '0',
  `WhisperFromUserID` int(11) NOT NULL default '0',
  `LastUserID` int(11) NOT NULL default '0',
  `CountWhispers` int(11) NOT NULL default '0',
  `DateLastActive` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`DiscussionID`,`WhisperFromUserID`),
  KEY `discussion_user_whisper_lastuser` (`LastUserID`),
  KEY `discussion_user_whisper_lastactive` (`DateLastActive`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_DiscussionUserWhisperTo`
--

DROP TABLE IF EXISTS `LUM_DiscussionUserWhisperTo`;
CREATE TABLE `LUM_DiscussionUserWhisperTo` (
  `DiscussionID` int(11) NOT NULL default '0',
  `WhisperToUserID` int(11) NOT NULL default '0',
  `LastUserID` int(11) NOT NULL default '0',
  `CountWhispers` int(11) NOT NULL default '0',
  `DateLastActive` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`DiscussionID`,`WhisperToUserID`),
  KEY `discussion_user_whisperto_lastuser` (`LastUserID`),
  KEY `discussion_user_whisperto_lastactive` (`DateLastActive`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_IpHistory`
--

DROP TABLE IF EXISTS `LUM_IpHistory`;
CREATE TABLE `LUM_IpHistory` (
  `IpHistoryID` int(11) NOT NULL auto_increment,
  `RemoteIp` varchar(30) NOT NULL default '',
  `UserID` int(11) NOT NULL default '0',
  `DateLogged` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`IpHistoryID`)
) ENGINE=MyISAM AUTO_INCREMENT=17329 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_Messages`
--

DROP TABLE IF EXISTS `LUM_Messages`;
CREATE TABLE `LUM_Messages` (
  `MessageID` bigint(20) NOT NULL auto_increment,
  `SenderID` int(11) NOT NULL default '0',
  `RecieverID` int(11) NOT NULL default '0',
  `Message` text NOT NULL,
  `DateCreated` date NOT NULL default '0000-00-00',
  `Hidden` enum('0','1') NOT NULL default '0',
  `Visited` enum('0','1') NOT NULL default '0',
  PRIMARY KEY  (`MessageID`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8 COMMENT='created by UserMessages Extension';

--
-- Table structure for table `LUM_Role`
--

DROP TABLE IF EXISTS `LUM_Role`;
CREATE TABLE `LUM_Role` (
  `RoleID` int(2) NOT NULL auto_increment,
  `Name` varchar(100) NOT NULL default '',
  `Icon` varchar(155) NOT NULL default '',
  `Description` varchar(200) NOT NULL default '',
  `Active` enum('1','0') NOT NULL default '1',
  `PERMISSION_SIGN_IN` enum('1','0') NOT NULL default '0',
  `PERMISSION_HTML_ALLOWED` enum('0','1') NOT NULL default '0',
  `PERMISSION_RECEIVE_APPLICATION_NOTIFICATION` enum('1','0') NOT NULL default '0',
  `Permissions` text,
  `Priority` int(11) NOT NULL default '0',
  `UnAuthenticated` enum('1','0') NOT NULL default '0',
  PRIMARY KEY  (`RoleID`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_Style`
--

DROP TABLE IF EXISTS `LUM_Style`;
CREATE TABLE `LUM_Style` (
  `StyleID` int(3) NOT NULL auto_increment,
  `AuthUserID` int(11) NOT NULL default '0',
  `Name` varchar(50) NOT NULL default '',
  `Url` varchar(255) NOT NULL default '',
  `PreviewImage` varchar(20) NOT NULL default '',
  PRIMARY KEY  (`StyleID`)
) ENGINE=MyISAM AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_User`
--

DROP TABLE IF EXISTS `LUM_User`;
CREATE TABLE `LUM_User` (
  `UserID` int(10) NOT NULL auto_increment,
  `RoleID` int(2) NOT NULL default '0',
  `StyleID` int(3) NOT NULL default '1',
  `CustomStyle` varchar(255) default NULL,
  `FirstName` varchar(50) NOT NULL default '',
  `LastName` varchar(50) NOT NULL default '',
  `Name` varchar(20) NOT NULL default '',
  `Password` varchar(32) default NULL,
  `VerificationKey` varchar(50) NOT NULL default '',
  `EmailVerificationKey` varchar(50) default NULL,
  `Email` varchar(200) NOT NULL default '',
  `UtilizeEmail` enum('1','0') NOT NULL default '0',
  `ShowName` enum('1','0') NOT NULL default '1',
  `Icon` varchar(255) default NULL,
  `Picture` varchar(255) default NULL,
  `Attributes` text,
  `CountVisit` int(8) NOT NULL default '0',
  `CountDiscussions` int(8) NOT NULL default '0',
  `CountComments` int(8) NOT NULL default '0',
  `DateFirstVisit` datetime NOT NULL default '0000-00-00 00:00:00',
  `DateLastActive` datetime NOT NULL default '0000-00-00 00:00:00',
  `RemoteIp` varchar(100) NOT NULL default '',
  `LastDiscussionPost` datetime default NULL,
  `DiscussionSpamCheck` int(11) NOT NULL default '0',
  `LastCommentPost` datetime default NULL,
  `CommentSpamCheck` int(11) NOT NULL default '0',
  `UserBlocksCategories` enum('1','0') NOT NULL default '0',
  `DefaultFormatType` varchar(20) default NULL,
  `Discovery` text,
  `Preferences` text,
  `SendNewApplicantNotifications` enum('1','0') NOT NULL default '0',
  PRIMARY KEY  (`UserID`),
  KEY `user_role` (`RoleID`),
  KEY `user_style` (`StyleID`),
  KEY `user_name` (`Name`)
) ENGINE=MyISAM AUTO_INCREMENT=59 DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_UserBookmark`
--

DROP TABLE IF EXISTS `LUM_UserBookmark`;
CREATE TABLE `LUM_UserBookmark` (
  `UserID` int(10) NOT NULL default '0',
  `DiscussionID` int(8) NOT NULL default '0',
  PRIMARY KEY  (`UserID`,`DiscussionID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_UserDiscussionWatch`
--

DROP TABLE IF EXISTS `LUM_UserDiscussionWatch`;
CREATE TABLE `LUM_UserDiscussionWatch` (
  `UserID` int(10) NOT NULL default '0',
  `DiscussionID` int(8) NOT NULL default '0',
  `CountComments` int(11) NOT NULL default '0',
  `LastViewed` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`UserID`,`DiscussionID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_UserRoleHistory`
--

DROP TABLE IF EXISTS `LUM_UserRoleHistory`;
CREATE TABLE `LUM_UserRoleHistory` (
  `UserID` int(10) NOT NULL default '0',
  `RoleID` int(2) NOT NULL default '0',
  `Date` datetime NOT NULL default '0000-00-00 00:00:00',
  `AdminUserID` int(10) NOT NULL default '0',
  `Notes` varchar(200) default NULL,
  `RemoteIp` varchar(100) default NULL,
  KEY `UserID` (`UserID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_VoteOnComment`
--

DROP TABLE IF EXISTS `LUM_VoteOnComment`;
CREATE TABLE `LUM_VoteOnComment` (
  `VoteID` int(11) NOT NULL auto_increment,
  `CommentID` int(11) NOT NULL default '0',
  `UserID` int(11) NOT NULL default '0',
  `Vote` int(11) NOT NULL default '0',
  `DateCreated` datetime NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`VoteID`),
  KEY `comment` (`CommentID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Table structure for table `LUM_VoteOnDiscussion`
--

DROP TABLE IF EXISTS `LUM_VoteOnDiscussion`;
CREATE TABLE `LUM_VoteOnDiscussion` (
  `DiscussionID` int(11) NOT NULL default '0',
  `CanVote` enum('1','0') NOT NULL default '1',
  PRIMARY KEY  (`DiscussionID`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2007-12-01 22:07:47
