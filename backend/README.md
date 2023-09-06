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
   
   APP_SECRET_KEY=some-random-string
   IAM_CLIENT_ID=
   IAM_CLIENT_SECRET=
   IAM_DOMAIN=
   ```
4. For IAM data ask one of the IAM admins: @xTaube or @MD-00
5. Make sure docker is running.
6. Run `just setup` in backend directory.

## How to obtain authorization token
1. Enter `localhost:8000/api/auth` in web browser.
2. Sing up or sing in our application IAM.
3. You should be redirected to page with your token data.