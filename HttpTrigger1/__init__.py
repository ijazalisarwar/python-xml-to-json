import logging
import json, xmltodict
import azure.functions as func
import xml.etree.ElementTree as ET


def main(req: func.HttpRequest,  inputblob: func.InputStream, outputblob: func.Out[func.InputStream]) -> func.HttpResponse:

    try:
        data = inputblob.read()   # read data from blob
        root = ET.fromstringlist(data.decode("utf-8"))
        instance_element = root.findall("./Properties/InstanceElement")
        
        list_dict = []
        # iterate over childs of inatance element:
        for element in instance_element:
            # in child we have to insert id of parent
            for sub_element in element:
                sub_element.set("IDElement", element.attrib["ID"])
                list_dict.append(sub_element.attrib)
        outputblob.set(json.dumps(list_dict))


        return func.HttpResponse(
                "This HTTP triggered function executed successfully.",
                status_code=200
            )
    except ValueError as ex:
        return func.HttpResponse(
             "Unknown error has occured tih message: " + str(ex),
             status_code=400
        )

        
