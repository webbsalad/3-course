-- +goose Up
-- +goose StatementBegin
CREATE TABLE transactions
(
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES user_info(id),
    amount FLOAT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE transactions;
-- +goose StatementEnd
