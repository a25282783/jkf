# jkf 
CREATE TABLE `jkf` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `url` varchar(255) DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content` text DEFAULT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `url` (`url`),
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4  

>cd dir  
>python(version<3.9) PY(version>=3.9) jkf.py [main1] [main2]  
>安裝:  
>>xampp  
>>composer  
>>git  
>>python  
>>>pymysql  
>>>requests  
>>>beautifulsoup4  


