#!/usr/bin/env python3
"""Original fictional equipment manual with measured text frames and vector figures."""
import argparse
import importlib.util
import json
from collections import defaultdict
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('preflight', ROOT / 'skills/plain-docs/scripts/preflight.py')
preflight = importlib.util.module_from_spec(spec)
spec.loader.exec_module(preflight)
W, H = A4
INK, BLUE, MUTED, RULE, PALE = '#172B3A', '#006B92', '#52636E', '#CED7DD', '#EDF4F7'


class Manual:
    def __init__(self, args):
        self.args, self.page, self.records = args, 0, []
        self.used, self.faces = defaultdict(str), {}
        self.paths = {'en': args.latin_regular, 'enb': args.latin_bold,
                      'tc': args.tc_regular, 'tcb': args.tc_bold,
                      'sc': args.sc_regular, 'scb': args.sc_bold}
        for name, path in self.paths.items():
            self.faces[name] = TTFont(name, str(path), subfontIndex=0)
            pdfmetrics.registerFont(self.faces[name])
        args.out.parent.mkdir(parents=True, exist_ok=True)
        self.c = Canvas(str(args.out), pagesize=A4, initialFontName='en', lang='en', pageCompression=1)
        self.c.setTitle('SampleLogger S1 User Manual - Design Evaluation Edition')
        self.c.setAuthor('Plain Docs')
        self.c.setSubject('Original fictional technical equipment manual with English and Chinese reference pages')

    def color(self, value):
        return colors.HexColor(value)

    def line(self, x1, y1, x2, y2, color=RULE, width=.65):
        self.c.setStrokeColor(self.color(color)); self.c.setLineWidth(width)
        self.c.line(x1, H-y1, x2, H-y2)

    def rect(self, x, y, w, h, fill=None, stroke=RULE, radius=0, lw=.7):
        self.c.setLineWidth(lw)
        if fill: self.c.setFillColor(self.color(fill))
        if stroke: self.c.setStrokeColor(self.color(stroke))
        f = self.c.roundRect if radius else self.c.rect
        args = [x,H-y-h,w,h] + ([radius] if radius else [])
        f(*args, fill=bool(fill), stroke=bool(stroke))

    def circle(self, x, y, r, fill=None, stroke=BLUE, lw=.8):
        self.c.setLineWidth(lw)
        if fill: self.c.setFillColor(self.color(fill))
        if stroke: self.c.setStrokeColor(self.color(stroke))
        self.c.circle(x,H-y,r,fill=bool(fill),stroke=bool(stroke))

    def markup(self, text, font):
        runs = []
        for ch in text:
            chosen = font if ord(ch) in self.faces[font].face.charToGlyph else ('enb' if font.endswith('b') else 'en')
            if ord(ch) not in self.faces[chosen].face.charToGlyph:
                raise ValueError(f'No glyph for {ch!r} in {font}')
            self.used[chosen] += ch
            if runs and runs[-1][0] == chosen: runs[-1][1] += ch
            else: runs.append([chosen,ch])
        return ''.join(escape(s) if f==font else f'<font name="{f}">{escape(s)}</font>' for f,s in runs)

    def p(self, x, y, w, text, font='en', size=11, leading=None, color=INK, maxh=None):
        style = ParagraphStyle('p',fontName=font,fontSize=size,leading=leading or size*1.38,
                               textColor=self.color(color),wordWrap='CJK' if font[:2] in ('tc','sc') else None)
        para = Paragraph(self.markup(text,font),style)
        _, height = para.wrap(w, H)
        if maxh is not None and height > maxh+.2:
            raise ValueError(f'Page {self.page}: frame overflow {height:.1f}>{maxh}: {text[:45]}')
        if y+height>H-15: raise ValueError(f'Page overflow: {text[:45]}')
        para.drawOn(self.c,x,H-y-height)
        self.records.append(dict(page=self.page,text=text,bbox=[x,y,w,height]))
        return height

    def txt(self,x,y,text,size=10,font='en',color=INK,align='left'):
        # Labels with mixed-script fallback use the paragraph path.
        return self.p(x if align=='left' else x-pdfmetrics.stringWidth(text,font,size),y,
                      max(pdfmetrics.stringWidth(text,font,size)+3,4),text,font,size,leading=size*1.15,color=color)

    def label(self,x,y,text): self.txt(x,y,text,9,'enb',BLUE)

    def caption(self, y, number, text, x=48, w=499):
        self.label(x,y,f'FIGURE {number}')
        self.p(x+62,y,w-62,text,size=9,color=MUTED)

    def number(self,x,y,n):
        self.circle(x,y,9,fill=BLUE,stroke=None)
        width=pdfmetrics.stringWidth(str(n),'enb',9)
        self.txt(x-width/2,y-5.3,str(n),9,'enb','#FFFFFF')

    def leader(self,n,x,y,tx,ty,bend=None):
        points=[(x,y)] + ([bend] if bend else []) + [(tx,ty)]
        for (a,b),(c,d) in zip(points,points[1:]): self.line(a,b,c,d,BLUE,.65)
        self.circle(tx,ty,2,fill=BLUE,stroke=None)
        self.number(x,y,n)

    def arrow(self,x1,y1,x2,y2):
        from math import atan2,cos,sin,pi
        self.line(x1,y1,x2,y2,BLUE,1.1)
        a=atan2(y2-y1,x2-x1)
        for sign in (-1,1):
            self.line(x2,y2,x2-6*cos(a+sign*pi/7),y2-6*sin(a+sign*pi/7),BLUE,1.1)

    def device(self,x,y,w=320,state='STOPPED',large=False):
        s=w/320
        def r(a,b,c,d,**kw): self.rect(x+a*s,y+b*s,c*s,d*s,**kw)
        def t(a,b,text,size=8,font='en',color=INK): self.txt(x+a*s,y+b*s,text,size*s,font,color)
        r(7,7,320,168,fill='#DDE5EA',stroke='#8396A3',radius=7*s,lw=.9)
        r(0,0,320,168,fill='#F5F7F8',stroke='#6C818F',radius=7*s,lw=1)
        r(5,5,310,158,stroke='#C7D1D8',radius=5*s,lw=.6)
        t(22,11,'SampleLogger',9,'enb'); t(279,11,'S1',9,'enb')
        r(22,31,150,78,fill='#172B3A',stroke=None,radius=3*s)
        t(31,41,'TEMPERATURE',6.5,color='#B6CAD5')
        t(31,56,'23.8 °C',24,'enb','#FFFFFF')
        t(31,89,state+'   4 READINGS',6.5,color='#DAE8EF')
        self.circle(x+202*s,y+39*s,3*s,fill=BLUE,stroke=None)
        t(211,34,'READY',7,'enb')
        for bx,label in [(192,'START'),(251,'STOP')]:
            r(bx,64,48,26,fill='#FFFFFF',stroke='#8396A3',radius=3*s)
            t(bx+8,72,label,8,'enb')
        self.circle(x+215*s,y+133*s,8*s,fill='#FFFFFF',stroke='#6C818F',lw=.8)
        self.circle(x+215*s,y+133*s,3*s,fill='#172B3A',stroke=None)
        t(197,113,'SENSOR',6.5,'enb')
        r(261,128,29,10,fill='#172B3A',stroke=None,radius=4*s)
        r(267,131,17,3,fill='#AABDC7',stroke=None)
        t(266,113,'USB',6.5,'enb')
        for sx in (13,307):
            for sy in (17,151): self.circle(x+sx*s,y+sy*s,1.5*s,stroke='#A2B1BB',lw=.5)
        return {1:(x+22*s,y+70*s),2:(x+202*s,y+39*s),3:(x+216*s,y+64*s),
                4:(x+275*s,y+90*s),5:(x+215*s,y+133*s),6:(x+276*s,y+133*s)}

    def start(self, section,title,slug,font='en'):
        if self.page: self.c.showPage()
        self.page+=1
        self.c.bookmarkPage(slug); self.c.addOutlineEntry(title,slug,level=0)
        self.txt(48,25,'SAMPLELOGGER  /  S1',8.5,'enb',MUTED)
        self.txt(547,25,section,8.5,'en',MUTED,'right')
        self.line(48,48,547,48,BLUE,1.5)
        self.p(48,72,499,title,font+'b',25,leading=32,maxh=64)
        self.footer()

    def footer(self):
        self.line(48,795,547,795)
        self.txt(48,807,'S1 user manual  /  Design evaluation edition',8,'en',MUTED)
        self.txt(493,807,'Contents',8,'en',BLUE,'right')
        self.c.linkRect('', 'contents', (452,H-821,496,H-804), relative=0, thickness=0)
        self.txt(547,804,f'{self.page:02d}',11,'enb',INK,'right')

    def step(self,n,y,title,body,x=198,w=349,font='en',height=66):
        self.number(x+9,y+10,n)
        self.p(x+30,y,w-30,title,font+'b',12,leading=16,maxh=32)
        self.p(x+30,y+23,w-30,body,font,10.5,leading=15,maxh=height-24)

    def table(self,x,y,width,headers,rows,ratios,font='en',size=10.5,rowmin=31):
        cols=[width*r for r in ratios]
        allrows=[headers]+rows
        top=y
        for n,row in enumerate(allrows):
            ff=font+'b' if n==0 else font
            heights=[]
            for value,cw in zip(row,cols):
                pp=Paragraph(self.markup(value,ff),ParagraphStyle('measure',fontName=ff,fontSize=size,leading=size*1.4,wordWrap='CJK' if font!='en' else None))
                heights.append(pp.wrap(cw-16,H)[1])
            rh=max(rowmin,max(heights)+15)
            if n==0: self.rect(x,top,width,rh,fill=PALE,stroke=None)
            xx=x
            for value,cw in zip(row,cols):
                self.p(xx+8,top+7,cw-16,value,ff,size,leading=size*1.4,maxh=rh-13)
                xx+=cw
            self.line(x,top+rh,x+width,top+rh)
            top+=rh
        return top

    def cover(self):
        self.page=1
        self.c.bookmarkPage('contents'); self.c.addOutlineEntry('Contents','contents',0)
        self.txt(48,33,'SAMPLELOGGER',12,'enb',INK)
        self.label(48,89,'S1 TEMPERATURE LOGGER')
        self.p(48,111,499,'User manual','enb',40,leading=46)
        self.p(48,168,405,'Connections, measurement, and data export',size=14,color=MUTED)
        self.device(127,258,337)
        self.p(48,489,499,'A technical manual design specimen for fictional equipment. The instrument, interface, and operating values are original demonstration content.',size=10.5,color=MUTED)
        self.line(48,548,547,548,BLUE,1.3)
        self.label(48,566,'IN THIS GUIDE')
        entries=[('01  Instrument overview','overview',2),('02  Connect and configure','connect',3),
                 ('03  Record a session','record',4),('04  Export and verify','export',5),
                 ('05  Specifications and recovery','reference',6)]
        for i,(label,key,page) in enumerate(entries):
            yy=593+i*28
            self.txt(48,yy,label,11,'en',INK); self.txt(547,yy,f'{page:02d}',11,'enb',BLUE,'right')
            self.c.linkRect('',key,(48,H-yy-19,547,H-yy+2),relative=0,thickness=0)
        self.p(48,743,499,'Chinese quick references: Traditional Chinese 07  /  Simplified Chinese 08',size=9,color=MUTED)
        self.c.linkRect('','traditional',(48,H-762,310,H-741),relative=0,thickness=0)
        self.c.linkRect('','simplified',(310,H-762,547,H-741),relative=0,thickness=0)
        self.footer()

    def overview(self):
        self.start('01  /  INSTRUMENT','Instrument overview','overview')
        self.p(48,119,499,'Identify the display, session controls, and connectors before setting up a measurement. Figure 1 shows the original S1 concept; it is not a manufacturing drawing.',size=11)
        points=self.device(106,214,354)
        self.leader(1,65,269,*points[1]); self.leader(2,340,185,*points[2])
        self.leader(3,496,266,*points[3],bend=(477,266))
        self.leader(4,507,318,*points[4],bend=(487,318))
        self.leader(5,325,434,*points[5]); self.leader(6,431,434,*points[6])
        self.caption(461,1,'S1 front panel. Numbered callouts correspond to the controls below.')
        legends=[('Display','Shows the current temperature, session state, and reading count.'),
                 ('Status indicator','Ready confirms that the sensor is connected.'),
                 ('Start key','Begins recording the configured session.'),
                 ('Stop key','Ends recording and keeps the collected readings.'),
                 ('Sensor input','Connection for the temperature sensor.'),
                 ('USB connector','Connection to the host computer.')]
        for i,(title,body) in enumerate(legends):
            col=i//3; row=i%3; xx=48+col*258; yy=506+row*79
            self.number(xx+9,yy+9,i+1)
            self.p(xx+27,yy-1,212,title,'enb',11)
            self.p(xx+27,yy+19,212,body,size=10.5,leading=14.5,maxh=45)

    def connect(self):
        self.start('02  /  SETUP','Connect and configure','connect')
        self.p(48,119,499,'Connect the sensor and host computer, then confirm the instrument state before creating a session.',size=11)
        self.label(48,176,'CONNECTION PATH')
        # A probe, the same instrument, and a host computer; connectors are kept visible.
        self.rect(69,229,10,72,fill='#F5F7F8',stroke='#728997',radius=5)
        self.line(74,301,74,320,'#728997',1.2)
        points=self.device(153,207,214)
        self.line(74,229,74,200,BLUE,1.1); self.line(74,200,121,200,BLUE,1.1)
        self.line(121,200,121,338,BLUE,1.1); self.line(121,338,points[5][0],338,BLUE,1.1)
        self.line(points[5][0],338,*points[5],BLUE,1.1)
        self.rect(423,215,95,66,fill='#FFFFFF',stroke='#728997',radius=3)
        self.rect(430,222,81,51,fill=PALE,stroke=None)
        self.line(414,286,527,286,'#728997',2)
        self.line(points[6][0],points[6][1],393,points[6][1],BLUE,1.1)
        self.line(393,points[6][1],393,266,BLUE,1.1); self.line(393,266,423,266,BLUE,1.1)
        self.txt(54,349,'Sensor',10,'enb'); self.txt(225,349,'S1',10,'enb'); self.txt(439,349,'Computer',10,'enb')
        self.caption(379,2,'Connect the sensor input and USB host connection. Cable routing is schematic.')
        self.label(48,436,'BEFORE CONNECTION')
        self.p(48,458,119,'Stop any active session. Locate the SENSOR input and USB port using Figure 1.',size=10,color=MUTED,maxh=95)
        self.line(178,433,178,731)
        self.step(1,433,'Connect the sensor','Insert the sensor connector into the SENSOR input shown in Figure 1.',height=76)
        self.step(2,524,'Connect the computer','Connect the USB port to the host computer. Open the SampleLogger application.',height=76)
        self.step(3,615,'Confirm Ready','Check that the status reads Ready. Set Interval to 1 s or longer before recording.',height=81)
        self.line(198,724,547,724)
        self.p(198,737,349,'Expected state: Ready, with no recording in progress.',size=10,color=BLUE)

    def ui(self,x,y,w):
        self.rect(x,y,w,211,fill='#FFFFFF',stroke='#8DA0AC',radius=4)
        self.rect(x,y,w,31,fill=PALE,stroke=None)
        self.txt(x+14,y+9,'S1  /  Session 001',10,'enb')
        self.txt(x+w-14,y+9,'STOPPED',9,'enb',BLUE,'right')
        self.txt(x+14,y+45,'Interval  1 s',9,'en')
        self.txt(x+150,y+45,'Readings  4',9,'en')
        for xx,label in [(x+w-154,'Start'),(x+w-88,'Export')]:
            self.rect(xx,y+39,57,23,fill='#FFFFFF',stroke=RULE,radius=2)
            self.txt(xx+10,y+44,label,9,'enb')
        self.line(x+13,y+72,x+w-13,y+72)
        self.txt(x+18,y+81,'Timestamp',9,'enb',MUTED)
        self.txt(x+226,y+81,'Temperature',9,'enb',MUTED)
        self.txt(x+w-72,y+81,'State',9,'enb',MUTED)
        for i,(time,value) in enumerate([('10:00:00','23.6 °C'),('10:00:01','23.6 °C'),('10:00:02','23.7 °C'),('10:00:03','23.8 °C')]):
            yy=y+105+i*23
            self.txt(x+18,yy,time,10); self.txt(x+226,yy,value,10); self.txt(x+w-72,yy,'Saved',9)
            if i<3: self.line(x+13,yy+18,x+w-13,yy+18)

    def record(self):
        self.start('03  /  OPERATION','Record a session','record')
        self.p(48,119,499,'Create a named session, select the recording interval, and collect readings. The display and application show the same session state.',size=11)
        self.ui(48,184,499)
        self.caption(413,3,'Schematic application interface after a four-reading session. This is a fictional UI.')
        self.label(48,462,'SESSION SEQUENCE')
        for i,(title,body) in enumerate([
            ('Name the measurement','Select New session. Enter a name that identifies the measurement.'),
            ('Set the interval and start','Set Interval to 1 s or longer. Select Start in the application or press the instrument Start key.'),
            ('Watch the count, then stop','Confirm that readings appear and the count increases. Select Stop or press the instrument Stop key when finished.')]):
            self.step(i+1,490+i*85,title,body,x=48,w=499,height=79)
        self.p(78,757,469,'Continue with Export and verify on page 05.',size=10,color=BLUE)
        self.c.linkRect('','export',(78,H-775,350,H-754),relative=0,thickness=0)

    def export(self):
        self.start('04  /  DATA','Export and verify','export')
        self.p(48,119,499,'Export the completed session as CSV (UTF-8). Confirm that the file contains every reading before you archive it.',size=11)
        self.label(48,184,'SAVE THE SESSION')
        self.step(1,216,'Choose the format','Select Export, then choose CSV (UTF-8).',x=48,w=229,height=78)
        self.step(2,313,'Save the file','Save the export as session-001.csv in your chosen folder.',x=48,w=229,height=78)
        self.step(3,410,'Open with UTF-8','Use the import setting for UTF-8 if the application asks you to choose an encoding.',x=48,w=229,height=96)
        self.rect(307,214,240,252,fill='#F6F8F9',stroke=RULE)
        self.txt(324,231,'session-001.csv',11,'enb')
        self.line(324,258,530,258)
        lines=['timestamp,temperature_C','10:00:00,23.6','10:00:01,23.6','10:00:02,23.7','10:00:03,23.8']
        for i,t in enumerate(lines):
            self.txt(323,279+i*28,f'{i+1:02d}',8,'en',MUTED)
            self.txt(347,277+i*28,t,9.5,'en',INK)
        self.caption(487,4,'Example CSV content.',x=307,w=240)
        self.line(48,553,547,553,BLUE,1)
        self.p(48,574,499,'Verify before filing','enb',17)
        self.table(48,612,499,['Check','Expected result'],[
            ['Content','Each data row has a timestamp and temperature value.'],
            ['Row count','4 data rows match the 4 readings in Figure 3. The header is not a reading.'],
            ['Encoding','Text is legible after import with UTF-8. Keep the original file unchanged while checking settings.']],[.25,.75],size=10.5,rowmin=37)

    def reference(self):
        self.start('05  /  REFERENCE','Specifications and recovery','reference')
        self.p(48,119,499,'Reference values for the fictional S1 concept. These values demonstrate technical typesetting and are not specifications for a real instrument.',size=11)
        self.table(48,183,499,['Parameter','Value'],[
            ['Temperature range','−10 °C to 50 °C'],['Resolution','0.1 °C'],
            ['Stated accuracy','±0.5 °C'],['Recording interval','≥ 1 s'],
            ['Input resistance','10 kΩ'],['Standby current','≤ 10 µA'],
            ['Sensor dimensions','20 × 30 mm']],[.58,.42],size=10.5,rowmin=34)
        self.p(48,497,499,'Resolve a problem','enb',17)
        self.table(48,535,499,['Observed state','Check','Next action'],[
            ['Disconnected','Sensor connection','Reconnect the sensor. Confirm Ready before starting again.'],
            ['No new readings','Session state','Confirm that recording has started and the count increases.'],
            ['Garbled CSV text','Import encoding','Import the original CSV with UTF-8 selected.']],[.28,.28,.44],size=10.5,rowmin=52)
        self.p(48,747,499,'Related procedures: connection on page 03; recording on page 04; export on page 05.',size=9.5,color=MUTED)

    def chinese(self, traditional):
        f='tc' if traditional else 'sc'
        title='快速開始' if traditional else '快速开始'
        language='TRADITIONAL CHINESE' if traditional else 'SIMPLIFIED CHINESE'
        self.start('06  /  '+language,title,'traditional' if traditional else 'simplified',f)
        intro=('本頁提供 S1 的操作摘要。產品及圖示均為虛構示範內容；介面名稱保留英文，以便對照控制項。' if traditional else
               '本页提供 S1 的操作摘要。产品及图示均为虚构演示内容；界面名称保留英文，便于对照控件。')
        self.p(48,121,499,intro,f,11,leading=17,maxh=51)
        self.device(298,207,231)
        self.p(48,205,209,'操作順序' if traditional else '操作顺序',f+'b',14)
        steps=([
            ('連接','接妥 SENSOR 與 USB，確認狀態顯示 Ready。'),
            ('設定','選取 New session 並命名。將 Interval 設為 1 s 或更長。'),
            ('記錄','選取 Start。確認讀數筆數增加，完成後選取 Stop。'),
            ('匯出','選取 Export，再選擇 CSV (UTF-8)，儲存至所需資料夾。')]
            if traditional else [
            ('连接','接好 SENSOR 与 USB，确认状态显示 Ready。'),
            ('设置','选择 New session 并命名。将 Interval 设为 1 s 或更长。'),
            ('记录','选择 Start。确认读数数量增加，完成后选择 Stop。'),
            ('导出','选择 Export，再选择 CSV (UTF-8)，保存到所需文件夹。')])
        for i,(t,b) in enumerate(steps):
            yy=241+i*87; self.number(57,yy+9,i+1)
            self.p(78,yy,192,t,f+'b',11.5)
            self.p(78,yy+22,192,b,f,10.5,leading=16,maxh=63)
        self.p(299,356,248,'S1 正面示意圖' if traditional else 'S1 正面示意图',f,9,color=MUTED)
        self.p(299,395,248,'參考數值' if traditional else '参考数值',f+'b',14)
        params=[['溫度範圍' if traditional else '温度范围','−10 °C 至 50 °C'],
                ['解析度' if traditional else '分辨率','0.1 °C'],
                ['標示準確度' if traditional else '标示准确度','±0.5 °C'],
                ['記錄間隔' if traditional else '记录间隔','≥ 1 s']]
        self.table(298,429,249,['參數' if traditional else '参数','數值' if traditional else '数值'],params,[.46,.54],font=f,size=10,rowmin=34)
        self.line(48,642,547,642,BLUE,1)
        self.p(48,665,499,'確認結果' if traditional else '确认结果',f+'b',15)
        check=('以 UTF-8 開啟檔案。每一資料列應包含時間戳記與溫度值，資料列數應與讀數筆數一致；欄位標題列不計入讀數。' if traditional else
               '以 UTF-8 打开文件。每个数据行应包含时间戳与温度值，数据行数应与读数数量一致；列标题行不计入读数。')
        self.p(48,698,499,check,f,11,leading=17,maxh=51)
        self.p(48,756,499,'詳見英文操作圖解，第 03 至 05 頁。' if traditional else '操作图解见英文部分第 03 至 05 页。',f,9.5,color=BLUE)

    def save(self):
        for name,text in self.used.items():
            issues=preflight.scan_text(text,name)+preflight.check_font(text,self.paths[name])
            bad=[i for i in issues if i['level']=='error' or i['code']=='no_subsetting']
            if bad: raise ValueError(json.dumps(bad,ensure_ascii=True))
        self.c.save()
        if self.args.manifest:
            self.args.manifest.parent.mkdir(parents=True,exist_ok=True)
            self.args.manifest.write_text(json.dumps(self.records,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'pdf':str(self.args.out),'pages':self.page,'text_frames':len(self.records)}))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--manifest',type=Path)
    for prefix in ('latin','tc','sc'):
        for weight in ('regular','bold'):
            parser.add_argument(f'--{prefix}-{weight}',type=Path,required=True)
    m=Manual(parser.parse_args())
    m.cover(); m.overview(); m.connect(); m.record(); m.export(); m.reference()
    m.chinese(True); m.chinese(False); m.save()


if __name__=='__main__': main()
