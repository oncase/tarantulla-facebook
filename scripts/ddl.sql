CREATE TABLE staging.stg_facebook
(
  post_id VARCHAR(50)
, data_created TIMESTAMP
, publisher_fb VARCHAR(100)
, publisher_name VARCHAR(100)
, post_content VARCHAR(500)
, total_likes DOUBLE PRECISION
, total_shares DOUBLE PRECISION
, total_comments DOUBLE PRECISION
, engagement DOUBLE PRECISION
, likes_page DOUBLE PRECISION
)
;
