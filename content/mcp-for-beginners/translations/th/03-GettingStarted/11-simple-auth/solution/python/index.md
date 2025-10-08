<!--
CO_OP_TRANSLATOR_METADATA:
{
  "original_hash": "fd28e690667b8ad84bb153cb025cfd73",
  "translation_date": "2025-10-07T01:17:30+00:00",
  "source_file": "03-GettingStarted/11-simple-auth/solution/python/README.md",
  "language_code": "th"
}
-->
# รันตัวอย่าง

## สร้างสภาพแวดล้อม

```sh
python -m venv venv
source ./venv/bin/activate
```

## ติดตั้ง dependencies

```sh
pip install "mcp[cli]" dotenv PyJWT requeests
```

## สร้างโทเค็น

คุณจะต้องสร้างโทเค็นที่ไคลเอนต์จะใช้ในการสื่อสารกับเซิร์ฟเวอร์

เรียกใช้:

```sh
python util.py
```

## รันโค้ด

รันโค้ดด้วย:

```sh
python server.py
```

ในเทอร์มินัลอีกหน้าต่างหนึ่ง ให้พิมพ์:

```sh
python client.py
```

ในเทอร์มินัลของเซิร์ฟเวอร์ คุณควรเห็นข้อความบางอย่างคล้ายกับ:

```text
Valid token, proceeding...
User exists, proceeding...
User has required scope, proceeding...
```

ในหน้าต่างไคลเอนต์ คุณควรเห็นข้อความที่คล้ายกับ:

```text
Tool result: meta=None content=[TextContent(type='text', text='{\n  "current_time": "2025-10-06T17:37:39.847457",\n  "timezone": "UTC",\n  "timestamp": 1759772259.847457,\n  "formatted": "2025-10-06 17:37:39"\n}', annotations=None, meta=None)] structuredContent={'current_time': '2025-10-06T17:37:39.847457', 'timezone': 'UTC', 'timestamp': 1759772259.847457, 'formatted': '2025-10-06 17:37:39'} isError=False
```

นี่หมายความว่าทุกอย่างทำงานได้ถูกต้อง

### เปลี่ยนข้อมูลเพื่อดูข้อผิดพลาด

ค้นหาโค้ดนี้ใน *server.py*:

```python
 if not has_scope(has_header, "Admin.Write"):
```

เปลี่ยนให้เป็นข้อความว่า "User.Write" โทเค็นปัจจุบันของคุณไม่มีระดับสิทธิ์นี้ ดังนั้นหากคุณรีสตาร์ทเซิร์ฟเวอร์และลองรันไคลเอนต์อีกครั้ง คุณควรเห็นข้อผิดพลาดที่คล้ายกับข้อความต่อไปนี้ในเทอร์มินัลของเซิร์ฟเวอร์:

```text
Valid token, proceeding...
User exists, proceeding...
-> Missing required scope!
```

คุณสามารถเปลี่ยนโค้ดเซิร์ฟเวอร์กลับไปเป็นแบบเดิม หรือสร้างโทเค็นใหม่ที่มี scope เพิ่มเติมนี้ก็ได้ ขึ้นอยู่กับคุณ

---

**ข้อจำกัดความรับผิดชอบ**:  
เอกสารนี้ได้รับการแปลโดยใช้บริการแปลภาษา AI [Co-op Translator](https://github.com/Azure/co-op-translator) แม้ว่าเราจะพยายามให้การแปลมีความถูกต้อง แต่โปรดทราบว่าการแปลอัตโนมัติอาจมีข้อผิดพลาดหรือความไม่ถูกต้อง เอกสารต้นฉบับในภาษาดั้งเดิมควรถือเป็นแหล่งข้อมูลที่เชื่อถือได้ สำหรับข้อมูลที่สำคัญ ขอแนะนำให้ใช้บริการแปลภาษามืออาชีพ เราจะไม่รับผิดชอบต่อความเข้าใจผิดหรือการตีความผิดที่เกิดจากการใช้การแปลนี้