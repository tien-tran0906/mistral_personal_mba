install: 
	pip install -r requirements.txt
run: install
	python main.py
freeze:
	pip freeze > requirements.txt
run-streamlit:
	streamlit run app.py
remove-origin:
	git remote remove origin
add-remote:
	git remote add origin $(REPO_URL)	
	git remote -v
# make msg="mesage_here" add-all
add-all:
	git add .
	git commit -m '$(msg)'
	git push
create-env:
	conda create -n '$(name)'
remote-env:
	conda env remove -n '$(name)'