## Custom chatbot using Langchain:
### Extract data from https://brainlox.com/courses/category/technical using URL loaders from Langchain
- Extracted all sub links (only courses) from the root link
- Used ```UnstructuredURLLoader``` to obtain the data from the URLs
- Split the data into chunks

### Cerate embeddings and store it in a vector-store
- Used ```sentence-transformers``` (size = 384) and stored the embeddings in ```pinecone``` vectorDB (```/url_extract_upload_data.py```)

### Create a FLASK RESTFUL API to handle the conversation
- Used llama2 LLM and Flask API for the Q&A (google colab | GPU ```/langchain-llama2-pinecone-qa```)
- Tested in Postman software whose screenshots are stored in ```/demo-screenshots``` directory