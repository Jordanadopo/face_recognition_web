# This is a _very simple_ example of a web service that recognizes faces in uploaded images.
# Upload an image file and it will check if the image contains a picture of me or Barack Obama.
# The result is returned as also web page. For example:
#
# $ curl -XPOST -F "file=@obama2.jpg" http://127.0.0.1:5001
#
# Returns: a web page where your picture is juged on face detection, my identification or Obama's identification
#
#By Jordan Adopo
#
# This example is based on the Flask file upload example: http://flask.pocoo.org/docs/0.12/patterns/fileuploads/

# NOTE: This example requires flask to be installed! You can install it with pip:
# $ pip3 install flask

import face_recognition
from flask import Flask, jsonify, request, redirect

# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            return detect_faces_in_image(file)

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
    <head>
    <title>Obama ou Adopo?</title>
    <script src="//code.jquery.com/jquery-1.11.0.min.js"></script>
    <script src="//netdna.bootstrapcdn.com/bootstrap/3.1.1/js/bootstrap.min.js"></script>
    <link href="//netdna.bootstrapcdn.com/bootstrap/3.1.1/css/bootstrap.min.css" rel="stylesheet">
    <style type="text/css">
    body {
         font-family: sans-serif;
          background-color: #eeeeee;
        }

        .file-upload {
          background-color: #ffffff;
          width: 600px;
          margin: 0 auto;
          padding: 20px;
        }

        .file-upload-btn {
          width: 100%;
          margin: 0;
          color: #fff;
          background: #1FB264;
          border: none;
          padding: 10px;
          border-radius: 4px;
          border-bottom: 4px solid #15824B;
          transition: all .2s ease;
          outline: none;
          text-transform: uppercase;
          font-weight: 700;
        }

        .file-upload-btn:hover {
          background: #1AA059;
          color: #ffffff;
          transition: all .2s ease;
          cursor: pointer;
        }

        .file-upload-btn:active {
          border: 0;
          transition: all .2s ease;
        }

        .file-upload-content {
          display: none;
          text-align: center;
        }

        .file-upload-input {
          position: absolute;
          margin: 0;
          padding: 0;
          width: 100%;
          height: 100%;
          outline: none;
          opacity: 0;
          cursor: pointer;
        }

        .image-upload-wrap {
          margin-top: 20px;
          border: 4px dashed #1FB264;
          position: relative;
        }

        .image-dropping,
        .image-upload-wrap:hover {
          background-color: #1FB264;
          border: 4px dashed #ffffff;
        }

        .image-title-wrap {
          padding: 0 15px 15px 15px;
          color: #222;
        }

        .drag-text {
          text-align: center;
        }

        .drag-text h3 {
          font-weight: 100;
          text-transform: uppercase;
          color: #15824B;
          padding: 60px 0;
        }

        .file-upload-image {
          max-height: 200px;
          max-width: 200px;
          margin: auto;
          padding: 20px;
        }

        .remove-image {
          width: 200px;
          margin: 0;
          color: #fff;
          background: #cd4535;
          border: none;
          padding: 10px;
          border-radius: 4px;
          border-bottom: 4px solid #b02818;
          transition: all .2s ease;
          outline: none;
          text-transform: uppercase;
          font-weight: 700;
        }

        .remove-image:hover {
          background: #c13b2a;
          color: #ffffff;
          transition: all .2s ease;
          cursor: pointer;
        }

        .remove-image:active {
          border: 0;
          transition: all .2s ease;
        }
    }
    </style>
    </head>
    <body>
    <div class="container" style="margin-top: 20px;">
        <div class="col-md-8 col-md-offset-2">
            <form method="POST" enctype="multipart/form-data">
                <!-- COMPONENT START -->
               <div class="col-md-12 col-md-12 col-12">
                    <div class="file-upload">
                      <button class="file-upload-btn" type="button" onclick="$('.file-upload-input').trigger( 'click' )">Veuillez ajouter un image</button>

                      <div class="image-upload-wrap">
                        <input class="file-upload-input" type='file' name='file' onchange="readURL(this);" accept="image/*" />
                        <div class="drag-text">
                          <h3>Glissez et déposez ou cliquez pour ajouter une image</h3>
                        </div>
                      </div>
                      <div class="file-upload-content">
                        <img class="file-upload-image" src="#" alt="your image" />
                        <div class="image-title-wrap">
                          <button type="button" onclick="removeUpload()" class="remove-image">Supprimer l'image? <span class="image-title">Image téléchargée</span></button>
                        </div>
                      </div>
                    </div>
                </div>
                <!-- COMPONENT END -->
                <div class="form-group">
                        <button type="submit" class="btn btn-primary pull-right">Télécharger</button>
                </div>
            </div>
           </form>
        
             
      </div>
   </div>
    <!--<form method="POST" enctype="multipart/form-data">
      <input class="btn btn-primary" type="file" name="file">
      <input class="btn btn-success" type="submit" value="Upload">
    </form>-->
    <script type="text/javascript">
        function readURL(input) {
                  if (input.files && input.files[0]) {

                    var reader = new FileReader();

                    reader.onload = function(e) {
                      $('.image-upload-wrap').hide();

                      $('.file-upload-image').attr('src', e.target.result);
                      $('.file-upload-content').show();

                      $('.image-title').html(input.files[0].name);
                    };

                    reader.readAsDataURL(input.files[0]);

                  } else {
                    removeUpload();
                  }
                }

                function removeUpload() {
                  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
                  $('.file-upload-content').hide();
                  $('.image-upload-wrap').show();
                }
                $('.image-upload-wrap').bind('dragover', function () {
                        $('.image-upload-wrap').addClass('image-dropping');
                    });
                    $('.image-upload-wrap').bind('dragleave', function () {
                        $('.image-upload-wrap').removeClass('image-dropping');
                });
    </script>
    </body>
    '''


def detect_faces_in_image(file_stream):
    # Pre-calculated face encoding of Obama generated with face_recognition.face_encodings(img)
    known_face_encoding = [-0.09634063,  0.12095481, -0.00436332, -0.07643753,  0.0080383,
                            0.01902981, -0.07184699, -0.09383309,  0.18518871, -0.09588896,
                            0.23951106,  0.0986533 , -0.22114635, -0.1363683 ,  0.04405268,
                            0.11574756, -0.19899382, -0.09597053, -0.11969153, -0.12277931,
                            0.03416885, -0.00267565,  0.09203379,  0.04713435, -0.12731361,
                           -0.35371891, -0.0503444 , -0.17841317, -0.00310897, -0.09844551,
                           -0.06910533, -0.00503746, -0.18466514, -0.09851682,  0.02903969,
                           -0.02174894,  0.02261871,  0.0032102 ,  0.20312519,  0.02999607,
                           -0.11646006,  0.09432904,  0.02774341,  0.22102901,  0.26725179,
                            0.06896867, -0.00490024, -0.09441824,  0.11115381, -0.22592428,
                            0.06230862,  0.16559327,  0.06232892,  0.03458837,  0.09459756,
                           -0.18777156,  0.00654241,  0.08582542, -0.13578284,  0.0150229 ,
                            0.00670836, -0.08195844, -0.04346499,  0.03347827,  0.20310158,
                            0.09987706, -0.12370517, -0.06683611,  0.12704916, -0.02160804,
                            0.00984683,  0.00766284, -0.18980607, -0.19641446, -0.22800779,
                            0.09010898,  0.39178532,  0.18818057, -0.20875394,  0.03097027,
                           -0.21300618,  0.02532415,  0.07938635,  0.01000703, -0.07719778,
                           -0.12651891, -0.04318593,  0.06219772,  0.09163868,  0.05039065,
                           -0.04922386,  0.21839413, -0.02394437,  0.06173781,  0.0292527 ,
                            0.06160797, -0.15553983, -0.02440624, -0.17509389, -0.0630486 ,
                            0.01428208, -0.03637431,  0.03971229,  0.13983178, -0.23006812,
                            0.04999552,  0.0108454 , -0.03970895,  0.02501768,  0.08157793,
                           -0.03224047, -0.04502571,  0.0556995 , -0.24374914,  0.25514284,
                            0.24795187,  0.04060191,  0.17597422,  0.07966681,  0.01920104,
                           -0.01194376, -0.02300822, -0.17204897, -0.0596558 ,  0.05307484,
                            0.07417042,  0.07126575,  0.00209804]
    
    a_encoding = [-0.15979747,  0.11725173,  0.0818087 , -0.02158123, -0.01732353,
                  -0.0731382,  0.05176253, -0.13538845,  0.12685721, -0.10944723,
                   0.28563839, -0.03036234, -0.14474882, -0.16070049,  0.04730692,
                  0.12523291, -0.12845218, -0.17832589, -0.14313689, -0.13918057,
                  -0.03259875,  0.02421018, -0.06361292,  0.06311235, -0.04510239,
                  -0.27867585, -0.09638466, -0.12430044,  0.11761242, -0.10083037,
                  0.03685942,  0.13631061, -0.19299495, -0.06254671, -0.00595804,
                  0.04665301,  0.0683083 ,  0.02792542,  0.15861699, -0.05299835,
                  -0.13917799, -0.04530797,  0.04267046,  0.29034117,  0.16585641,
                  -0.0136914 , -0.03366099,  0.01163224,  0.092876  , -0.14058056,
                  0.04022713,  0.11352476,  0.17514004,  0.0900005 , -0.02912742,
                  -0.14503297, -0.01939636,  0.03622018, -0.19273476,  0.05921833,
                  0.05310556, -0.23893405, -0.11866745, -0.03162903,  0.20987603,
                  0.07785077, -0.08230844, -0.15094753,  0.20967671, -0.14542995,
                  -0.00971203,  0.07929692, -0.1592225 , -0.07446391, -0.28543797,
                  0.11418304,  0.37574568,  0.11917469, -0.16391426,  0.0424001,
                  -0.1198158 ,  0.00877618, -0.02162134,  0.06880209, -0.10572942,
                  0.01880184, -0.07784066,  0.06743132,  0.14184281,  0.03138403,
                  -0.05919201,  0.19156733, -0.04985109,  0.02160328,  0.01526462,
                  -0.03684   ,  0.01038721, -0.09967578, -0.09673397, -0.03741285,
                  0.00590326, -0.06931225, -0.00388304,  0.10051759, -0.12867557,
                  0.1505523 ,  0.02545144,  0.0688523 , -0.02471977,  0.07219093,
                  -0.02804666, -0.08638357,  0.14506565, -0.15486895,  0.18954615,
                  0.14935641,  0.05621736,  0.13684021,  0.04446177,  0.11077023,
                  -0.03843602, -0.07129879, -0.11508757, -0.04579731,  0.1227126,
                  -0.02488962,  0.0749531 ,  0.04734895]
    

    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    source=file_stream.filename
    face_found = False
    is_obama = False
    is_adopo = False


    if len(unknown_face_encodings) > 0:
        face_found = True
        # See if the first face in the uploaded image matches the known face of Obama
        match_results1 = face_recognition.compare_faces([known_face_encoding], unknown_face_encodings[0])
        if match_results1[0]:
            is_obama = True
        
        match_results = face_recognition.compare_faces([a_encoding], unknown_face_encodings[0])
        if match_results[0]:
            is_adopo = True
            
    trouve="Pas de visage reconnu dans votre image: ["+source+"];"
    if face_found:
        trouve="On a trouvé un visage dans votre image: ["+source+"];"

    obama="Barack Obama n'a pas été reconnu dans votre image: ["+source+"];" 
    if is_obama:
        obama="On a reconnu Barack Obama dans votre image: ["+source+"];"

    adopo="Jordan Adopo pas reconnu n'a pas été reconnu dans votre image: ["+source+"];"
    if is_adopo:
        adopo="On a reconnu Jordan Adopo dans votre image: ["+source+"];"
    
    # Return the result as json
    result = {
        "face_found_in_image": face_found,
        "is_picture_of_obama": is_obama,
        "is_picture_of_adopo": is_adopo
    }
    im1="/jumbotron_bg.jpg"
    im2="/obama.jpg"
    im3="/moi.png"
    
    return '''
    <!doctype html>
    <head>
    <title>Résultats: Obama ou Adopo!</title>
    <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.bundle.min.js"></script>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css" rel="stylesheet">
    </head>
    <body>
    <div class="container" style="margin-top: 20px;">

  <h1 class="font-weight-light text-center text-lg-left mt-4 mb-0">Résultats de votre image: Obama ou Adopo?</h1>

  <hr class="mt-2 mb-5">

  <div class="row text-center text-lg-left">

    <div class="col-lg-2 col-md-2 col-2">
      <!--<a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail detect"  src="#" alt="Detection de visage">
          </a>-->
    </div>
    
    <div class="col-lg-6 col-md-6 col-6">
      <h3 class="font-weight-light text-center text-lg-left mt-4 mb-0">'''+trouve+'''</h3>
    </div>
    <div class="col-lg-4 col-md-4 col-4">
      <!--<a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail source" src"#" alt="votre image">
          </a>-->
    </div>
    </div>
    <br/>
    <div class="row text-center text-lg-left">
    <div class="col-lg-2 col-md-2 col-2">
      <!--<a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail obama" src"#" alt="Obama">
          </a>-->
    </div>
    <div class="col-lg-6 col-md-6 col-6">
      <h3 class="font-weight-light text-center text-lg-left mt-4 mb-0">'''+obama+'''</h3> 
    </div>
    <div class="col-lg-4 col-md-4 col-4">
      <!--<a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail source" src"#" alt="votre image">
          </a>-->
    </div>
    </div>
    <br/>
    <div class="row text-center text-lg-left">
    <div class="col-lg-2 col-md-2 col-2">
      <!--<a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail adopo" src"#" alt="Jordan Adopo">
          </a>-->
    </div>
    <div class="col-lg-6 col-md-6 col-6">
      <h3 class="font-weight-light text-center text-lg-left mt-4 mb-0">'''+adopo+'''</h3> 
    </div>
    <div class="col-lg-4 col-md-4 col-4">
     <!-- <a href="#" class="d-block mb-4 h-100">
            <img class="img-fluid img-thumbnail source" src"#" alt="votre image">
          </a>-->
    </div>
    </div>
    <br/>
  </div>

</div>
<!-- /.container -->
<script type="text/javascript">
    $('.file-upload-image').attr('src', e.target.result);
</script>
    </body>
    '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
