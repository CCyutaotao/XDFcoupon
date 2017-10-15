# -*- coding:utf-8 -*-
import os

from django.http import StreamingHttpResponse

def excel_download(request, filename):
    print filename
    def file_iterator(file_name, chunk_size = 512):
	with open('{}/{}'.format(os.path.dirname(__file__), filename), 'rb') as f:
		while True:
			c = f.read(chunk_size)
			if c:
				yield c
			else:
				break


    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/vnd.ms-excel'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)

    return response


def docx_download(request, filename):
    print filename
    def file_iterator(file_name, chunk_size = 512):
        with open('{}/{}'.format(os.path.dirname(__file__), filename), 'rb') as f:
                while True:
                        c = f.read(chunk_size)
                        if c:
                                yield c
                        else:
                                break


    response = StreamingHttpResponse(file_iterator(filename))
    response['Content-Type'] = 'application/vnd.ms-word'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(filename)

    return response

