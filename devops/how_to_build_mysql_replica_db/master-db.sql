USE test;

/* create test data */
CREATE TABLE account (
    id int,
    name varchar(255)
);

INSERT INTO account (id, name) VALUES (1, 'JIM');

/* check test data */
SELECT * FROM account;

/* let account `user` can connect from outside */
GRANT ALL PRIVILEGES ON *.* TO 'user'@'%';

/* lock tables only read  */
FLUSH TABLES WITH READ LOCK;

/* unlock tables */
UNLOCK TABLES;

/* check master status */
SHOW MASTER STATUS \G

/* check slave hosts which connect to this master */
SHOW SLAVE HOSTS;


ALTER USER 'user' IDENTIFIED WITH mysql_native_password;