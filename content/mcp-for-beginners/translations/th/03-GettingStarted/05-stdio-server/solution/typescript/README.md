<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "9d799c4a30a8383e0a74af9153262972",
  "translation_date": "2025-08-26T20:10:09+00:00",
  "source_file": "03-GettingStarted/05-stdio-server/solution/typescript/README.md",
  "language_code": "th"
}
-->
# MCP stdio Server - TypeScript Solution

> **⚠️ สำคัญ**: โซลูชันนี้ได้รับการอัปเดตให้ใช้ **stdio transport** ตามที่แนะนำใน MCP Specification 2025-06-18 โดยการส่งข้อมูลแบบ SSE เดิมได้ถูกยกเลิกแล้ว

## ภาพรวม

โซลูชัน TypeScript นี้แสดงให้เห็นวิธีการสร้าง MCP server โดยใช้ stdio transport ในปัจจุบัน ซึ่ง stdio transport นั้นง่ายกว่า ปลอดภัยกว่า และมีประสิทธิภาพดีกว่าการส่งข้อมูลแบบ SSE ที่ถูกยกเลิกไปแล้ว

## สิ่งที่ต้องเตรียม

- Node.js 18+ หรือเวอร์ชันที่ใหม่กว่า
- ตัวจัดการแพ็กเกจ npm หรือ yarn

## คำแนะนำในการตั้งค่า

### ขั้นตอนที่ 1: ติดตั้ง dependencies

```bash
npm install
```

### ขั้นตอนที่ 2: สร้างโปรเจกต์

```bash
npm run build
```

## การรันเซิร์ฟเวอร์

เซิร์ฟเวอร์ stdio ทำงานแตกต่างจากเซิร์ฟเวอร์ SSE แบบเก่า โดยแทนที่จะเริ่มต้นเว็บเซิร์ฟเวอร์ มันจะสื่อสารผ่าน stdin/stdout:

```bash
npm start
```

**สำคัญ**: เซิร์ฟเวอร์อาจดูเหมือนค้าง - นี่เป็นเรื่องปกติ! มันกำลังรอข้อความ JSON-RPC จาก stdin

## การทดสอบเซิร์ฟเวอร์

### วิธีที่ 1: ใช้ MCP Inspector (แนะนำ)

```bash
npm run inspector
```

สิ่งนี้จะ:
1. เปิดเซิร์ฟเวอร์ของคุณเป็น subprocess
2. เปิดอินเทอร์เฟซเว็บสำหรับการทดสอบ
3. ให้คุณทดสอบเครื่องมือเซิร์ฟเวอร์ทั้งหมดแบบโต้ตอบ

### วิธีที่ 2: การทดสอบผ่านคำสั่งใน command line โดยตรง

คุณสามารถทดสอบได้โดยการเปิด Inspector โดยตรง:

```bash
npx @modelcontextprotocol/inspector node build/index.js
```

### เครื่องมือที่มีให้ใช้งาน

เซิร์ฟเวอร์มีเครื่องมือดังต่อไปนี้:

- **add(a, b)**: บวกตัวเลขสองตัวเข้าด้วยกัน
- **multiply(a, b)**: คูณตัวเลขสองตัวเข้าด้วยกัน  
- **get_greeting(name)**: สร้างข้อความทักทายแบบเฉพาะบุคคล
- **get_server_info()**: รับข้อมูลเกี่ยวกับเซิร์ฟเวอร์

### การทดสอบกับ Claude Desktop

หากต้องการใช้เซิร์ฟเวอร์นี้กับ Claude Desktop ให้เพิ่มการตั้งค่านี้ลงใน `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "example-stdio-server": {
      "command": "node",
      "args": ["path/to/build/index.js"]
    }
  }
}
```

## โครงสร้างโปรเจกต์

```
typescript/
├── src/
│   └── index.ts          # Main server implementation
├── build/                # Compiled JavaScript (generated)
├── package.json          # Project configuration
├── tsconfig.json         # TypeScript configuration
└── README.md            # This file
```

## ความแตกต่างสำคัญจาก SSE

**stdio transport (ปัจจุบัน):**
- ✅ การตั้งค่าง่ายกว่า - ไม่ต้องใช้ HTTP server
- ✅ ความปลอดภัยดีกว่า - ไม่มี HTTP endpoints
- ✅ การสื่อสารแบบ subprocess
- ✅ JSON-RPC ผ่าน stdin/stdout
- ✅ ประสิทธิภาพดีกว่า

**SSE transport (ถูกยกเลิก):**
- ❌ ต้องตั้งค่า Express server
- ❌ ต้องจัดการ routing และ session ที่ซับซ้อน
- ❌ มี dependencies มากกว่า (Express, HTTP handling)
- ❌ มีข้อพิจารณาด้านความปลอดภัยเพิ่มเติม
- ❌ ถูกยกเลิกใน MCP 2025-06-18

## เคล็ดลับสำหรับการพัฒนา

- ใช้ `console.error()` สำหรับการบันทึกข้อความ (อย่าใช้ `console.log()` เพราะมันเขียนไปยัง stdout)
- สร้างโปรเจกต์ด้วย `npm run build` ก่อนการทดสอบ
- ทดสอบด้วย Inspector เพื่อการดีบักแบบภาพ
- ตรวจสอบให้แน่ใจว่าข้อความ JSON ทั้งหมดถูกจัดรูปแบบอย่างถูกต้อง
- เซิร์ฟเวอร์จัดการการปิดตัวลงอย่างปลอดภัยโดยอัตโนมัติเมื่อได้รับ SIGINT/SIGTERM

โซลูชันนี้ปฏิบัติตาม MCP specification ในปัจจุบันและแสดงให้เห็นถึงแนวทางปฏิบัติที่ดีที่สุดสำหรับการใช้งาน stdio transport ด้วย TypeScript

---

**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้ว่าเราจะพยายามให้การแปลมีความถูกต้อง แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่แม่นยำ เอกสารต้นฉบับในภาษาดั้งเดิมควรถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลภาษามนุษย์ที่เป็นมืออาชีพ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความที่ผิดพลาดซึ่งเกิดจากการใช้การแปลนี้