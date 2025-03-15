import os

from flask import Flask, render_template, flash, request, redirect

app = Flask(__name__)
app.config["SECRET_KEY"] = "nadoeli_zadachi"


@app.route("/")
def task_name():
    return "Галерея с загрузкой"


@app.route("/gallery", methods=("GET", "POST"))
def gallery():
    gallery_path = "static/img"
    if request.method == "GET":
        slides = map(lambda filname: os.path.join(gallery_path, filname), os.listdir(gallery_path))
        return render_template("gallery.html", slide_paths=slides)
    elif request.method == "POST":
        if 'file' not in request.files:
            flash('Ошибка загрузки', "error")
            return redirect(request.url)
        f = request.files["file"]
        if not f.filename:
            flash("Файл не выбран", "error")
            return redirect(request.url)
        if f and ('.' in f.filename and f.filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}):
            last_slide = max(map(int, map(lambda fname: fname.rsplit(".")[0][5:], os.listdir(gallery_path))))
            new_name = f"slide{last_slide + 1}.{f.filename.rsplit('.')[1]}"
            f.save(os.path.join(gallery_path, new_name))
            flash("Картинка загружена", "info")
            return redirect(request.url)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
