install: 
	pip install -r requirements.txt
run: install
	python main.py
freeze:
	pip freeze > requirements.txt
streamlit:
	streamlit run main.py
	
