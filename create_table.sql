CREATE TABLE IF NOT EXISTS `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) NOT NULL,
  `social_id` varchar(45) NOT NULL,
  `registration_time` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `name_social_index` (`user_name`,`social_id`) USING BTREE,
  UNIQUE KEY `social_id_UNIQUE` (`social_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `beacon` (
  `beacon_id` int(11) NOT NULL AUTO_INCREMENT,
  `mac_addr` varchar(45) NOT NULL,
  `advertising_data` varchar(45) NOT NULL,
  `x` int(11) NOT NULL,
  `y` int(11) NOT NULL,
  PRIMARY KEY (`beacon_id`),
  UNIQUE KEY `mac_ad_index` (`mac_addr`,`advertising_data`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=121 DEFAULT CHARSET=utf8;