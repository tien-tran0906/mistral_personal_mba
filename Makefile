install: 
	pip install -r requirements.txt
run: install
	python main.py
freeze:
	pip freeze > requirements.txt
streamlit:
	streamlit run main.py
remove-origin:
	git remote remove origin
add-remote:
	git remote add origin $(REPO_URL)	
	git remote -v
add-all:
	git add .	
push:
	git push
	
