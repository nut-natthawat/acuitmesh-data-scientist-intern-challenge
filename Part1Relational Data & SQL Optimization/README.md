## 1. การสร้าง Schema
การสร้าง schema ผมสร้าง table data อันหลักมาอันนึงก่อน และเพิ่ม column `Geometry point` ไว้เก็บพิกัดบนแผนที่ ต่อมาผมได้สร้าง `b-tree index` บน coulmn `crime_date` มาอีกอันเพื่อความเร็วในการหาข้อมูลในdatabase ทำให้ db ไม่ต้องไปหา data จากทั้ง db ต่อจากอันนี้ผมได้เพิ่ม index ของ district เข้าไปด้วยเพื่อให้นำ data ออกมาใช้ได้ง่ายๆ ต่อมาผมใช้ **PostGIS** ในการสร้าง index เพื่อใช้ในการ query พื้นที่

---

## 2. การ Ingest Data และ Data Integrity
ในส่วนต่อมาคือการ ingest data เข้า db ก่อนจะเอา data เข้าผมได้ทำ check data integrity โดยเฉพาะ column `Latitude/Longitude` ผลลัพธ์คือมี **Missing Latitude/Longitude: 71 rows (0.07%)** และ Handling Strategy ที่ผมคิดไว้คือถ้า missing ไปเกิน 5-10% ก็ drop ทิ้งครับ แต่ถ้าไม่ drop จริงๆจะใช้การประมาณค่าของ district กับเขตที่ใกล้เคียงและหาจุดกึ่งกลางของเขตนั้นๆครับ ไม่ใช้ค่า mean/median 

ต่อมาผมได้ tranform data นิดหน่อยครับคือการเปลี่ยนชื่อ column จาก `Case Number` เป็น `case_number` เพื่อไม่ให้เกิดปัญหาตอนเอา data เข้า db ครับ ต่อมาผมก็ใช้การแบ่งข้อมูลทีละนิดเข้า db เข้าทีละ 10000 row เพื่อไม้ให้มันระเบิดครับ ต่อมาผมใช้ **PostGSI** เอาตัวเลข `Latitude/Longitude` เก็บไปใน coloumn `geom` ครับ

---

## 3. SQL: การคำนวณ 7-Day Rolling Average
ในส่วน sql ในการหา 7-day rolling average ได้ทำการหาวันล่าสุดของข้อมูลก่อนเพื่อที่จะย้อนหลังไปได้ 30 วัน ต่อมาผมก็ filter เอาแค่ theft แล้วเอามารวมกันโดย `group by` district กับ date ว่ารวมกี่คดี 

ต่อมาการคำนวนผมใช้ `PARTITION BY district` เพื่อให้ db มันคำนวนตาม district แบบแยกกัน `order by` date เพื่อเรียงวัน เสร็จแล้วผมใช้ `RANGE BETWEEN INTERVAL '6 days' PRECEDING` บังคับให้ Database รวมวันปัจจุบัน + ย้อนไป 6 วัน = 7 วันพอดีเผื่อมีบางวันที่หายไปอาจทำให้ db เอา data ของวันอื่นมาแทน


###สิ่งที่ทำไม่เสร็จคือ Part2 ครับเพราะว่าผมทำไม่ทันครับ project ที่คณะเยอะมากครับผมขอโทษ
