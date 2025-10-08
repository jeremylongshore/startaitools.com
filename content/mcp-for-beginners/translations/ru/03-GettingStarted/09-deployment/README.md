<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1d9dc83260576b76f272d330ed93c51f",
  "translation_date": "2025-07-13T22:05:52+00:00",
  "source_file": "03-GettingStarted/09-deployment/README.md",
  "language_code": "ru"
}
-->
# Развертывание MCP серверов

Развертывание вашего MCP сервера позволяет другим получить доступ к его инструментам и ресурсам за пределами вашей локальной среды. Существует несколько стратегий развертывания, которые стоит рассмотреть в зависимости от ваших требований к масштабируемости, надежности и удобству управления. Ниже вы найдете рекомендации по развертыванию MCP серверов локально, в контейнерах и в облаке.

## Обзор

В этом уроке рассматривается, как развернуть ваше приложение MCP Server.

## Цели обучения

К концу этого урока вы сможете:

- Оценивать различные подходы к развертыванию.
- Развернуть ваше приложение.

## Локальная разработка и развертывание

Если ваш сервер предназначен для использования на машине пользователя, выполните следующие шаги:

1. **Скачайте сервер**. Если вы не писали сервер, сначала скачайте его на свой компьютер.  
1. **Запустите процесс сервера**: Запустите ваше приложение MCP server.

Для SSE (не требуется для сервера типа stdio)

1. **Настройте сеть**: Убедитесь, что сервер доступен на ожидаемом порту.  
1. **Подключите клиентов**: Используйте локальные URL, например `http://localhost:3000`.

## Развертывание в облаке

MCP серверы можно развернуть на различных облачных платформах:

- **Serverless Functions**: Развертывайте легковесные MCP серверы как бессерверные функции.  
- **Container Services**: Используйте сервисы, такие как Azure Container Apps, AWS ECS или Google Cloud Run.  
- **Kubernetes**: Развертывайте и управляйте MCP серверами в кластерах Kubernetes для высокой доступности.

### Пример: Azure Container Apps

Azure Container Apps поддерживает развертывание MCP серверов. Это всё ещё в разработке, и в настоящее время поддерживаются SSE серверы.

Вот как это можно сделать:

1. Клонируйте репозиторий:

  ```sh
  git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
  ```

1. Запустите локально для тестирования:

  ```sh
  uv venv
  uv sync

  # linux/macOS
  export API_KEYS=<AN_API_KEY>
  # windows
  set API_KEYS=<AN_API_KEY>

  uv run fastapi dev main.py
  ```

1. Чтобы попробовать локально, создайте файл *mcp.json* в директории *.vscode* и добавьте следующий контент:

  ```json
  {
      "inputs": [
          {
              "type": "promptString",
              "id": "weather-api-key",
              "description": "Weather API Key",
              "password": true
          }
      ],
      "servers": {
          "weather-sse": {
              "type": "sse",
              "url": "http://localhost:8000/sse",
              "headers": {
                  "x-api-key": "${input:weather-api-key}"
              }
          }
      }
  }
  ```

  После запуска SSE сервера вы можете нажать на иконку воспроизведения в JSON файле, теперь инструменты сервера должны быть распознаны GitHub Copilot, обратите внимание на иконку Tool.

1. Для развертывания выполните следующую команду:

  ```sh
  az containerapp up -g <RESOURCE_GROUP_NAME> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
  ```

Вот и всё, разверните локально или в Azure, следуя этим шагам.

## Дополнительные ресурсы

- [Azure Functions + MCP](https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/)
- [Статья про Azure Container Apps](https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-in-azure-container-apps/4403550)
- [Репозиторий Azure Container Apps MCP](https://github.com/anthonychu/azure-container-apps-mcp-sample)

## Что дальше

- Далее: [Практическая реализация](../../04-PracticalImplementation/README.md)

**Отказ от ответственности**:  
Этот документ был переведен с помощью сервиса автоматического перевода [Co-op Translator](https://github.com/Azure/co-op-translator). Несмотря на наши усилия по обеспечению точности, просим учитывать, что автоматический перевод может содержать ошибки или неточности. Оригинальный документ на его исходном языке следует считать авторитетным источником. Для получения критически важной информации рекомендуется обращаться к профессиональному переводу, выполненному человеком. Мы не несем ответственности за любые недоразумения или неправильные толкования, возникшие в результате использования данного перевода.