# from turtle import pd
import lxml
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from django.contrib import messages
import json
from lxml import etree
from io import StringIO, BytesIO
from . import validators


def addDataSource(request):
    return render(request, "app/add_data_source.html")


def upload(request):
    if request.method == 'POST':
        filename = str(request.FILES["myFile"])
        if filename.endswith('.json'):
            uploaded_file = request.FILES['myFile']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            file = open('media/' + str(uploaded_file))
            json_string = file.read()
            file.close()

            res = {}
            req = {}
            try:
                req = json.loads(json_string)
            except Exception as e:
                res["details"] = "Invalid request body"
            validation = validators.validate_api(req)
            if not validation["success"]:
                messages.error(request, validation["errors"])
            else:
                messages.success(request, filename + " JSON is valid!")

        elif filename.endswith('.xml'):
            uploaded_file = request.FILES['myFile']
            fs = FileSystemStorage()
            fs.save(uploaded_file.name, uploaded_file)
            filename_xsd = 'file_name.xsd'
            filename_xml = uploaded_file

            # open and read xml file
            with open(str('media/%s' % filename_xml), 'r') as xml_file:
                xml_to_check = xml_file.read()

            # parse xml
            try:
                xml_data = xml_to_check.encode('ascii')
                xml_file = lxml.etree.parse(BytesIO(xml_data))
                xml_validator = lxml.etree.XMLSchema(file='task/%s' % filename_xsd)
                is_valid = xml_validator.validate(xml_file)

                if not is_valid:
                    raise ValueError

                messages.success(request, filename + ' XML well formed, syntax ok.')

            # check for file IO error
            except IOError:
                messages.error(request, 'Invalid File')
            # check for XML syntax errors
            except etree.XMLSyntaxError as err:
                messages.error(request, err)
                with open('error_syntax.log', 'w') as error_log_file:
                    error_log_file.write(str(err.error_log))
            except:
                messages.error(request, 'Unknown error, exiting.')

        else:
            messages.error(request, "File uploaded is not .json or .xml")
    return redirect('/')
