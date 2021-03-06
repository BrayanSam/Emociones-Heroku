from flask import Flask, render_template, request, make_response
from . import service
#Librerias de analisis
from dotenv import load_dotenv
import os
from os import remove
from PIL import Image, ImageDraw
from matplotlib import pyplot as plt

# Import namespaces
from azure.cognitiveservices.vision.face import FaceClient
from azure.cognitiveservices.vision.face.models import FaceAttributeType
from msrest.authentication import CognitiveServicesCredentials

app=Flask(__name__)

Foto=False

def DetectFaces(image_file):
    print('Detectando rostros en', image_file)

    # Specify facial features to be retrieved
    features = [FaceAttributeType.age,
                FaceAttributeType.gender,
                FaceAttributeType.emotion,
                FaceAttributeType.glasses]

    # Get faces
    with open(image_file, mode="rb") as image_data:
        Tabla=[]
        detected_faces = face_client.face.detect_with_stream(image=image_data,
    return_face_attributes=features)

        if len(detected_faces) > 0:
            Tabla.append(str(len(detected_faces))+' rostros detectados')

            # Prepare image for drawing
            fig = plt.figure(figsize=(8, 6))
            plt.axis('off')
            image = Image.open(image_file)
            draw = ImageDraw.Draw(image)
            color = 'lightgreen'

            # Draw and annotate each face
            for face in detected_faces:

                # Get face properties
                Tabla.append('Rostro ID: {}'.format(face.face_id))
                detected_attributes = face.face_attributes.as_dict()
                age = 'age unknown' if 'age' not in detected_attributes.keys() else int(detected_attributes['age'])
                Tabla.append(' - Edad: {}'.format(age))
                
                if 'gender' in detected_attributes:
                    if format(detected_attributes['gender'])=="male":
                        Tabla.append('-Sexo: Masculino')
                    else:
                        Tabla.append('-Sexo: Femenino')

                if 'emotion' in detected_attributes:
                    Tabla.append('--- Emociones ---')
                    Espa??ol=['-Enfado','-Desprecio','-Asco','-Miedo', '-Felicidad','-Neutral','-Tristeza','-Sorpresa']
                    i=0
                    for emotion_name in detected_attributes['emotion']:
                        Tabla.append('   - {}: {}'.format(Espa??ol[i], detected_attributes['emotion'][emotion_name]))
                        i+=1
                        
                if 'glasses' in detected_attributes:
                    Tabla.append(' - Anteojos: {}'.format(detected_attributes['glasses']))

                # Draw and annotate face
                r = face.face_rectangle
                bounding_box = ((r.left, r.top), (r.left + r.width, r.top + r.height))
                draw = ImageDraw.Draw(image)
                draw.rectangle(bounding_box, outline=color, width=5)
                annotation = 'Face ID: {}'.format(face.face_id)
                plt.annotate(annotation,(r.left, r.top), backgroundcolor=color)

            # Save annotated image
            plt.imshow(image)
            outputfile = 'detected_faces.jpg'
            fig.savefig(os.path.join('./app/static/images', outputfile))

            print('Results saved in', outputfile)
            return Tabla
        else:
            image = Image.open(image_file)
            fig = plt.figure(figsize=(8, 6))
            plt.imshow(image)
            outputfile = 'detected_faces.jpg'
            fig.savefig(os.path.join('./app/static/images', outputfile))
            return Tabla

@app.route('/')
def index():
    #return "!HOLA mundo??"
    #return render_template('index.html')
    data={
        'titulo':'Reconocimiento de Emociones',
        'bienvenida':'!Saludos??'
    }
    return render_template('index.html',data=data)

@app.route('/Captura')
def Captura():
    return render_template('Captura.html')

@app.route('/guardar_img', methods=["POST"])
def captura_img():
    msg = service.save_img(request.form["img"])
    return make_response(msg)

@app.route('/borrar', methods=["POST"])
def borrar():
    try:
        remove(os.path.join('./app/static/images/Rostro.jpg'))
        msg="SUCEES"
    except FileNotFoundError:
        msg="SUCEES"
    return make_response(msg)

@app.route("/analisis")
def Analisis():
    global face_client
    try:
        # Get Configuration Settings
        load_dotenv()
        cog_endpoint = os.getenv('COG_SERVICE_ENDPOINT')
        cog_key = os.getenv('COG_SERVICE_KEY')

        # Authenticate Face client
        credentials = CognitiveServicesCredentials(cog_key)
        face_client = FaceClient(cog_endpoint, credentials)
        try:
            Tabla=DetectFaces(os.path.join('./app/static/images/Rostro.jpg'))
            Rostro=1
        except FileNotFoundError:
            Tabla=[]
            Rostro=0
    except Exception as ex:
        Tabla=[]
        print(ex)
    Datos= {
            'Emociones':Tabla,
            'Num_Emociones':len(Tabla),
            'Foto':Rostro
            }
    return render_template('analisis.html',Datos=Datos)


def pagina_no_encontrada(error):
    return render_template('404.html'), 404
    #return redirect(url_for('index'))

if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()

Tabla=[]
