-- +goose Up
-- +goose StatementBegin
CREATE TABLE audio (
  generated_id TEXT PRIMARY KEY,
  telegram_file_id TEXT NOT NULL
);
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE audio;
-- +goose StatementEnd
