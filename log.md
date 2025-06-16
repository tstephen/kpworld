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
   - stopped after implementing user and auth, let's see how it did