-- +goose Up
-- +goose StatementBegin
CREATE TABLE bonus_levels
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    min_spendings FLOAT NOT NULL,
    cashback_percentage FLOAT NOT NULL
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE bonus_levels;
-- +goose StatementEnd
