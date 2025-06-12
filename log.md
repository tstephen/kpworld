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