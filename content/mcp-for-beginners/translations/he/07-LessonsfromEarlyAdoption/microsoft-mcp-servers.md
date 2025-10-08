<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T11:46:30+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "he"
}
-->
# 🚀 10 שרתי Microsoft MCP שמשנים את הפרודוקטיביות של מפתחים

## 🎯 מה תלמדו במדריך הזה

המדריך המעשי הזה מציג עשרה שרתי Microsoft MCP שמשנים באופן פעיל את אופן העבודה של מפתחים עם עוזרי AI. במקום רק להסביר מה שרתי MCP *יכולים* לעשות, נציג שרתים שכבר עושים שינוי אמיתי בשגרות הפיתוח היומיומיות במיקרוסופט ומעבר לה.

כל שרת במדריך זה נבחר בהתבסס על שימוש אמיתי ומשוב מפתחים. תגלה לא רק מה כל שרת עושה, אלא גם למה זה חשוב ואיך להפיק ממנו את המירב בפרויקטים שלך. בין אם אתה חדש לגמרי ב-MCP או מחפש להרחיב את ההגדרות הקיימות שלך, שרתים אלה מייצגים כמה מהכלים הפרקטיים והמשפיעים ביותר במערכת האקולוגית של מיקרוסופט.

> **💡 טיפ התחלה מהירה**
> 
> חדש ב-MCP? אל דאגה! המדריך הזה מותאם למתחילים. נסביר מושגים תוך כדי, ותמיד תוכל לחזור ל[הקדמה ל-MCP](../00-Introduction/README.md) ול[מושגי יסוד](../01-CoreConcepts/README.md) לעומק נוסף.

## סקירה כללית

מדריך מקיף זה בוחן עשרה שרתי Microsoft MCP שמשנים את האופן שבו מפתחים מתקשרים עם עוזרי AI וכלים חיצוניים. מניהול משאבי Azure ועד עיבוד מסמכים, שרתים אלה מדגימים את כוח פרוטוקול הקשר המודלי ביצירת זרימות עבודה חלקות ויעילות בפיתוח.

## מטרות הלמידה

בסיום המדריך תוכל:
- להבין כיצד שרתי MCP משפרים את הפרודוקטיביות של מפתחים
- ללמוד על מימושי שרתי MCP המשפיעים ביותר של מיקרוסופט
- לגלות מקרים מעשיים לשימוש בכל שרת
- לדעת כיצד להגדיר ולכוון את השרתים ב-VS Code ו-Visual Studio
- לחקור את מערכת האקולוגית הרחבה של MCP וכיווני העתיד

## 🔧 הבנת שרתי MCP: מדריך למתחילים

### מה הם שרתי MCP?

כמתחיל בפרוטוקול הקשר המודלי (MCP), אולי תתעניין: "מה בעצם שרת MCP ולמה זה חשוב לי?" נתחיל בדימוי פשוט.

תחשוב על שרתי MCP כעוזרים מיוחדים שמאפשרים לעוזר הקידוד שלך מבוסס AI (כמו GitHub Copilot) להתחבר לכלים ושירותים חיצוניים. בדיוק כמו שאתה משתמש באפליקציות שונות בטלפון למשימות שונות — אחת למזג אוויר, אחת לניווט, אחת לבנקאות — שרתי MCP נותנים לעוזר ה-AI שלך את היכולת לתקשר עם כלים ושירותי פיתוח שונים.

### הבעיה ששרתי MCP פותרים

לפני שרתי MCP, אם רצית:
- לבדוק את משאבי Azure שלך
- ליצור issue ב-GitHub
- לשאול את מסד הנתונים שלך
- לחפש בתיעוד

היית צריך להפסיק לקודד, לפתוח דפדפן, לנווט לאתר המתאים ולבצע את המשימות ידנית. המעבר התדיר בין הקשרים שובר את הזרימה שלך ומפחית את הפרודוקטיביות.

### איך שרתי MCP משנים את חוויית הפיתוח שלך

עם שרתי MCP, תוכל להישאר בסביבת הפיתוח שלך (VS Code, Visual Studio וכו') ולבקש מהעוזר AI שלך לטפל במשימות האלה. לדוגמה:

**במקום זרימת עבודה מסורתית כזו:**
1. להפסיק לקודד  
2. לפתוח דפדפן  
3. לנווט לפורטל Azure  
4. לבדוק פרטי חשבון אחסון  
5. לחזור ל-VS Code  
6. להמשיך לקודד  

**עכשיו אפשר לעשות כך:**
1. לשאול את ה-AI: "מה מצב חשבונות האחסון שלי ב-Azure?"  
2. להמשיך לקודד עם המידע שקיבלת  

### יתרונות מרכזיים למתחילים

#### 1. 🔄 **להישאר במצב זרימה**
- לא צריך לעבור בין אפליקציות שונות  
- לשמור על ריכוז בקוד שאתה כותב  
- להפחית עומס מנטלי של ניהול כלים שונים  

#### 2. 🤖 **שימוש בשפה טבעית במקום פקודות מורכבות**
- במקום לזכור תחביר SQL, תאר את הנתונים שאתה צריך  
- במקום לזכור פקודות Azure CLI, הסבר מה אתה רוצה להשיג  
- תן ל-AI לטפל בפרטים הטכניים בזמן שאתה מתמקד בלוגיקה  

#### 3. 🔗 **חיבור בין כלים שונים**
- ליצור זרימות עבודה חזקות על ידי שילוב שירותים שונים  
- דוגמה: "קבל את כל ה-issues האחרונים ב-GitHub ויצר פריטי עבודה מתאימים ב-Azure DevOps"  
- לבנות אוטומציה בלי לכתוב סקריפטים מורכבים  

#### 4. 🌐 **גישה למערכת אקולוגית מתפתחת**
- ליהנות משרתים שנבנו על ידי מיקרוסופט, GitHub וחברות נוספות  
- לשלב כלים מספקים שונים בצורה חלקה  
- להצטרף למערכת סטנדרטית שעובדת עם עוזרי AI שונים  

#### 5. 🛠️ **למידה דרך עשייה**
- להתחיל עם שרתים מוכנים להבנה של המושגים  
- לבנות בהדרגה שרתים משלך ככל שתתמקצע  
- להשתמש ב-SDK ובתיעוד הזמינים להכוונה בלמידה  

### דוגמה מעשית למתחילים

נניח שאתה חדש בפיתוח ווב ועובד על הפרויקט הראשון שלך. כך שרתי MCP יכולים לעזור:

**גישה מסורתית:**  
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**עם שרתי MCP:**  
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### יתרון התקן הארגוני

MCP הופך לתקן תעשייתי רחב, מה שאומר:  
- **עקביות**: חווית משתמש דומה בכלים ובחברות שונות  
- **אינטראופרביליות**: שרתים מספקים שונים עובדים יחד  
- **הכנה לעתיד**: מיומנויות והגדרות ניתנות להעברה בין עוזרי AI שונים  
- **קהילה**: מערכת אקולוגית גדולה של ידע ומשאבים משותפים  

### להתחיל: מה תלמד

במדריך זה נחקור 10 שרתי Microsoft MCP שמועילים במיוחד למפתחים בכל הרמות. כל שרת מיועד ל:  
- לפתור אתגרים נפוצים בפיתוח  
- להפחית משימות חוזרות  
- לשפר את איכות הקוד  
- להעצים הזדמנויות למידה  

> **💡 טיפ ללמידה**  
> 
> אם אתה חדש לגמרי ב-MCP, התחל עם מודולי [הקדמה ל-MCP](../00-Introduction/README.md) ו[מושגי יסוד](../01-CoreConcepts/README.md). לאחר מכן חזור לכאן לראות את המושגים בפעולה עם כלים אמיתיים של מיקרוסופט.  
> 
> להקשר נוסף על חשיבות MCP, עיין בפוסט של מריה נגגה: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps).

## התחלה עם MCP ב-VS Code ו-Visual Studio 🚀

הגדרת שרתי MCP אלה פשוטה אם אתה משתמש ב-Visual Studio Code או Visual Studio 2022 עם GitHub Copilot.

### הגדרת VS Code

הנה התהליך הבסיסי ל-VS Code:

1. **הפעל מצב Agent**: ב-VS Code, עבור למצב Agent בחלון שיחת Copilot  
2. **הגדר שרתי MCP**: הוסף הגדרות שרתים לקובץ settings.json של VS Code  
3. **הפעל שרתים**: לחץ על כפתור "התחל" עבור כל שרת שברצונך להשתמש בו  
4. **בחר כלים**: בחר אילו שרתי MCP להפעיל במפגש הנוכחי  

להוראות מפורטות, עיין ב[תיעוד MCP ל-VS Code](https://code.visualstudio.com/docs/copilot/copilot-mcp).

> **💡 טיפ מקצועי: נהל שרתי MCP כמו מקצוען!**  
> 
> תצוגת ההרחבות ב-VS Code כוללת כעת [ממשק ניהול חדש ונוח לשרתי MCP](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode)! יש לך גישה מהירה להפעלה, עצירה וניהול של כל שרתי MCP מותקנים בממשק ברור ופשוט. נסה זאת!

### הגדרת Visual Studio 2022

עבור Visual Studio 2022 (גרסה 17.14 ומעלה):

1. **הפעל מצב Agent**: לחץ על תפריט הנפתח "Ask" בחלון שיחת GitHub Copilot ובחר "Agent"  
2. **צור קובץ הגדרות**: צור קובץ `.mcp.json` בתיקיית הפתרון שלך (מיקום מומלץ: `<SOLUTIONDIR>\.mcp.json`)  
3. **הגדר שרתים**: הוסף את הגדרות שרתי MCP בפורמט הסטנדרטי  
4. **אישור כלים**: כאשר תתבקש, אשר את הכלים שברצונך להשתמש בהם עם ההרשאות המתאימות  

להוראות מפורטות, עיין ב[תיעוד MCP ל-Visual Studio](https://learn.microsoft.com/visualstudio/ide/mcp-servers).

לכל שרת MCP יש דרישות הגדרה משלו (מחרוזות חיבור, אימות וכו'), אך דפוס ההגדרה עקבי בשני ה-IDE.

## לקחים משרתי Microsoft MCP 🛠️

### 1. 📚 שרת Microsoft Learn Docs MCP

[![התקן ב-VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![התקן ב-VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**מה הוא עושה**: שרת Microsoft Learn Docs MCP הוא שירות מבוסס ענן שמספק לעוזרי AI גישה בזמן אמת לתיעוד הרשמי של מיקרוסופט דרך פרוטוקול הקשר המודלי. הוא מתחבר ל-`https://learn.microsoft.com/api/mcp` ומאפשר חיפוש סמנטי ברחבי Microsoft Learn, תיעוד Azure, תיעוד Microsoft 365 ומקורות רשמיים נוספים של מיקרוסופט.

**למה זה שימושי**: למרות שזה נראה כמו "סתם תיעוד", השרת הזה חיוני לכל מפתח שמשתמש בטכנולוגיות מיקרוסופט. אחת התלונות הגדולות של מפתחי .NET על עוזרי קידוד מבוססי AI היא שהם לא מעודכנים בגרסאות האחרונות של .NET ו-C#. שרת Microsoft Learn Docs MCP פותר זאת על ידי מתן גישה בזמן אמת לתיעוד העדכני ביותר, הפניות API והנחיות עבודה מומלצות. בין אם אתה עובד עם ה-SDKs החדשים של Azure, בוחן תכונות חדשות ב-C# 13, או מיישם דפוסי Aspire מתקדמים ב-.NET, השרת הזה מבטיח שלעוזר ה-AI שלך תהיה גישה למידע מוסמך, עדכני, ליצירת קוד מדויק ומודרני.

**שימוש בעולם האמיתי**: "מהן פקודות az cli ליצירת אפליקציית container ב-Azure לפי התיעוד הרשמי של Microsoft Learn?" או "איך להגדיר Entity Framework עם dependency injection ב-ASP.NET Core?" או "בדוק את הקוד הזה כדי לוודא שהוא תואם להמלצות הביצועים בתיעוד Microsoft Learn." השרת מספק כיסוי מקיף ב-Microsoft Learn, תיעוד Azure ותיעוד Microsoft 365 באמצעות חיפוש סמנטי מתקדם למציאת המידע הרלוונטי ביותר בהקשר. הוא מחזיר עד 10 קטעי תוכן איכותיים עם כותרות מאמרים וקישורים, תמיד ניגש לתיעוד העדכני ביותר של מיקרוסופט כפי שמתפרסם.

**דוגמה מובלטת**: השרת חושף את הכלי `microsoft_docs_search` שמבצע חיפוש סמנטי בתיעוד הטכני הרשמי של מיקרוסופט. לאחר ההגדרה, ניתן לשאול שאלות כמו "איך מיישמים אימות JWT ב-ASP.NET Core?" ולקבל תשובות מפורטות ורשמיות עם קישורי מקור. איכות החיפוש מצוינת כי הוא מבין הקשר – שאילתא על "containers" בהקשר של Azure תחזיר תיעוד של Azure Container Instances, בעוד שבאותו מונח בהקשר של .NET יוחזר מידע רלוונטי על אוספים ב-C#.

זה שימושי במיוחד עבור ספריות ומקרים שמשתנים במהירות או עודכנו לאחרונה. לדוגמה, בפרויקטי קידוד אחרונים רציתי לנצל תכונות בגרסאות האחרונות של .NET Aspire ו-Microsoft.Extensions.AI. על ידי הכללת שרת Microsoft Learn Docs MCP, הצלחתי לנצל לא רק תיעוד API, אלא גם מדריכים והסברים שפורסמו זה עתה.
> **💡 טיפ מקצועי**
> 
> אפילו מודלים שמתאימים לכלים זקוקים לעידוד כדי להשתמש בכלי MCP! כדאי לשקול להוסיף פקודת מערכת או [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) כמו: "יש לך גישה ל-`microsoft.docs.mcp` – השתמש בכלי הזה כדי לחפש בתיעוד הרשמי העדכני ביותר של מיקרוסופט כשאתה מתמודד עם שאלות על טכנולוגיות מיקרוסופט כמו C#, Azure, ASP.NET Core או Entity Framework."
>
> לדוגמה מצוינת לכך בפעולה, עיין במצב הצ'אט [C# .NET Janitor](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) מתוך מאגר Awesome GitHub Copilot. מצב זה מנצל במיוחד את שרת Microsoft Learn Docs MCP כדי לסייע בניקוי ומודרניזציה של קוד C# תוך שימוש בתבניות ובשיטות הטובות ביותר העדכניות.
### 2. ☁️ שרת Azure MCP

[![התקן ב-VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![התקן ב-VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**מה זה עושה**: שרת Azure MCP הוא חבילה מקיפה של יותר מ-15 מחברים ייעודיים לשירותי Azure, שמכניסה את כל האקוסיסטם של Azure לתוך זרימת העבודה של ה-AI שלך. זה לא רק שרת בודד – זו אוסף חזק שכולל ניהול משאבים, חיבוריות למסדי נתונים (PostgreSQL, SQL Server), ניתוח לוגים עם KQL ב-Azure Monitor, אינטגרציה עם Cosmos DB ועוד המון.

**למה זה שימושי**: מעבר לניהול משאבי Azure בלבד, השרת הזה משפר משמעותית את איכות הקוד כשעובדים עם Azure SDKs. כשאתה משתמש ב-Azure MCP במצב Agent, הוא לא רק עוזר לך לכתוב קוד – הוא עוזר לך לכתוב *קוד Azure טוב יותר* שעוקב אחרי דפוסי אימות עדכניים, שיטות טיפול בשגיאות מיטביות, ומנצל את התכונות החדשות ביותר של ה-SDK. במקום לקבל קוד כללי שעשוי לעבוד, אתה מקבל קוד שעוקב אחרי ההמלצות של Azure לעומסי עבודה בפרודקשן.

**מודולים מרכזיים כוללים**:
- **🗄️ מחברי מסדי נתונים**: גישה ישירה בשפה טבעית למסדי הנתונים של Azure PostgreSQL ו-SQL Server
- **📊 Azure Monitor**: ניתוח לוגים מבוסס KQL ותובנות תפעוליות
- **🌐 ניהול משאבים**: ניהול מחזור חיים מלא של משאבי Azure
- **🔐 אימות**: דפוסי DefaultAzureCredential וזהויות מנוהלות
- **📦 שירותי אחסון**: פעולות Blob Storage, Queue Storage ו-Table Storage
- **🚀 שירותי מכולות**: ניהול Azure Container Apps, Container Instances ו-AKS
- ועוד מחברים ייעודיים רבים

**שימוש במציאות**: "רשום את חשבונות האחסון שלי ב-Azure", "שאילתה על סביבת Log Analytics שלי לגבי שגיאות בשעה האחרונה", או "עזור לי לבנות אפליקציית Azure ב-Node.js עם אימות נכון"

**תסריט הדגמה מלא**: הנה מדריך מלא שמראה את הכוח שבשילוב Azure MCP עם תוסף GitHub Copilot for Azure ב-VS Code. כשיש לך את שניהם מותקנים ואתה מזין:

> "צור סקריפט Python שמעלה קובץ ל-Azure Blob Storage באמצעות אימות DefaultAzureCredential. הסקריפט צריך להתחבר לחשבון האחסון שלי בשם 'mycompanystorage', להעלות למכולה בשם 'documents', ליצור קובץ בדיקה עם חותמת זמן נוכחית להעלאה, לטפל בשגיאות בצורה חלקה ולספק פלט אינפורמטיבי, לעקוב אחרי שיטות העבודה המומלצות של Azure לאימות וטיפול בשגיאות, לכלול הערות שמסבירות איך עובד אימות DefaultAzureCredential, ולבנות את הסקריפט בצורה מסודרת עם פונקציות ותיעוד."

שרת Azure MCP ייצור סקריפט Python מלא ומוכן לפרודקשן ש:
- משתמש ב-SDK העדכני ביותר של Azure Blob Storage עם דפוסי async נכונים
- מיישם DefaultAzureCredential עם הסבר מפורט על שרשרת הגיבוי
- כולל טיפול שגיאות חזק עם סוגי חריגות ספציפיות ל-Azure
- עוקב אחרי שיטות העבודה המומלצות של Azure SDK לניהול משאבים וחיבורים
- מספק רישום מפורט ופלט קונסולה אינפורמטיבי
- יוצר סקריפט מובנה היטב עם פונקציות, תיעוד ורמזי טיפוס

מה שמיוחד בזה הוא שבלי Azure MCP, היית מקבל קוד Blob Storage כללי שעשוי לעבוד אבל לא עוקב אחרי דפוסי Azure העדכניים. עם Azure MCP, אתה מקבל קוד שמנצל את שיטות האימות החדשות, מטפל בתרחישי שגיאות ספציפיים ל-Azure ועוקב אחרי ההמלצות של מיקרוסופט לאפליקציות פרודקשן.

**דוגמה בולטת**: התקשיתי לזכור את הפקודות המדויקות של ה-CLI של `az` ו-`azd` לשימוש חד-פעמי. תמיד זה תהליך דו-שלבי בשבילי: קודם מחפש את התחביר, ואז מריץ את הפקודה. לעיתים אני פשוט נכנס לפורטל ומקליק כדי לסיים את העבודה כי אני לא רוצה להודות שאני לא זוכר את התחביר של ה-CLI. היכולת פשוט לתאר מה אני רוצה היא מדהימה, ועוד יותר טוב לעשות את זה בלי לצאת מה-IDE שלי!

יש רשימה מצוינת של מקרי שימוש ב-[מאגר Azure MCP](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) כדי להתחיל. למדריכים מקיפים והגדרות מתקדמות, עיין ב-[התיעוד הרשמי של Azure MCP](https://learn.microsoft.com/azure/developer/azure-mcp-server/).

### 3. 🐙 שרת GitHub MCP

[![התקן ב-VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![התקן ב-VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**מה זה עושה**: שרת GitHub MCP הרשמי מספק אינטגרציה חלקה עם כל האקוסיסטם של GitHub, ומציע גם גישה מרוחקת מתארחת וגם אפשרויות פריסה מקומית באמצעות Docker. זה לא רק פעולות בסיסיות על מאגרים – זו ערכת כלים מקיפה שכוללת ניהול GitHub Actions, זרימות עבודה של pull requests, מעקב אחרי בעיות, סריקות אבטחה, התראות ויכולות אוטומציה מתקדמות.

**למה זה שימושי**: השרת הזה משנה את האופן שבו אתה מתקשר עם GitHub על ידי הבאת חוויית הפלטפורמה המלאה ישירות לסביבת הפיתוח שלך. במקום לעבור כל הזמן בין VS Code ל-GitHub.com לניהול פרויקטים, סקירות קוד ומעקב CI/CD, אתה יכול לטפל בכל זה באמצעות פקודות בשפה טבעית תוך כדי שמירה על ריכוז בקוד שלך.

> **ℹ️ הערה: סוגים שונים של 'סוכנים'**
> 
> אל תבלבל בין שרת GitHub MCP הזה לבין GitHub Coding Agent (הסוכן AI שניתן להקצות לו בעיות למשימות קידוד אוטומטיות). שרת GitHub MCP פועל במצב Agent של VS Code כדי לספק אינטגרציה עם GitHub API, בעוד ש-GitHub Coding Agent הוא תכונה נפרדת שיוצרת pull requests כשמוקצה לבעיות ב-GitHub.

**יכולות מרכזיות כוללות**:
- **⚙️ GitHub Actions**: ניהול מלא של צינורות CI/CD, מעקב אחרי זרימות עבודה וטיפול בארטיפקטים
- **🔀 Pull Requests**: יצירה, סקירה, מיזוג וניהול PRs עם מעקב סטטוס מקיף
- **🐛 Issues**: ניהול מחזור חיים מלא של בעיות, תגובות, תיוגים והקצאות
- **🔒 אבטחה**: התראות סריקת קוד, גילוי סודות ואינטגרציה עם Dependabot
- **🔔 התראות**: ניהול חכם של התראות ושליטה במנוי למאגרים
- **📁 ניהול מאגרים**: פעולות על קבצים, ניהול סניפים ומינהל מאגרים
- **👥 שיתוף פעולה**: חיפוש משתמשים וארגונים, ניהול צוותים ושליטה בגישה

**שימוש במציאות**: "צור pull request מהסניף feature שלי", "הראה לי את כל ריצות ה-CI שנכשלו השבוע", "רשום את כל התראות האבטחה הפתוחות במאגרים שלי", או "מצא את כל הבעיות שהוקצו לי בכל הארגונים שלי"

**תסריט הדגמה מלא**: הנה זרימת עבודה עוצמתית שמדגימה את יכולות שרת GitHub MCP:

> "אני צריך להתכונן לסקירת הספרינט שלנו. הראה לי את כל ה-pull requests שיצרתי השבוע, בדוק את מצב צינורות ה-CI/CD שלנו, צור סיכום של כל התראות האבטחה שצריך לטפל בהן, ועזור לי לנסח הערות שחרור על בסיס PRs ממוזגים עם התג 'feature'."

שרת GitHub MCP יבצע:
- שאילתת pull requests אחרונים עם מידע מפורט על הסטטוס
- ניתוח ריצות זרימות עבודה והדגשת כשלונות או בעיות ביצועים
- איסוף תוצאות סריקות אבטחה ותעדוף התראות קריטיות
- יצירת הערות שחרור מקיפות על ידי חילוץ מידע מ-PRs ממוזגים
- מתן צעדים מעשיים לתכנון ספרינט והכנת שחרור

**דוגמה בולטת**: אני אוהב להשתמש בזה לזרימות עבודה של סקירת קוד. במקום לקפוץ בין VS Code, התראות GitHub ודפי pull request, אני יכול לומר "הראה לי את כל ה-PRs שמחכים לסקירה שלי" ואז "הוסף תגובה ל-PR #123 לגבי טיפול השגיאות בשיטת האימות." השרת מטפל בקריאות ל-GitHub API, שומר על הקשר בדיון ואפילו עוזר לי לנסח תגובות סקירה בונות יותר.

**אפשרויות אימות**: השרת תומך גם ב-OAuth (שקוף ב-VS Code) וגם ב-Personal Access Tokens, עם ערכות כלים שניתן להגדיר כדי לאפשר רק את הפונקציונליות של GitHub שאתה צריך. אפשר להריץ אותו כשירות מרוחק מתארח להתקנה מיידית או מקומית דרך Docker לשליטה מלאה.

> **💡 טיפ מקצועי**
> 
> אפשר להפעיל רק את ערכות הכלים שאתה צריך על ידי הגדרת הפרמטר `--toolsets` בהגדרות שרת MCP שלך כדי לצמצם את גודל ההקשר ולשפר את בחירת כלי ה-AI. לדוגמה, הוסף `"--toolsets", "repos,issues,pull_requests,actions"` לארגומנטים של ההגדרה שלך לזרימות עבודה מרכזיות בפיתוח, או השתמש ב-`"--toolsets", "notifications, security"` אם אתה רוצה בעיקר יכולות מעקב GitHub.

### 4. 🔄 שרת Azure DevOps MCP

[![התקן ב-VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![התקן ב-VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**מה זה עושה**: מתחבר לשירותי Azure DevOps לניהול פרויקטים מקיף, מעקב אחרי work items, ניהול צינורות build ופעולות על מאגרים.

**למה זה שימושי**: עבור צוותים שמשתמשים ב-Azure DevOps כפלטפורמת DevOps עיקרית, שרת MCP זה מבטל את הצורך לעבור כל הזמן בין סביבת הפיתוח לממשק האינטרנטי של Azure DevOps. אפשר לנהל work items, לבדוק סטטוס build, לשאול מאגרים ולטפל במשימות ניהול פרויקטים ישירות מהעוזר ה-AI שלך.

**שימוש במציאות**: "הראה לי את כל ה-work items הפעילים בספרינט הנוכחי עבור פרויקט WebApp", "צור דוח באג לבעיה בכניסה שמצאתי עכשיו", או "בדוק את מצב צינורות ה-build שלנו והראה לי כל כשלון אחרון"

**דוגמה בולטת**: אפשר בקלות לבדוק את מצב הספרינט הנוכחי של הצוות עם שאילתה פשוטה כמו "הראה לי את כל ה-work items הפעילים בספרינט הנוכחי עבור פרויקט WebApp" או "צור דוח באג לבעיה בכניסה שמצאתי עכשיו" בלי לצאת מסביבת הפיתוח.

### 5. 📝 שרת MarkItDown MCP
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**מה זה עושה**: MarkItDown הוא שרת המרת מסמכים מקיף שממיר פורמטים שונים של קבצים ל-Markdown איכותי, מותאם לצריכת LLM ולזרימות עבודה של ניתוח טקסט.

**למה זה שימושי**: חיוני לזרימות עבודה מודרניות של תיעוד! MarkItDown מטפל במגוון מרשים של פורמטים תוך שמירה על מבנה המסמך הקריטי כמו כותרות, רשימות, טבלאות וקישורים. בניגוד לכלי חילוץ טקסט פשוטים, הוא מתמקד בשמירה על המשמעות הסמנטית והעיצוב החשובים הן לעיבוד בינה מלאכותית והן לקריאות אנושית.

**פורמטים נתמכים**:
- **מסמכי Office**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **קבצי מדיה**: תמונות (עם מטא-דאטה EXIF ו-OCR), אודיו (עם מטא-דאטה EXIF ותמלול דיבור)
- **תוכן אינטרנט**: HTML, פידים RSS, כתובות YouTube, דפי ויקיפדיה
- **פורמטי נתונים**: CSV, JSON, XML, קבצי ZIP (מעבד תוכן רקורסיבית)
- **פורמטים להוצאה לאור**: EPub, מחברות Jupyter (.ipynb)
- **אימייל**: הודעות Outlook (.msg)
- **מתקדם**: אינטגרציה עם Azure Document Intelligence לעיבוד PDF משופר

**יכולות מתקדמות**: MarkItDown תומך בתיאורי תמונות מבוססי LLM (כאשר מסופק לקוח OpenAI), Azure Document Intelligence לעיבוד PDF משופר, תמלול אודיו לתוכן דיבור, ומערכת תוספים להרחבה לפורמטים נוספים.

**שימוש בעולם האמיתי**: "המר מצגת PowerPoint זו ל-Markdown עבור אתר התיעוד שלנו", "חלץ טקסט מה-PDF הזה עם מבנה כותרות תקין", או "המר גיליון Excel זה לפורמט טבלה קריא".

**דוגמה מובלטת**: לציטוט מתוך [תיעוד MarkItDown](https://github.com/microsoft/markitdown#why-markdown):

> Markdown קרוב מאוד לטקסט פשוט, עם מינימום סימון או עיצוב, אך עדיין מספק דרך לייצג מבנה מסמך חשוב. מודלים מרכזיים של LLM, כמו GPT-4o של OpenAI, "מדברים" Markdown באופן טבעי, ולעיתים משלבים Markdown בתשובותיהם ללא בקשה. זה מרמז שהם אומנו על כמויות עצומות של טקסט בפורמט Markdown, ומבינים אותו היטב. כתוספת, קונבנציות Markdown גם מאוד יעילות מבחינת טוקנים.

MarkItDown מצטיין בשמירה על מבנה המסמך, דבר חשוב לזרימות עבודה של בינה מלאכותית. לדוגמה, בהמרת מצגת PowerPoint, הוא שומר על ארגון השקופיות עם הכותרות הנכונות, מחלץ טבלאות כטבלאות Markdown, כולל טקסט חלופי לתמונות, ואפילו מעבד את הערות הדובר. תרשימים מומרות לטבלאות נתונים קריאות, וה-Markdown המתקבל שומר על הזרימה הלוגית של המצגת המקורית. זה מושלם להזנת תוכן מצגות למערכות AI או ליצירת תיעוד מהשקופיות הקיימות.

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**מה זה עושה**: מספק גישה שיחתית למסדי נתונים של SQL Server (במקום, Azure SQL או Fabric)

**למה זה שימושי**: דומה לשרת PostgreSQL אך עבור מערכת Microsoft SQL. התחבר עם מחרוזת חיבור פשוטה והתחל לשאול בשפה טבעית – בלי לעבור בין הקשרים!

**שימוש בעולם האמיתי**: "מצא את כל ההזמנות שלא בוצעו ב-30 הימים האחרונים" מתורגם לשאילתות SQL מתאימות ומחזיר תוצאות מעוצבות.

**דוגמה מובלטת**: לאחר הגדרת חיבור למסד הנתונים, אפשר להתחיל לנהל שיחות עם הנתונים מיד. הפוסט בבלוג מדגים זאת עם שאלה פשוטה: "לאיזה מסד נתונים אתה מחובר?" שרת MCP מגיב על ידי קריאה לכלי המתאים למסד הנתונים, מתחבר למופע SQL Server שלך ומחזיר פרטים על חיבור המסד הנוכחי – הכל בלי לכתוב שורת SQL אחת. השרת תומך בפעולות מסד נתונים מקיפות, מניהול סכמות ועד מניפולציית נתונים, הכל דרך פקודות בשפה טבעית. להוראות התקנה מלאות ודוגמאות קונפיגורציה עם VS Code ו-Claude Desktop, ראו: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/).

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**מה זה עושה**: מאפשר לסוכני AI לתקשר עם דפי אינטרנט לצורך בדיקות ואוטומציה

> **ℹ️ מפעיל את GitHub Copilot**
> 
> שרת Playwright MCP מפעיל את סוכן הקידוד של GitHub Copilot, ומעניק לו יכולות גלישה באינטרנט! [למידע נוסף על תכונה זו](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).

**למה זה שימושי**: מושלם לבדיקות אוטומטיות המונעות מתיאורים בשפה טבעית. AI יכול לנווט באתרים, למלא טפסים ולחלץ נתונים דרך צילומי מצב נגישות מובנים – זה כלי עוצמתי במיוחד!

**שימוש בעולם האמיתי**: "בדוק את תהליך ההתחברות ואמת שהלוח הראשי נטען כראוי" או "צור בדיקה שמחפשת מוצרים ומאמתת את דף התוצאות" – הכל בלי צורך בקוד המקור של האפליקציה.

**דוגמה מובלטת**: עמיתתי Debbie O'Brien עושה עבודה מדהימה עם Playwright MCP Server לאחרונה! למשל, היא הראתה לאחרונה איך אפשר ליצור בדיקות Playwright שלמות בלי גישה לקוד המקור של האפליקציה. בתרחיש שלה, ביקשה מ-Copilot ליצור בדיקה לאפליקציית חיפוש סרטים: לנווט לאתר, לחפש "Garfield", ולאמת שהסרט מופיע בתוצאות. ה-MCP הפעל סשן דפדפן, חקר את מבנה הדף באמצעות צילומי DOM, זיהה את הסלקטורים הנכונים, ויצר בדיקת TypeScript עובדת במלואה שעברה בהצלחה מהריצה הראשונה.

מה שהופך את זה לעוצמתי במיוחד הוא שהוא גשר בין הוראות בשפה טבעית לקוד בדיקה שניתן להריץ. גישות מסורתיות דורשות כתיבת בדיקות ידנית או גישה לקוד המקור להקשר. אבל עם Playwright MCP, אפשר לבדוק אתרים חיצוניים, אפליקציות לקוח, או לעבוד בתרחישי בדיקות "קופסה שחורה" ללא גישה לקוד.

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**מה זה עושה**: מנהל סביבות Microsoft Dev Box דרך שפה טבעית

**למה זה שימושי**: מפשט מאוד את ניהול סביבות הפיתוח! צור, קונפג ונהל סביבות פיתוח בלי לזכור פקודות ספציפיות.

**שימוש בעולם האמיתי**: "הקם Dev Box חדש עם ה-SDK האחרון של .NET וקונפג אותו לפרויקט שלנו", "בדוק את מצב כל סביבות הפיתוח שלי", או "צור סביבה דמו סטנדרטית למצגות הצוות שלנו".

**דוגמה מובלטת**: אני מעריך מאוד את השימוש ב-Dev Box לפיתוח אישי. הרגע שבו הבנתי את זה היה כש-James Montemagno הסביר כמה Dev Box מצוין לדמו בכנסים, כי יש לו חיבור את'רנט מהיר במיוחד בלי קשר ל-WiFi של הכנס/מלון/מטוס שבו אני נמצא. למעשה, לאחרונה עשיתי תרגול דמו בכנס בזמן שהמחשב שלי היה מחובר לנקודת חיבור של הטלפון שלי בנסיעה באוטובוס מברוז' לאנטוורפן! אבל הצעד הבא שלי הוא להעמיק בניהול צוות עם סביבות פיתוח מרובות וסביבות דמו סטנדרטיות. ומקרה שימוש נוסף ששמעתי מלקוחות ועמיתים הוא כמובן שימוש ב-Dev Box לסביבות פיתוח מוכנות מראש. בשני המקרים, שימוש ב-MCP לקונפיגורציה וניהול Dev Boxes מאפשר אינטראקציה בשפה טבעית, תוך כדי הישארות בסביבת הפיתוח שלך.

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**מה זה עושה**: שרת Azure AI Foundry MCP מספק למפתחים גישה מקיפה לאקוסיסטם ה-AI של Azure, כולל קטלוגי מודלים, ניהול פריסות, אינדוקס ידע עם Azure AI Search וכלי הערכה. שרת ניסיוני זה מהווה גשר בין פיתוח AI לתשתית החזקה של Azure AI, ומקל על בנייה, פריסה והערכת יישומי AI.

**למה זה שימושי**: השרת משנה את אופן העבודה עם שירותי Azure AI על ידי הבאת יכולות AI ברמת ארגונית ישירות לתהליך הפיתוח שלך. במקום לעבור בין פורטל Azure, תיעוד ו-IDE, תוכל לגלות מודלים, לפרוס שירותים, לנהל מאגרי ידע ולהעריך ביצועי AI באמצעות פקודות בשפה טבעית. זה חזק במיוחד למפתחים שבונים יישומי RAG (Retrieval-Augmented Generation), מנהלים פריסות מרובות מודלים או מיישמים צינורות הערכה מקיפים ל-AI.

**יכולות מפתח למפתחים**:
- **🔍 גילוי ופריסת מודלים**: חקור את קטלוג המודלים של Azure AI Foundry, קבל מידע מפורט עם דוגמאות קוד, ופרוס מודלים לשירותי Azure AI
- **📚 ניהול ידע**: צור ונהל אינדקסים ב-Azure AI Search, הוסף מסמכים, הגדר אינדקסרים ובנה מערכות RAG מתקדמות
- **⚡ אינטגרציה עם סוכני AI**: התחבר לסוכני Azure AI, שאול סוכנים קיימים והערך ביצועים בתרחישי ייצור
- **📊 מסגרת הערכה**: הרץ הערכות טקסט וסוכנים מקיפות, הפק דוחות ב-Markdown ויישם בקרת איכות ליישומי AI
- **🚀 כלי פרוטוטייפינג**: קבל הוראות התקנה לפרוטוטייפינג מבוסס GitHub וגישה ל-Azure AI Foundry Labs למחקר מתקדם במודלים

**שימוש מעשי במפתחים**: "פרוס מודל Phi-4 לשירותי Azure AI עבור היישום שלי", "צור אינדקס חיפוש חדש למערכת RAG של התיעוד שלי", "הערך את תגובות הסוכן שלי מול מדדי איכות", או "מצא את מודל ההסקה הטוב ביותר למשימות הניתוח המורכבות שלי"

**תסריט הדגמה מלא**: הנה תהליך פיתוח AI עוצמתי:


> "אני בונה סוכן תמיכה ללקוחות. עזור לי למצוא מודל הסקה טוב בקטלוג, לפרוס אותו לשירותי Azure AI, ליצור מאגר ידע מהתיעוד שלנו, להקים מסגרת הערכה לבדיקת איכות התגובות, ואז לעזור לי לפרוטוטייפ את האינטגרציה עם טוקן GitHub לבדיקה."

שרת Azure AI Foundry MCP יבצע:
- שאילת קטלוג המודלים להמלצה על מודלי הסקה מיטביים בהתאם לדרישותיך
- יספק פקודות פריסה ומידע על מכסות לאזור Azure המועדף עליך
- יקים אינדקסים ב-Azure AI Search עם סכימה מתאימה לתיעוד שלך
- יגדיר צינורות הערכה עם מדדי איכות ובדיקות בטיחות
- יפיק קוד פרוטוטייפינג עם אימות GitHub לבדיקות מיידיות
- יספק מדריכי התקנה מקיפים המותאמים לערכת הטכנולוגיה שלך

**דוגמה בולטת**: כמפתח, התקשיתי לעקוב אחרי מודלי LLM השונים הזמינים. אני מכיר כמה עיקריים, אבל הרגשתי שאני מפספס שיפורי פרודוקטיביות ויעילות. ניהול טוקנים ומכסות מלחיץ וקשה – אף פעם לא בטוח אם בחרתי במודל הנכון למשימה או מבזבז תקציב בצורה לא יעילה. שמעתי על שרת MCP הזה מג'יימס מונטמאגנו כשבדקתי המלצות עם חברי צוות, ואני נרגש להתחיל להשתמש בו! יכולות גילוי המודלים נראות מרשימות במיוחד למי כמוני שרוצה לחקור מעבר למודלים הרגילים ולמצוא מודלים מותאמים למשימות ספציפיות. מסגרת ההערכה תעזור לי לוודא שאני באמת משיג תוצאות טובות יותר, ולא רק מנסה משהו חדש לשם הניסיון.

> **ℹ️ סטטוס ניסיוני**
> 
> שרת MCP זה הוא ניסיוני ומתפתח באופן פעיל. תכונות ו-APIs עשויים להשתנות. מתאים לחקר יכולות Azure AI ולבניית פרוטוטייפים, אך יש לבדוק דרישות יציבות לשימוש בייצור.

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**מה זה עושה**: מספק למפתחים כלים חיוניים לבניית סוכני AI ויישומים שמשתלבים עם Microsoft 365 ו-Microsoft 365 Copilot, כולל אימות סכימות, קבלת דוגמאות קוד וסיוע בפתרון תקלות.

**למה זה שימושי**: פיתוח עבור Microsoft 365 ו-Copilot כולל סכימות מורכבות ודפוסי פיתוח ספציפיים. שרת MCP זה מביא משאבי פיתוח חיוניים ישירות לסביבת הקוד שלך, ועוזר לאמת סכימות, למצוא דוגמאות קוד ולפתור בעיות נפוצות בלי צורך לעיין בתיעוד כל הזמן.

**שימוש מעשי**: "אמת את המניפסט הדקלרטיבי של הסוכן שלי ותתקן שגיאות סכימה", "הראה לי דוגמאות קוד ליישום תוסף Microsoft Graph API", או "עזור לי לפתור בעיות אימות באפליקציית Teams שלי"

**דוגמה בולטת**: פניתי לחברי ג'ון מילר אחרי שדיברנו ב-Build על סוכני M365, והוא המליץ על MCP הזה. זה יכול להיות מצוין למפתחים חדשים לסוכני M365 כי הוא מספק תבניות, דוגמאות קוד ותשתית התחלתית בלי לטבוע בתיעוד. יכולות אימות הסכימות נראות שימושיות במיוחד למניעת שגיאות במבנה המניפסט שיכולות לגרום לשעות של דיבוג.

> **💡 טיפ מקצועי**
> 
> השתמש בשרת זה יחד עם שרת MCP של Microsoft Learn Docs לתמיכה מקיפה בפיתוח M365 – האחד מספק את התיעוד הרשמי והשני מציע כלים מעשיים לפיתוח וסיוע בפתרון תקלות.

## מה הלאה? 🔮

## 📋 סיכום

פרוטוקול Model Context (MCP) משנה את האופן שבו מפתחים מתקשרים עם עוזרי AI וכלים חיצוניים. עשרת שרתי ה-MCP של מיקרוסופט הללו מדגימים את כוח האינטגרציה הסטנדרטית של AI, ומאפשרים זרימות עבודה חלקות ששומרות על ריכוז המפתחים תוך גישה ליכולות חיצוניות עוצמתיות.

מהאינטגרציה המקיפה של אקוסיסטם Azure ועד לכלים מיוחדים כמו Playwright לאוטומציה בדפדפן ו-MarkItDown לעיבוד מסמכים, שרתים אלו מראים כיצד MCP יכול לשפר את הפרודוקטיביות במגוון תרחישי פיתוח. הפרוטוקול הסטנדרטי מבטיח שכלים אלו עובדים יחד בהרמוניה, ויוצרים חוויית פיתוח מגובשת.

ככל שאקוסיסטם MCP ממשיך להתפתח, חשוב להישאר מעורב בקהילה, לחקור שרתים חדשים ולבנות פתרונות מותאמים אישית כדי למקסם את הפרודוקטיביות שלך. הטבע הפתוח של MCP מאפשר לך לשלב כלים מספקים שונים ליצירת זרימת עבודה מושלמת לצרכים הספציפיים שלך.

## 🔗 משאבים נוספים

- [מאגר MCP הרשמי של מיקרוסופט](https://github.com/microsoft/mcp)
- [קהילת MCP ותיעוד](https://modelcontextprotocol.io/introduction)
- [תיעוד MCP ל-VS Code](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [תיעוד MCP ל-Visual Studio](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [תיעוד Azure MCP](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [בואו נלמד – אירועי MCP](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [התאמות אישיות מדהימות ל-GitHub Copilot](https://github.com/awesome-copilot)
- [SDK MCP ל-C#](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [ימי פיתוח MCP בשידור חי 29/30 ביולי או צפייה לפי דרישה](https://aka.ms/mcpdevdays)

## 🎯 תרגילים

1. **התקנה וקונפיגורציה**: התקן אחד משרתי MCP בסביבת VS Code שלך ובדוק פונקציונליות בסיסית.
2. **אינטגרציית זרימת עבודה**: עצב זרימת עבודה שמשלבת לפחות שלושה שרתי MCP שונים.
3. **תכנון שרת מותאם אישית**: זהה משימה בשגרת הפיתוח היומית שלך שיכולה להרוויח משרת MCP מותאם וכתוב מפרט עבורו.
4. **ניתוח ביצועים**: השווה את היעילות של שימוש בשרתי MCP לעומת גישות מסורתיות למשימות פיתוח נפוצות.
5. **הערכת אבטחה**: הערך את ההשלכות האבטחתיות של שימוש בשרתי MCP בסביבת הפיתוח שלך והצע שיטות עבודה מומלצות.

Next:[Best Practices](../08-BestPractices/README.md)

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש לקחת בחשבון כי תרגומים אוטומטיים עלולים להכיל שגיאות או אי-דיוקים. המסמך המקורי בשפת המקור שלו נחשב למקור הסמכותי. למידע קריטי מומלץ להשתמש בתרגום מקצועי על ידי מתרגם אנושי. אנו לא נושאים באחריות לכל אי-הבנה או פרשנות שגויה הנובעת משימוש בתרגום זה.