Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
python -m "venv" env
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt