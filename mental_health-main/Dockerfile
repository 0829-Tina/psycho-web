FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["bash","start.sh"]