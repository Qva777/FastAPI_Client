<h1>📍How to install: </h1>

<h3>Automatic command execution for the first run</h3>
<ul>
  <li>🔧for Windows:     <b>first_start.bat</b></li>
  <li>⚙for Linux/MacOS: <b>first_start.sh</b></li>
</ul>
<h3>Manual start⬇</h3>
<h4>1 - Connect venv:</h4> 
<i>python -m venv venv</i>
<h4>2 - Activate it:</h4> 
<ul>
  <li>cd venv</li>
  <li>cd Scripts</li>
  <li>activate</li>
</ul>
<h4>3 - In the Console, go to the root folder:</h4>
<i>cd ../..</i>
<h4>4 - Install libraries:</h4>
<i>pip install -r requirements.txt</i>
<h4>5 - In root folder create file ".evn"</h4>
<i>echo SECRET_KEY=YOUR_SECRET_KEY > .env</i>
<h4>6 - Run server:</h4>
<i>uvicorn main:app --reload</i> 

<h1>📮How to connect Postman: </h1>
<h4>1 - Import Postman_Client folder into Postman</h4> 
<h4>2 - The environment settings are called FastAPI User Data</h4>
<h4>3 - The FastAPI collection contains requests</h4>

<h1>🐳How to connect Docker:</h1>
<h4>1 - Creat image:</h4>
<i>docker build --tag fastapi .</i>
<h4>2 - Look images:</h4>
<i>docker images</i>
<h4>3 - Run Container</h4>
<i>docker run -d --name mycont -p 8000:8000 fastapi</i>