# -*- coding:utf-8 -*-
import os
import xlwt
import decimal

from datetime import datetime 


def excelwrite(jsondata, username):
        book = xlwt.Workbook(encoding = 'utf-8', style_compression = 0)
        sheet = book.add_sheet('output', cell_overwrite_ok = True)
        firstlinestyle = xlwt.easyxf('pattern:pattern solid, fore_colour blue; align: vertical center, horizontal center; font: height 300, bold true, colour white; borders: top double, bottom double, left double, right double;')
        contentstyle = xlwt.easyxf('pattern:pattern solid, fore_colour white; align: wrap on, vertical center, horizontal center; font: bold true, colour black; borders: top double, bottom double, left double, right double;')
        for colIndex in range(0, 10):
                if colIndex in [2, 5] :
                        sheet.col(colIndex).width = 10000
                else :
                        sheet.col(colIndex).width = 7000
        sheet.write(0, 0, u'批件编号', firstlinestyle)
        sheet.write(0, 1, u'批件名', firstlinestyle)
        sheet.write(0, 2, u'批件内容', firstlinestyle)
        sheet.write(0, 3, u'批件开始时间', firstlinestyle)
        sheet.write(0, 4, u'批件结束时间', firstlinestyle)
        sheet.write(0, 5, u'单个优惠金额/已经优惠金额(元)', firstlinestyle)
        sheet.write(0, 8, u'使用率(百分比)', firstlinestyle)
        sheet.write(0, 6, u'所属部门',firstlinestyle)
        sheet.write(0, 7, u'批准数量/已使用', firstlinestyle)
        sheet.write_merge(0, 0, 9, 10, u'使用情况', firstlinestyle)
        sumline = 0
       
        for index, data in enumerate(jsondata):
                used = 0
                startline = sumline +1   
                if data["couponusage"]:            
                        for i in data["couponusage"].all():
                                sumline = sumline + 1
                                sheet.write(sumline, 9, i.get('registrationplace', u'无').encode("utf-8").replace('u', '').replace('\'', ''),contentstyle)
                                sheet.write(sumline, 10, i.get('count', 0),contentstyle)
				used = used + i.get('count', 0)
                else :
                        sumline = sumline + 1
			sheet.write(sumline, 9, u'无',contentstyle)
                        sheet.write(sumline, 10, 0,contentstyle)
                endline = sumline if sumline>= startline else startline
                sheet.write_merge(startline, endline, 0, 0, data["coreid"], contentstyle)
                sheet.write_merge(startline, endline, 1, 1, data["couponname"], contentstyle)
                sheet.write_merge(startline, endline, 2, 2, data["content"], contentstyle)
                sheet.write_merge(startline, endline, 3, 3, data["starttime"], contentstyle)
                sheet.write_merge(startline, endline, 4, 4, data["endtime"], contentstyle)
                sheet.write_merge(startline, endline, 5, 5, '{}/{}'.format(data["account"],(decimal.Decimal(data["account"])*used).quantize(decimal.Decimal('0.00'))), contentstyle)
                sheet.write_merge(startline, endline, 8, 8, (decimal.Decimal(used)/decimal.Decimal(data["amount"])*100).quantize(decimal.Decimal('0.00')) , contentstyle)
                sheet.write_merge(startline, endline, 6, 6, data["departmentname"],contentstyle)
                sheet.write_merge(startline, endline, 7, 7, '{}/{}'.format(data["amount"],used),contentstyle)
        filename = 'coupon_{0}__{1}.xls'.format(datetime.now().strftime("_%b_%d_%Y_%H_%M_%S_"), username)
        filefullpath = '{}/{}'.format(os.path.dirname(__file__), filename)
        book.save(filefullpath)
        return '/download/excel/{}'.format(filename) 
