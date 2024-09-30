use yuanyu_aigroup;

CREATE TABLE `yuanyu_activity_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL COMMENT '组名',
  `activity_id` int(10)  NOT NULL COMMENT '活动id',
  `status` tinyint(1) DEFAULT '1' COMMENT '-1=失败，0=正在处理，1=排队中，2=生成成功',
  `create_time` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3),
  `update_time` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) ON UPDATE CURRENT_TIMESTAMP(3),
  `delete_time` datetime(3) DEFAULT NULL
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 ;

