<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "c8f283730b5421082ddd26cc85c07831",
  "translation_date": "2025-07-18T11:33:44+00:00",
  "source_file": "07-LessonsfromEarlyAdoption/microsoft-mcp-servers.md",
  "language_code": "th"
}
-->
# 🚀 10 เซิร์ฟเวอร์ Microsoft MCP ที่เปลี่ยนแปลงประสิทธิภาพการทำงานของนักพัฒนา

## 🎯 สิ่งที่คุณจะได้เรียนรู้ในคู่มือนี้

คู่มือเชิงปฏิบัตินี้นำเสนอเซิร์ฟเวอร์ Microsoft MCP จำนวนสิบตัวที่กำลังเปลี่ยนแปลงวิธีการทำงานของนักพัฒนาด้วยผู้ช่วย AI แทนที่จะอธิบายแค่สิ่งที่เซิร์ฟเวอร์ MCP *สามารถ* ทำได้ เราจะแสดงให้คุณเห็นเซิร์ฟเวอร์ที่กำลังสร้างความแตกต่างจริงในกระบวนการพัฒนารายวันที่ Microsoft และที่อื่น ๆ

เซิร์ฟเวอร์แต่ละตัวในคู่มือนี้ถูกคัดเลือกจากการใช้งานจริงและความคิดเห็นของนักพัฒนา คุณจะได้รู้ไม่เพียงแค่ว่าแต่ละเซิร์ฟเวอร์ทำอะไร แต่ยังเข้าใจว่าทำไมมันถึงสำคัญและวิธีใช้ให้เกิดประโยชน์สูงสุดในโปรเจกต์ของคุณ ไม่ว่าคุณจะเป็นมือใหม่กับ MCP หรือกำลังมองหาขยายการตั้งค่าที่มีอยู่ เซิร์ฟเวอร์เหล่านี้เป็นเครื่องมือที่ใช้งานได้จริงและมีผลกระทบสูงในระบบนิเวศของ Microsoft

> **💡 เคล็ดลับเริ่มต้นอย่างรวดเร็ว**
> 
> เพิ่งเริ่มใช้ MCP? ไม่ต้องกังวล! คู่มือนี้ออกแบบมาให้เหมาะกับผู้เริ่มต้น เราจะอธิบายแนวคิดไปพร้อมกัน และคุณสามารถย้อนกลับไปดู [Introduction to MCP](../00-Introduction/README.md) และ [Core Concepts](../01-CoreConcepts/README.md) เพื่อเสริมความเข้าใจได้เสมอ

## ภาพรวม

คู่มือฉบับสมบูรณ์นี้สำรวจเซิร์ฟเวอร์ Microsoft MCP จำนวนสิบตัวที่ปฏิวัติวิธีที่นักพัฒนาสื่อสารกับผู้ช่วย AI และเครื่องมือภายนอก ตั้งแต่การจัดการทรัพยากร Azure ไปจนถึงการประมวลผลเอกสาร เซิร์ฟเวอร์เหล่านี้แสดงให้เห็นพลังของ Model Context Protocol ในการสร้างกระบวนการพัฒนาที่ราบรื่นและมีประสิทธิภาพ

## วัตถุประสงค์การเรียนรู้

เมื่อจบคู่มือนี้ คุณจะสามารถ:
- เข้าใจว่าเซิร์ฟเวอร์ MCP ช่วยเพิ่มประสิทธิภาพการทำงานของนักพัฒนาอย่างไร
- เรียนรู้เกี่ยวกับการใช้งานเซิร์ฟเวอร์ MCP ที่มีผลกระทบสูงของ Microsoft
- ค้นพบกรณีการใช้งานจริงสำหรับแต่ละเซิร์ฟเวอร์
- รู้วิธีตั้งค่าและกำหนดค่าเซิร์ฟเวอร์เหล่านี้ใน VS Code และ Visual Studio
- สำรวจระบบนิเวศ MCP ที่กว้างขึ้นและทิศทางในอนาคต

## 🔧 ทำความเข้าใจเซิร์ฟเวอร์ MCP: คู่มือสำหรับผู้เริ่มต้น

### เซิร์ฟเวอร์ MCP คืออะไร?

ถ้าคุณเป็นมือใหม่กับ Model Context Protocol (MCP) คุณอาจสงสัยว่า: "เซิร์ฟเวอร์ MCP คืออะไร และทำไมฉันต้องสนใจ?" มาเริ่มด้วยการเปรียบเทียบง่าย ๆ

ลองนึกถึงเซิร์ฟเวอร์ MCP เป็นผู้ช่วยเฉพาะทางที่ช่วยให้ผู้ช่วย AI ด้านการเขียนโค้ดของคุณ (เช่น GitHub Copilot) เชื่อมต่อกับเครื่องมือและบริการภายนอก เหมือนกับที่คุณใช้แอปต่าง ๆ บนโทรศัพท์สำหรับงานต่าง ๆ — แอปหนึ่งสำหรับดูสภาพอากาศ แอปหนึ่งสำหรับนำทาง แอปหนึ่งสำหรับธนาคาร — เซิร์ฟเวอร์ MCP ช่วยให้ผู้ช่วย AI ของคุณสามารถโต้ตอบกับเครื่องมือและบริการพัฒนาต่าง ๆ ได้

### ปัญหาที่เซิร์ฟเวอร์ MCP แก้ไข

ก่อนจะมีเซิร์ฟเวอร์ MCP หากคุณต้องการ:
- ตรวจสอบทรัพยากร Azure ของคุณ
- สร้าง GitHub issue
- สืบค้นฐานข้อมูลของคุณ
- ค้นหาข้อมูลในเอกสาร

คุณต้องหยุดเขียนโค้ด เปิดเบราว์เซอร์ ไปยังเว็บไซต์ที่เกี่ยวข้อง และทำงานเหล่านี้ด้วยตนเอง การสลับบริบทบ่อย ๆ แบบนี้ทำให้ขาดสมาธิและลดประสิทธิภาพการทำงาน

### เซิร์ฟเวอร์ MCP เปลี่ยนประสบการณ์การพัฒนาของคุณอย่างไร

ด้วยเซิร์ฟเวอร์ MCP คุณสามารถอยู่ในสภาพแวดล้อมการพัฒนาของคุณ (VS Code, Visual Studio ฯลฯ) และแค่ขอให้ผู้ช่วย AI จัดการงานเหล่านี้ให้ เช่น:

**แทนที่จะทำงานแบบเดิมนี้:**
1. หยุดเขียนโค้ด
2. เปิดเบราว์เซอร์
3. ไปที่พอร์ทัล Azure
4. ดูรายละเอียดบัญชีเก็บข้อมูล
5. กลับมาที่ VS Code
6. เขียนโค้ดต่อ

**คุณสามารถทำแบบนี้ได้:**
1. ถาม AI: "สถานะของบัญชีเก็บข้อมูล Azure ของฉันเป็นอย่างไร?"
2. เขียนโค้ดต่อพร้อมข้อมูลที่ได้รับ

### ประโยชน์หลักสำหรับผู้เริ่มต้น

#### 1. 🔄 **อยู่ในสภาวะโฟกัสของคุณ**
- ไม่ต้องสลับไปมาระหว่างแอปหลายตัว
- รักษาสมาธิที่โค้ดที่คุณกำลังเขียน
- ลดภาระทางจิตใจจากการจัดการเครื่องมือต่าง ๆ

#### 2. 🤖 **ใช้ภาษาธรรมชาติแทนคำสั่งซับซ้อน**
- แทนที่จะจำไวยากรณ์ SQL อธิบายว่าคุณต้องการข้อมูลอะไร
- แทนที่จะจำคำสั่ง Azure CLI อธิบายสิ่งที่คุณต้องการทำ
- ให้ AI จัดการรายละเอียดทางเทคนิคในขณะที่คุณโฟกัสที่ตรรกะ

#### 3. 🔗 **เชื่อมต่อเครื่องมือต่าง ๆ เข้าด้วยกัน**
- สร้างเวิร์กโฟลว์ที่ทรงพลังโดยรวมบริการต่าง ๆ
- ตัวอย่าง: "ดึง GitHub issues ล่าสุดทั้งหมดและสร้างงานใน Azure DevOps ตามนั้น"
- สร้างระบบอัตโนมัติโดยไม่ต้องเขียนสคริปต์ซับซ้อน

#### 4. 🌐 **เข้าถึงระบบนิเวศที่เติบโตขึ้นเรื่อย ๆ**
- ได้ประโยชน์จากเซิร์ฟเวอร์ที่สร้างโดย Microsoft, GitHub และบริษัทอื่น ๆ
- ผสมผสานเครื่องมือจากผู้ขายต่าง ๆ ได้อย่างราบรื่น
- เข้าร่วมระบบนิเวศมาตรฐานที่ทำงานร่วมกับผู้ช่วย AI ต่าง ๆ ได้

#### 5. 🛠️ **เรียนรู้ผ่านการลงมือทำ**
- เริ่มต้นด้วยเซิร์ฟเวอร์ที่สร้างไว้แล้วเพื่อเข้าใจแนวคิด
- ค่อย ๆ สร้างเซิร์ฟเวอร์ของคุณเองเมื่อคุณคุ้นเคยมากขึ้น
- ใช้ SDK และเอกสารที่มีให้เพื่อช่วยในการเรียนรู้

### ตัวอย่างจริงสำหรับผู้เริ่มต้น

สมมติว่าคุณเพิ่งเริ่มพัฒนาเว็บและกำลังทำโปรเจกต์แรก นี่คือวิธีที่เซิร์ฟเวอร์ MCP ช่วยได้:

**วิธีแบบเดิม:**
```
1. Code a feature
2. Open browser → Navigate to GitHub
3. Create an issue for testing
4. Open another tab → Check Azure docs for deployment
5. Open third tab → Look up database connection examples
6. Return to VS Code
7. Try to remember what you were doing
```

**ด้วยเซิร์ฟเวอร์ MCP:**
```
1. Code a feature
2. Ask AI: "Create a GitHub issue for testing this login feature"
3. Ask AI: "How do I deploy this to Azure according to the docs?"
4. Ask AI: "Show me the best way to connect to my database"
5. Continue coding with all the information you need
```

### ข้อได้เปรียบของมาตรฐานองค์กร

MCP กำลังกลายเป็นมาตรฐานในอุตสาหกรรม ซึ่งหมายความว่า:
- **ความสม่ำเสมอ**: ประสบการณ์ที่คล้ายกันในเครื่องมือและบริษัทต่าง ๆ
- **ความสามารถในการทำงานร่วมกัน**: เซิร์ฟเวอร์จากผู้ขายต่าง ๆ ทำงานร่วมกันได้
- **รองรับอนาคต**: ทักษะและการตั้งค่าถ่ายโอนระหว่างผู้ช่วย AI ต่าง ๆ ได้
- **ชุมชน**: ระบบนิเวศขนาดใหญ่ของความรู้และทรัพยากรที่ใช้ร่วมกัน

### เริ่มต้น: สิ่งที่คุณจะได้เรียนรู้

ในคู่มือนี้ เราจะสำรวจเซิร์ฟเวอร์ Microsoft MCP จำนวน 10 ตัวที่มีประโยชน์สำหรับนักพัฒนาทุกระดับ เซิร์ฟเวอร์แต่ละตัวถูกออกแบบมาเพื่อ:
- แก้ไขปัญหาการพัฒนาที่พบบ่อย
- ลดงานซ้ำซ้อน
- ปรับปรุงคุณภาพโค้ด
- เพิ่มโอกาสในการเรียนรู้

> **💡 เคล็ดลับการเรียนรู้**
> 
> หากคุณเป็นมือใหม่กับ MCP เริ่มจาก [Introduction to MCP](../00-Introduction/README.md) และ [Core Concepts](../01-CoreConcepts/README.md) ก่อน แล้วค่อยกลับมาดูตัวอย่างการใช้งานจริงกับเครื่องมือ Microsoft
>
> สำหรับบริบทเพิ่มเติมเกี่ยวกับความสำคัญของ MCP ลองอ่านโพสต์ของ Maria Naggaga: [Connect Once, Integrate Anywhere with MCP](https://devblogs.microsoft.com/blog/connect-once-integrate-anywhere-with-mcps)

## เริ่มต้นกับ MCP ใน VS Code และ Visual Studio 🚀

การตั้งค่าเซิร์ฟเวอร์ MCP เหล่านี้ทำได้ง่ายถ้าคุณใช้ Visual Studio Code หรือ Visual Studio 2022 พร้อม GitHub Copilot

### การตั้งค่า VS Code

ขั้นตอนพื้นฐานสำหรับ VS Code มีดังนี้:

1. **เปิดใช้งานโหมด Agent**: ใน VS Code ให้เปลี่ยนไปที่โหมด Agent ในหน้าต่าง Copilot Chat
2. **กำหนดค่าเซิร์ฟเวอร์ MCP**: เพิ่มการตั้งค่าเซิร์ฟเวอร์ในไฟล์ settings.json ของ VS Code
3. **เริ่มเซิร์ฟเวอร์**: คลิกปุ่ม "Start" สำหรับเซิร์ฟเวอร์ที่ต้องการใช้
4. **เลือกเครื่องมือ**: เลือกเซิร์ฟเวอร์ MCP ที่จะเปิดใช้งานในเซสชันปัจจุบัน

ดูคำแนะนำการตั้งค่าอย่างละเอียดได้ที่ [VS Code MCP documentation](https://code.visualstudio.com/docs/copilot/copilot-mcp)

> **💡 เคล็ดลับมือโปร: จัดการเซิร์ฟเวอร์ MCP อย่างมืออาชีพ!**
> 
> ตอนนี้ใน VS Code Extensions view มี [UI ใหม่ที่ใช้งานง่ายสำหรับจัดการเซิร์ฟเวอร์ MCP ที่ติดตั้ง](https://code.visualstudio.com/docs/copilot/chat/mcp-servers#_use-mcp-tools-in-agent-mode) คุณสามารถเริ่ม หยุด และจัดการเซิร์ฟเวอร์ MCP ได้อย่างรวดเร็วผ่านอินเทอร์เฟซที่ชัดเจน ลองใช้ดู!

### การตั้งค่า Visual Studio 2022

สำหรับ Visual Studio 2022 (เวอร์ชัน 17.14 ขึ้นไป):

1. **เปิดใช้งานโหมด Agent**: คลิกเมนู "Ask" ในหน้าต่าง GitHub Copilot Chat แล้วเลือก "Agent"
2. **สร้างไฟล์กำหนดค่า**: สร้างไฟล์ `.mcp.json` ในไดเรกทอรีโซลูชัน (แนะนำให้เก็บที่ `<SOLUTIONDIR>\.mcp.json`)
3. **กำหนดค่าเซิร์ฟเวอร์**: เพิ่มการตั้งค่าเซิร์ฟเวอร์ MCP ตามรูปแบบมาตรฐาน
4. **อนุมัติเครื่องมือ**: เมื่อได้รับแจ้ง ให้อนุมัติเครื่องมือที่ต้องการใช้พร้อมสิทธิ์ที่เหมาะสม

ดูคำแนะนำการตั้งค่า Visual Studio อย่างละเอียดได้ที่ [Visual Studio MCP documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers)

เซิร์ฟเวอร์ MCP แต่ละตัวมีข้อกำหนดการตั้งค่าของตัวเอง (เช่น สตริงการเชื่อมต่อ การยืนยันตัวตน ฯลฯ) แต่รูปแบบการตั้งค่าจะเหมือนกันทั้งสอง IDE

## บทเรียนจากเซิร์ฟเวอร์ Microsoft MCP 🛠️

### 1. 📚 Microsoft Learn Docs MCP Server

[![ติดตั้งใน VS Code](https://img.shields.io/badge/VS_Code-Install_Microsoft_Docs_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D) [![ติดตั้งใน VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Microsoft_Docs_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=microsoft.docs.mcp&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Flearn.microsoft.com%2Fapi%2Fmcp%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**ทำอะไรได้บ้าง**: Microsoft Learn Docs MCP Server เป็นบริการโฮสต์บนคลาวด์ที่ให้ผู้ช่วย AI เข้าถึงเอกสารทางการของ Microsoft แบบเรียลไทม์ผ่าน Model Context Protocol เชื่อมต่อกับ `https://learn.microsoft.com/api/mcp` และเปิดใช้งานการค้นหาเชิงความหมายใน Microsoft Learn, เอกสาร Azure, เอกสาร Microsoft 365 และแหล่งข้อมูลทางการอื่น ๆ ของ Microsoft

**ทำไมถึงมีประโยชน์**: แม้มันจะดูเหมือนแค่ "เอกสาร" แต่เซิร์ฟเวอร์นี้สำคัญมากสำหรับนักพัฒนาที่ใช้เทคโนโลยี Microsoft หนึ่งในข้อร้องเรียนใหญ่ของนักพัฒนา .NET เกี่ยวกับผู้ช่วย AI คือข้อมูลไม่อัปเดตเกี่ยวกับเวอร์ชันล่าสุดของ .NET และ C# Microsoft Learn Docs MCP Server แก้ปัญหานี้โดยให้การเข้าถึงเอกสารล่าสุด, เอกสารอ้างอิง API และแนวทางปฏิบัติที่ดีที่สุดแบบเรียลไทม์ ไม่ว่าคุณจะใช้ Azure SDKs เวอร์ชันล่าสุด, สำรวจฟีเจอร์ใหม่ของ C# 13 หรือใช้งาน .NET Aspire patterns รุ่นใหม่ เซิร์ฟเวอร์นี้ช่วยให้ผู้ช่วย AI ของคุณเข้าถึงข้อมูลที่ถูกต้องและทันสมัยเพื่อสร้างโค้ดที่แม่นยำและทันสมัย

**การใช้งานจริง**: "คำสั่ง az cli สำหรับสร้าง Azure container app ตามเอกสาร Microsoft Learn คืออะไร?" หรือ "ฉันจะตั้งค่า Entity Framework กับ dependency injection ใน ASP.NET Core อย่างไร?" หรือ "ช่วยตรวจสอบโค้ดนี้ให้แน่ใจว่าเป็นไปตามคำแนะนำด้านประสิทธิภาพใน Microsoft Learn Documentation" เซิร์ฟเวอร์นี้ครอบคลุม Microsoft Learn, เอกสาร Azure และ Microsoft 365 โดยใช้การค้นหาเชิงความหมายขั้นสูงเพื่อหาข้อมูลที่เกี่ยวข้องที่สุดในบริบทนั้น ๆ มันส่งคืนเนื้อหาคุณภาพสูงสูงสุด 10 ชิ้นพร้อมชื่อบทความและ URL โดยเข้าถึงเอกสาร Microsoft ล่าสุดเสมอเมื่อมีการเผยแพร่

**ตัวอย่างเด่น**: เซิร์ฟเวอร์นี้เปิดใช้งานเครื่องมือ `microsoft_docs_search` ที่ทำการค้นหาเชิงความหมายในเอกสารทางเทคนิคอย่างเป็นทางการของ Microsoft เมื่อกำหนดค่าแล้ว คุณสามารถถามคำถามเช่น "ฉันจะใช้งาน JWT authentication ใน ASP.NET Core อย่างไร?" และได้รับคำตอบอย่างละเอียดพร้อมลิงก์แหล่งที่มา คุณภาพการค้นหายอดเยี่ยมเพราะเข้าใจบริบท — ถ้าถามเกี่ยวกับ "containers" ในบริบท Azure จะได้เอกสาร Azure Container Instances แต่ถ้าในบริบท .NET จะได้ข้อมูลเกี่ยวกับ collection ใน C#

สิ่งนี้มีประโยชน์อย่างยิ่งสำหรับไลบรารีและกรณีใช้งานที่เปลี่ยนแปลงเร็วหรือเพิ่งอัปเดต เช่น ในโปรเจกต์โค้ดดิ้งล่าสุดที่ผมต้องการใช้ฟีเจอร์ในเวอร์ชันล่าสุดของ .NET Aspire และ Microsoft.Extensions.AI โดยการเพิ่ม Microsoft Learn Docs MCP server ผมสามารถใช้ประโยชน์ไม่เพียงแค่เอกสาร API แต่ยังรวมถึงคำแนะนำและวิธีใช้งานที่เพิ่งเผยแพร่ใหม่ด้วย
> **💡 เคล็ดลับมือโปร**
> 
> แม้แต่โมเดลที่เป็นมิตรกับเครื่องมือก็ยังต้องการแรงจูงใจในการใช้เครื่องมือ MCP! ลองเพิ่มคำสั่งระบบหรือ [copilot-instructions.md](https://docs.github.com/copilot/how-tos/custom-instructions/adding-repository-custom-instructions-for-github-copilot) เช่น: "คุณสามารถเข้าถึง `microsoft.docs.mcp` – ใช้เครื่องมือนี้เพื่อค้นหาข้อมูลทางการล่าสุดของ Microsoft เมื่อจัดการกับคำถามเกี่ยวกับเทคโนโลยีของ Microsoft เช่น C#, Azure, ASP.NET Core หรือ Entity Framework"
>
> สำหรับตัวอย่างที่ดีของการใช้งานนี้ ลองดู [โหมดแชท C# .NET Janitor](https://github.com/awesome-copilot/chatmodes/blob/main/csharp-dotnet-janitor.chatmode.md) จาก Awesome GitHub Copilot repository โหมดนี้ใช้ประโยชน์จาก Microsoft Learn Docs MCP server โดยเฉพาะเพื่อช่วยทำความสะอาดและปรับปรุงโค้ด C# ให้ทันสมัยด้วยรูปแบบและแนวทางปฏิบัติที่ดีที่สุดในปัจจุบัน
### 2. ☁️ Azure MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fazure-mcp%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ทำอะไรได้บ้าง**: Azure MCP Server คือชุดเครื่องมือครบวงจรที่ประกอบด้วยตัวเชื่อมต่อบริการ Azure เฉพาะทางมากกว่า 15 ตัว ที่นำระบบนิเวศของ Azure ทั้งหมดมาไว้ในเวิร์กโฟลว์ AI ของคุณ นี่ไม่ใช่แค่เซิร์ฟเวอร์เดียว แต่เป็นคอลเลกชันทรงพลังที่รวมถึงการจัดการทรัพยากร การเชื่อมต่อฐานข้อมูล (PostgreSQL, SQL Server) การวิเคราะห์ล็อก Azure Monitor ด้วย KQL การผสาน Cosmos DB และอื่นๆ อีกมากมาย

**ทำไมถึงมีประโยชน์**: นอกจากการจัดการทรัพยากร Azure แล้ว เซิร์ฟเวอร์นี้ยังช่วยยกระดับคุณภาพโค้ดเมื่อทำงานกับ Azure SDKs เมื่อคุณใช้ Azure MCP ในโหมด Agent มันไม่ได้แค่ช่วยเขียนโค้ด แต่ช่วยให้คุณเขียนโค้ด Azure ที่ *ดีกว่า* ตามรูปแบบการยืนยันตัวตนปัจจุบัน การจัดการข้อผิดพลาดที่ดีที่สุด และใช้ประโยชน์จากฟีเจอร์ SDK ล่าสุด แทนที่จะได้โค้ดทั่วไปที่อาจใช้งานได้ คุณจะได้โค้ดที่เป็นไปตามแนวทางที่แนะนำของ Azure สำหรับงานในสภาพแวดล้อมจริง

**โมดูลหลักประกอบด้วย**:
- **🗄️ ตัวเชื่อมต่อฐานข้อมูล**: เข้าถึง Azure Database สำหรับ PostgreSQL และ SQL Server ด้วยภาษาธรรมชาติได้โดยตรง
- **📊 Azure Monitor**: การวิเคราะห์ล็อกด้วย KQL และข้อมูลเชิงลึกด้านการปฏิบัติการ
- **🌐 การจัดการทรัพยากร**: การจัดการวงจรชีวิตทรัพยากร Azure อย่างครบถ้วน
- **🔐 การยืนยันตัวตน**: รูปแบบ DefaultAzureCredential และ managed identity
- **📦 บริการจัดเก็บข้อมูล**: การดำเนินการกับ Blob Storage, Queue Storage และ Table Storage
- **🚀 บริการคอนเทนเนอร์**: การจัดการ Azure Container Apps, Container Instances และ AKS
- **และตัวเชื่อมต่อเฉพาะทางอื่นๆ อีกมากมาย**

**การใช้งานจริง**: "แสดงบัญชีจัดเก็บข้อมูล Azure ของฉัน", "ค้นหาข้อผิดพลาดใน Log Analytics workspace ของฉันในชั่วโมงที่ผ่านมา" หรือ "ช่วยฉันสร้างแอป Azure ด้วย Node.js พร้อมการยืนยันตัวตนที่ถูกต้อง"

**ตัวอย่างสาธิตเต็มรูปแบบ**: นี่คือการสาธิตแบบครบถ้วนที่แสดงพลังของการรวม Azure MCP กับส่วนขยาย GitHub Copilot for Azure ใน VS Code เมื่อคุณติดตั้งทั้งสองและสั่งว่า:

> "สร้างสคริปต์ Python ที่อัปโหลดไฟล์ไปยัง Azure Blob Storage โดยใช้การยืนยันตัวตน DefaultAzureCredential สคริปต์ต้องเชื่อมต่อกับบัญชีจัดเก็บข้อมูล Azure ของฉันชื่อ 'mycompanystorage' อัปโหลดไปยังคอนเทนเนอร์ชื่อ 'documents' สร้างไฟล์ทดสอบที่มีเวลาปัจจุบันเพื่ออัปโหลด จัดการข้อผิดพลาดอย่างเหมาะสมและแสดงผลลัพธ์ที่ชัดเจน ปฏิบัติตามแนวทางปฏิบัติที่ดีที่สุดของ Azure สำหรับการยืนยันตัวตนและการจัดการข้อผิดพลาด รวมคอมเมนต์อธิบายการทำงานของ DefaultAzureCredential และจัดโครงสร้างสคริปต์อย่างดีด้วยฟังก์ชันและเอกสารประกอบ"

Azure MCP Server จะสร้างสคริปต์ Python ที่พร้อมใช้งานในสภาพแวดล้อมจริงที่:
- ใช้ SDK ล่าสุดของ Azure Blob Storage พร้อมรูปแบบ async ที่เหมาะสม
- ใช้ DefaultAzureCredential พร้อมคำอธิบาย fallback chain อย่างละเอียด
- มีการจัดการข้อผิดพลาดที่แข็งแกร่งพร้อมประเภทข้อยกเว้นเฉพาะของ Azure
- ปฏิบัติตามแนวทางปฏิบัติที่ดีที่สุดของ Azure SDK สำหรับการจัดการทรัพยากรและการเชื่อมต่อ
- มีการบันทึกข้อมูลและแสดงผลลัพธ์บนคอนโซลอย่างละเอียด
- สร้างสคริปต์ที่มีโครงสร้างดี มีฟังก์ชัน เอกสารประกอบ และคำบอกชนิดข้อมูล

สิ่งที่น่าทึ่งคือถ้าไม่มี Azure MCP คุณอาจได้โค้ด blob storage ทั่วไปที่ใช้งานได้แต่ไม่เป็นไปตามรูปแบบปัจจุบันของ Azure แต่กับ Azure MCP คุณจะได้โค้ดที่ใช้วิธีการยืนยันตัวตนล่าสุด จัดการกับสถานการณ์ข้อผิดพลาดเฉพาะของ Azure และปฏิบัติตามแนวทางที่ Microsoft แนะนำสำหรับแอปพลิเคชันในสภาพแวดล้อมจริง

**ตัวอย่างเด่น**: ผมมักลืมคำสั่งเฉพาะของ `az` และ `azd` CLI สำหรับใช้งานแบบ ad-hoc เสมอ มันมักเป็นกระบวนการสองขั้นตอนสำหรับผม: ค้นหาสังเขปคำสั่งก่อน แล้วค่อยรันคำสั่ง ผมมักจะเข้าไปในพอร์ทัลแล้วคลิกทำงานแทนเพราะไม่อยากยอมรับว่าจำคำสั่ง CLI ไม่ได้ การที่สามารถอธิบายสิ่งที่ต้องการได้เลยนั้นยอดเยี่ยมมาก และยิ่งดีขึ้นไปอีกที่ทำได้โดยไม่ต้องออกจาก IDE!

มีรายการกรณีใช้งานที่ดีมากใน [Azure MCP repository](https://github.com/Azure/azure-mcp?tab=readme-ov-file#-what-can-you-do-with-the-azure-mcp-server) เพื่อช่วยให้คุณเริ่มต้น สำหรับคู่มือการตั้งค่าอย่างละเอียดและตัวเลือกการกำหนดค่าขั้นสูง ดูได้ที่ [เอกสาร Azure MCP อย่างเป็นทางการ](https://learn.microsoft.com/azure/developer/azure-mcp-server/)  

### 3. 🐙 GitHub MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Server-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Server-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=github&config=%7B%22type%22%3A%20%22http%22%2C%22url%22%3A%20%22https%3A%2F%2Fapi.githubcopilot.com%2Fmcp%2F%22%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/github/github-mcp-server)

**ทำอะไรได้บ้าง**: GitHub MCP Server อย่างเป็นทางการให้การผสานรวมอย่างราบรื่นกับระบบนิเวศของ GitHub ทั้งหมด โดยมีตัวเลือกทั้งการเข้าถึงระยะไกลแบบโฮสต์และการติดตั้งแบบ Docker ในเครื่อง นี่ไม่ใช่แค่การจัดการรีโพซิทอรีพื้นฐาน แต่เป็นชุดเครื่องมือครบวงจรที่รวมถึงการจัดการ GitHub Actions, เวิร์กโฟลว์ pull request, การติดตามปัญหา, การสแกนความปลอดภัย, การแจ้งเตือน และความสามารถในการทำงานอัตโนมัติขั้นสูง

**ทำไมถึงมีประโยชน์**: เซิร์ฟเวอร์นี้เปลี่ยนวิธีที่คุณโต้ตอบกับ GitHub โดยนำประสบการณ์แพลตฟอร์มทั้งหมดมาไว้ในสภาพแวดล้อมการพัฒนาของคุณ แทนที่จะต้องสลับไปมาระหว่าง VS Code กับ GitHub.com เพื่อจัดการโปรเจกต์ ตรวจสอบโค้ด และติดตาม CI/CD คุณสามารถจัดการทุกอย่างผ่านคำสั่งภาษาธรรมชาติในขณะที่ยังคงโฟกัสกับโค้ดของคุณ

> **ℹ️ Note: Different Types of 'Agents'**
> 
> อย่าสับสนระหว่าง GitHub MCP Server กับ GitHub's Coding Agent (เอเจนต์ AI ที่คุณสามารถมอบหมายปัญหาให้เพื่อทำงานเขียนโค้ดอัตโนมัติ) GitHub MCP Server ทำงานในโหมด Agent ของ VS Code เพื่อให้การผสานรวม GitHub API ในขณะที่ GitHub's Coding Agent เป็นฟีเจอร์แยกที่สร้าง pull request เมื่อได้รับมอบหมายใน GitHub issues

**ความสามารถหลักประกอบด้วย**:
- **⚙️ GitHub Actions**: การจัดการ pipeline CI/CD อย่างครบถ้วน การติดตามเวิร์กโฟลว์ และการจัดการ artifacts
- **🔀 Pull Requests**: สร้าง ตรวจสอบ รวม และจัดการ PR พร้อมติดตามสถานะอย่างละเอียด
- **🐛 Issues**: การจัดการวงจรชีวิตของ issue อย่างครบถ้วน การคอมเมนต์ การติดป้าย และการมอบหมาย
- **🔒 ความปลอดภัย**: การแจ้งเตือนการสแกนโค้ด การตรวจจับความลับ และการผสาน Dependabot
- **🔔 การแจ้งเตือน**: การจัดการการแจ้งเตือนอย่างชาญฉลาดและการควบคุมการสมัครสมาชิกรีโพซิทอรี
- **📁 การจัดการรีโพซิทอรี**: การดำเนินการไฟล์ การจัดการสาขา และการบริหารรีโพซิทอรี
- **👥 การทำงานร่วมกัน**: การค้นหาผู้ใช้และองค์กร การจัดการทีม และการควบคุมการเข้าถึง

**การใช้งานจริง**: "สร้าง pull request จากฟีเจอร์สาขาของฉัน", "แสดงการรัน CI ที่ล้มเหลวทั้งหมดในสัปดาห์นี้", "แสดงรายการแจ้งเตือนความปลอดภัยที่เปิดอยู่สำหรับรีโพซิทอรีของฉัน" หรือ "ค้นหาปัญหาทั้งหมดที่มอบหมายให้ฉันในองค์กรของฉัน"

**ตัวอย่างสาธิตเต็มรูปแบบ**: นี่คือเวิร์กโฟลว์ที่ทรงพลังซึ่งแสดงความสามารถของ GitHub MCP Server:

> "ฉันต้องเตรียมตัวสำหรับการรีวิวสปรินต์ แสดง pull request ทั้งหมดที่ฉันสร้างในสัปดาห์นี้ ตรวจสอบสถานะ pipeline CI/CD ของเรา สร้างสรุปแจ้งเตือนความปลอดภัยที่ต้องจัดการ และช่วยร่างบันทึกการปล่อยเวอร์ชันจาก PR ที่รวมแล้วซึ่งมีป้าย 'feature'"

GitHub MCP Server จะ:
- ดึงข้อมูล pull request ล่าสุดพร้อมสถานะอย่างละเอียด
- วิเคราะห์การรันเวิร์กโฟลว์และเน้นข้อผิดพลาดหรือปัญหาด้านประสิทธิภาพ
- รวบรวมผลการสแกนความปลอดภัยและจัดลำดับความสำคัญของแจ้งเตือนที่สำคัญ
- สร้างบันทึกการปล่อยเวอร์ชันอย่างครบถ้วนโดยดึงข้อมูลจาก PR ที่รวมแล้ว
- ให้ขั้นตอนถัดไปที่สามารถดำเนินการได้สำหรับการวางแผนสปรินต์และการเตรียมปล่อยเวอร์ชัน

**ตัวอย่างเด่น**: ผมชอบใช้ตัวนี้สำหรับเวิร์กโฟลว์การตรวจสอบโค้ด แทนที่จะต้องสลับไปมาระหว่าง VS Code, การแจ้งเตือน GitHub และหน้าของ pull request ผมแค่พูดว่า "แสดง PR ทั้งหมดที่รอการตรวจสอบของฉัน" แล้วตามด้วย "เพิ่มคอมเมนต์ใน PR #123 ถามเกี่ยวกับการจัดการข้อผิดพลาดในวิธีการยืนยันตัวตน" เซิร์ฟเวอร์จะจัดการเรียก GitHub API รักษาบริบทของการสนทนา และช่วยผมร่างคอมเมนต์ตรวจสอบที่สร้างสรรค์มากขึ้น

**ตัวเลือกการยืนยันตัวตน**: เซิร์ฟเวอร์รองรับทั้ง OAuth (ใช้งานได้อย่างราบรื่นใน VS Code) และ Personal Access Tokens พร้อมชุดเครื่องมือที่ปรับแต่งได้เพื่อเปิดใช้งานเฉพาะฟังก์ชัน GitHub ที่คุณต้องการ คุณสามารถรันเป็นบริการโฮสต์ระยะไกลสำหรับการตั้งค่าทันที หรือรันในเครื่องผ่าน Docker เพื่อควบคุมอย่างเต็มที่

> **💡 Pro Tip**
> 
> เปิดใช้งานเฉพาะชุดเครื่องมือที่คุณต้องการโดยกำหนดพารามิเตอร์ `--toolsets` ในการตั้งค่า MCP server เพื่อลดขนาดบริบทและปรับปรุงการเลือกเครื่องมือ AI เช่น เพิ่ม `"--toolsets", "repos,issues,pull_requests,actions"` ในอาร์กิวเมนต์การกำหนดค่า MCP สำหรับเวิร์กโฟลว์การพัฒนาหลัก หรือใช้ `"--toolsets", "notifications, security"` หากคุณต้องการเฉพาะความสามารถในการติดตาม GitHub เป็นหลัก

### 4. 🔄 Azure DevOps MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_DevOps_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_DevOps_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20DevOps%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-azure-devops%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/azure-devops-mcp)

**ทำอะไรได้บ้าง**: เชื่อมต่อกับบริการ Azure DevOps เพื่อการจัดการโปรเจกต์อย่างครบถ้วน การติดตาม work item การจัดการ build pipeline และการดำเนินการกับรีโพซิทอรี

**ทำไมถึงมีประโยชน์**: สำหรับทีมที่ใช้ Azure DevOps เป็นแพลตฟอร์ม DevOps หลัก MCP server นี้ช่วยลดการสลับแท็บระหว่างสภาพแวดล้อมการพัฒนาของคุณกับเว็บอินเทอร์เฟซ Azure DevOps คุณสามารถจัดการ work item ตรวจสอบสถานะ build สืบค้นรีโพซิทอรี และจัดการงานโปรเจกต์ได้โดยตรงจากผู้ช่วย AI ของคุณ

**การใช้งานจริง**: "แสดง work item ที่กำลังทำอยู่ทั้งหมดในสปรินต์ปัจจุบันสำหรับโปรเจกต์ WebApp", "สร้างรายงานบั๊กสำหรับปัญหาเข้าสู่ระบบที่เพิ่งพบ" หรือ "ตรวจสอบสถานะ build pipeline ของเราและแสดงความล้มเหลวล่าสุด"

**ตัวอย่างเด่น**: คุณสามารถตรวจสอบสถานะสปรินต์ปัจจุบันของทีมได้ง่ายๆ ด้วยคำสั่งอย่าง "แสดง work item ที่กำลังทำอยู่ทั้งหมดในสปรินต์ปัจจุบันสำหรับโปรเจกต์ WebApp" หรือ "สร้างรายงานบั๊กสำหรับปัญหาเข้าสู่ระบบที่เพิ่งพบ" โดยไม่ต้องออกจากสภาพแวดล้อมการพ
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_MarkItDown_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_MarkItDown_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=MarkItDown%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-markitdown%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/markitdown)

**ทำอะไรได้บ้าง**: MarkItDown คือเซิร์ฟเวอร์แปลงเอกสารแบบครบวงจรที่เปลี่ยนไฟล์หลากหลายรูปแบบให้กลายเป็น Markdown คุณภาพสูง ซึ่งเหมาะสำหรับการใช้งานกับ LLM และกระบวนการวิเคราะห์ข้อความ

**ทำไมถึงมีประโยชน์**: จำเป็นสำหรับเวิร์กโฟลว์เอกสารสมัยใหม่! MarkItDown รองรับไฟล์หลากหลายประเภทพร้อมรักษาโครงสร้างสำคัญของเอกสาร เช่น หัวข้อ รายการ ตาราง และลิงก์ ต่างจากเครื่องมือดึงข้อความธรรมดา มันเน้นการรักษาความหมายเชิงสัญลักษณ์และรูปแบบที่มีคุณค่าสำหรับทั้งการประมวลผล AI และการอ่านของมนุษย์

**รูปแบบไฟล์ที่รองรับ**:
- **เอกสารสำนักงาน**: PDF, PowerPoint (PPTX), Word (DOCX), Excel (XLSX/XLS)
- **ไฟล์มีเดีย**: รูปภาพ (พร้อมข้อมูล EXIF และ OCR), เสียง (พร้อมข้อมูล EXIF และการถอดเสียง)
- **เนื้อหาเว็บ**: HTML, ฟีด RSS, URL YouTube, หน้า Wikipedia
- **รูปแบบข้อมูล**: CSV, JSON, XML, ไฟล์ ZIP (ประมวลผลเนื้อหาแบบวนซ้ำ)
- **รูปแบบการเผยแพร่**: EPub, โน้ตบุ๊ก Jupyter (.ipynb)
- **อีเมล**: ข้อความ Outlook (.msg)
- **ขั้นสูง**: การผสานรวม Azure Document Intelligence เพื่อการประมวลผล PDF ที่ดียิ่งขึ้น

**ความสามารถขั้นสูง**: MarkItDown รองรับคำอธิบายภาพด้วย LLM (เมื่อมี OpenAI client), Azure Document Intelligence สำหรับการประมวลผล PDF ขั้นสูง, การถอดเสียงเสียงพูด และระบบปลั๊กอินสำหรับขยายไปยังรูปแบบไฟล์เพิ่มเติม

**การใช้งานจริง**: "แปลงงานนำเสนอ PowerPoint นี้เป็น Markdown สำหรับเว็บไซต์เอกสารของเรา", "ดึงข้อความจาก PDF นี้พร้อมโครงสร้างหัวข้อที่ถูกต้อง", หรือ "แปลงสเปรดชีต Excel นี้เป็นตารางที่อ่านง่าย"

**ตัวอย่างเด่น**: อ้างอิงจาก [เอกสาร MarkItDown](https://github.com/microsoft/markitdown#why-markdown):


> Markdown ใกล้เคียงกับข้อความธรรมดามาก โดยมีเครื่องหมายหรือรูปแบบน้อย แต่ยังคงให้วิธีแสดงโครงสร้างเอกสารที่สำคัญ LLM ชั้นนำ เช่น GPT-4o ของ OpenAI "พูด" Markdown โดยตรง และมักจะใส่ Markdown ลงในคำตอบโดยไม่ต้องสั่ง นั่นแสดงว่าพวกมันได้รับการฝึกด้วยข้อความที่มีรูปแบบ Markdown จำนวนมากและเข้าใจมันดี อีกทั้ง Markdown ยังมีประสิทธิภาพในการใช้โทเค็นสูงด้วย

MarkItDown ทำงานได้ดีมากในการรักษาโครงสร้างเอกสาร ซึ่งสำคัญสำหรับเวิร์กโฟลว์ AI เช่น เมื่อแปลงงานนำเสนอ PowerPoint มันจะรักษาการจัดระเบียบสไลด์ด้วยหัวข้อที่เหมาะสม ดึงตารางเป็นตาราง Markdown ใส่ข้อความแทนภาพสำหรับรูปภาพ และแม้แต่ประมวลผลบันทึกผู้บรรยาย แผนภูมิจะถูกแปลงเป็นตารางข้อมูลที่อ่านได้ และ Markdown ที่ได้จะรักษาการไหลของเนื้อหาแบบตรรกะของงานนำเสนอเดิม เหมาะอย่างยิ่งสำหรับการป้อนเนื้อหางานนำเสนอเข้าสู่ระบบ AI หรือสร้างเอกสารจากสไลด์ที่มีอยู่

### 6. 🗃️ SQL Server MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_SQL_Database-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_SQL_Database-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20SQL%20Database&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40azure%2Fmcp%40latest%22%2C%22server%22%2C%22start%22%2C%22--namespace%22%2C%22sql%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/Azure/azure-mcp)

**ทำอะไรได้บ้าง**: ให้การเข้าถึงฐานข้อมูล SQL Server ผ่านการสนทนา (ทั้งแบบ on-premises, Azure SQL หรือ Fabric)

**ทำไมถึงมีประโยชน์**: คล้ายกับเซิร์ฟเวอร์ PostgreSQL แต่สำหรับระบบนิเวศ Microsoft SQL เชื่อมต่อด้วย connection string ง่ายๆ แล้วเริ่มสืบค้นด้วยภาษาธรรมชาติ – ไม่ต้องสลับบริบทอีกต่อไป!

**การใช้งานจริง**: "ค้นหาคำสั่งซื้อทั้งหมดที่ยังไม่ดำเนินการใน 30 วันที่ผ่านมา" จะถูกแปลงเป็นคำสั่ง SQL ที่เหมาะสมและส่งผลลัพธ์ในรูปแบบที่อ่านง่าย

**ตัวอย่างเด่น**: เมื่อคุณตั้งค่าการเชื่อมต่อฐานข้อมูลแล้ว คุณสามารถเริ่มสนทนากับข้อมูลได้ทันที บล็อกโพสต์แสดงตัวอย่างด้วยคำถามง่ายๆ: "คุณเชื่อมต่อกับฐานข้อมูลไหน?" เซิร์ฟเวอร์ MCP จะเรียกใช้เครื่องมือฐานข้อมูลที่เหมาะสม เชื่อมต่อกับอินสแตนซ์ SQL Server ของคุณ และส่งรายละเอียดการเชื่อมต่อฐานข้อมูลปัจจุบันกลับมา – ทั้งหมดนี้โดยไม่ต้องเขียน SQL เลย เซิร์ฟเวอร์รองรับการจัดการฐานข้อมูลอย่างครบถ้วนตั้งแต่การจัดการสคีมาไปจนถึงการจัดการข้อมูล ผ่านคำสั่งภาษาธรรมชาติ สำหรับคำแนะนำการตั้งค่าและตัวอย่างการกำหนดค่ากับ VS Code และ Claude Desktop ดูได้ที่: [Introducing MSSQL MCP Server (Preview)](https://devblogs.microsoft.com/azure-sql/introducing-mssql-mcp-server/).

### 7. 🎭 Playwright MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Playwright_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Playwright_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Playwright%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-playwright%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/playwright-mcp)

**ทำอะไรได้บ้าง**: ช่วยให้เอเจนต์ AI โต้ตอบกับเว็บเพจเพื่อการทดสอบและอัตโนมัติ

> **ℹ️ ขับเคลื่อน GitHub Copilot**
> 
> Playwright MCP Server ขับเคลื่อน Coding Agent ของ GitHub Copilot ทำให้มันมีความสามารถในการท่องเว็บ! [เรียนรู้เพิ่มเติมเกี่ยวกับฟีเจอร์นี้](https://github.blog/changelog/2025-07-02-copilot-coding-agent-now-has-its-own-web-browser/).

**ทำไมถึงมีประโยชน์**: เหมาะสำหรับการทดสอบอัตโนมัติที่ขับเคลื่อนด้วยคำอธิบายภาษาธรรมชาติ AI สามารถนำทางเว็บไซต์ กรอกแบบฟอร์ม และดึงข้อมูลผ่านสแนปช็อตการเข้าถึงที่มีโครงสร้าง – นี่คือความสามารถที่ทรงพลังมาก!

**การใช้งานจริง**: "ทดสอบกระบวนการล็อกอินและตรวจสอบว่าหน้าปัดโหลดถูกต้อง" หรือ "สร้างการทดสอบที่ค้นหาสินค้าและตรวจสอบหน้าผลลัพธ์" – ทั้งหมดนี้โดยไม่ต้องใช้โค้ดต้นฉบับของแอปพลิเคชัน

**ตัวอย่างเด่น**: เพื่อนร่วมงานของฉัน Debbie O'Brien ทำงานกับ Playwright MCP Server ได้อย่างน่าทึ่ง! เช่น เธอแสดงให้เห็นว่าคุณสามารถสร้างการทดสอบ Playwright แบบสมบูรณ์ได้โดยไม่ต้องเข้าถึงโค้ดต้นฉบับ ในสถานการณ์ของเธอ เธอขอให้ Copilot สร้างการทดสอบสำหรับแอปค้นหาหนัง: ไปที่เว็บไซต์ ค้นหา "Garfield" และตรวจสอบว่าหนังปรากฏในผลลัพธ์ MCP เปิดเซสชันเบราว์เซอร์ สำรวจโครงสร้างหน้าโดยใช้สแนปช็อต DOM หาตัวเลือกที่ถูกต้อง และสร้างการทดสอบ TypeScript ที่ทำงานได้สมบูรณ์และผ่านการทดสอบครั้งแรก

สิ่งที่ทำให้ทรงพลังคือมันเชื่อมช่องว่างระหว่างคำสั่งภาษาธรรมชาติกับโค้ดทดสอบที่รันได้ วิธีเดิมต้องเขียนทดสอบด้วยมือหรือเข้าถึงโค้ดเพื่อบริบท แต่กับ Playwright MCP คุณสามารถทดสอบเว็บไซต์ภายนอก แอปไคลเอนต์ หรือทำการทดสอบแบบกล่องดำที่ไม่สามารถเข้าถึงโค้ดได้

### 8. 💻 Dev Box MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Dev_Box_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Dev_Box_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Dev%20Box%20MCP&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22%40microsoft%2Fmcp-devbox%40latest%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/microsoft/mcp)

**ทำอะไรได้บ้าง**: จัดการสภาพแวดล้อม Microsoft Dev Box ผ่านภาษาธรรมชาติ

**ทำไมถึงมีประโยชน์**: ช่วยให้การจัดการสภาพแวดล้อมการพัฒนาง่ายขึ้นมาก! สร้าง กำหนดค่า และจัดการสภาพแวดล้อมโดยไม่ต้องจำคำสั่งเฉพาะ

**การใช้งานจริง**: "ตั้งค่า Dev Box ใหม่พร้อม .NET SDK เวอร์ชันล่าสุดและกำหนดค่าสำหรับโปรเจกต์ของเรา", "ตรวจสอบสถานะของสภาพแวดล้อมการพัฒนาทั้งหมดของฉัน" หรือ "สร้างสภาพแวดล้อมสาธิตมาตรฐานสำหรับการนำเสนอทีม"

**ตัวอย่างเด่น**: ฉันชอบใช้ Dev Box สำหรับการพัฒนาส่วนตัว ช่วงที่ประทับใจคือเมื่อ James Montemagno อธิบายว่า Dev Box ดีแค่ไหนสำหรับการสาธิตในงานประชุม เพราะมีการเชื่อมต่ออีเธอร์เน็ตที่รวดเร็วไม่ว่าจะอยู่ที่ไหน ไม่ว่าจะเป็นงานประชุม โรงแรม หรือไวไฟบนเครื่องบิน จริงๆ แล้วฉันเพิ่งฝึกสาธิตงานประชุมขณะใช้โน้ตบุ๊กเชื่อมต่อกับฮอตสปอตโทรศัพท์มือถือระหว่างนั่งรถบัสจากบรูกส์ไปแอนต์เวิร์ป! ขั้นตอนต่อไปของฉันคือการจัดการทีมที่มีหลายสภาพแวดล้อมการพัฒนาและสภาพแวดล้อมสาธิตมาตรฐาน อีกหนึ่งกรณีการใช้งานที่ได้ยินจากลูกค้าและเพื่อนร่วมงานคือการใช้ Dev Box สำหรับสภาพแวดล้อมพัฒนาที่ตั้งค่าล่วงหน้า ในทั้งสองกรณี การใช้ MCP เพื่อกำหนดค่าและจัดการ Dev Box ช่วยให้คุณโต้ตอบด้วยภาษาธรรมชาติได้ทั้งหมดโดยไม่ต้องออกจากสภาพแวดล้อมการพัฒนา

### 9. 🤖 Azure AI Foundry MCP Server
[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_Azure_AI_Foundry_MCP-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_Azure_AI_Foundry_MCP-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=Azure%20Foundry%20MCP%20Server&config=%7B%22type%22%3A%22stdio%22%2C%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22--prerelease%3Dallow%22%2C%22--from%22%2C%22git%2Bhttps%3A%2F%2Fgithub.com%2Fazure-ai-foundry%2Fmcp-foundry.git%22%2C%22run-azure-ai-foundry-mcp%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/azure-ai-foundry/mcp-foundry)

**สิ่งที่ทำได้**: Azure AI Foundry MCP Server มอบการเข้าถึงระบบนิเวศ AI ของ Azure อย่างครบถ้วนสำหรับนักพัฒนา รวมถึงแคตตาล็อกโมเดล การจัดการการปรับใช้ การจัดทำดัชนีความรู้ด้วย Azure AI Search และเครื่องมือประเมินผล เซิร์ฟเวอร์ทดลองนี้เป็นสะพานเชื่อมระหว่างการพัฒนา AI กับโครงสร้างพื้นฐาน AI อันทรงพลังของ Azure ช่วยให้ง่ายต่อการสร้าง ปรับใช้ และประเมินแอปพลิเคชัน AI

**ทำไมถึงมีประโยชน์**: เซิร์ฟเวอร์นี้เปลี่ยนวิธีการทำงานกับบริการ Azure AI โดยนำความสามารถ AI ระดับองค์กรมาไว้ในกระบวนการพัฒนาของคุณโดยตรง แทนที่จะต้องสลับไปมาระหว่างพอร์ทัล Azure เอกสาร และ IDE คุณสามารถค้นหาโมเดล ปรับใช้บริการ จัดการฐานความรู้ และประเมินประสิทธิภาพ AI ผ่านคำสั่งภาษาธรรมชาติ เหมาะอย่างยิ่งสำหรับนักพัฒนาที่สร้างแอป RAG (Retrieval-Augmented Generation) จัดการการปรับใช้โมเดลหลายตัว หรือสร้างกระบวนการประเมิน AI อย่างครบวงจร

**ความสามารถหลักสำหรับนักพัฒนา**:
- **🔍 ค้นหาและปรับใช้โมเดล**: สำรวจแคตตาล็อกโมเดลของ Azure AI Foundry ดูข้อมูลโมเดลอย่างละเอียดพร้อมตัวอย่างโค้ด และปรับใช้โมเดลไปยัง Azure AI Services
- **📚 การจัดการความรู้**: สร้างและจัดการดัชนี Azure AI Search เพิ่มเอกสาร กำหนดค่าตัวจัดทำดัชนี และสร้างระบบ RAG ที่ซับซ้อน
- **⚡ การเชื่อมต่อ AI Agent**: เชื่อมต่อกับ Azure AI Agents สอบถามเอเจนต์ที่มีอยู่ และประเมินประสิทธิภาพเอเจนต์ในสถานการณ์ใช้งานจริง
- **📊 กรอบการประเมินผล**: รันการประเมินข้อความและเอเจนต์อย่างครบถ้วน สร้างรายงานในรูปแบบ markdown และนำไปใช้กับการประกันคุณภาพของแอป AI
- **🚀 เครื่องมือสร้างต้นแบบ**: รับคำแนะนำการตั้งค่าสำหรับการสร้างต้นแบบบน GitHub และเข้าถึง Azure AI Foundry Labs สำหรับโมเดลวิจัยล้ำสมัย

**การใช้งานจริงของนักพัฒนา**: "ปรับใช้โมเดล Phi-4 ไปยัง Azure AI Services สำหรับแอปของฉัน", "สร้างดัชนีการค้นหาใหม่สำหรับระบบ RAG ของเอกสาร", "ประเมินการตอบสนองของเอเจนต์ตามเกณฑ์คุณภาพ" หรือ "ค้นหาโมเดลเหตุผลที่ดีที่สุดสำหรับงานวิเคราะห์ที่ซับซ้อนของฉัน"

**สถานการณ์สาธิตเต็มรูปแบบ**: นี่คือเวิร์กโฟลว์การพัฒนา AI ที่ทรงพลัง:


> "ฉันกำลังสร้างเอเจนต์สนับสนุนลูกค้า ช่วยฉันหโมเดลเหตุผลที่ดีจากแคตตาล็อก ปรับใช้ไปยัง Azure AI Services สร้างฐานความรู้จากเอกสารของเรา ตั้งค่ากรอบการประเมินผลเพื่อทดสอบคุณภาพการตอบสนอง และช่วยฉันสร้างต้นแบบการเชื่อมต่อกับ GitHub token สำหรับการทดสอบ"

Azure AI Foundry MCP Server จะ:
- สอบถามแคตตาล็อกโมเดลเพื่อแนะนำโมเดลเหตุผลที่เหมาะสมตามความต้องการของคุณ
- ให้คำสั่งปรับใช้และข้อมูลโควตาสำหรับภูมิภาค Azure ที่คุณเลือก
- ตั้งค่า Azure AI Search ดัชนีด้วยสคีมาที่เหมาะสมสำหรับเอกสารของคุณ
- กำหนดค่ากระบวนการประเมินผลด้วยเกณฑ์คุณภาพและการตรวจสอบความปลอดภัย
- สร้างโค้ดต้นแบบพร้อมการยืนยันตัวตน GitHub สำหรับการทดสอบทันที
- ให้คำแนะนำการตั้งค่าอย่างละเอียดที่เหมาะกับเทคโนโลยีของคุณ

**ตัวอย่างเด่น**: ในฐานะนักพัฒนา ฉันเคยลำบากกับการตามหาโมเดล LLM ที่หลากหลาย รู้จักแค่ไม่กี่โมเดลหลัก แต่รู้สึกเหมือนพลาดโอกาสในการเพิ่มประสิทธิภาพและผลผลิต และการจัดการโทเค็นกับโควตาก็เครียดและยากที่จะควบคุม – ไม่เคยแน่ใจว่ากำลังเลือกโมเดลที่เหมาะสมกับงานหรือใช้จ่ายงบประมาณอย่างไม่คุ้มค่า ฉันเพิ่งได้ยินเกี่ยวกับ MCP Server นี้จาก James Montemagno ขณะพูดคุยกับเพื่อนร่วมงานเกี่ยวกับคำแนะนำ MCP Server สำหรับโพสต์นี้ และตื่นเต้นที่จะได้ลองใช้ ความสามารถในการค้นหาโมเดลดูน่าประทับใจมากสำหรับคนอย่างฉันที่อยากสำรวจโมเดลนอกเหนือจากที่รู้จัก และหาโมเดลที่เหมาะกับงานเฉพาะ กรอบการประเมินผลน่าจะช่วยยืนยันว่าฉันได้ผลลัพธ์ที่ดีขึ้นจริง ไม่ใช่แค่ลองของใหม่เฉยๆ

> **ℹ️ สถานะทดลอง**
> 
> MCP server นี้อยู่ในสถานะทดลองและกำลังพัฒนาอย่างต่อเนื่อง ฟีเจอร์และ API อาจมีการเปลี่ยนแปลง เหมาะสำหรับการสำรวจความสามารถของ Azure AI และสร้างต้นแบบ แต่ควรตรวจสอบความเสถียรสำหรับการใช้งานจริง

### 10. 🏢 Microsoft 365 Agents Toolkit MCP Server

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_M365_Agents_Toolkit-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D) [![Install in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-Install_M365_Agents_Toolkit-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=M365AgentsToolkit%20Server&config=%7B%22command%22%3A%22npx%22%2C%22args%22%3A%5B%22-y%22%2C%22@microsoft%2Fm365agentstoolkit-mcp%40latest%22%2C%22server%22%2C%22start%22%5D%7D&quality=insiders) [![GitHub](https://img.shields.io/badge/GitHub-View_Repository-181717?style=flat-square&logo=github&logoColor=white)](https://github.com/OfficeDev/microsoft-365-agents-toolkit)

**สิ่งที่ทำได้**: มอบเครื่องมือสำคัญสำหรับนักพัฒนาในการสร้างเอเจนต์ AI และแอปพลิเคชันที่ผสานกับ Microsoft 365 และ Microsoft 365 Copilot รวมถึงการตรวจสอบสคีมา การดึงตัวอย่างโค้ด และช่วยแก้ไขปัญหา

**ทำไมถึงมีประโยชน์**: การพัฒนาสำหรับ Microsoft 365 และ Copilot มีความซับซ้อนในเรื่องสคีมา manifest และรูปแบบการพัฒนาเฉพาะ เซิร์ฟเวอร์ MCP นี้นำทรัพยากรสำคัญมาไว้ในสภาพแวดล้อมการเขียนโค้ดของคุณ ช่วยตรวจสอบสคีมา ค้นหาตัวอย่างโค้ด และแก้ไขปัญหาทั่วไปโดยไม่ต้องเปิดเอกสารบ่อยๆ

**การใช้งานจริง**: "ตรวจสอบ manifest ของเอเจนต์แบบ declarative และแก้ไขข้อผิดพลาดสคีมา", "แสดงตัวอย่างโค้ดสำหรับการใช้งาน Microsoft Graph API plugin" หรือ "ช่วยแก้ไขปัญหาการยืนยันตัวตนของแอป Teams ของฉัน"

**ตัวอย่างเด่น**: ฉันติดต่อเพื่อน John Miller หลังจากคุยกับเขาที่งาน Build เกี่ยวกับ M365 Agents และเขาแนะนำ MCP นี้ เหมาะมากสำหรับนักพัฒนาที่เพิ่งเริ่มกับ M365 Agents เพราะมีเทมเพลต ตัวอย่างโค้ด และโครงสร้างพื้นฐานให้เริ่มต้นโดยไม่ต้องจมกับเอกสาร ฟีเจอร์ตรวจสอบสคีมาดูมีประโยชน์มากในการหลีกเลี่ยงข้อผิดพลาดโครงสร้าง manifest ที่อาจทำให้ต้องดีบักนานหลายชั่วโมง

> **💡 เคล็ดลับมือโปร**
> 
> ใช้เซิร์ฟเวอร์นี้ควบคู่กับ Microsoft Learn Docs MCP Server เพื่อการสนับสนุนการพัฒนา M365 อย่างครบถ้วน – ตัวหนึ่งให้เอกสารอย่างเป็นทางการ อีกตัวให้เครื่องมือพัฒนาและช่วยแก้ไขปัญหา

## ต่อไปคืออะไร? 🔮

## 📋 สรุป

Model Context Protocol (MCP) กำลังเปลี่ยนวิธีที่นักพัฒนาสื่อสารกับผู้ช่วย AI และเครื่องมือภายนอก เซิร์ฟเวอร์ MCP ของ Microsoft ทั้ง 10 ตัวนี้แสดงให้เห็นถึงพลังของการผสานรวม AI แบบมาตรฐาน ช่วยให้เวิร์กโฟลว์ทำงานได้อย่างราบรื่นและรักษาสภาวะการทำงานของนักพัฒนาในขณะที่เข้าถึงความสามารถภายนอกที่ทรงพลัง

ตั้งแต่การผสานรวมระบบนิเวศ Azure อย่างครบถ้วนไปจนถึงเครื่องมือเฉพาะทางอย่าง Playwright สำหรับอัตโนมัติบนเบราว์เซอร์ และ MarkItDown สำหรับประมวลผลเอกสาร เซิร์ฟเวอร์เหล่านี้แสดงให้เห็นว่า MCP สามารถเพิ่มประสิทธิภาพการทำงานในสถานการณ์พัฒนาที่หลากหลายได้อย่างไร โปรโตคอลมาตรฐานช่วยให้เครื่องมือเหล่านี้ทำงานร่วมกันได้อย่างไร้รอยต่อ สร้างประสบการณ์การพัฒนาที่สอดคล้องกัน

เมื่อระบบนิเวศ MCP ยังคงพัฒนาอย่างต่อเนื่อง การมีส่วนร่วมกับชุมชน สำรวจเซิร์ฟเวอร์ใหม่ๆ และสร้างโซลูชันเฉพาะจะเป็นกุญแจสำคัญในการเพิ่มประสิทธิภาพการพัฒนาของคุณ ธรรมชาติแบบเปิดของ MCP หมายความว่าคุณสามารถผสมผสานเครื่องมือจากผู้ขายต่างๆ เพื่อสร้างเวิร์กโฟลว์ที่สมบูรณ์แบบสำหรับความต้องการเฉพาะของคุณ

## 🔗 แหล่งข้อมูลเพิ่มเติม

- [Official Microsoft MCP Repository](https://github.com/microsoft/mcp)
- [MCP Community & Documentation](https://modelcontextprotocol.io/introduction)
- [VS Code MCP Documentation](https://code.visualstudio.com/docs/copilot/copilot-mcp)
- [Visual Studio MCP Documentation](https://learn.microsoft.com/visualstudio/ide/mcp-servers)
- [Azure MCP Documentation](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- [Let's Learn – MCP Events](https://techcommunity.microsoft.com/blog/azuredevcommunityblog/lets-learn---mcp-events-a-beginners-guide-to-the-model-context-protocol/4429023)
- [Awesome GitHub Copilot Customizations](https://github.com/awesome-copilot)
- [C# MCP SDK](https://developer.microsoft.com/blog/microsoft-partners-with-anthropic-to-create-official-c-sdk-for-model-context-protocol)
- [MCP Dev Days Live 29th/30th July or watch on Demand ](https://aka.ms/mcpdevdays)

## 🎯 แบบฝึกหัด

1. **ติดตั้งและตั้งค่า**: ตั้งค่า MCP server ตัวใดตัวหนึ่งในสภาพแวดล้อม VS Code ของคุณและทดสอบฟังก์ชันพื้นฐาน
2. **ผสานเวิร์กโฟลว์**: ออกแบบเวิร์กโฟลว์การพัฒนาที่รวม MCP server อย่างน้อยสามตัวเข้าด้วยกัน
3. **วางแผนเซิร์ฟเวอร์เฉพาะ**: ระบุงานในกิจวัตรการพัฒนาประจำวันของคุณที่อาจได้รับประโยชน์จาก MCP server เฉพาะ และสร้างข้อกำหนดสำหรับมัน
4. **วิเคราะห์ประสิทธิภาพ**: เปรียบเทียบประสิทธิภาพการใช้ MCP server กับวิธีการแบบดั้งเดิมสำหรับงานพัฒนาทั่วไป
5. **ประเมินความปลอดภัย**: ประเมินผลกระทบด้านความปลอดภัยของการใช้ MCP server ในสภาพแวดล้อมการพัฒนาของคุณและเสนอแนวทางปฏิบัติที่ดีที่สุด

ถัดไป:[Best Practices](../08-BestPractices/README.md)

**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษาอัตโนมัติ [Co-op Translator](https://github.com/Azure/co-op-translator) แม้เราจะพยายามให้ความถูกต้องสูงสุด แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาต้นทางถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลโดยผู้เชี่ยวชาญมนุษย์ เราไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดใด ๆ ที่เกิดจากการใช้การแปลนี้