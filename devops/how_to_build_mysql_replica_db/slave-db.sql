/* setting slave */
CHANGE MASTER TO MASTER_HOST='master', 
          MASTER_USER='user', 
          MASTER_PASSWORD='12345',
          MASTER_PORT=3306,
          MASTER_LOG_FILE='mysql-bin.000003', 
          MASTER_LOG_POS=891, 
          MASTER_CONNECT_RETRY=30;

START SLAVE;
STOP SLAVE;
RESET SLAVE;

SHOW SLAVE STATUS \G