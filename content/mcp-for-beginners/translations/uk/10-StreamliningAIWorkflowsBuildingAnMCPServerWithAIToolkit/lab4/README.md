<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "f83bc722dc758efffd68667d6a1db470",
  "translation_date": "2025-07-14T08:49:28+00:00",
  "source_file": "10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab4/README.md",
  "language_code": "uk"
}
-->
# 🐙 Модуль 4: Практична розробка MCP – Кастомний сервер клонування GitHub

![Duration](https://img.shields.io/badge/Duration-30_minutes-blue?style=flat-square)
![Difficulty](https://img.shields.io/badge/Difficulty-Intermediate-orange?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-Custom%20Server-purple?style=flat-square&logo=github)
![VS Code](https://img.shields.io/badge/VS%20Code-Integration-blue?style=flat-square&logo=visualstudiocode)
![GitHub Copilot](https://img.shields.io/badge/GitHub%20Copilot-Agent%20Mode-green?style=flat-square&logo=github)

> **⚡ Швидкий старт:** Створіть готовий до продакшену MCP сервер, який автоматизує клонування репозиторіїв GitHub та інтеграцію з VS Code всього за 30 хвилин!

## 🎯 Цілі навчання

Після завершення цього лабораторного заняття ви зможете:

- ✅ Створювати кастомний MCP сервер для реальних робочих процесів розробки
- ✅ Реалізувати функціонал клонування репозиторіїв GitHub через MCP
- ✅ Інтегрувати кастомні MCP сервери з VS Code та Agent Builder
- ✅ Використовувати GitHub Copilot Agent Mode з кастомними MCP інструментами
- ✅ Тестувати та розгортати кастомні MCP сервери у продакшен-середовищах

## 📋 Вимоги

- Завершення лабораторних 1-3 (основи MCP та розширена розробка)
- Підписка на GitHub Copilot ([доступна безкоштовна реєстрація](https://github.com/github-copilot/signup))
- VS Code з розширеннями AI Toolkit та GitHub Copilot
- Встановлений та налаштований Git CLI

## 🏗️ Огляд проєкту

### **Реальна задача розробки**
Як розробники, ми часто використовуємо GitHub для клонування репозиторіїв та відкриття їх у VS Code або VS Code Insiders. Цей ручний процес включає:
1. Відкриття терміналу/командного рядка
2. Перехід у потрібну директорію
3. Виконання команди `git clone`
4. Відкриття VS Code у склонированій директорії

**Наше MCP рішення спрощує це до однієї інтелектуальної команди!**

### **Що ви створите**
**GitHub Clone MCP Server** (`git_mcp_server`), який надає:

| Функція | Опис | Перевага |
|---------|-------------|---------|
| 🔄 **Інтелектуальне клонування репозиторіїв** | Клонування GitHub репозиторіїв з валідацією | Автоматична перевірка помилок |
| 📁 **Розумне керування директоріями** | Перевірка та безпечне створення директорій | Запобігає перезапису |
| 🚀 **Кросплатформна інтеграція з VS Code** | Відкриття проєктів у VS Code/Insiders | Плавний перехід у робочий процес |
| 🛡️ **Надійна обробка помилок** | Обробка мережевих, прав доступу та шляхів | Готовність до продакшену |

---

## 📖 Покрокова реалізація

### Крок 1: Створення GitHub агента в Agent Builder

1. **Запустіть Agent Builder** через розширення AI Toolkit
2. **Створіть нового агента** з наступною конфігурацією:
   ```
   Agent Name: GitHubAgent
   ```

3. **Ініціалізуйте кастомний MCP сервер:**
   - Перейдіть у **Tools** → **Add Tool** → **MCP Server**
   - Оберіть **"Create A new MCP Server"**
   - Виберіть **Python шаблон** для максимальної гнучкості
   - **Назва сервера:** `git_mcp_server`

### Крок 2: Налаштування GitHub Copilot Agent Mode

1. **Відкрийте GitHub Copilot** у VS Code (Ctrl/Cmd + Shift + P → "GitHub Copilot: Open")
2. **Оберіть модель агента** у інтерфейсі Copilot
3. **Виберіть модель Claude 3.7** для покращеного розуміння та логіки
4. **Увімкніть інтеграцію MCP** для доступу до інструментів

> **💡 Порада:** Claude 3.7 забезпечує кращий аналіз робочих процесів розробки та шаблонів обробки помилок.

### Крок 3: Реалізація основного функціоналу MCP сервера

**Використайте наступний детальний запит для GitHub Copilot Agent Mode:**

```
Create two MCP tools with the following comprehensive requirements:

🔧 TOOL A: clone_repository
Requirements:
- Clone any GitHub repository to a specified local folder
- Return the absolute path of the successfully cloned project
- Implement comprehensive validation:
  ✓ Check if target directory already exists (return error if exists)
  ✓ Validate GitHub URL format (https://github.com/user/repo)
  ✓ Verify git command availability (prompt installation if missing)
  ✓ Handle network connectivity issues
  ✓ Provide clear error messages for all failure scenarios

🚀 TOOL B: open_in_vscode
Requirements:
- Open specified folder in VS Code or VS Code Insiders
- Cross-platform compatibility (Windows/Linux/macOS)
- Use direct application launch (not terminal commands)
- Auto-detect available VS Code installations
- Handle cases where VS Code is not installed
- Provide user-friendly error messages

Additional Requirements:
- Follow MCP 1.9.3 best practices
- Include proper type hints and documentation
- Implement logging for debugging purposes
- Add input validation for all parameters
- Include comprehensive error handling
```

### Крок 4: Тестування MCP сервера

#### 4a. Тестування в Agent Builder

1. **Запустіть конфігурацію налагодження** для Agent Builder
2. **Налаштуйте агента з цим системним запитом:**

```
SYSTEM_PROMPT:
You are my intelligent coding repository assistant. You help developers efficiently clone GitHub repositories and set up their development environment. Always provide clear feedback about operations and handle errors gracefully.
```

3. **Перевірте на реалістичних сценаріях користувача:**

```
USER_PROMPT EXAMPLES:

Scenario : Basic Clone and Open
"Clone {Your GitHub Repo link such as https://github.com/kinfey/GHCAgentWorkshop
 } and save to {The global path you specify}, then open it with VS Code Insiders"
```

![Agent Builder Testing](../../../../translated_images/DebugAgent.81d152370c503241b3b39a251b8966f7f739286df19dd57f9147f6402214a012.uk.png)

**Очікувані результати:**
- ✅ Успішне клонування з підтвердженням шляху
- ✅ Автоматичний запуск VS Code
- ✅ Чіткі повідомлення про помилки у некоректних випадках
- ✅ Коректна обробка крайніх ситуацій

#### 4b. Тестування в MCP Inspector

![MCP Inspector Testing](../../../../translated_images/DebugInspector.eb5c95f94c69a8ba36944941b9a3588309a3a2fae101ace470ee09bde41d1667.uk.png)

---

**🎉 Вітаємо!** Ви успішно створили практичний MCP сервер, готовий до продакшену, який вирішує реальні задачі робочих процесів розробки. Ваш кастомний сервер клонування GitHub демонструє потужність MCP для автоматизації та підвищення продуктивності розробників.

### 🏆 Досягнення:
- ✅ **MCP Developer** – створено кастомний MCP сервер
- ✅ **Workflow Automator** – оптимізовано процеси розробки  
- ✅ **Integration Expert** – інтегровано кілька інструментів розробки
- ✅ **Production Ready** – створено рішення, готові до розгортання

---

## 🎓 Завершення воркшопу: Ваша подорож з Model Context Protocol

**Шановний учаснику воркшопу,**

Вітаємо з успішним завершенням усіх чотирьох модулів воркшопу Model Context Protocol! Ви пройшли великий шлях від розуміння базових концепцій AI Toolkit до створення продакшен MCP серверів, які вирішують реальні задачі розробки.

### 🚀 Підсумок вашого навчання:

**[Модуль 1](../lab1/README.md)**: Ви почали з вивчення основ AI Toolkit, тестування моделей та створення першого AI агента.

**[Модуль 2](../lab2/README.md)**: Вивчили архітектуру MCP, інтегрували Playwright MCP та створили першого агента для автоматизації браузера.

**[Модуль 3](../lab3/README.md)**: Поглибили знання у розробці кастомних MCP серверів на прикладі Weather MCP сервера та освоїли інструменти налагодження.

**[Модуль 4](../lab4/README.md)**: Застосували все на практиці, створивши інструмент автоматизації робочого процесу з репозиторіями GitHub.

### 🌟 Що ви опанували:

- ✅ **Екосистема AI Toolkit**: моделі, агенти та патерни інтеграції
- ✅ **Архітектура MCP**: клієнт-серверний дизайн, транспортні протоколи та безпека
- ✅ **Інструменти розробника**: від Playground до Inspector та продакшен розгортання
- ✅ **Кастомна розробка**: створення, тестування та розгортання власних MCP серверів
- ✅ **Практичні застосування**: вирішення реальних задач робочих процесів за допомогою AI

### 🔮 Ваші наступні кроки:

1. **Створіть власний MCP сервер**: застосуйте ці навички для автоматизації своїх унікальних робочих процесів
2. **Приєднуйтесь до спільноти MCP**: діліться своїми розробками та вчіться у інших
3. **Вивчайте розширену інтеграцію**: підключайте MCP сервери до корпоративних систем
4. **Внесіть свій вклад у Open Source**: допомагайте покращувати інструменти та документацію MCP

Пам’ятайте, цей воркшоп – лише початок. Екосистема Model Context Protocol швидко розвивається, і тепер ви готові бути на передовій інструментів розробки з підтримкою AI.

**Дякуємо за вашу участь та прагнення до навчання!**

Сподіваємося, цей воркшоп надихнув вас на ідеї, які змінять ваш підхід до створення та взаємодії з AI інструментами у вашій розробці.

**Щасливого кодування!**

---

**Відмова від відповідальності**:  
Цей документ було перекладено за допомогою сервісу автоматичного перекладу [Co-op Translator](https://github.com/Azure/co-op-translator). Хоча ми прагнемо до точності, будь ласка, майте на увазі, що автоматичні переклади можуть містити помилки або неточності. Оригінальний документ рідною мовою слід вважати авторитетним джерелом. Для критично важливої інформації рекомендується звертатися до професійного людського перекладу. Ми не несемо відповідальності за будь-які непорозуміння або неправильні тлумачення, що виникли внаслідок використання цього перекладу.