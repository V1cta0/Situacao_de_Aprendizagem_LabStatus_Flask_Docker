# LabStatus — Respostas e roteiro de demonstração

## Comandos (Etapas A a E)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install Flask
python app.py                      # testar localhost:5000 e /api/status
python -m pip freeze > requirements.txt

docker build -t labstatus:v1 .
docker images
docker run -d --name labstatus-app -p 8080:5000 labstatus:v1
docker ps
docker logs labstatus-app          # testar localhost:8080 e /api/status
```

## Versão 2
Alterar em `app.py`: "Sistema de Impressão" -> "Servidor de Impressão" e incluir
`{"nome": "Servidor de Backup", "status": "online"}`. Depois:
```powershell
docker stop labstatus-app
docker rm labstatus-app
docker build -t labstatus:v2 .
docker run -d --name labstatus-app -p 8080:5000 labstatus:v2
```

**Questão 1 — O container em execução será atualizado automaticamente?**
Não. O container foi criado a partir da imagem labstatus:v1, que é um pacote imutável
(um "retrato") com o código copiado no momento do build (`COPY . .`). Editar os arquivos
locais não altera a imagem nem o container; ele continua rodando o código antigo.

**Questão 2 — Por que foi necessário construir uma nova imagem?**
Porque o código está dentro da imagem (copiado pelo `COPY . .`) e nesta configuração não
há volume/bind mount ligando a pasta local ao container. Para o novo código chegar ao
container é preciso refazer o build (labstatus:v2) e criar um novo container a partir dela.

## Questões de reflexão
1. **Frontend:** apresentar a interface ao usuário (HTML estrutura o conteúdo, CSS define a aparência) e exibir os serviços, seus status e o link para a API.
2. **Backend Flask:** definir as rotas (`/` e `/api/status`), manter os dados dos serviços, renderizar o template e devolver a resposta JSON.
3. **Por que testar antes da imagem:** para separar erros de código de erros de conteinerização; se algo falhar no Docker, já se sabe que a aplicação em si funciona.
4. **Dockerfile x imagem x container:** o Dockerfile é a receita (texto com instruções); a imagem é o resultado do build, um pacote pronto e imutável; o container é uma instância em execução de uma imagem.
5. **Quando o RUN executa:** durante o `docker build`, não ao iniciar o container. O resultado fica gravado em uma camada da imagem.
6. **EXPOSE 5000:** apenas documenta que a aplicação usa a porta 5000 no container. Não publica a porta no host; isso é feito com `-p` no `docker run`.
7. **-p 8080:5000:** publica a porta 5000 do container na porta 8080 do computador (host): `host:container`. Acessa-se `localhost:8080` e a requisição chega ao Flask na 5000.
8. **Verificar se o container roda:** `docker ps` (use `docker ps -a` para ver também os parados).
9. **Ver mensagens da aplicação:** `docker logs labstatus-app`.
10. **Alteração local não muda a imagem:** a imagem é imutável e guarda uma cópia dos arquivos do momento do build; é preciso reconstruí-la para incorporar mudanças.

## Explicação do Dockerfile
- `FROM python:3.13-slim`: imagem base com Python (versão leve). Use a tag indicada pelo professor.
- `WORKDIR /app`: define /app como diretório de trabalho dentro do container.
- `COPY requirements.txt .`: copia só as dependências primeiro, para aproveitar o cache de camadas.
- `RUN python -m pip install --no-cache-dir -r requirements.txt`: instala o Flask durante o build, sem guardar cache.
- `COPY . .`: copia o restante do projeto (respeitando o .dockerignore).
- `EXPOSE 5000`: documenta a porta usada pela aplicação.
- `CMD ["python", "app.py"]`: comando executado quando o container inicia.
