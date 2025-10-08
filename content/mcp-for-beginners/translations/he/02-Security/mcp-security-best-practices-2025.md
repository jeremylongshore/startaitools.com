<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "057dd5cc6bea6434fdb788e6c93f3f3d",
  "translation_date": "2025-08-18T16:49:39+00:00",
  "source_file": "02-Security/mcp-security-best-practices-2025.md",
  "language_code": "he"
}
-->
# עדכון שיטות אבטחה MCP - אוגוסט 2025

> **חשוב**: מסמך זה משקף את דרישות האבטחה העדכניות ביותר של [MCP Specification 2025-06-18](https://spec.modelcontextprotocol.io/specification/2025-06-18/) ואת [שיטות האבטחה המומלצות של MCP](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices). תמיד יש להסתמך על המפרט הנוכחי לקבלת ההנחיות המעודכנות ביותר.

## שיטות אבטחה חיוניות ליישומי MCP

פרוטוקול Model Context מציג אתגרי אבטחה ייחודיים החורגים מעבר לאבטחת תוכנה מסורתית. שיטות אלו מתמודדות עם דרישות אבטחה בסיסיות ואיומים ספציפיים ל-MCP, כולל הזרקת פקודות, הרעלת כלים, חטיפת סשנים, בעיות "סגן מבולבל" ופגיעויות העברת טוקנים.

### **דרישות אבטחה חובה**

**דרישות קריטיות מתוך מפרט MCP:**

> **אסור**: שרתי MCP **אסור** שיקבלו טוקנים שלא הונפקו במפורש עבור שרת MCP  
>  
> **חובה**: שרתי MCP המיישמים הרשאות **חייבים** לאמת את כל הבקשות הנכנסות  
>  
> **אסור**: שרתי MCP **אסור** שישתמשו בסשנים לצורך אימות  
>  
> **חובה**: שרתי פרוקסי MCP המשתמשים ב-Client IDs סטטיים **חייבים** לקבל הסכמה מהמשתמש עבור כל לקוח שנרשם באופן דינמי  

---

## 1. **אבטחת טוקנים ואימות**

**בקרות אימות והרשאה:**
   - **סקירת הרשאות קפדנית**: ערכו ביקורות מקיפות על לוגיקת ההרשאות של שרת MCP כדי להבטיח שרק משתמשים ולקוחות מורשים יוכלו לגשת למשאבים  
   - **שילוב ספקי זהות חיצוניים**: השתמשו בספקי זהות מבוססים כמו Microsoft Entra ID במקום ליישם פתרונות אימות מותאמים אישית  
   - **אימות קהל הטוקנים**: תמיד ודאו שטוקנים הונפקו במפורש עבור שרת MCP שלכם - לעולם אל תקבלו טוקנים ממעלה הזרם  
   - **ניהול מחזור חיים נכון של טוקנים**: יישמו מדיניות סיבוב טוקנים, תוקף, ומנעו התקפות שחזור טוקנים  

**אחסון טוקנים מוגן:**
   - השתמשו ב-Azure Key Vault או מאגרי אישורים מאובטחים דומים לכל הסודות  
   - יישמו הצפנה לטוקנים הן במצב מנוחה והן במעבר  
   - סיבוב אישורים קבוע ומעקב אחר גישה לא מורשית  

## 2. **ניהול סשנים ואבטחת תעבורה**

**שיטות סשן מאובטחות:**
   - **מזהי סשן מאובטחים קריפטוגרפית**: השתמשו במזהי סשן מאובטחים ולא דטרמיניסטיים שנוצרו עם מחוללי מספרים אקראיים מאובטחים  
   - **קישוריות ספציפית למשתמש**: קשרו מזהי סשן לזהויות משתמש בפורמטים כמו `<user_id>:<session_id>` כדי למנוע ניצול סשנים בין משתמשים  
   - **ניהול מחזור חיים של סשנים**: יישמו תוקף, סיבוב וביטול נכונים כדי לצמצם חלונות פגיעות  
   - **אכיפת HTTPS/TLS**: חובה להשתמש ב-HTTPS לכל התקשורת כדי למנוע יירוט מזהי סשן  

**אבטחת שכבת תעבורה:**
   - הגדירו TLS 1.3 במידת האפשר עם ניהול תעודות נכון  
   - יישמו הצמדת תעודות עבור חיבורים קריטיים  
   - סיבוב תעודות קבוע ואימות תוקף  

## 3. **הגנה מפני איומים ספציפיים ל-AI** 🤖

**הגנה מפני הזרקת פקודות:**
   - **Microsoft Prompt Shields**: פרסו Prompt Shields של Microsoft לזיהוי מתקדם וסינון של הוראות זדוניות  
   - **ניקוי קלט**: ודאו ונקו את כל הקלטים כדי למנוע התקפות הזרקה ובעיות "סגן מבולבל"  
   - **גבולות תוכן**: השתמשו במערכות מפריד וסימון נתונים כדי להבחין בין הוראות אמינות לתוכן חיצוני  

**מניעת הרעלת כלים:**
   - **אימות מטא-נתונים של כלים**: יישמו בדיקות שלמות עבור הגדרות כלים ומעקב אחר שינויים בלתי צפויים  
   - **מעקב דינמי אחר כלים**: עקבו אחר התנהגות בזמן ריצה והגדירו התראות עבור דפוסי ביצוע בלתי צפויים  
   - **תהליכי אישור**: דרשו אישור מפורש מהמשתמש עבור שינויים בכלים וביכולות  

## 4. **בקרת גישה והרשאות**

**עקרון המינימום ההכרחי:**
   - העניקו לשרתי MCP רק את ההרשאות המינימליות הנדרשות לפונקציונליות המיועדת  
   - יישמו בקרת גישה מבוססת תפקידים (RBAC) עם הרשאות מדויקות  
   - ערכו סקירות הרשאות קבועות ומעקב מתמשך אחר הסלמת הרשאות  

**בקרות הרשאות בזמן ריצה:**
   - יישמו מגבלות משאבים כדי למנוע התקפות מיצוי משאבים  
   - השתמשו בבידוד מכולות עבור סביבות ביצוע כלים  
   - יישמו גישה לפי דרישה עבור פונקציות ניהוליות  

## 5. **בטיחות תוכן ומעקב**

**יישום בטיחות תוכן:**
   - **שילוב Azure Content Safety**: השתמשו ב-Azure Content Safety לזיהוי תוכן מזיק, ניסיונות פריצה למדיניות, והפרות מדיניות  
   - **ניתוח התנהגותי**: יישמו מעקב התנהגותי בזמן ריצה לזיהוי אנומליות בשרת MCP ובביצוע כלים  
   - **רישום מקיף**: רשמו את כל ניסיונות האימות, הפעלת כלים ואירועי אבטחה עם אחסון מאובטח ועמיד בפני שינויים  

**מעקב מתמשך:**
   - התראות בזמן אמת עבור דפוסים חשודים וניסיונות גישה לא מורשים  
   - שילוב עם מערכות SIEM לניהול מרכזי של אירועי אבטחה  
   - ערכו ביקורות אבטחה קבועות ובדיקות חדירה ליישומי MCP  

## 6. **אבטחת שרשרת אספקה**

**אימות רכיבים:**
   - **סריקת תלות**: השתמשו בסריקות פגיעות אוטומטיות עבור כל תלות התוכנה ורכיבי AI  
   - **אימות מקור**: ודאו את המקור, הרישוי והשלמות של מודלים, מקורות נתונים ושירותים חיצוניים  
   - **חבילות חתומות**: השתמשו בחבילות חתומות קריפטוגרפית ואמתו חתימות לפני פריסה  

**צינור פיתוח מאובטח:**
   - **GitHub Advanced Security**: יישמו סריקת סודות, ניתוח תלות וניתוח סטטי עם CodeQL  
   - **אבטחת CI/CD**: שלבו אימותי אבטחה לאורך צינורות פריסה אוטומטיים  
   - **שלמות ארטיפקטים**: יישמו אימות קריפטוגרפי עבור ארטיפקטים וקונפיגורציות שפורסמו  

## 7. **אבטחת OAuth ומניעת "סגן מבולבל"**

**יישום OAuth 2.1:**
   - **יישום PKCE**: השתמשו ב-Proof Key for Code Exchange (PKCE) עבור כל בקשות ההרשאה  
   - **הסכמה מפורשת**: קבלו הסכמה מהמשתמש עבור כל לקוח שנרשם באופן דינמי כדי למנוע התקפות "סגן מבולבל"  
   - **אימות URI להפניה**: יישמו אימות קפדני של URI להפניה ומזהי לקוח  

**אבטחת פרוקסי:**
   - מנעו עקיפת הרשאות דרך ניצול מזהי לקוח סטטיים  
   - יישמו תהליכי הסכמה נכונים עבור גישה ל-API של צד שלישי  
   - עקבו אחר גניבת קודי הרשאה וגישה לא מורשית ל-API  

## 8. **תגובה לאירועים והתאוששות**

**יכולות תגובה מהירה:**
   - **תגובה אוטומטית**: יישמו מערכות אוטומטיות לסיבוב אישורים והכלה של איומים  
   - **נהלי חזרה לאחור**: יכולת לחזור במהירות לקונפיגורציות ורכיבים ידועים כטובים  
   - **יכולות פורנזיות**: עקבות ביקורת מפורטות ורישום לצורך חקירת אירועים  

**תקשורת ותיאום:**
   - נהלי הסלמה ברורים עבור אירועי אבטחה  
   - שילוב עם צוותי תגובה לאירועים בארגון  
   - סימולציות אירועי אבטחה ותרגילי שולחן קבועים  

## 9. **ציות וממשל**

**ציות רגולטורית:**
   - ודאו שיישומי MCP עומדים בדרישות ספציפיות לתעשייה (GDPR, HIPAA, SOC 2)  
   - יישמו בקרות סיווג נתונים ופרטיות עבור עיבוד נתוני AI  
   - שמרו על תיעוד מקיף לצורך ביקורת ציות  

**ניהול שינויים:**
   - תהליכי סקירת אבטחה פורמליים עבור כל שינויי מערכת MCP  
   - בקרת גרסאות ותהליכי אישור עבור שינויים בקונפיגורציה  
   - הערכות ציות קבועות וניתוח פערים  

## 10. **בקרות אבטחה מתקדמות**

**ארכיטקטורת Zero Trust:**
   - **לעולם אל תסמוך, תמיד תוודא**: אימות מתמשך של משתמשים, מכשירים וחיבורים  
   - **מיקרו-סגמנטציה**: בקרות רשת גרעיניות המבודדות רכיבי MCP בודדים  
   - **גישה מותנית**: בקרות גישה מבוססות סיכון המותאמות להקשר והתנהגות נוכחיים  

**הגנת יישומים בזמן ריצה:**
   - **Runtime Application Self-Protection (RASP)**: פרסו טכניקות RASP לזיהוי איומים בזמן אמת  
   - **מעקב ביצועי יישומים**: עקבו אחר אנומליות ביצועים שעשויות להצביע על התקפות  
   - **מדיניות אבטחה דינמית**: יישמו מדיניות אבטחה המותאמת על בסיס נוף האיומים הנוכחי  

## 11. **שילוב אקוסיסטם אבטחה של Microsoft**

**אבטחה מקיפה של Microsoft:**
   - **Microsoft Defender for Cloud**: ניהול מצב אבטחת ענן עבור עומסי עבודה של MCP  
   - **Azure Sentinel**: יכולות SIEM ו-SOAR מבוססות ענן לזיהוי מתקדם של איומים  
   - **Microsoft Purview**: ממשל נתונים וציות עבור זרימות עבודה של AI ומקורות נתונים  

**ניהול זהויות וגישה:**
   - **Microsoft Entra ID**: ניהול זהויות ארגוני עם מדיניות גישה מותנית  
   - **Privileged Identity Management (PIM)**: גישה לפי דרישה ותהליכי אישור עבור פונקציות ניהוליות  
   - **Identity Protection**: גישה מותנית מבוססת סיכון ותגובה אוטומטית לאיומים  

## 12. **התפתחות אבטחה מתמשכת**

**להישאר מעודכנים:**
   - **מעקב אחר מפרט**: סקירה קבועה של עדכוני מפרט MCP ושינויים בהנחיות אבטחה  
   - **מודיעין איומים**: שילוב של הזנות איומים ספציפיות ל-AI ומדדי פשרה  
   - **מעורבות בקהילת אבטחה**: השתתפות פעילה בקהילת אבטחת MCP ותוכניות גילוי פגיעויות  

**אבטחה אדפטיבית:**
   - **אבטחת למידת מכונה**: השתמשו בזיהוי אנומליות מבוסס ML לזיהוי דפוסי התקפה חדשים  
   - **אנליטיקה אבטחתית חזויה**: יישמו מודלים חזויים לזיהוי איומים באופן פרואקטיבי  
   - **אוטומציית אבטחה**: עדכוני מדיניות אבטחה אוטומטיים המבוססים על מודיעין איומים ושינויים במפרט  

---

## **משאבי אבטחה קריטיים**

### **תיעוד רשמי של MCP**
- [MCP Specification (2025-06-18)](https://spec.modelcontextprotocol.io/specification/2025-06-18/)  
- [MCP Security Best Practices](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices)  
- [MCP Authorization Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization)  

### **פתרונות אבטחה של Microsoft**
- [Microsoft Prompt Shields](https://learn.microsoft.com/azure/ai-services/content-safety/concepts/jailbreak-detection)  
- [Azure Content Safety](https://learn.microsoft.com/azure/ai-services/content-safety/)  
- [Microsoft Entra ID Security](https://learn.microsoft.com/entra/identity-platform/secure-least-privileged-access)  
- [GitHub Advanced Security](https://github.com/security/advanced-security)  

### **תקני אבטחה**
- [OAuth 2.0 Security Best Practices (RFC 9700)](https://datatracker.ietf.org/doc/html/rfc9700)  
- [OWASP Top 10 for Large Language Models](https://genai.owasp.org/)  
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)  

### **מדריכי יישום**
- [Azure API Management MCP Authentication Gateway](https://techcommunity.microsoft.com/blog/integrationsonazureblog/azure-api-management-your-auth-gateway-for-mcp-servers/4402690)  
- [Microsoft Entra ID with MCP Servers](https://den.dev/blog/mcp-server-auth-entra-id-session/)  

---

> **הודעת אבטחה**: שיטות אבטחת MCP מתפתחות במהירות. תמיד ודאו מול [מפרט MCP הנוכחי](https://spec.modelcontextprotocol.io/) ו[תיעוד האבטחה הרשמי](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices) לפני יישום.

**כתב ויתור**:  
מסמך זה תורגם באמצעות שירות תרגום מבוסס בינה מלאכותית [Co-op Translator](https://github.com/Azure/co-op-translator). למרות שאנו שואפים לדיוק, יש להיות מודעים לכך שתרגומים אוטומטיים עשויים להכיל שגיאות או אי דיוקים. המסמך המקורי בשפתו המקורית צריך להיחשב כמקור סמכותי. עבור מידע קריטי, מומלץ להשתמש בתרגום מקצועי על ידי אדם. איננו נושאים באחריות לאי הבנות או לפרשנויות שגויות הנובעות משימוש בתרגום זה.