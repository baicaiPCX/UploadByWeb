from flask import Flask,render_template,request,send_from_directory,jsonify,redirect,url_for
import os

app=Flask(__name__)

app.config["UPLOAD_FOLDER"]=os.getcwd()
download_floder=app.config["UPLOAD_FOLDER"]+"/upload"

def allow_file(filename):
    allow_list=["png","PNG","jpg","doc","docx","txt","rar","zip","pdf","PDF","xls","exe","md","beb","json"]
    a=filename.split(".")[1]
    if a in allow_list:
        return True
    else:
        return False

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/getlist")
def getlist():
    print("getlist......")
    file_url_list=[]
    file_floder=app.config["UPLOAD_FOLDER"]+"/upload"
    file_list=os.listdir(file_floder)
    for filename in file_list:
        file_url=url_for("download",filename=filename)
        file_url_list.append(file_url)
    return jsonify(file_list)

@app.route("/download/<filename>")
def download(filename):
    print("download....")
    return send_from_directory(download_floder,filename,as_attachment=True)

@app.route("/upload",methods=["POST","GET"])
def upload():
    print("upload...")
    file=request.files['file']
    if not file:
        return render_template("index.html",status="null")
    if allow_file(file.filename):
        file.save(os.path.join(app.config["UPLOAD_FOLDER"]+"/upload/",file.filename))
        return render_template("index.html",status="OK")
    else:
        return "NO"

if __name__ == "__main__":
    # app.run(debug=True,host="0.0.0.0")
    app.run(host="0.0.0.0")