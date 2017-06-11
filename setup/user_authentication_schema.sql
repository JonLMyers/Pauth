DROP Database IF NOT EXISTS user_authentication;
CREATE SCHEMA IF NOT EXISTS `user_authentication` DEFAULT CHARACTER SET utf8;
USE `user_authentication`;

CREATE TABLE IF NOT EXISTS users(
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password_hash VARCHAR(256) NOT NULL,
    session_token VARCHAR(128)
);
