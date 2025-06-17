# Log of prompts provided

1. please implement the docs/openapi.yaml contract using the instructions provided

  - did nothing but highlight what I had done (generated stubs with pass)

1. i'd like you to implement all the stubs in the kpworld/routers directory

  - used mocks 'because no db layer'
  - server started and runs api
    - was able to GET articles and POST new article but
    - when GET articles again, my articles was not listed, only the mock

1. Asked why and it said 'only returning valid response not updating the in-memory db (dict)"

  - it offered to fix, I accepted, the resulting code didn't even run (ValidationError)

1. added some implementation guidelines, also generated but seemed sensible.

  - it seemed confused by not having a database so reverted to 'Ask' mode and told it generate a script to start a postgres container. 

1. cleared out the generated code back to empty fast API stubs and prompted (this time using Claude 3.5): 

   > Please implement the methods under kpworld/routers to provide the crud operations expected by openapi.yaml.

   - a lot of interactive prompts such as poetry install, poetry run alembic init ... 
   - stopped after implementing user and auth, offering to continue on other methods when I said so.
   - So let's pause and see how it did.
   - The server failed to start because `Depends(get_token)` was used before it was defined.
     I did note it reordering methods at one point, so perhaps this was a style based feedback that did not understand the `Depends` construct.
     However, it was a simple fix after which the app started.
   - I also noticed that the Real World `openapi.yaml` only contained the reference url so I added the local development server.
   - After that, I was able to create a new user (whilst unauthenticated, but ok, server initialisation is tricky).
     But not able to login with this user--because CORS not set up.
   - Prompted to setup CORS

     > Before implementing more routers we need to set up cors support. I have updated the copilot-instructions accordingly

     I had to set Origin to permit Swagger UI
     It still didn't work so I asked:

     > Cors requests to /api/users/login from Origin http://127.0.0.1:8000 are rejected why would this be?

     > 1. Fix parsing of "*" in CORS_METHODS and CORS_HEADERS
     > 2. Mount all routers under a separate FastAPI app with /api prefix
     > 3. Remove servers config since we're handling the /api prefix properly now

     1 & 3 were unnecessary, and IMO undesirable.

     I restored the servers and overrode the openapi.yaml to ensure we serve the actual contract not a potentially divergent one based on routers.

1. Shutdown at this point and on restarting the db is empty. Asked copilot:

   > Can you add a script to pyproject.toml and scripts.py that will initialise the database from the current alembic state

   It went further adding demo user, sample tags and a welcome article. In its comfort zone here!

   Remember to `poetry install` before this new init-db is available.

1. Login worked and provided token, so thought I'd try to update the user:

   ```
   File "/mnt/data/git/kpworld/kpworld/routers/user_and_authentication.py", line 57, in get_current_user
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tstephen/.cache/pypoetry/virtualenvs/kpworld-rB5i1SEH-py3.12/lib/python3.12/site-packages/jose/jwt.py", line 159, in decode
    payload = jws.verify(token, key, algorithms, verify=verify_signature)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/tstephen/.cache/pypoetry/virtualenvs/kpworld-rB5i1SEH-py3.12/lib/python3.12/site-packages/jose/jws.py", line 74, in verify
    header, payload, signing_input, signature = _load(token)
                                                ^^^^^^^^^^^^
  File "/home/tstephen/.cache/pypoetry/virtualenvs/kpworld-rB5i1SEH-py3.12/lib/python3.12/site-packages/jose/jws.py", line 180, in _load
    signing_input, crypto_segment = jwt.rsplit(b".", 1)
                                    ^^^^^^^^^^
  AttributeError: 'NoneType' object has no attribute 'rsplit'
  INFO:     127.0.0.1:53906 - "PUT /api/user?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZW1vQGRlbW8uY29tIiwiZXhwIjoxNzUwMTcwMzI0fQ.eT_yAqDczbuQQLAHC5BmXDGjO_SzuH-q_anBKPR8jc0 HTTP/1.1" 500 Internal Server Error
   ```

1. We're going to need some logging so I wrote some instructions and prompted:

   > please generate a logging.conf file to configure Python's built-in logging framework to log to console and file at the debug threshold for this project's code and warning for all third party code.
   > load this configuration within main.py in accordance with the copilot-instructions

   I did not specify the format of the file so it inferred ini-style from the .conf ending. No matter.

1. When all's said and done, I was not suppling the `Token ` prefix required by `openapi.yaml` but only the JWT in the authorization field. But the field should _NOT_ have been there, it should be aN Authorization header.

   So is this a fastapi generator issue or Copilot?

   Yep, copilot.

   Regenerated stubs and no Authorization parameter in sight.