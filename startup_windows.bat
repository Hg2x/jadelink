call conda activate jadelink
start cmd /K "cd C:\Projects\jadelink && uvicorn main:app --reload"

cd "C:\Projects\jadedoor"
npm start
