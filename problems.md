# Current workflow
- Currently only the selected file is sent to the llm. This can be improved by also sending the files imported by the main file we are sending.
- We can also send already written test files as a blueprint
  - invoice_upload_list

# Problems with generated tests
- too much mocking (can be helpeful for isolation)
- import errors
- wrong assumptions about the imported types in the main file send (lack of context. sending imported files can help)
- some functions are misinterpreted by the llm (a better model can help)
- llm has no idea about the source code structure, a fine tuning may help here
