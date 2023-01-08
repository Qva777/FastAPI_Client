<h1>📍How to install: </h1>

<details><summary><h3>Automatic command execution for the first run</h3></summary><br>
<ul>
  <li>🔧for Windows:     <b>first_start.bat</b></li>
  <li>⚙for Linux/MacOS: <b>first_start.sh</b></li>
</ul>
<h3>Manual start⬇</h3>
<h4>1 - Connect venv:</h4> 
<pre>python -m venv venv</pre>
<h4>2 - Activate it:</h4> 
<pre>.\venv\Scripts\activate</pre>
<h4>3 - Install libraries:</h4>
<pre>pip install -r requirements.txt</pre>
<h4>4 - In root folder create file ".evn"</h4>
<pre>echo SECRET_KEY=YOUR_SECRET_KEY > .env</pre>
<h4>5 - Run server:</h4>
<pre>uvicorn main:app --reload</pre> 
</details>
<h1>📮How to connect Postman: </h1>
<h4>1 - Import Postman_Client folder into Postman</h4> 
<h4>2 - The environment settings are called FastAPI User Data</h4>
<h4>3 - The FastAPI collection contains requests</h4>

<h1>🐳How to connect Docker:</h1>
<h4>1 - Creat image:</h4>
<pre>docker build --tag fastapi .</pre>
<h4>2 - Look images:</h4>
<pre>docker images</pre>
<h4>3 - Run Container localhost - 127.0.0.1:8000</h4>
<pre>docker run -d --name mycontainer -p 8000:8000 fastapi</pre>
