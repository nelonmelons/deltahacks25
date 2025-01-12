CREATE TABLE profiles (
  id uuid REFERENCES auth.users ON DELETE CASCADE,
  username text,
  points integer DEFAULT 0,
  groups text[] DEFAULT '{}',
  PRIMARY KEY (id)
);

