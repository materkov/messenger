DROP SCHEMA IF EXISTS messenger;
CREATE SCHEMA messenger;

CREATE TABLE messenger.conversations (
  id INT NOT NULL AUTO_INCREMENT,
  title VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE messenger.conversations_users (
  id INT(11) NOT NULL AUTO_INCREMENT,
  conversation_id INT(11) NOT NULL,
  last_msg_id INT(11) NOT NULL,
  user_id INT(11) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE messenger.users (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  login VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE messenger.messages (
  id INT NOT NULL AUTO_INCREMENT,
  conversation_id INT(11) NOT NULL,
  user_id INT(11) NOT NULL,
  body TEXT NOT NULL,
  type TINYINT NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO messenger.conversations_users(conversation_id, last_msg_id, user_id) VALUES (1, 555, 123);
INSERT INTO messenger.conversations_users(conversation_id, last_msg_id, user_id) VALUES (5, 6457475, 123);

INSERT INTO messenger.conversations(id, title) VALUES (1, 'title1');
INSERT INTO messenger.conversations(id, title) VALUES (2, 'title2');
INSERT INTO messenger.conversations(id, title) VALUES (5, 'title5');

INSERT INTO messenger.users(id, name, login, password) VALUES (1, 'user1', '', '');
INSERT INTO messenger.users(id, name, login, password) VALUES (123, 'user123', '12345', '');

INSERT INTO messenger.messages(id, conversation_id, user_id, body, type) VALUES (555, 1, 123, 'msfsfsg', 1);
INSERT INTO messenger.messages(id, conversation_id, user_id, body, type) VALUES (6457475, 5, 123, '1111111', 1);
