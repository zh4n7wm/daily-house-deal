FROM python:3.6-stretch
WORKDIR /app
ADD . /app
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
EXPOSE 5000
CMD ["python", "run.py"]
