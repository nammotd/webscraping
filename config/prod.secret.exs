use Mix.Config

# In this file, we keep production configuration that
# you likely want to automate and keep it away from
# your version control system.
#
# You should document the content of this
# file or create a script for recreating it, since it's
# kept out of version control and might be hard to recover
# or recreate for your teammates (or you later on).
config :hello, Hello.Endpoint,
  secret_key_base: "ourmZPfCY+051MVJ/6lBl/NTO4eFQF4624U+sqc1/SxQM44BdIDOLuk1brQvFzHp"

# Configure your database
config :hello, Hello.Repo,
  adapter: Ecto.Adapters.Postgres,
  username: "postgres",
  password: "postgres",
  database: "hello_prod",
  pool_size: 20
config :hello, Hello.Endpoint, server: true
