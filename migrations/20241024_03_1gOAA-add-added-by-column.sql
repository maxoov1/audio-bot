-- add_added_by_column
-- depends: 20241024_02_47tCr-create-admin
ALTER TABLE audio ADD COLUMN added_by INTEGER NOT NULL DEFAULT "000000000";
