-- phpMyAdmin SQL Dump
-- version 3.4.4
-- http://www.phpmyadmin.net
--
-- Хост: localhost
-- Время создания: Янв 04 2012 г., 15:53
-- Версия сервера: 5.0.51
-- Версия PHP: 5.2.4-2ubuntu5.18

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- База данных: `it`
--

-- --------------------------------------------------------

--
-- Структура таблицы `assetcategory`
--

CREATE TABLE IF NOT EXISTS `assetcategory` (
  `AssetCategoryNumber` int(10) unsigned NOT NULL auto_increment,
  `Name` varchar(30) default NULL,
  PRIMARY KEY  (`AssetCategoryNumber`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=49 ;

--
-- Дамп данных таблицы `assetcategory`
--

INSERT INTO `assetcategory` (`AssetCategoryNumber`, `Name`) VALUES
(0, 'Принтер'),
(1, 'Картридж'),
(2, 'Блок питания'),
(3, 'Материнка AM3'),
(4, 'CPU'),
(5, 'Корпус'),
(6, 'Телефонная розетка'),
(7, 'Ремонт оргтехники'),
(8, 'DDR3'),
(9, 'Вентилятор'),
(10, 'Розетка Ethernet'),
(11, 'HDD IDE'),
(12, 'Гарнитура'),
(13, 'Коврик для мышки'),
(14, 'Колонки'),
(15, 'Мышка USB'),
(16, 'HDD SATA'),
(17, 'Телефон DECT'),
(18, 'Ремонт телефония'),
(19, 'Термопаста'),
(20, 'Прочее'),
(21, 'DDR'),
(22, 'Телефонный провод'),
(23, 'Свич'),
(24, 'Корпус'),
(25, 'Материнка 478'),
(26, 'Flash`ка'),
(27, 'Батарейка ААА'),
(28, 'Сканер А4'),
(30, 'Доставка'),
(31, 'Внешний флопповод'),
(32, 'Телефон дальнобойный'),
(33, ''),
(34, 'Батарейка CR2025'),
(35, 'Батарейка С'),
(36, 'Ремонт UPS'),
(37, 'Замена батарей UPS'),
(38, 'Ноубук'),
(39, 'UPS'),
(40, 'Телефон обычный'),
(41, 'UPS'),
(42, 'Монитор ЖК'),
(43, 'Барабан принтера'),
(44, 'USB удлинитель'),
(45, 'Приход по заявке'),
(46, 'Модем GSM'),
(47, 'Программа'),
(48, 'CR-ROM IDE');

-- --------------------------------------------------------

--
-- Структура таблицы `assets`
--

CREATE TABLE IF NOT EXISTS `assets` (
  `AssetNumber` int(10) unsigned NOT NULL auto_increment,
  `AssetCategoryNumber` int(10) unsigned default NULL,
  `Model` varchar(50) default NULL,
  `SerialNumber` varchar(20) default NULL,
  `StatusCode` int(10) unsigned default NULL,
  `Place` varchar(100) default NULL,
  `PCName` varchar(20) default NULL,
  `ByeDate` date default NULL,
  `Garanty` int(10) unsigned default NULL,
  `Notes` mediumtext,
  `Price` decimal(10,0) default NULL,
  `DistributorName` varchar(30) default NULL,
  `BillNumber` varchar(20) default NULL,
  `BillCashlessNumber` int(10) unsigned default NULL,
  `MethodOfPayment` enum('C','NC') default NULL,
  `GarantyNumber` int(10) unsigned default NULL,
  `CancellationDate` date default NULL,
  PRIMARY KEY  (`AssetNumber`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=327 ;

--
-- Дамп данных таблицы `assets`
--



-- --------------------------------------------------------

--
-- Структура таблицы `billcashless`
--

CREATE TABLE IF NOT EXISTS `billcashless` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `BilNumber` varchar(20) default NULL,
  `DistributorName` varchar(30) default NULL,
  `BillDate` date NOT NULL,
  `Peselev` tinyint(1) default NULL,
  `Motya` tinyint(1) default NULL,
  `Boroda` tinyint(1) default NULL,
  `Oplata` tinyint(1) default NULL,
  `Documents` tinyint(1) default NULL,
  `DocReturnDate` date default NULL,
  `DeliveryDate` date default NULL,
  PRIMARY KEY  (`ID`),
  KEY `fk_DistributorName` (`DistributorName`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- Дамп данных таблицы `billcashless`
--


-- --------------------------------------------------------

--
-- Структура таблицы `cartridge_cartridge_type`
--

CREATE TABLE IF NOT EXISTS `cartridge_cartridge_type` (
  `Model` varchar(20) NOT NULL default '',
  `CartridgeType` varchar(20) default NULL,
  `Color` enum('K','Y','M','C') default NULL,
  PRIMARY KEY  (`Model`),
  KEY `fk_cartrige_type` (`CartridgeType`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cartridge_cartridge_type`
--

INSERT INTO `cartridge_cartridge_type` (`Model`, `CartridgeType`, `Color`) VALUES
('05X', '05X', 'K'),
('106R01412', 'Ph3300', 'K'),
('12A', '12A', 'K'),
('15A', '15A', 'K'),
('1710567-002', 'PP1380', 'K'),
('285A', '285A', 'K'),
('920XL-C', '920-C', 'C'),
('920XL-K', '920-K', 'K'),
('920XL-M', '920-M', 'M'),
('920XL-Y', '920-Y', 'Y'),
('A0FP021', 'PP5650', 'K'),
('A0FP022', 'PP5650', 'K'),
('A0V301H', '1600W-K', 'K'),
('A0V305H', '1600W-Y', 'Y'),
('A0V306H', '1600W-Y', 'Y'),
('A0V30AH', '1600W-M', 'M'),
('A0V30CH', '1600W-M', 'M'),
('A0V30GH', '1600W-C', 'C'),
('A0V30HH', '1600W-C', 'C'),
('A1UC050', 'BH164A', 'K'),
('c4096a', '96A', 'K'),
('CE310A', 'CP1025-K', 'K'),
('CE311A', 'CP1025-C', 'C'),
('CE312A', 'CP1025-Y', 'Y'),
('CE313A', 'CP1025-M', 'M'),
('CT-12A', '12A', 'K'),
('CT-15A', '15A', 'K'),
('CT-285A', '285A', 'K'),
('CT-96A', '96A', 'K'),
('CT-CE310A', 'CP1025-K', 'K'),
('CT-CE311A', 'CP1025-C', 'C'),
('CT-CE312A', 'CP1025-Y', 'Y'),
('CT-CE313A', 'CP1025-M', 'M'),
('1710566-002', 'PP1380', 'K'),
('CT-05X', '05X', 'K');

-- --------------------------------------------------------

--
-- Структура таблицы `cartridge_model`
--

CREATE TABLE IF NOT EXISTS `cartridge_model` (
  `Model` varchar(20) NOT NULL default '',
  `CartridgeCapacity` int(10) unsigned default NULL,
  `Original` tinyint(1) default NULL,
  PRIMARY KEY  (`Model`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `cartridge_model`
--

INSERT INTO `cartridge_model` (`Model`, `CartridgeCapacity`, `Original`) VALUES
('05X', 6000, 1),
('106R01412', 0, 1),
('12A', 0, 1),
('15A', 0, 1),
('1710567-002', 6000, 1),
('285A', 0, 1),
('920XL-C', 700, 1),
('920XL-K', 1200, 1),
('920XL-M', 700, 1),
('920XL-Y', 700, 1),
('A0FP021', 11000, 1),
('A0FP022', 19000, 1),
('A0V301H', 2500, 1),
('A0V305H', 1500, 1),
('A0V306H', 2500, 1),
('A0V30AH', 0, 1),
('A0V30CH', 2500, 1),
('A0V30GH', 0, 1),
('A0V30HH', 2500, 1),
('A1UC050', 0, 1),
('c4096a', 0, 1),
('CE285A', 1600, 1),
('CE310A', 1200, 1),
('CE311A', 1000, 1),
('CE312A', 1000, 1),
('CE313A', 1000, 1),
('CT-12A', 0, 0),
('CT-15A', 0, 0),
('CT-285A', 0, 0),
('CT-96A', 0, 0),
('CT-CE310A', 0, 0),
('CT-CE311A', 0, 0),
('CT-CE312A', 0, 0),
('CT-CE313A', 0, 0);

-- --------------------------------------------------------

--
-- Структура таблицы `departments`
--

CREATE TABLE IF NOT EXISTS `departments` (
  `Department` varchar(20) NOT NULL default '',
  PRIMARY KEY  (`Department`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `departments`
--

INSERT INTO `departments` (`Department`) VALUES
('Списание');

-- --------------------------------------------------------

--
-- Структура таблицы `distributors`
--

CREATE TABLE IF NOT EXISTS `distributors` (
  `DistributorName` varchar(30) NOT NULL default '',
  `ContactPerson` varchar(50) default NULL,
  `ContactPersonJob` varchar(50) default NULL,
  `Email` varchar(30) default NULL,
  `Tel` varchar(20) default NULL,
  `Fax` varchar(20) default NULL,
  `Adress` varchar(70) default NULL,
  PRIMARY KEY  (`DistributorName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `distributors`
--


-- --------------------------------------------------------

--
-- Структура таблицы `pcnames`
--

CREATE TABLE IF NOT EXISTS `pcnames` (
  `PCName` varchar(20) NOT NULL default '',
  `Notes` mediumtext,
  `IP` varchar(15) default NULL,
  PRIMARY KEY  (`PCName`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `pcnames`
--


-- --------------------------------------------------------

--
-- Структура таблицы `pcsoft`
--

CREATE TABLE IF NOT EXISTS `pcsoft` (
  `PCName` varchar(20) NOT NULL default '',
  `Programm` varchar(30) NOT NULL default '',
  `ProgrammKey` varchar(30) default NULL,
  `Notes` text,
  `Verified` tinyint(1) default NULL,
  `Free` tinyint(1) default NULL,
  `NonLegal` tinyint(1) default NULL,
  PRIMARY KEY  (`PCName`,`Programm`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Структура таблицы `printer_cartridge`
--

CREATE TABLE IF NOT EXISTS `printer_cartridge` (
  `Printer` int(10) unsigned default NULL,
  `Cartridge` int(10) unsigned NOT NULL default '0',
  `put` datetime default NULL,
  PRIMARY KEY  (`Cartridge`),
  KEY `fk_printer` (`Printer`),
  KEY `Cartridge` (`Cartridge`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `printer_cartridge`
--


-- --------------------------------------------------------

--
-- Структура таблицы `printer_cartridge_type`
--

CREATE TABLE IF NOT EXISTS `printer_cartridge_type` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Model` varchar(20) default NULL,
  `CartridgeType` varchar(20) default NULL,
  `Color` tinyint(1) default NULL,
  PRIMARY KEY  (`ID`),
  KEY `fk_model` (`Model`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=39 ;

--
-- Дамп данных таблицы `printer_cartridge_type`
--

INSERT INTO `printer_cartridge_type` (`ID`, `Model`, `CartridgeType`, `Color`) VALUES
(1, 'KM 1600W', '1600W-K', 1),
(2, 'KM 1600W', '1600W-C', 1),
(3, 'KM 1600W', '1600W-Y', 1),
(4, 'KM 1600W', '1600W-M', 1),
(9, 'HP LJ 1020', '12A', 0),
(10, 'HP LJ CP1025', 'CP1025-K', 1),
(11, 'HP LJ CP1025', 'CP1025-Y', 1),
(12, 'HP LJ CP1025', 'CP1025-C', 1),
(13, 'HP LJ CP1025', 'CP1025-M', 1),
(14, 'HP LJ 1200', '15A', 0),
(15, 'KM 1380', 'PP1380', 0),
(18, 'HP P1102', '285A', 0),
(19, 'KM 164A', 'BH164A', 0),
(21, 'HP LJ 2100', '96A', 0),
(22, 'Phaser 3300MFP', 'Ph3300', 0),
(27, 'HP LJ 1000', '15A', 0),
(29, 'HP OJ 7000', '920-Y', 1),
(30, 'HP OJ 7000', '920-M', 1),
(31, 'HP OJ 7000', '920-C', 1),
(32, 'HP OJ 7000', '920-K', 1),
(33, 'HP LJ Pro M1132', '285A', 0),
(36, 'HP LaserJet P2055d', '05X', 0),
(38, 'KM PP 5650', 'PP5650', 0);

-- --------------------------------------------------------

--
-- Структура таблицы `printer_department`
--

CREATE TABLE IF NOT EXISTS `printer_department` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `Printer` int(10) unsigned default NULL,
  `Department` varchar(20) default NULL,
  `puted` datetime NOT NULL,
  `removed` datetime default NULL,
  PRIMARY KEY  (`ID`),
  KEY `fk_printer` (`Printer`),
  KEY `fk_dep` (`Department`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=30 ;

--
-- Дамп данных таблицы `printer_department`
--


-- --------------------------------------------------------

--
-- Структура таблицы `repairing`
--

CREATE TABLE IF NOT EXISTS `repairing` (
  `ID` int(10) unsigned NOT NULL auto_increment,
  `AssetNumber` int(10) unsigned default NULL,
  `Breakdown` mediumtext,
  `DistributorName` varchar(30) default NULL,
  `StartDate` date default NULL,
  `EndDate` date default NULL,
  `Garanty` int(10) unsigned default NULL,
  `Price` decimal(10,0) unsigned default NULL,
  `BillDate` date default NULL,
  `GarantyNumber` int(10) unsigned default NULL,
  `BillNumber` varchar(20) default NULL,
  `MethodOfPayment` enum('C','NC') default NULL,
  PRIMARY KEY  (`ID`),
  KEY `fk_AssetNumber` (`AssetNumber`),
  KEY `fk_DistributorName` (`DistributorName`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=15 ;

--
-- Дамп данных таблицы `repairing`
--


-- --------------------------------------------------------

--
-- Структура таблицы `statuses`
--

CREATE TABLE IF NOT EXISTS `statuses` (
  `StatusCode` int(10) unsigned NOT NULL auto_increment,
  `StatusName` varchar(20) default NULL,
  PRIMARY KEY  (`StatusCode`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=7 ;

--
-- Дамп данных таблицы `statuses`
--

INSERT INTO `statuses` (`StatusCode`, `StatusName`) VALUES
(0, 'Новое'),
(1, 'Б/У'),
(2, 'Глючное'),
(3, 'Не рабочее'),
(4, 'Возврат по гарантии'),
(5, 'Списано'),
(6, 'Заказано');

-- --------------------------------------------------------

--
-- Структура таблицы `tokens`
--

CREATE TABLE IF NOT EXISTS `tokens` (
  `token` varchar(32) NOT NULL,
  `login` varchar(20) NOT NULL,
  `start` timestamp NOT NULL default CURRENT_TIMESTAMP,
  `end` timestamp NOT NULL default '0000-00-00 00:00:00',
  PRIMARY KEY  (`token`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `tokens`
--


-- --------------------------------------------------------

--
-- Структура таблицы `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `login` varchar(20) NOT NULL default '',
  `password` varchar(32) NOT NULL default '',
  `email` varchar(30) default NULL,
  PRIMARY KEY  (`login`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`login`, `password`, `email`) VALUES
('ishayahu', '912ec803b2ce49e4a541068d495ab570', 'alexgor1@rambler.ru');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
