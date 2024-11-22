from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Kết nối cơ sở dữ liệu
def get_db_connection():
    conn = psycopg2.connect(
        dbname='BT3',
        user='postgres',
        password='123456',
        host='localhost',
        port='5432'
    )
    return conn

# Trang danh sách sinh viên
@app.route("/", methods=["GET", "POST"])
def index():
    search_query = request.args.get("search")  
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    if search_query:
        # Nếu có từ khóa tìm kiếm, tìm sinh viên theo tên và sắp xếp theo ID
        cur.execute("SELECT * FROM danhsach WHERE HOTEN ILIKE %s ORDER BY id ASC", ('%' + search_query + '%',))
    else:
        # Nếu không có từ khóa tìm kiếm, hiển thị tất cả sinh viên và sắp xếp theo ID
        cur.execute("SELECT * FROM danhsach ORDER BY id ASC")
    
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("index.html", rows=rows)

# Thêm sinh viên
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        mssv = request.form["mssv"]
        hoten = request.form["hoten"]
        lop = request.form["lop"]
        diachi = request.form["diachi"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO danhsach (MSSV, HOTEN, LOP, DIACHI) VALUES (%s, %s, %s, %s)",
                    (mssv, hoten, lop, diachi))
        conn.commit()
        cur.close()
        conn.close()
        flash("Thêm sinh viên thành công!")
        return redirect(url_for("index"))

    return render_template("add.html")

# Cập nhật thông tin sinh viên
@app.route("/update/<int:id>", methods=["GET", "POST"])
def update_student(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        mssv = request.form["mssv"]
        hoten = request.form["hoten"]
        lop = request.form["lop"]
        diachi = request.form["diachi"]
        cur.execute("UPDATE danhsach SET MSSV=%s, HOTEN=%s, LOP=%s, DIACHI=%s WHERE id=%s",
                    (mssv, hoten, lop, diachi, id))
        conn.commit()
        cur.close()
        conn.close()
        flash("Cập nhật thành công!")
        return redirect(url_for("index"))
    
    cur.execute("SELECT * FROM danhsach WHERE id = %s", (id,))
    student = cur.fetchone()
    cur.close()
    conn.close()
    return render_template("update.html", student=student)

# Xóa sinh viên
@app.route("/delete/<int:id>", methods=["POST"])
def delete_student(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM danhsach WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    flash("Xóa sinh viên thành công!")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
