import os
from flask import Flask, render_template, request, redirect
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import ContainerClient
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
import json
import datetime

app = Flask(__name__)
CONNECT_STR = "DefaultEndpointsProtocol=https;AccountName=storimjm;AccountKey=inwD1dGGh5ATh04sp56JLdcs+UY" \
              "KnTpnv3tYIKSCrAbFnn1vRi8wJe917limiLQFyGLhqKNyUf48+ASt1LnOsA==;EndpointSuffix=core.windows.net"
CONTAINER_NAME = "762e7379-5fb4-4154-86a7-5add55bdb720"
DOWNLOAD_PATH = 'static/media/upload/'
cog_key = '5fe06065538f4ddaa44af1eea2d2b62a'
cog_endpoint = 'https://ress-vis-jm.cognitiveservices.azure.com/'
computervision_client = ComputerVisionClient(cog_endpoint, CognitiveServicesCredentials(cog_key))


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('viewHome.html')


@app.route('/viewFood', methods=['GET'])
def viewFood():
    food = []
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONNECT_STR)
    container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        tags = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob.name).get_blob_tags()
        food.append({'blob': blob, 'tags': tags})
    return render_template('viewFood.html', foods=food)


@app.route('/deleteFood/<blob_name>', methods=['POST'])
def deleteFood(blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONNECT_STR)
    container_client = blob_service_client.get_container_client(container=CONTAINER_NAME)
    container_client.delete_blob(blob=blob_name)
    return redirect('/viewFood')


@app.route('/inputFoodSearch', methods=['GET'])
def inputFoodSearch():
    return render_template('viewInputFoodSearch.html')


@app.route('/foodSearch', methods=['POST'])
def foodSearch():
    tag = request.form['tag']
    foods = []
    blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONNECT_STR)
    container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        tags = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=blob.name).get_blob_tags()
        food = {'blob': blob, 'tags': tags}
        if tag in food['tags'].keys():
            foods.append(food)
    return render_template('viewFoodImages.html', foods=foods)


@app.route('/viewUploadFood', methods=['GET'])
def viewUploadFood():
    return render_template('viewUploadFood.html')


@app.route('/uploadFood', methods=['POST'])
def uploadFood():
    container_client = ContainerClient.from_connection_string(conn_str=CONNECT_STR, container_name=CONTAINER_NAME)
    files = [request.files.get("file[%d]" % i) for i in range(0, len(request.files))]
    for file in files:
        try:
            container_client.upload_blob(name=file.filename, data=file)
        except:
            print('Blob already exist')
        download_file_path = os.path.join(DOWNLOAD_PATH, file.filename)
        blob_service_client = BlobServiceClient.from_connection_string(conn_str=CONNECT_STR)
        blob_client = blob_service_client.get_container_client(container=CONTAINER_NAME)
        with open(download_file_path, "wb") as download_file:
            download_file.write(blob_client.download_blob(file.filename).readall())
        content = {}
        image_stream = open(DOWNLOAD_PATH + file.filename, "rb")
        description = computervision_client.describe_image_in_stream(image_stream)
        tags = json.dumps(description.tags)
        title = json.dumps(description.captions[0].text)
        date = datetime.datetime.fromisoformat('2020-01-08').now()
        date = str(date).split(".")[0]
        nom = (DOWNLOAD_PATH + file.filename).split('/')[-1]
        nom = nom.replace("é", "e")
        content["name"] = nom
        content["tags"] = tags
        content["title"] = title
        content["dateModif"] = date[:10]
        tagim = content["tags"]
        meta = content
        del meta['tags']
        temp = tagim.replace('"', '')
        temp = temp.replace("[", "")
        temp = temp.replace("]", "")
        temp = temp.replace(" ", "")
        taglist = temp.split(",")
        dictag = {"tags": taglist}
        imtags = {}
        for tag in dictag['tags']:
            imtags[tag] = 'empty'
        blob_client = blob_service_client.get_blob_client(container=CONTAINER_NAME, blob=file.filename)
        blob_client.set_blob_tags(imtags)
        blob_client.set_blob_metadata(meta)
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
