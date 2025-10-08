<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "1d9dc83260576b76f272d330ed93c51f",
  "translation_date": "2025-07-13T22:11:19+00:00",
  "source_file": "03-GettingStarted/09-deployment/README.md",
  "language_code": "bg"
}
-->
# Разгръщане на MCP сървъри

Разгръщането на вашия MCP сървър позволява на други да имат достъп до неговите инструменти и ресурси извън локалната ви среда. Съществуват няколко стратегии за разгръщане, които да разгледате, в зависимост от вашите изисквания за мащабируемост, надеждност и лесно управление. По-долу ще намерите насоки за разгръщане на MCP сървъри локално, в контейнери и в облака.

## Преглед

Този урок обхваща как да разположите вашето MCP Server приложение.

## Учебни цели

Към края на този урок ще можете да:

- Оценявате различни подходи за разгръщане.
- Разгърнете вашето приложение.

## Локална разработка и разгръщане

Ако вашият сървър е предназначен да се използва на машината на потребителя, можете да следвате следните стъпки:

1. **Изтеглете сървъра**. Ако не сте писали сървъра, първо го изтеглете на вашата машина.  
1. **Стартирайте сървърния процес**: Стартирайте вашето MCP server приложение.

За SSE (не е необходимо за stdio тип сървър)

1. **Конфигурирайте мрежата**: Уверете се, че сървърът е достъпен на очаквания порт.  
1. **Свържете клиентите**: Използвайте локални URL адреси като `http://localhost:3000`.

## Разгръщане в облака

MCP сървърите могат да бъдат разгръщани на различни облачни платформи:

- **Serverless функции**: Разгърнете леки MCP сървъри като serverless функции.  
- **Контейнерни услуги**: Използвайте услуги като Azure Container Apps, AWS ECS или Google Cloud Run.  
- **Kubernetes**: Разгръщайте и управлявайте MCP сървъри в Kubernetes клъстери за висока наличност.

### Пример: Azure Container Apps

Azure Container Apps поддържа разгръщане на MCP сървъри. Все още е в процес на разработка и в момента поддържа SSE сървъри.

Ето как можете да го направите:

1. Клонирайте репо:

  ```sh
  git clone https://github.com/anthonychu/azure-container-apps-mcp-sample.git
  ```

1. Стартирайте го локално, за да тествате:

  ```sh
  uv venv
  uv sync

  # linux/macOS
  export API_KEYS=<AN_API_KEY>
  # windows
  set API_KEYS=<AN_API_KEY>

  uv run fastapi dev main.py
  ```

1. За да го пробвате локално, създайте файл *mcp.json* в директория *.vscode* и добавете следното съдържание:

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

  След като SSE сървърът е стартиран, можете да кликнете върху иконата за пускане в JSON файла, сега трябва да видите инструментите на сървъра, които се разпознават от GitHub Copilot, вижте иконата Tool.

1. За да разположите, изпълнете следната команда:

  ```sh
  az containerapp up -g <RESOURCE_GROUP_NAME> -n weather-mcp --environment mcp -l westus --env-vars API_KEYS=<AN_API_KEY> --source .
  ```

Ето го, разположете го локално или в Azure чрез тези стъпки.

## Допълнителни ресурси

- [Azure Functions + MCP](https://learn.microsoft.com/en-us/samples/azure-samples/remote-mcp-functions-dotnet/remote-mcp-functions-dotnet/)  
- [Статия за Azure Container Apps](https://techcommunity.microsoft.com/blog/appsonazureblog/host-remote-mcp-servers-in-azure-container-apps/4403550)  
- [Azure Container Apps MCP репо](https://github.com/anthonychu/azure-container-apps-mcp-sample)  


## Какво следва

- Следва: [Практическа реализация](../../04-PracticalImplementation/README.md)

**Отказ от отговорност**:  
Този документ е преведен с помощта на AI преводаческа услуга [Co-op Translator](https://github.com/Azure/co-op-translator). Въпреки че се стремим към точност, моля, имайте предвид, че автоматизираните преводи могат да съдържат грешки или неточности. Оригиналният документ на неговия роден език трябва да се счита за авторитетен източник. За критична информация се препоръчва професионален човешки превод. Ние не носим отговорност за каквито и да е недоразумения или неправилни тълкувания, произтичащи от използването на този превод.