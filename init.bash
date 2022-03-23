


echo "Init virtual environment..."
if [ ! -d "venv" ]
then
   echo "venv does not exist => create it"
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
else
   source venv/bin/activate
fi



export PYTHONPATH="$(pwd)"