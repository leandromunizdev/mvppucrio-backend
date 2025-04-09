FROM python:3.9-slim

# Diretório no container
WORKDIR /app

# Copia o arquivo de requirements para o container
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código para o container
COPY . .

# Define variável de ambiente do Flask (caso sua aplicação precise)
# Arquivo principal da api
ENV FLASK_APP=app.py

# Porta em que a aplicação irá rodar
EXPOSE 5000

# Inicia a aplicação
CMD ["flask", "run", "--host=0.0.0.0"]
