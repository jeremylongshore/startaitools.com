<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "999c5e7623c1e2d5e5a07c2feb39eb67",
  "translation_date": "2025-07-14T08:23:05+00:00",
  "source_file": "10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/README.md",
  "language_code": "ar"
}
-->
# خادم Weather MCP

هذا نموذج لخادم MCP مكتوب بلغة Python يقوم بتنفيذ أدوات الطقس مع استجابات وهمية. يمكن استخدامه كأساس لإنشاء خادم MCP خاص بك. يتضمن الميزات التالية:

- **أداة الطقس**: أداة توفر معلومات طقس وهمية بناءً على الموقع المعطى.
- **الاتصال بـ Agent Builder**: ميزة تتيح لك ربط خادم MCP بـ Agent Builder للاختبار وتصحيح الأخطاء.
- **التصحيح في [MCP Inspector](https://github.com/modelcontextprotocol/inspector)**: ميزة تتيح لك تصحيح خادم MCP باستخدام MCP Inspector.

## البدء مع قالب Weather MCP Server

> **المتطلبات المسبقة**
>
> لتشغيل خادم MCP على جهاز التطوير المحلي لديك، ستحتاج إلى:
>
> - [Python](https://www.python.org/)
> - (*اختياري - إذا كنت تفضل uv*) [uv](https://github.com/astral-sh/uv)
> - [امتداد مصحح أخطاء Python](https://marketplace.visualstudio.com/items?itemName=ms-python.debugpy)

## إعداد البيئة

هناك طريقتان لإعداد البيئة لهذا المشروع. يمكنك اختيار أي منهما حسب تفضيلك.

> ملاحظة: أعد تحميل VSCode أو الطرفية للتأكد من استخدام بايثون البيئة الافتراضية بعد إنشائها.

| الطريقة | الخطوات |
| -------- | ----- |
| باستخدام `uv` | 1. إنشاء البيئة الافتراضية: `uv venv` <br>2. تشغيل أمر VSCode "***Python: Select Interpreter***" واختيار بايثون من البيئة الافتراضية التي تم إنشاؤها <br>3. تثبيت التبعيات (بما في ذلك تبعيات التطوير): `uv pip install -r pyproject.toml --extra dev` |
| باستخدام `pip` | 1. إنشاء البيئة الافتراضية: `python -m venv .venv` <br>2. تشغيل أمر VSCode "***Python: Select Interpreter***" واختيار بايثون من البيئة الافتراضية التي تم إنشاؤها<br>3. تثبيت التبعيات (بما في ذلك تبعيات التطوير): `pip install -e .[dev]` |

بعد إعداد البيئة، يمكنك تشغيل الخادم على جهاز التطوير المحلي عبر Agent Builder كعميل MCP للبدء:
1. افتح لوحة التصحيح في VS Code. اختر `Debug in Agent Builder` أو اضغط `F5` لبدء تصحيح خادم MCP.
2. استخدم AI Toolkit Agent Builder لاختبار الخادم باستخدام [هذا الطلب](../../../../../../../../../../open_prompt_builder). سيتم ربط الخادم تلقائيًا بـ Agent Builder.
3. اضغط `Run` لاختبار الخادم باستخدام الطلب.

**تهانينا**! لقد نجحت في تشغيل خادم Weather MCP على جهاز التطوير المحلي عبر Agent Builder كعميل MCP.
![DebugMCP](https://raw.githubusercontent.com/microsoft/windows-ai-studio-templates/refs/heads/dev/mcpServers/mcp_debug.gif)

## ما الذي يتضمنه القالب

| المجلد / الملف | المحتويات                                     |
| ------------ | -------------------------------------------- |
| `.vscode`    | ملفات VSCode الخاصة بالتصحيح                   |
| `.aitk`      | إعدادات AI Toolkit                            |
| `src`        | كود المصدر لخادم weather mcp                   |

## كيفية تصحيح خادم Weather MCP

> ملاحظات:
> - [MCP Inspector](https://github.com/modelcontextprotocol/inspector) هو أداة تطوير بصرية لاختبار وتصحيح خوادم MCP.
> - جميع أوضاع التصحيح تدعم نقاط التوقف، لذا يمكنك إضافة نقاط توقف في كود تنفيذ الأداة.

| وضع التصحيح | الوصف | خطوات التصحيح |
| ---------- | ----------- | --------------- |
| Agent Builder | تصحيح خادم MCP في Agent Builder عبر AI Toolkit. | 1. افتح لوحة التصحيح في VS Code. اختر `Debug in Agent Builder` واضغط `F5` لبدء تصحيح خادم MCP.<br>2. استخدم AI Toolkit Agent Builder لاختبار الخادم باستخدام [هذا الطلب](../../../../../../../../../../open_prompt_builder). سيتم ربط الخادم تلقائيًا بـ Agent Builder.<br>3. اضغط `Run` لاختبار الخادم باستخدام الطلب. |
| MCP Inspector | تصحيح خادم MCP باستخدام MCP Inspector. | 1. ثبت [Node.js](https://nodejs.org/)<br> 2. إعداد Inspector: `cd inspector` && `npm install` <br> 3. افتح لوحة التصحيح في VS Code. اختر `Debug SSE in Inspector (Edge)` أو `Debug SSE in Inspector (Chrome)`. اضغط F5 لبدء التصحيح.<br> 4. عند تشغيل MCP Inspector في المتصفح، اضغط زر `Connect` لربط هذا الخادم.<br> 5. بعدها يمكنك `List Tools`، اختيار أداة، إدخال المعطيات، و`Run Tool` لتصحيح كود الخادم.<br> |

## المنافذ الافتراضية والتخصيصات

| وضع التصحيح | المنافذ | التعريفات | التخصيصات | ملاحظة |
| ---------- | ----- | ------------ | -------------- |-------------- |
| Agent Builder | 3001 | [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json) | عدل [launch.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/launch.json)، [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json)، [\_\_init\_\_.py](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/src/__init__.py)، [mcp.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.aitk/mcp.json) لتغيير المنافذ أعلاه. | لا يوجد |
| MCP Inspector | 3001 (الخادم)؛ 5173 و 3000 (Inspector) | [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json) | عدل [launch.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/launch.json)، [tasks.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.vscode/tasks.json)، [\_\_init\_\_.py](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/src/__init__.py)، [mcp.json](../../../../../../10-StreamliningAIWorkflowsBuildingAnMCPServerWithAIToolkit/lab3/code/weather_mcp/.aitk/mcp.json) لتغيير المنافذ أعلاه.| لا يوجد |

## الملاحظات

إذا كان لديك أي ملاحظات أو اقتراحات لهذا القالب، يرجى فتح مشكلة في [مستودع AI Toolkit على GitHub](https://github.com/microsoft/vscode-ai-toolkit/issues)

**إخلاء المسؤولية**:  
تمت ترجمة هذا المستند باستخدام خدمة الترجمة الآلية [Co-op Translator](https://github.com/Azure/co-op-translator). بينما نسعى لتحقيق الدقة، يرجى العلم أن الترجمات الآلية قد تحتوي على أخطاء أو عدم دقة. يجب اعتبار المستند الأصلي بلغته الأصلية المصدر الموثوق به. للمعلومات الهامة، يُنصح بالاعتماد على الترجمة البشرية المهنية. نحن غير مسؤولين عن أي سوء فهم أو تفسير ناتج عن استخدام هذه الترجمة.