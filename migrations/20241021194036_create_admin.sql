-- +goose Up
-- +goose StatementBegin
CREATE TABLE admin (
  user_id INTEGER PRIMARY KEY
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE admin;
-- +goose StatementEnd
