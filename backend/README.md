# Backend

## How to run locally
1. Install just command runner -> [just github](https://github.com/casey/just).
2. Make sure you have `python 3.11.4` set as default or just for the current terminal process.
3. Fill `.env` file with these values:
    ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   POSTGRES_HOST=db
   POSTGRES_PORT=5432
   POSTGRES_DB=db
   ```
4. Make sure docker is running.
5. Run `just setup` in backend directory.