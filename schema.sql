DROP TABLE IF EXISTS `user`; --`user`という名前のテーブルが既に存在していたら削除。（コンフリクトを防ぐための処理）
CREATE TABLE `user` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `leader_card_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token` (`token`)
);

-------------------------------- ↑オリジナル↑ --------------------------------  
-------------------------------- ↓ 吉原追記 ↓ --------------------------------  


INSERT INTO `user` SET `name`="ほのか", `token`="RKMxBGuK", `leader_card_id`=42;
INSERT INTO `user` SET `name`="えり",   `token`="wzehoctC", `leader_card_id`=43;
INSERT INTO `user` SET `name`="ことり", `token`="wdUZxFXT", `leader_card_id`=44;

-- INSERT INTO `user` SET `name`="うみ", `token`="QwerAsdf", `leader_card_id`=45;
-- AUTO_INCREMENT　があるから、idは勝手に割り振られる。

SELECT `id`, `name`, `token`, `leader_card_id` FROM `user`;

-- select * from `user`;
-- SELECT * FROM `user`;
-- desc `user`;
-- SHOW CREATE TABLE `user`;
-- SELECT * FROM `user` WHERE `id`=2;
-- select * from `user` where `token`="wzehoctC";
-- 実行できたコマンドの確認用ログ

DROP TABLE IF EXISTS `room`;
CREATE TABLE `room` (
  `room_id` int,
  `live_id` int,
  `joined_user_count` int,
  `max_user_count` int
);

DROP TABLE IF EXISTS `room_member`;
CREATE TABLE `room_member` (
  `room_id` int,
  `user_id` int
);
