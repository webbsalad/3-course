-- +goose Up
-- +goose StatementBegin
CREATE TABLE user_info
(
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    passhash VARCHAR(200) NOT NULL,
    spendings FLOAT DEFAULT 0,
    level_id INT REFERENCES bonus_levels(id)
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE user_info;
-- +goose StatementEnd
