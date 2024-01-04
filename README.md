## Step 0:
Enable virtual environment (conda or env)

## Step 1:
pip install -r requirements.txt

## Step 2:
ollama pull mistral

# Step 3:
mkdir source_documents
then add your own document in this folder

# Step 4:
python ingest.py

# Step 5:
streamlit run main.py


