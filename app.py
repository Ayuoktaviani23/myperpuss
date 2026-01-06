import streamlit as st
import difflib
import re
import random
import time
from datetime import datetime
from difflib import SequenceMatcher

st.set_page_config(
    page_title="PerpusCode USK - Hafalan Kode Custom",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# INITIALIZE SESSION STATE
# =========================
if 'practice_scores' not in st.session_state:
    st.session_state.practice_scores = {}
if 'quiz_scores' not in st.session_state:
    st.session_state.quiz_scores = []
if 'last_viewed' not in st.session_state:
    st.session_state.last_viewed = []
if 'hafalan_mode' not in st.session_state:
    st.session_state.hafalan_mode = False
if 'custom_code_to_memorize' not in st.session_state:
    st.session_state.custom_code_to_memorize = ""
if 'original_full_code' not in st.session_state:
    st.session_state.original_full_code = ""
if 'current_mode' not in st.session_state:
    st.session_state.current_mode = "🏠 Dashboard"
if 'memorized_parts' not in st.session_state:
    st.session_state.memorized_parts = {}
if 'user_custom_codes' not in st.session_state:
    st.session_state.user_custom_codes = {}
if 'hafalan_timer' not in st.session_state:
    st.session_state.hafalan_timer = 0

# =========================
# DATASET MATERI LENGKAP (DITAMBAHKAN)
# =========================
materi = {
    # ---------- SESSION ----------
    "Login Page (HTML)": {
        "deskripsi": "Halaman login dengan form HTML dan styling CSS",
        "tipe": "html",
        "kode": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<style>
*{
    margin: 0px;
    padding: 0px;
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
}
body{
    background-color: #eee;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}
.form-box{
    background-color: white;
    width: 300px;
    padding: 20px;
    border: 2px solid #ccc;
    border-radius: 6px;
}
.form-box h2{
    text-align: center;
    margin-bottom: 15px;
}
label {
    font-size: 14px;
}
input[type="text"],
input[type="password"]{
    width: 100%;
    padding: 7px;
    margin: 5px 0 12px;
    border: 1px solid #9999;
    border-radius: 4px;
}
input:focus{
    outline: none;
    border-color: #4CAF50;
}
input[type="submit"]{
    width: 100%;
    padding: 8px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
input[type="submit"]:hover{
    background-color: #43a047;
}
</style>
<body>
<div class="form-box">
    <h2>Login</h2>
    <form action="proses_login.php" method="post">
        <label>Username</label>
        <input type="text" name="username" required>
        <label>Password</label>
        <input type="password" name="password" required>
        <input type="submit" value="Login">
    </form>
</div>
</body>
</html>""",
        "penjelasan": {
            "title": "Struktur Halaman Login",
            "points": [
                "**DOCTYPE html** → Deklarasi tipe dokumen HTML5",
                "**<meta name='viewport'>** → Untuk responsive design",
                "**CSS Box Model** → Penggunaan *{margin:0; padding:0; box-sizing:border-box}",
                "**Flexbox** → display:flex untuk penempatan tengah",
                "**Form Styling** → Styling input text dan submit button",
                "**:hover** → Efek hover pada tombol login"
            ]
        },
        "critical_parts": [
            "session_start()",
            "method=\"post\"",
            "action=\"proses_login.php\"",
            "required",
            "name=\"username\"",
            "name=\"password\""
        ]
    },

    "Index Page dengan Filter & Favorit (Session)": {
        "deskripsi": "Halaman utama dengan filter kategori, status, favorit, dan print button",
        "tipe": "php",
        "kode": """<?php
session_start();
require "../koneksi.php";

if (!isset($_SESSION['id_user'])) {
    header("Location: login.php");
    exit;
}

$id_user = $_SESSION['id_user'];

/* ===== FAVORIT (SESSION) ===== */
if (isset($_GET['fav'])) {
    $id = $_GET['fav'];
    $_SESSION['favorite'][$id] = $_SESSION['favorite'][$id] ?? 0;
    $_SESSION['favorite'][$id] = $_SESSION['favorite'][$id] ? 0 : 1;
    header("Location: index.php");
    exit;
}

/* ===== FILTER ===== */
$where = "WHERE t.id_user = '$id_user'";

if (!empty($_GET['category'])) {
    $where .= " AND t.id_category = '{$_GET['category']}'";
}

if (!empty($_GET['status'])) {
    $where .= " AND t.status = '{$_GET['status']}'";
}

$sql = "SELECT t.*, c.category 
        FROM todo t 
        LEFT JOIN category c ON t.id_category = c.id_category
        $where
        ORDER BY t.id_todo DESC";

$query    = mysqli_query($koneksi, $sql);
$kategori = mysqli_query($koneksi, "SELECT * FROM category");

$favorit = $_GET['favorite'] ?? 0;
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>My TodoList</title>

<style>
/* CSS akan dipisah di file terpisah */
</style>

</head>
<body>

<?php include "navbar.php"; ?>

<div class="content">
    <form method="get">
        <label>Filter Kategori</label>
        <select name="category" onchange="this.form.submit()">
            <option value="">Semua</option>
            <?php while($k=mysqli_fetch_assoc($kategori)): ?>
                <option value="<?= $k['id_category']; ?>"
                    <?= (@$_GET['category']==$k['id_category'])?'selected':'' ?>>
                    <?= $k['category']; ?>
                </option>
            <?php endwhile; ?>
        </select>
    </form>

    <form method="get">
        <label>Filter Status</label>
        <select name="status" onchange="this.form.submit()">
            <option value="">Semua</option>
            <option value="Pending" <?= (@$_GET['status']=='Pending')?'selected':'' ?>>Pending</option>
            <option value="Done" <?= (@$_GET['status']=='Done')?'selected':'' ?>>Done</option>
        </select>
    </form>

    <form method="get">
        <label>Filter Favorite</label>
        <select name="favorite" onchange="this.form.submit()">
            <option value="">Semua</option>
            <option value="1" <?= (@$_GET['favorite']=='1')?'selected':'' ?>>Favorite</option>
        </select>
    </form>
</div>

<center>
    <button onclick="window.print()" style="background:#5c5e5c;">Print</button>
    <br>
    <a href="tambah.php">
        <button style="background:#0c8f3e;margin-top:6px;">+ Tambah</button>
    </a>
</center>
<br>

<div class="todo-wrapper">
<?php while($todo=mysqli_fetch_assoc($query)): ?>
<?php
    $iniFavorit = $_SESSION['favorite'][$todo['id_todo']] ?? 0;
    if ($favorit && $iniFavorit != 1) continue;
?>
<div class="todo-card <?= $todo['status']=='Done'?'done':'' ?>">
    <h4><?= $todo['title']; ?></h4>
    <small><?= $todo['description']; ?></small>
    <p><b>Kategori:</b> <?= $todo['category']; ?></p>
    <p><b>Status:</b> <?= $todo['status']; ?></p>

    <div class="todo-action">
        <a href="edit.php?id_todo=<?= $todo['id_todo']; ?>" class="edit">Edit</a>
        <a href="hapus.php?id_todo=<?= $todo['id_todo']; ?>" class="hapus">Hapus</a>
        <a href="?fav=<?= $todo['id_todo']; ?>" style="background:#e91e63;">
            <?= $iniFavorit ? '❤️' : 'Favorit' ?>
        </a>
    </div>
</div>
<?php endwhile; ?>
</div>

</body>
</html>""",
        "penjelasan": {
            "title": "Index Page dengan Filter Multiple",
            "points": [
                "**session_start()** → Wajib untuk akses session",
                "**require** → Include koneksi database",
                "**Session Protection** → Cek apakah user sudah login",
                "**Favorit System** → Menggunakan session untuk simpan favorit",
                "**Dynamic WHERE Clause** → Filter berdasarkan kategori, status, favorit",
                "**LEFT JOIN** → Gabungkan tabel todo dan category",
                "**Auto Submit Filter** → onchange='this.form.submit()'",
                "**Print Function** → window.print() untuk cetak halaman",
                "**Ternary Operator** → <?= kondisi?value1:value2 ?>"
            ]
        },
        "critical_parts": [
            "session_start()",
            "require \"../koneksi.php\"",
            "if (!isset($_SESSION['id_user']))",
            "header(\"Location: login.php\")",
            "exit",
            "$_SESSION['favorite'][$id] = $_SESSION['favorite'][$id] ?? 0",
            "WHERE t.id_user = '$id_user'",
            "LEFT JOIN category c ON t.id_category = c.id_category",
            "onchange=\"this.form.submit()\"",
            "<?= (@$_GET['category']==$k['id_category'])?'selected':'' ?>",
            "<?php while($todo=mysqli_fetch_assoc($query)): ?>",
            "<?php endwhile; ?>"
        ]
    },

    "Form Daftar Pengguna Baru (HTML)": {
        "deskripsi": "Halaman pendaftaran user dengan validasi HTML5",
        "tipe": "html",
        "kode": """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daftar Pengguna Baru</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <?php include "navbar2.php"; ?>
    <div class="form-box">
        <h3>Daftar Pengguna Baru</h3>
        <form action="proses_daftar.php" method="post">
            <p style="padding-right: 197px; font-size: 15px;">Nama Lengkap</p>
            <input type="text" name="name" id="" required>

            <p style="padding-right: 260px; font-size: 15px;">Email</p>
            <input type="email" name="email" id="" required>
            
            <p style="padding-right: 230px; font-size: 15px;">Username</p>
            <input type="text" name="username" id="" required>
            
            <p style="padding-right: 230px; font-size: 15px;">Password</p>
            <input type="password" name="password" id="" required>
            
            <p style="padding-right: 208px; font-size: 15px;">Tanggal Lahir</p>
            <input type="date" name="birth_date" id="" required>

            <input type="submit" value="Daftar" style="background: #3b82f6; color: #fff;">

            <p>Sudah punya akun? <a href="login.php" style="text-decoration: none;">Login Disini</a></p>
        </form>
    </div>
</body>
</html>""",
        "penjelasan": {
            "title": "Form Registration HTML5",
            "points": [
                "**HTML5 Input Types** → type='email', type='date' untuk validasi otomatis",
                "**Required Attribute** → Validasi client-side wajib diisi",
                "**Method POST** → Data dikirim via POST (lebih aman)",
                "**Inline CSS** → Styling langsung di elemen",
                "**Link to Login** → Navigasi ke halaman login",
                "**Include Navbar** → <?php include 'navbar2.php'; ?>",
                "**Semantic HTML** → Penggunaan tag yang sesuai"
            ]
        },
        "critical_parts": [
            "<!DOCTYPE html>",
            "method=\"post\"",
            "action=\"proses_daftar.php\"",
            "type=\"text\" name=\"name\" required",
            "type=\"email\" name=\"email\" required",
            "type=\"text\" name=\"username\" required",
            "type=\"password\" name=\"password\" required",
            "type=\"date\" name=\"birth_date\" required",
            "type=\"submit\" value=\"Daftar\"",
            "<?php include \"navbar2.php\"; ?>"
        ]
    },

    "Proses Pendaftaran (INSERT)": {
        "deskripsi": "Proses menyimpan data pendaftaran ke database",
        "tipe": "php",
        "kode": """<?php
require "koneksi.php";

$nama = $_POST['name'];
$date = $_POST['birth_date'];
$email = $_POST['email'];
$username = $_POST['username'];
$password = $_POST['password'];

$sql = "INSERT INTO user (name, birth_date, email, username, password)
        VALUES
        ('$nama','$date','$email','$username',md5('$password'))";
$query = mysqli_query($koneksi, $sql);

if($query){
    header("location:login.php?daftar=sukses");
    exit;
} else {
    header("location:daftar.php?daftar=gagal");
    exit;
}
?>""",
        "penjelasan": {
            "title": "INSERT Data User Baru",
            "points": [
                "**$_POST** → Mengambil data dari form pendaftaran",
                "**md5()** → Enkripsi password sebelum disimpan",
                "**INSERT INTO** → Syntax untuk tambah data ke tabel user",
                "**Multiple Columns** → Menyimpan banyak field sekaligus",
                "**Conditional Redirect** → Redirect berdasarkan hasil query",
                "**Success/Failure** → Parameter URL untuk feedback (daftar=sukses/gagal)",
                "**exit** → Hentikan eksekusi setelah redirect"
            ]
        },
        "critical_parts": [
            "require \"koneksi.php\"",
            "$_POST['name']",
            "$_POST['birth_date']",
            "$_POST['email']",
            "$_POST['username']",
            "$_POST['password']",
            "INSERT INTO user (name, birth_date, email, username, password)",
            "VALUES ('$nama','$date','$email','$username',md5('$password'))",
            "mysqli_query($koneksi, $sql)",
            "if($query){",
            "header(\"location:login.php?daftar=sukses\")",
            "header(\"location:daftar.php?daftar=gagal\")",
            "exit"
        ]
    },

    "Halaman Profil User": {
        "deskripsi": "Menampilkan data profil user yang sedang login",
        "tipe": "php",
        "kode": """<?php
session_start();
require "koneksi.php";

$id_user = $_SESSION['id_user'];
$user = mysqli_query($koneksi, "SELECT * FROM user WHERE id_user = '$id_user'");
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profil Saya</title>
    <style>
        .profil{
            width: 320px; 
            margin: 40px auto; 
            background: #fff; 
            padding: 20px; 
            border-radius: 8px; 
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        .profil h3{
            margin-bottom: 12px;
            margin-top: 7px;
        }
        .profil p {
            margin-bottom: 4px;
        }
        .profil button{
            margin-bottom: 8px;
            background: #555;
        }
    </style>
</head>
<body>
    <?php include "navbar.php"; ?>
    <div class="profil">
        <h3>Profil Saya</h3>
        <?php while($u = mysqli_fetch_assoc($user)) { ?>
            <p><strong>Nama :</strong> <?= $u['name'] ?></p>
            <p><strong>Tanggal Lahir :</strong> <?= $u['birth_date'] ?></p>
            <p><strong>Email :</strong> <?= $u['email'] ?></p>
            <p><strong>Username :</strong> <?= $u['username'] ?></p>
            <p><strong>Password :</strong> ****</p>
            <center><button><a href="index.php" style="text-decoration: none; color: #fff;">Kembali</a></button></center>
        <?php } ?>
    </div>
</body>
</html>""",
        "penjelasan": {
            "title": "Menampilkan Data Profil",
            "points": [
                "**Session Protection** → Hanya user yang login bisa akses profil",
                "**SELECT WHERE** → Ambil data spesifik berdasarkan id_user",
                "**Inline Styling** → CSS langsung dalam style tag",
                "**Box Shadow** → Efek bayangan untuk card profil",
                "**Secure Display** → Password ditampilkan sebagai '****'",
                "**Loop while** → Menampilkan data user (meski hanya 1)",
                "**Back Button** → Navigasi kembali ke index"
            ]
        },
        "critical_parts": [
            "session_start()",
            "require \"koneksi.php\"",
            "$_SESSION['id_user']",
            "SELECT * FROM user WHERE id_user = '$id_user'",
            "mysqli_query($koneksi, $query)",
            "<?php include \"navbar.php\"; ?>",
            "<?php while($u = mysqli_fetch_assoc($user)) { ?>",
            "<?= $u['name'] ?>",
            "<?php } ?>"
        ]
    },

    "CSS Full Project (style.css)": {
        "deskripsi": "File CSS lengkap untuk project Todo List",
        "tipe": "css",
        "kode": """/* =========================
   RESET & GLOBAL
========================= */
*{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: Arial, Helvetica, sans-serif;
}

body{
    background:#f4f6f8;
}

/* =========================
   NAVBAR
========================= */
.navbar{
    background: linear-gradient(90deg, #111 0%, #333 100%);
    color: white;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.navbar a{
    color: white;
    text-decoration: none;
    margin-left: 20px;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background 0.3s;
}

.navbar a:hover{
    background: rgba(255,255,255,0.1);
}

.navbar a[href*="logout"]{
    background: #dc2626;
}

.navbar a[href*="logout"]:hover{
    background: #b91c1c;
}

/* =========================
   FILTER & BUTTON
========================= */
.content{
    display:flex;
    flex-wrap:wrap;
    justify-content:center;
    gap:15px;
    margin:20px 0;
}

label{
    display:block;
    font-weight:bold;
    margin-bottom:5px;
    text-align:center;
}

select{
    padding:6px 10px;
    border-radius:5px;
}

button{
    padding:7px 12px;
    border:none;
    border-radius:5px;
    color:#fff;
    cursor:pointer;
}

/* =========================
   TODO LIST GRID
========================= */
.todo-wrapper{
    width:90%;
    margin:auto;
    display:grid;
    grid-template-columns:repeat(auto-fill,minmax(280px,1fr));
    gap:15px;
}

.todo-card{
    background:#fff;
    padding:15px;
    border-radius:8px;
    box-shadow:0 2px 6px rgba(0,0,0,.1);
}

.todo-card.done{
    background:#333;
    color:#fff;
    text-decoration:line-through;
}

.todo-card h4{
    margin-bottom:5px;
}

.todo-action{
    margin-top:10px;
}

.todo-action a{
    display:inline-block;
    padding:6px 10px;
    border-radius:5px;
    text-decoration:none;
    color:#fff;
    font-size:13px;
    margin-right:5px;
}

.edit{background:#007bff;}
.hapus{background:#dc3545;}

/* =========================
   FORM LOGIN / REGISTER
========================= */
.form-wrapper{
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}

.form{
    background:#fff;
    width:300px;
    padding:20px;
    border:1px solid #ccc;
    border-radius:6px;
}

.form h2{
    text-align:center;
    margin-bottom:15px;
}

.form label{
    font-size:14px;
    text-align:left;
}

.form input[type="text"],
.form input[type="password"]{
    width:100%;
    padding:7px;
    margin:5px 0 12px;
    border:1px solid #999;
    border-radius:4px;
}

.login-submit input[type="submit"]{
    width:100%;
    padding:8px;
    background:#63d4f4;
    color:#fff;
    border:none;
    border-radius:4px;
    cursor:pointer;
}

.submit-regis input[type="submit"]{
    width:100%;
    padding:8px;
    background:#138d07;
    color:#fff;
    border:none;
    border-radius:4px;
    cursor:pointer;
}

.form p{
    font-size:13px;
    text-align:center;
    margin-top:10px;
}

/* =========================
   PROFILE PAGE
========================= */
.profil{
    width: 320px; 
    margin: 40px auto; 
    background: #fff; 
    padding: 20px; 
    border-radius: 8px; 
    box-shadow: 0 4px 8px rgba(0,0,0,0.05);
}

.profil h3{
    margin-bottom: 12px;
    margin-top: 7px;
}

.profil p {
    margin-bottom: 4px;
}

.profil button{
    margin-bottom: 8px;
    background: #555;
}

/* =========================
   RESPONSIVE DESIGN
========================= */
@media (max-width: 768px) {
    .navbar{
        padding: 10px 15px;
        flex-direction: column;
        gap: 10px;
    }
    
    .todo-wrapper{
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    }
    
    .content{
        flex-direction: column;
        align-items: center;
    }
    
    .form{
        width: 90%;
        margin: 20px auto;
    }
}""",
        "penjelasan": {
            "title": "CSS Best Practices Full Project",
            "points": [
                "**CSS Reset** → *{margin:0; padding:0; box-sizing:border-box}",
                "**Flexbox & Grid** → Layout modern untuk navbar dan todo cards",
                "**Sticky Navbar** → position:sticky untuk navbar tetap saat scroll",
                "**CSS Grid** → grid-template-columns untuk responsive layout",
                "**Media Queries** → Responsive design untuk mobile",
                "**Pseudo-classes** → :hover untuk efek interaktif",
                "**Attribute Selectors** → a[href*='logout'] untuk styling spesifik",
                "**Box Shadow** → Efek kedalaman untuk cards",
                "**CSS Variables** → Bisa ditambahkan untuk theming"
            ]
        },
        "critical_parts": [
            "*{margin:0; padding:0; box-sizing:border-box}",
            "display: flex",
            "justify-content: space-between",
            "position: sticky",
            "top: 0",
            "display:grid",
            "grid-template-columns:repeat(auto-fill,minmax(280px,1fr))",
            "gap:15px",
            "box-shadow:0 2px 6px rgba(0,0,0,.1)",
            "transition: background 0.3s",
            "@media (max-width: 768px)"
        ]
    },

    # ---------- CRUD OPS LAINNYA (dari versi sebelumnya) ----------
    "Proses Login (Session)": {
        "deskripsi": "Proses validasi login dan membuat session",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$username = $_POST['username'];
$password = $_POST['password'];

$sql = "SELECT * FROM user 
        WHERE username='$username' 
        AND password=md5('$password')";
$query = mysqli_query($koneksi,$sql);

if(mysqli_num_rows($query)==1){
    $user=mysqli_fetch_assoc($query);
    
    // BUAT SESSION
    $_SESSION['id_user']=$user['id_user'];
    $_SESSION['username']=$user['username'];
    
    header("location:index.php?login=sukses");
    exit;
}else{
    header("location:login.php?login=gagal");
    exit;
}
?>""",
        "penjelasan": {
            "title": "Mekanisme Session Login",
            "points": [
                "**session_start()** → WAJIB dipanggil pertama kali untuk mulai session",
                "**$_POST** → Mengambil data dari form login",
                "**md5()** → Fungsi hash untuk enkripsi password",
                "**mysqli_num_rows()** → Mengecek jumlah data yang ditemukan",
                "**$_SESSION[]** → Menyimpan data user ke dalam session",
                "**header()** → Redirect ke halaman lain",
                "**exit** → Menghentikan eksekusi script setelah redirect"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_POST['username']",
            "$_POST['password']",
            "md5('$password')",
            "mysqli_num_rows($query)==1",
            "mysqli_fetch_assoc($query)",
            "$_SESSION['id_user']",
            "$_SESSION['username']",
            "header(\"location:index.php\")",
            "exit"
        ]
    },

    "Logout (Session Destroy)": {
        "deskripsi": "Menghapus session dan logout user",
        "tipe": "php",
        "kode": """<?php
session_start();
session_destroy();
header("location:login.php");
?>""",
        "penjelasan": {
            "title": "Cara Logout yang Benar",
            "points": [
                "**session_start()** → Harus dipanggil untuk mengakses session",
                "**session_destroy()** → Menghancurkan semua data session",
                "**header()** → Redirect kembali ke halaman login"
            ]
        },
        "critical_parts": [
            "session_start()",
            "session_destroy()",
            "header(\"location:login.php\")"
        ]
    },

    "Form Tambah Data (Create)": {
        "deskripsi": "Form HTML untuk menambah data baru dengan validasi session",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

// PROTEKSI SESSION
if (!isset($_SESSION['id_user'])) {
    header("location:login.php");
    exit;
}

$sql_category = "SELECT * FROM category";
$query_category = mysqli_query($koneksi, $sql_category);
?>

<!DOCTYPE html>
<html>
<head>
<title>Tambah Todo</title>
<style>
/* BOX LAYOUT */
.box {
    width: 350px;
    background: white;
    border: 2px solid black;
    padding: 20px;
    margin: 60px auto;
    border-radius: 8px;
}

/* FORM ELEMENTS */
input, textarea, select {
    width: 100%;
    padding: 8px;
    margin: 8px 0 16px;
    border: 1px solid #111;
    border-radius: 4px;
    font-size: 14px;
}

/* LABEL */
label {
    font-weight: bold;
    font-size: 14px;
}

/* BUTTON */
button {
    background: #111;
    color: white;
    border: none;
    padding: 10px;
    width: 100%;
    border-radius: 4px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}
button:hover {
    background: #333;
}
</style>
</head>
<body>
<div class="box">
    <h3>Tambah Todo</h3>
    <form action="proses_tambah.php" method="post">
        <label>Judul</label>
        <input type="text" name="title" required>
        <label>Deskripsi</label>
        <textarea name="description" rows="3"></textarea>
        <label>Kategori</label>
        <select name="id_category">
            <?php while($c = mysqli_fetch_assoc($query_category)): ?>
                <option value="<?= $c['id_category']; ?>">
                    <?= $c['category']; ?>
                </option>
            <?php endwhile; ?>
        </select>
        <button type="submit">Simpan</button>
    </form>
</div>
</body>
</html>""",
        "penjelasan": {
            "title": "Form Create dengan PHP",
            "points": [
                "**required attribute** → Validasi wajib diisi di client side",
                "**<textarea>** → Untuk input teks multi-line",
                "**<select>** → Dropdown untuk pilihan kategori",
                "**while loop** → Menampilkan option kategori dari database",
                "**margin: auto** → Center align box secara horizontal",
                "**transition** → Efek transisi pada hover",
                "**cursor: pointer** → Mengubah kursor saat hover"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "if (!isset($_SESSION['id_user']))",
            "header(\"location:login.php\")",
            "exit",
            "$sql_category = \"SELECT * FROM category\"",
            "mysqli_query($koneksi, $sql_category)",
            "action=\"proses_tambah.php\"",
            "method=\"post\"",
            "name=\"title\"",
            "name=\"description\"",
            "name=\"id_category\"",
            "required",
            "<?php while($c = mysqli_fetch_assoc($query_category)): ?>",
            "<?= $c['id_category']; ?>",
            "<?= $c['category']; ?>",
            "<?php endwhile; ?>"
        ]
    },

    "Proses Tambah (INSERT)": {
        "deskripsi": "Proses menyimpan data ke database",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_user = $_SESSION['id_user'];
$title = $_POST['title'];
$description = $_POST['description'];
$id_category = $_POST['id_category'];

$sql = "INSERT INTO todo (id_user, title, description, id_category, status)
        VALUES ('$id_user', '$title', '$description', '$id_category', 'pending')";

mysqli_query($koneksi, $sql);

header("location:index.php");
?>""",
        "penjelasan": {
            "title": "INSERT Query Structure",
            "points": [
                "**$_SESSION['id_user']** → Mengambil ID user dari session",
                "**$_POST[]** → Mengambil data dari form",
                "**INSERT INTO** → Syntax untuk menambah data",
                "**VALUES()** → Nilai yang akan diinsert",
                "**'pending'** → Default value untuk status",
                "**mysqli_query()** → Eksekusi query ke database",
                "**header()** → Redirect setelah sukses"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_SESSION['id_user']",
            "$_POST['title']",
            "$_POST['description']",
            "$_POST['id_category']",
            "INSERT INTO todo",
            "VALUES ('$id_user', '$title', '$description', '$id_category', 'pending')",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")"
        ]
    },

    "Form Edit Data": {
        "deskripsi": "Form untuk mengedit data yang sudah ada",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

// PROTEKSI SESSION
if (!isset($_SESSION['id_user'])) {
    header("location:login.php");
    exit;
}

$id_todo = $_GET['id_todo'];

// AMBIL DATA YANG AKAN DIEDIT
$sql = "SELECT * FROM todo WHERE id_todo='$id_todo'";
$query = mysqli_query($koneksi, $sql);
$todo = mysqli_fetch_assoc($query);

// AMBIL DATA KATEGORI
$sql_category = "SELECT * FROM category";
$query_category = mysqli_query($koneksi, $sql_category);
?>""",
        "penjelasan": {
            "title": "Mengambil Data untuk Edit",
            "points": [
                "**$_GET['id_todo']** → Mengambil parameter ID dari URL",
                "**SELECT * WHERE** → Query untuk mengambil 1 data spesifik",
                "**mysqli_fetch_assoc()** → Mengambil data dalam bentuk array",
                "**$todo[]** → Variable yang menyimpan data lama",
                "**Saat Edit** → Form diisi dengan nilai dari database"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "if (!isset($_SESSION['id_user']))",
            "header(\"location:login.php\")",
            "exit",
            "$_GET['id_todo']",
            "SELECT * FROM todo WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "mysqli_fetch_assoc($query)",
            "SELECT * FROM category",
            "mysqli_query($koneksi, $sql_category)"
        ]
    },

    "Proses Edit (UPDATE)": {
        "deskripsi": "Proses update data di database",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_todo = $_POST['id_todo'];
$title = $_POST['title'];
$description = $_POST['description'];
$id_category = $_POST['id_category'];

$sql = "UPDATE todo SET
        title='$title',
        description='$description',
        id_category='$id_category'
        WHERE id_todo='$id_todo'";

mysqli_query($koneksi, $sql);

header("location:index.php");
?>""",
        "penjelasan": {
            "title": "UPDATE Query Structure",
            "points": [
                "**UPDATE table SET** → Syntax untuk update data",
                "**column='value'** → Mengatur nilai baru untuk kolom",
                "**WHERE** → WAJIB untuk menentukan data mana yang diupdate",
                "**Tanpa WHERE** → Semua data akan terupdate (BAHAYA!)",
                "**$id_todo** → Identifier unik untuk data yang diupdate"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_POST['id_todo']",
            "$_POST['title']",
            "$_POST['description']",
            "$_POST['id_category']",
            "UPDATE todo SET",
            "WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")"
        ]
    },

    "Proses Hapus (DELETE)": {
        "deskripsi": "Menghapus data dengan konfirmasi JavaScript",
        "tipe": "php",
        "kode": """<?php
session_start();
include '../koneksi.php';

$id_todo = $_GET['id_todo'];

$sql = "DELETE FROM todo WHERE id_todo='$id_todo'";
mysqli_query($koneksi, $sql);

header("location:index.php");
?>

<!-- JavaScript Confirm -->
<a href="hapus.php?id_todo=<?= $todo['id_todo']; ?>"
   class="btn btn-delete"
   onclick="return confirm('Yakin hapus data ini?')">
   Hapus
</a>""",
        "penjelasan": {
            "title": "DELETE dengan Keamanan",
            "points": [
                "**DELETE FROM** → Syntax untuk menghapus data",
                "**WHERE** → WAJIB agar tidak menghapus semua data",
                "**JavaScript confirm()** → Konfirmasi sebelum menghapus",
                "**return confirm()** → Jika false, link tidak diikuti",
                "**Best Practice** → Selalu gunakan konfirmasi untuk delete"
            ]
        },
        "critical_parts": [
            "session_start()",
            "include '../koneksi.php'",
            "$_GET['id_todo']",
            "DELETE FROM todo",
            "WHERE id_todo='$id_todo'",
            "mysqli_query($koneksi, $sql)",
            "header(\"location:index.php\")",
            "onclick=\"return confirm('Yakin hapus data ini?')\""
        ]
    },

    "Navbar CSS": {
        "deskripsi": "Navigation bar dengan styling modern",
        "tipe": "css",
        "kode": """<style>
/* NAVBAR STYLING */
.navbar{
    background: linear-gradient(90deg, #111 0%, #333 100%);
    color: white;
    padding: 15px 30px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

/* NAVBAR LINKS */
.navbar a{
    color: white;
    text-decoration: none;
    margin-left: 20px;
    padding: 8px 16px;
    border-radius: 4px;
    transition: background 0.3s;
}
.navbar a:hover{
    background: rgba(255,255,255,0.1);
}

/* LOGOUT BUTTON */
.navbar a[href*="logout"]{
    background: #dc2626;
}
.navbar a[href*="logout"]:hover{
    background: #b91c1c;
}
</style>

<!-- HTML NAVBAR -->
<div class="navbar">
    <h3>📝 Todo App</h3>
    <div>
        <a href="index.php">🏠 Home</a>
        <a href="tambah.php">➕ Tambah</a>
        <a href="profil.php">👤 Profil</a>
        <a href="logout.php">🚪 Logout</a>
    </div>
</div>""",
        "penjelasan": {
            "title": "CSS Navbar Techniques",
            "points": [
                "**display: flex** → Untuk layout horizontal",
                "**justify-content: space-between** → Space antara logo dan menu",
                "**position: sticky** → Navbar tetap saat scroll",
                "**z-index** → Menentukan layer/tingkatan",
                "**linear-gradient()** → Background gradient",
                "**rgba()** → Warna dengan opacity",
                "**a[href*='logout']** → Selector attribute untuk styling spesifik"
            ]
        },
        "critical_parts": [
            "display: flex",
            "justify-content: space-between",
            "align-items: center",
            "position: sticky",
            "top: 0",
            "z-index: 1000",
            "box-shadow: 0 2px 10px rgba(0,0,0,0.2)",
            "background: linear-gradient(90deg, #111 0%, #333 100%)",
            "text-decoration: none",
            "transition: background 0.3s",
            ":hover",
            "a[href*=\"logout\"]"
        ]
    },

    "Button Styling": {
        "deskripsi": "Berbagai style button untuk CRUD operations",
        "tipe": "css",
        "kode": """<style>
/* BUTTON BASE */
.btn{
    display: inline-block;
    padding: 8px 16px;
    text-decoration: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    border: none;
    cursor: pointer;
    transition: all 0.3s;
    margin: 5px;
}

/* BUTTON VARIANTS */
.btn-edit{
    background: #2563eb;
    color: white;
}
.btn-edit:hover{
    background: #1d4ed8;
    transform: translateY(-2px);
}

.btn-delete{
    background: #dc2626;
    color: white;
}
.btn-delete:hover{
    background: #b91c1c;
    transform: translateY(-2px);
}

.btn-add{
    background: #059669;
    color: white;
}
.btn-add:hover{
    background: #047857;
    transform: translateY(-2px);
}

.btn-save{
    background: #111;
    color: white;
    width: 100%;
    padding: 12px;
}
.btn-save:hover{
    background: #333;
}

/* BUTTON WITH ICON */
.btn i{
    margin-right: 6px;
}
</style>""",
        "penjelasan": {
            "title": "CSS Button Best Practices",
            "points": [
                "**transition: all 0.3s** → Smooth animation untuk semua properti",
                "**:hover** → State ketika mouse di atas button",
                "**transform: translateY()** → Efek mengangkat saat hover",
                "**Color Coding** → Warna berbeda untuk aksi berbeda",
                "**btn-edit (biru)** → Untuk update/edit",
                "**btn-delete (merah)** → Untuk delete/hapus",
                "**btn-add (hijau)** → Untuk tambah data",
                "**box-shadow** → Menambahkan depth perception"
            ]
        },
        "critical_parts": [
            "display: inline-block",
            "padding: 8px 16px",
            "text-decoration: none",
            "border-radius: 6px",
            "transition: all 0.3s",
            ":hover",
            "transform: translateY(-2px)",
            "cursor: pointer"
        ]
    }
}

# =========================
# FUNGSI UTILITY
# =========================
def calculate_similarity(text1, text2):
    """Hitung persentase kemiripan antara dua teks"""
    def clean_code(code):
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'\s+', ' ', code)
        return code.strip().lower()
    
    user_clean = clean_code(text1)
    correct_clean = clean_code(text2)
    
    similarity = SequenceMatcher(None, user_clean, correct_clean).ratio() * 100
    return round(similarity, 2)

def check_critical_parts(user_code, critical_parts):
    """Cek bagian-bagian kritis yang harus ada"""
    results = []
    user_code_lower = user_code.lower()
    
    for part in critical_parts:
        part_lower = part.lower()
        if part_lower in user_code_lower:
            results.append((part, True, "✅"))
        else:
            results.append((part, False, "❌"))
    
    return results

def analyze_code_errors(user_code, correct_code, code_type):
    """Analisis kesalahan umum dalam kode"""
    errors = []
    warnings = []
    suggestions = []
    
    user_code_lower = user_code.lower()
    
    if "php" in code_type:
        if "session_start()" not in user_code:
            errors.append("❌ **session_start()** tidak ditemukan! (WAJIB ada di baris pertama)")
        
        if "include" not in user_code_lower and "require" not in user_code_lower:
            errors.append("❌ **include/require** koneksi database tidak ditemukan!")
        
        if "header(" in user_code and "exit" not in user_code and "die" not in user_code:
            warnings.append("⚠️ **header()** digunakan tanpa **exit()** atau **die()**")
        
        if "update" in user_code_lower and "where" not in user_code_lower:
            errors.append("❌ **UPDATE** query tanpa **WHERE** clause! (SANGAT BERBAHAYA)")
        
        if "delete" in user_code_lower and "where" not in user_code_lower:
            errors.append("❌ **DELETE** query tanpa **WHERE** clause! (SANGAT BERBAHAYA)")
        
        if "insert" in user_code_lower and "values" not in user_code_lower:
            warnings.append("⚠️ **INSERT** query tanpa **VALUES()**")
        
        if "select" in user_code_lower and "from" not in user_code_lower:
            errors.append("❌ **SELECT** query tanpa **FROM** clause")
    
    elif "html" in code_type:
        if "<!doctype" not in user_code_lower:
            errors.append("❌ **DOCTYPE** declaration tidak ditemukan")
        
        if "<form" in user_code_lower and ("method=" not in user_code_lower or "action=" not in user_code_lower):
            warnings.append("⚠️ Form tanpa **method** atau **action** attribute")
        
        if "required" not in user_code_lower and "name=" in user_code_lower:
            warnings.append("⚠️ Input field tanpa **required** attribute")
    
    elif "css" in code_type:
        if "{" in user_code and "}" not in user_code:
            errors.append("❌ Kurung kurawal **{}** tidak ditutup")
        
        if ":" in user_code and ";" not in user_code:
            warnings.append("⚠️ Property CSS tanpa titik koma **;**")
        
        if "display:" in user_code and ("flex" not in user_code_lower and "grid" not in user_code_lower):
            warnings.append("⚠️ **display** property tanpa value yang jelas")
    
    # Suggestions berdasarkan similarity
    similarity = calculate_similarity(user_code, correct_code)
    if similarity < 50:
        suggestions.append("💡 Pelajari lagi struktur dasar dari materi ini")
    elif similarity < 75:
        suggestions.append("💡 Fokus pada bagian yang masih kurang tepat")
    elif similarity < 90:
        suggestions.append("💡 Hampir sempurna! Perbaiki detail kecil")
    else:
        suggestions.append("🎉 Excellent! Kode sudah sangat mirip dengan contoh")
    
    return errors, warnings, suggestions

def extract_code_segments(full_code, num_segments=3):
    """Ekstrak bagian-bagian kode yang penting untuk dihafal"""
    lines = full_code.split('\n')
    segments = []
    
    # Cari bagian-bagian kritis
    keywords = ["session_start", "include", "require", "SELECT", "INSERT", "UPDATE", "DELETE", 
                "WHERE", "header(", "exit", "mysqli_query", "DOCTYPE", "<form", 
                "display:", "grid-template", "function", "if(", "while(", "foreach",
                "<?php", "?>", "VALUES", "JOIN", "LEFT JOIN", "method=", "action="]
    
    current_segment = []
    for line in lines:
        if any(keyword in line for keyword in keywords):
            if current_segment:
                segments.append('\n'.join(current_segment))
                current_segment = []
            # Ambil beberapa line sekitar keyword
            line_idx = lines.index(line)
            start = max(0, line_idx - 1)
            end = min(len(lines), line_idx + 3)
            segment = '\n'.join(lines[start:end])
            segments.append(segment)
    
    # Jika tidak cukup segment, bagi menjadi bagian-bagian
    if len(segments) < num_segments:
        segment_size = len(lines) // num_segments
        segments = []
        for i in range(num_segments):
            start = i * segment_size
            end = (i + 1) * segment_size if i < num_segments - 1 else len(lines)
            if end - start > 5:  # Minimal 5 baris
                segments.append('\n'.join(lines[start:end]))
    
    # Pilih 3 segment terbaik
    return segments[:min(num_segments, len(segments))]

# =========================
# TIMER FUNGSI UTILITY
# =========================
def format_time(seconds):
    """Format waktu dalam MM:SS"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"

def update_timer():
    """Update timer setiap detik"""
    if 'hafalan_timer_start' in st.session_state:
        elapsed = time.time() - st.session_state.hafalan_timer_start
        return max(0, st.session_state.hafalan_timer_duration - elapsed)
    return 0

# =========================
# SIDEBAR NAVIGATION
# =========================
with st.sidebar:
    st.title("📚 PerpusCode USK")
    
    # Mode selection using radio buttons instead of option_menu
    st.markdown("### 🎯 Mode Belajar")
    mode_options = ["🏠 Dashboard", "📖 Belajar", "✏️ Praktek", "🎯 Simulasi", "📊 Progress", "❓ Quiz"]
    selected_mode = st.radio(
        "Pilih Mode:",
        mode_options,
        index=mode_options.index(st.session_state.current_mode) if st.session_state.current_mode in mode_options else 0,
        label_visibility="collapsed"
    )
    
    # Update session state
    st.session_state.current_mode = selected_mode
    
    st.markdown("---")
    
    # Pilih materi
    materi_list = list(materi.keys())
    selected_topic = st.selectbox(
        "📖 Pilih Materi:",
        materi_list,
        key="selected_topic"
    )
    
    # Update last viewed
    if selected_topic not in st.session_state.last_viewed:
        st.session_state.last_viewed.append(selected_topic)
        if len(st.session_state.last_viewed) > 5:
            st.session_state.last_viewed.pop(0)
    
    st.markdown("---")
    
    # Toggle Hafalan Mode
    hafalan_aktif = st.checkbox("🧠 Mode Hafalan Kode", value=st.session_state.hafalan_mode)
    if hafalan_aktif != st.session_state.hafalan_mode:
        st.session_state.hafalan_mode = hafalan_aktif
        st.rerun()
    
    # Quick stats
    if selected_topic in st.session_state.practice_scores:
        latest_score = st.session_state.practice_scores[selected_topic][-1]
        st.metric("Skor Terakhir", f"{latest_score}%")
    else:
        st.metric("Skor Terakhir", "Belum ada")
    
    # Timer setting untuk hafalan
    if st.session_state.hafalan_mode:
        st.markdown("---")
        st.markdown("### ⏱️ Timer Hafalan")
        timer_setting = st.slider(
            "Waktu (detik):",
            30, 300, 120,
            key="sidebar_timer"
        )
        st.session_state.hafalan_timer = timer_setting
    
    # Last viewed
    with st.expander("📖 Riwayat Materi"):
        for item in reversed(st.session_state.last_viewed):
            st.caption(f"✓ {item}")
        
        # Tampilkan custom codes yang sudah dibuat
        if st.session_state.user_custom_codes:
            st.markdown("---")
            st.markdown("**🧠 Kode Custom:**")
            for topic, codes in st.session_state.user_custom_codes.items():
                for i, code in enumerate(codes):
                    st.caption(f"• {topic} - Bagian {i+1}")

# =========================
# DASHBOARD MODE
# =========================
if selected_mode == "🏠 Dashboard":
    st.title("🏠 Dashboard - Persiapan USK")
    
    # Header stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        total_materi = len(materi)
        st.metric("Total Materi", total_materi)
    with col2:
        practiced = len(st.session_state.practice_scores)
        st.metric("Sudah Dipraktekkan", practiced)
    with col3:
        if st.session_state.practice_scores:
            all_scores = []
            for scores in st.session_state.practice_scores.values():
                all_scores.extend(scores)
            avg_score = sum(all_scores) / len(all_scores)
            st.metric("Rata-rata Skor", f"{avg_score:.1f}%")
        else:
            st.metric("Rata-rata Skor", "0%")
    with col4:
        # Hitung total kode custom yang dibuat
        total_custom = sum(len(codes) for codes in st.session_state.user_custom_codes.values())
        st.metric("Kode Custom", total_custom)
    
    # Materi baru yang ditambahkan
    st.markdown("---")
    st.subheader("🆕 Materi Baru yang Ditambahkan:")
    
    new_materials = [
        "Index Page dengan Filter & Favorit (Session)",
        "Form Daftar Pengguna Baru (HTML)",
        "Proses Pendaftaran (INSERT)",
        "Halaman Profil User",
        "CSS Full Project (style.css)"
    ]
    
    for mat in new_materials:
        st.markdown(f"✅ **{mat}**")
    
    # Fitur baru: Hafalan Kode Custom
    st.markdown("---")
    st.subheader("🧠 Fitur Baru: Hafalan Kode Custom")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("""
        **🎯 Fitur Hafalan Kode CUSTOM:**
        
        1. **Pilih bagian kode** yang ingin dihafal
        2. **Atau buat kode custom** sendiri
        3. **Set timer** untuk menghafal
        4. **Tulis dari ingatan**
        5. **Dapatkan analisis** detail
        6. **Simpan progress** hafalan
        """)
    
    with col2:
        st.success("""
        **✨ Fleksibel & Personal:**
        
        • Bisa pilih dari materi yang ada
        • Bisa input kode custom sendiri
        • Pilih bahasa: PHP, HTML, CSS, JS
        • Atur waktu menghafal sesuai kemampuan
        • Simpan kode favorit untuk latihan
        """)
    
    # Quick actions
    st.markdown("---")
    st.subheader("🚀 Aksi Cepat")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📖 Lanjut Belajar", use_container_width=True, type="primary"):
            st.session_state.current_mode = "📖 Belajar"
            st.rerun()
    with col2:
        if st.button("✏️ Mulai Praktek", use_container_width=True, type="primary"):
            st.session_state.current_mode = "✏️ Praktek"
            st.rerun()
    with col3:
        if st.button("🧠 Buat Hafalan Custom", use_container_width=True, type="primary"):
            st.session_state.current_mode = "✏️ Praktek"
            st.session_state.hafalan_mode = True
            st.session_state.show_custom_input = True
            st.rerun()

# =========================
# BELAJAR MODE
# =========================
elif selected_mode == "📖 Belajar":
    st.title("📖 Mode Belajar")
    
    topic_data = materi[selected_topic]
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.subheader(f"{selected_topic}")
    with col2:
        st.caption(f"Tipe: {topic_data['tipe'].upper()}")
    
    st.markdown(f"**Deskripsi:** {topic_data['deskripsi']}")
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📝 Kode Lengkap", "📚 Penjelasan", "💡 Tips", "🧠 Buat Hafalan"])
    
    with tab1:
        st.code(topic_data["kode"], language=topic_data["tipe"])
        
        # Critical parts
        st.markdown("### ⚠️ Bagian Kritis (WAJIB DIINGAT):")
        for i, part in enumerate(topic_data["critical_parts"][:10]):  # Tampilkan 10 pertama
            st.markdown(f"{i+1}. `{part}`")
        
        # Jika masih ada bagian kritis lainnya
        if len(topic_data["critical_parts"]) > 10:
            with st.expander("Lihat semua bagian kritis"):
                for i, part in enumerate(topic_data["critical_parts"][10:]):
                    st.markdown(f"{i+11}. `{part}`")
    
    with tab2:
        penjelasan = topic_data["penjelasan"]
        st.subheader(penjelasan["title"])
        
        for point in penjelasan["points"]:
            st.markdown(f"• {point}")
        
        # Additional notes berdasarkan jenis materi
        if "Index Page" in selected_topic:
            st.info("""
            **Catatan Penting Filter & Favorit:**
            1. **$_SESSION['favorite']** digunakan untuk menyimpan status favorit tanpa database
            2. **Dynamic WHERE** memungkinkan filter bertumpuk (kategori + status + favorit)
            3. **LEFT JOIN** memastikan semua todo ditampilkan meski tanpa kategori
            4. **Auto Submit** dengan onchange memberikan UX yang lebih baik
            """)
        elif "Daftar" in selected_topic or "Pendaftaran" in selected_topic:
            st.info("""
            **Catatan Penting Pendaftaran:**
            1. **HTML5 Input Types** memberikan validasi otomatis (email, date)
            2. **md5()** digunakan untuk hashing password (lebih baik gunakan password_hash())
            3. **Feedback via URL Parameter** (?daftar=sukses/gagal) untuk user experience
            4. **Include Navbar** memastikan konsistensi UI
            """)
        elif "Profil" in selected_topic:
            st.info("""
            **Catatan Penting Profil:**
            1. **Session Protection** hanya user yang login bisa akses profil sendiri
            2. **Password Security** password tidak ditampilkan langsung (****)
            3. **Inline CSS** untuk halaman sederhana yang tidak memerlukan file CSS terpisah
            4. **Back Navigation** selalu sediakan tombol kembali ke halaman utama
            """)
        elif "CSS Full" in selected_topic:
            st.info("""
            **Best Practice CSS Project:**
            1. **Organized Structure** kelompokkan CSS berdasarkan komponen
            2. **Mobile First** design dengan media queries di akhir
            3. **Consistent Naming** gunakan naming convention yang konsisten
            4. **Reusable Classes** buat class yang bisa dipakai ulang
            """)
        elif "Session" in selected_topic:
            st.info("""
            **Catatan Penting Session:**
            1. `session_start()` harus dipanggil SEBELUM output apapun ke browser
            2. Session data disimpan di server, aman dari client-side manipulation
            3. Gunakan `session_destroy()` untuk logout yang aman
            """)
        elif "CSS" in selected_topic:
            st.info("""
            **Best Practice CSS:**
            1. Gunakan class selector daripada tag selector untuk reusable style
            2. Implement mobile-first design dengan media queries
            3. Gunakan CSS Grid/Flexbox untuk layout modern
            """)
    
    with tab3:
        # Tips berdasarkan jenis materi
        if "Index Page" in selected_topic:
            st.success("""
            **Tips Filter & Pagination:**
            1. **SQL Injection Prevention** gunakan prepared statements untuk filter
            2. **Session Storage** untuk data kecil seperti favorit (tidak perlu database)
            3. **URL Parameters** gunakan untuk state management filter
            4. **Print Function** window.print() untuk fitur cetak tanpa library
            """)
        elif "Daftar" in selected_topic:
            st.warning("""
            **Tips Form Registration:**
            1. **Validation** validasi email format dan password strength
            2. **Duplicate Check** cek apakah username/email sudah terdaftar
            3. **Password Hashing** gunakan password_hash() bukan md5()
            4. **Email Verification** kirim email verifikasi sebelum aktivasi
            """)
        elif "Profil" in selected_topic:
            st.info("""
            **Tips Profile Page:**
            1. **Edit Function** tambahkan form edit profil
            2. **Password Change** sediakan form ubah password terpisah
            3. **Avatar Upload** tambahkan fitur upload foto profil
            4. **Activity Log** tampilkan riwayat aktivitas user
            """)
        elif "CSS Full" in selected_topic:
            st.info("""
            **Tips CSS Optimization:**
            1. **CSS Variables** gunakan :root untuk theme colors
            2. **BEM Methodology** untuk scalable CSS architecture
            3. **Minification** minify CSS untuk production
            4. **Critical CSS** inline critical CSS untuk faster loading
            """)
        elif "Login" in selected_topic:
            st.success("""
            **Tips Login System:**
            1. Selalu gunakan password hashing (md5, password_hash)
            2. Tambahkan limit attempt untuk prevent brute force
            3. Gunakan prepared statements untuk prevent SQL injection
            4. Always redirect setelah login/logout
            """)
        elif "INSERT" in selected_topic or "CREATE" in selected_topic:
            st.warning("""
            **Tips INSERT Data:**
            1. Validasi input di server-side (tidak hanya client-side)
            2. Gunakan prepared statements untuk keamanan
            3. Berikan feedback setelah insert (sukses/gagal)
            4. Redirect ke halaman list setelah insert
            """)
        elif "UPDATE" in selected_topic:
            st.warning("""
            **Tips UPDATE Data:**
            1. SELALU gunakan WHERE clause, jika tidak semua data akan terupdate
            2. Ambil data lama sebelum edit untuk default value
            3. Validasi bahwa user memiliki akses untuk edit data tersebut
            4. Gunakan hidden input untuk menyimpan ID data
            """)
        elif "DELETE" in selected_topic:
            st.error("""
            **Tips DELETE Data:**
            1. WAJIB gunakan WHERE dengan primary key
            2. Tambahkan konfirmasi JavaScript
            3. Pertimbangkan soft delete (tambah kolom is_deleted)
            4. Backup data penting sebelum delete operation
            """)
        elif "CSS" in selected_topic:
            st.info("""
            **Tips CSS:**
            1. Organize CSS dengan BEM methodology
            2. Use CSS variables for consistent theming
            3. Test on multiple screen sizes
            4. Use developer tools for debugging
            """)
    
    with tab4:
        st.markdown("### 🧠 Buat Hafalan dari Materi Ini")
        
        # Pilihan: Auto extract atau manual select
        hafalan_type = st.radio(
            "Pilih cara membuat hafalan:",
            ["Auto Extract (Program pilih bagian penting)", "Manual Select (Saya pilih sendiri)"]
        )
        
        if hafalan_type == "Auto Extract":
            # Auto extract segments
            segments = extract_code_segments(topic_data["kode"], 3)
            
            st.markdown("#### 📋 Bagian-bagian yang akan dihafal:")
            for i, segment in enumerate(segments):
                with st.expander(f"Bagian {i+1}", expanded=i==0):
                    st.code(segment, language=topic_data["tipe"])
            
            if st.button("✅ Gunakan untuk Hafalan", type="primary"):
                st.session_state.code_segments = segments
                st.session_state.current_segment_index = 0
                st.session_state.hafalan_mode = True
                st.session_state.current_mode = "✏️ Praktek"
                st.rerun()
        
        else:  # Manual Select
            st.markdown("#### ✍️ Pilih/Salin bagian kode yang ingin dihafal:")
            
            # Tampilkan kode dengan line numbers untuk memudahkan pemilihan
            code_lines = topic_data["kode"].split('\n')
            line_numbers = list(range(1, len(code_lines) + 1))
            
            # Buat text area untuk user memilih bagian
            st.markdown("**Kode lengkap:**")
            st.code(topic_data["kode"], language=topic_data["tipe"])
            
            st.markdown("**Salin bagian yang ingin dihafal:**")
            custom_code = st.text_area(
                "Tempel/salin kode yang ingin dihafal:",
                height=200,
                placeholder="Salin bagian kode dari atas yang ingin kamu hafal...\nContoh:\nsession_start();\nrequire '../koneksi.php';\n// ... dst",
                key="manual_select_code"
            )
            
            if st.button("✅ Buat Hafalan Custom", type="primary"):
                if custom_code.strip():
                    st.session_state.custom_code_to_memorize = custom_code
                    st.session_state.hafalan_mode = True
                    st.session_state.current_mode = "✏️ Praktek"
                    st.session_state.is_custom_code = True
                    st.rerun()
                else:
                    st.warning("⚠️ Silakan masukkan kode yang ingin dihafal!")
        
        # Tampilkan custom codes yang sudah dibuat untuk materi ini
        if selected_topic in st.session_state.user_custom_codes:
            st.markdown("---")
            st.markdown("#### 📚 Hafalan Custom yang Sudah Dibuat:")
            custom_codes = st.session_state.user_custom_codes[selected_topic]
            
            for i, code in enumerate(custom_codes):
                with st.expander(f"Hafalan Custom {i+1}", expanded=False):
                    st.code(code[:500] + "..." if len(code) > 500 else code, language=topic_data["tipe"])
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🔄 Gunakan Lagi {i+1}", key=f"use_custom_{i}"):
                            st.session_state.custom_code_to_memorize = code
                            st.session_state.hafalan_mode = True
                            st.session_state.current_mode = "✏️ Praktek"
                            st.session_state.is_custom_code = True
                            st.rerun()
                    with col2:
                        if st.button(f"🗑️ Hapus {i+1}", key=f"delete_custom_{i}"):
                            st.session_state.user_custom_codes[selected_topic].pop(i)
                            if not st.session_state.user_custom_codes[selected_topic]:
                                del st.session_state.user_custom_codes[selected_topic]
                            st.rerun()

# =========================
# PRAKTEK MODE (DENGAN FITUR HAFALAN CUSTOM & TIMER IMPROVED)
# =========================
elif selected_mode == "✏️ Praktek":
    st.title("✏️ Mode Praktek Menulis Kode")
    
    # Toggle untuk pilihan mode
    if not st.session_state.hafalan_mode:
        # MODE NORMAL - Pilihan awal
        st.markdown("### 📋 Pilih Mode Praktek:")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📝 Praktek Normal", use_container_width=True, type="primary"):
                st.session_state.hafalan_mode = False
                st.rerun()
        
        with col2:
            if st.button("🧠 Mode Hafalan", use_container_width=True, type="primary"):
                st.session_state.hafalan_mode = True
                st.rerun()
        
        # Penjelasan singkat
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            st.info("""
            **📝 Praktek Normal:**
            - Tulis kode lengkap
            - Dengan petunjuk & timer
            - Analisis similarity
            - Cocok untuk latihan umum
            """)
        
        with col2:
            st.success("""
            **🧠 Mode Hafalan:**
            - Fokus menghafal bagian spesifik
            - Bisa custom atau dari materi
            - Timer menghafal khusus
            - Cocok untuk persiapan USK
            """)
    
    elif st.session_state.hafalan_mode:
        # MULAI MODE HAFALAN
        st.warning("🧠 **MODE HAFALAN AKTIF**")
        
        # Pilih sumber kode untuk dihafal
        if 'hafalan_source_selected' not in st.session_state:
            st.session_state.hafalan_source_selected = False
        
        if not st.session_state.hafalan_source_selected:
            st.markdown("### 📋 Pilih Sumber Kode untuk Dihafal:")
            
            tab1, tab2 = st.tabs(["📚 Dari Materi", "✍️ Custom Code"])
            
            with tab1:
                # Pilih dari materi yang ada
                topic_data = materi[selected_topic]
                
                st.markdown(f"**Materi:** {selected_topic}")
                st.markdown(f"**Tipe:** {topic_data['tipe'].upper()}")
                
                # Tampilkan kode lengkap
                with st.expander("👁️ Lihat Kode Lengkap", expanded=False):
                    st.code(topic_data["kode"], language=topic_data["tipe"])
                
                # Pilihan: Auto atau Manual
                st.markdown("#### 🎯 Pilih Bagian untuk Dihafal:")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🤖 Auto Pilih 3 Bagian", use_container_width=True):
                        segments = extract_code_segments(topic_data["kode"], 3)
                        st.session_state.code_segments = segments
                        st.session_state.current_segment_index = 0
                        st.session_state.hafalan_source = "auto_material"
                        st.session_state.hafalan_source_selected = True
                        st.session_state.hafalan_start_time = time.time()
                        st.rerun()
                
                with col2:
                    if st.button("✋ Saya Pilih Sendiri", use_container_width=True):
                        st.session_state.show_manual_select = True
                        st.rerun()
                
                # Jika user memilih manual select
                if 'show_manual_select' in st.session_state and st.session_state.show_manual_select:
                    st.markdown("---")
                    st.markdown("#### ✍️ Pilih Bagian Kode:")
                    
                    # Tampilkan kode dengan checkbox per bagian
                    code_parts = topic_data["kode"].split('\n\n')  # Bagi berdasarkan paragraf kosong
                    
                    selected_parts = []
                    for i, part in enumerate(code_parts):
                        if len(part.strip()) > 10:  # Hanya bagian yang cukup panjang
                            col1, col2 = st.columns([1, 4])
                            with col1:
                                select = st.checkbox(f"Pilih", key=f"part_{i}")
                            with col2:
                                st.code(part[:200] + "..." if len(part) > 200 else part, 
                                      language=topic_data["tipe"])
                            
                            if select:
                                selected_parts.append(part)
                    
                    if selected_parts:
                        if st.button("✅ Gunakan Bagian Terpilih", type="primary"):
                            st.session_state.code_segments = selected_parts
                            st.session_state.current_segment_index = 0
                            st.session_state.hafalan_source = "manual_material"
                            st.session_state.hafalan_source_selected = True
                            st.session_state.hafalan_start_time = time.time()
                            st.rerun()
                    else:
                        st.warning("Pilih minimal 1 bagian kode")
            
            with tab2:
                # Input custom code
                st.markdown("#### ✍️ Buat Hafalan Custom")
                
                # Pilih tipe kode
                code_type = st.selectbox(
                    "Pilih Bahasa/Tipe Kode:",
                    ["php", "html", "css", "javascript", "sql", "lainnya"]
                )
                
                # Input kode custom
                custom_code = st.text_area(
                    "Masukkan kode yang ingin dihafal:",
                    height=300,
                    placeholder="Contoh:\n<?php\nsession_start();\nrequire 'koneksi.php';\n\n$username = $_POST['username'];\n// ... tambahkan kode lainnya",
                    key="custom_code_input"
                )
                
                # Beri nama untuk kode ini
                code_name = st.text_input(
                    "Beri nama untuk kode ini (opsional):",
                    placeholder="Contoh: Session Login, CRUD Delete, dll"
                )
                
                if st.button("✅ Buat Hafalan Custom", type="primary"):
                    if custom_code.strip():
                        # Simpan kode custom
                        st.session_state.custom_code_to_memorize = custom_code
                        st.session_state.custom_code_type = code_type
                        st.session_state.custom_code_name = code_name or "Kode Custom"
                        st.session_state.hafalan_source = "custom"
                        st.session_state.hafalan_source_selected = True
                        st.session_state.hafalan_start_time = time.time()
                        
                        # Simpan ke daftar custom codes
                        if "Custom" not in st.session_state.user_custom_codes:
                            st.session_state.user_custom_codes["Custom"] = []
                        st.session_state.user_custom_codes["Custom"].append(custom_code)
                        
                        st.rerun()
                    else:
                        st.warning("⚠️ Silakan masukkan kode terlebih dahulu!")
            
            # Tombol untuk kembali
            if st.button("⬅️ Kembali ke Pilihan Mode", type="secondary"):
                st.session_state.hafalan_mode = False
                st.rerun()
        
        else:
            # TAMPILAN MODE HAFALAN AKTIF
            # Tentukan kode yang akan dihafal
            if st.session_state.hafalan_source == "custom":
                # Custom code
                code_to_memorize = st.session_state.custom_code_to_memorize
                code_type = st.session_state.custom_code_type
                code_name = st.session_state.custom_code_name
                
                st.markdown(f"### 🧠 HAFALAN: {code_name}")
                st.caption(f"Tipe: {code_type.upper()} | Sumber: Custom Code")
                
                # Tampilkan sebagai single segment
                segments = [code_to_memorize]
                current_index = 0
                total_segments = 1
            
            else:
                # Dari materi
                topic_data = materi[selected_topic]
                code_type = topic_data["tipe"]
                
                if st.session_state.hafalan_source == "auto_material":
                    st.markdown(f"### 🧠 HAFALAN: {selected_topic} (Auto)")
                else:
                    st.markdown(f"### 🧠 HAFALAN: {selected_topic} (Manual)")
                
                st.caption(f"Tipe: {code_type.upper()} | Sumber: Materi")
                
                segments = st.session_state.code_segments
                current_index = st.session_state.current_segment_index
                total_segments = len(segments)
            
            # Tampilkan progress
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Bagian", f"{current_index + 1}/{total_segments}")
            with col2:
                # Hitung waktu sudah menghafal
                elapsed = time.time() - st.session_state.hafalan_start_time
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                st.metric("Waktu Total", f"{minutes:02d}:{seconds:02d}")
            with col3:
                # Tombol reset/ulang
                if st.button("🔄 Ulang Bagian", use_container_width=True):
                    st.session_state.hafalan_start_time = time.time()
                    st.session_state.show_hafalan_editor = False
                    st.session_state.show_hafalan_results = False
                    st.session_state.hafalan_timer_start = None
                    st.rerun()
            
            # Tampilkan segment untuk dihafal
            current_segment = segments[current_index]
            
            st.markdown("### 📖 HAFALKAN KODE INI:")
            st.code(current_segment, language=code_type)
            
            # Timer dan kontrol hafalan
            st.markdown("---")
            col1, col2 = st.columns([2, 1])
            
            with col1:
                # Timer setting
                if 'hafalan_timer_duration' not in st.session_state:
                    st.session_state.hafalan_timer_duration = st.session_state.hafalan_timer
                
                hafalan_waktu = st.slider(
                    "⏱️ Set waktu menghafal (detik):",
                    30, 300, st.session_state.hafalan_timer_duration,
                    key="hafalan_timer_setting",
                    on_change=lambda: setattr(st.session_state, 'hafalan_timer_duration', st.session_state.hafalan_timer_setting)
                )
            
            with col2:
                if st.button("⏱️ Mulai Hafalan", type="primary", use_container_width=True):
                    st.session_state.hafalan_timer_start = time.time()
                    st.session_state.show_hafalan_editor = True
                    st.session_state.show_hafalan_results = False
                    st.session_state.auto_editor_shown = False
                    st.rerun()
            
            # Proses menghafal dengan timer
            if 'hafalan_timer_start' in st.session_state and st.session_state.hafalan_timer_start:
                elapsed = time.time() - st.session_state.hafalan_timer_start
                remaining = max(0, hafalan_waktu - elapsed)
                
                # Progress bar timer
                progress = min(1.0, elapsed / hafalan_waktu)
                
                # Create a custom progress bar with time display
                col_prog1, col_prog2 = st.columns([3, 1])
                with col_prog1:
                    st.progress(progress)
                with col_prog2:
                    st.markdown(f"**{format_time(remaining)}**")
                
                if remaining > 0:
                    st.info(f"⏱️ **Waktu menghafal tersisa:** {format_time(remaining)}")
                    
                    # Auto refresh timer
                    time.sleep(0.1)
                    st.rerun()
                else:
                    st.error("⏰ **WAKTU HABIS!** Tutup kode dan tulis dari ingatan.")
                    
                    # Auto tampilkan editor setelah waktu habis
                    if not st.session_state.get('auto_editor_shown', False):
                        st.session_state.show_hafalan_editor = True
                        st.session_state.auto_editor_shown = True
                        st.rerun()
            
            # Editor untuk menulis dari ingatan
            if 'show_hafalan_editor' in st.session_state and st.session_state.show_hafalan_editor:
                st.markdown("---")
                st.markdown("### ✍️ TULIS DARI INGATAN:")
                
                user_code = st.text_area(
                    "Tulis kode yang kamu hafal:",
                    height=250,
                    placeholder=f"Tulis kode yang baru saja kamu hafal...\nTips: Fokus pada struktur dan sintaks yang benar.",
                    key=f"hafalan_editor_{current_index}"
                )
                
                # Action buttons
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("✅ Cek Hafalan", type="primary", use_container_width=True):
                        if user_code.strip():
                            # Hitung similarity
                            similarity = calculate_similarity(user_code, current_segment)
                            
                            # Analisis kesalahan
                            errors, warnings, suggestions = analyze_code_errors(
                                user_code, 
                                current_segment, 
                                code_type
                            )
                            
                            # Simpan hasil
                            st.session_state.show_hafalan_results = True
                            st.session_state.last_hafalan_similarity = similarity
                            st.session_state.last_hafalan_errors = errors
                            st.session_state.last_hafalan_warnings = warnings
                            st.session_state.last_hafalan_suggestions = suggestions
                            st.session_state.last_user_code = user_code
                            st.rerun()
                        else:
                            st.warning("⚠️ Silakan tulis kode terlebih dahulu!")
                
                with col2:
                    if st.button("👁️ Lihat Kode Asli", use_container_width=True):
                        with st.expander("📖 Kode Asli", expanded=True):
                            st.code(current_segment, language=code_type)
                
                with col3:
                    if st.button("🔄 Ulang Hafalan", use_container_width=True):
                        st.session_state.hafalan_timer_start = time.time()
                        st.session_state.show_hafalan_results = False
                        st.session_state.auto_editor_shown = False
                        st.rerun()
                
                # Tampilkan hasil hafalan
                if 'show_hafalan_results' in st.session_state and st.session_state.show_hafalan_results:
                    st.markdown("---")
                    st.markdown("## 📊 HASIL HAFALAN")
                    
                    similarity = st.session_state.last_hafalan_similarity
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Kemiripan", f"{similarity}%")
                    with col2:
                        if similarity >= 90:
                            grade = "SEMPURNA 🎉"
                            color = "success"
                        elif similarity >= 80:
                            grade = "BAIK 👍"
                            color = "info"
                        elif similarity >= 70:
                            grade = "CUKUP 💪"
                            color = "warning"
                        else:
                            grade = "ULANGI 🔄"
                            color = "error"
                        st.metric("Status", grade)
                    with col3:
                        # Tombol bandingkan
                        if st.button("🔍 Bandingkan", use_container_width=True):
                            st.session_state.show_comparison = True
                            st.rerun()
                    
                    # Progress bar visual
                    progress_html = f"""
                    <div style="background-color: #f0f0f0; border-radius: 10px; padding: 3px; margin: 10px 0;">
                        <div style="background-color: {'#4CAF50' if similarity >= 90 else '#2196F3' if similarity >= 80 else '#FF9800' if similarity >= 70 else '#F44336'}; 
                                    width: {similarity}%; 
                                    height: 20px; 
                                    border-radius: 8px;">
                        </div>
                    </div>
                    """
                    st.markdown(progress_html, unsafe_allow_html=True)
                    
                    # Tampilkan evaluasi
                    if similarity >= 80:
                        st.success(f"🎉 **Bagus sekali!** Kamu sudah menghafal {similarity}% dengan benar!")
                    elif similarity >= 60:
                        st.info(f"👍 **Sudah cukup baik.** {similarity}% benar. Tingkatkan lagi!")
                    else:
                        st.warning(f"📚 **Perlu lebih fokus.** Hanya {similarity}% benar. Coba hafalkan lagi.")
                    
                    # Tampilkan kesalahan jika ada
                    if st.session_state.last_hafalan_errors:
                        st.markdown("#### ❌ Kesalahan Fatal:")
                        for error in st.session_state.last_hafalan_errors:
                            st.error(error)
                    
                    if st.session_state.last_hafalan_warnings:
                        st.markdown("#### ⚠️ Peringatan:")
                        for warning in st.session_state.last_hafalan_warnings:
                            st.warning(warning)
                    
                    if st.session_state.last_hafalan_suggestions:
                        st.markdown("#### 💡 Saran:")
                        for suggestion in st.session_state.last_hafalan_suggestions:
                            st.info(suggestion)
                    
                    # Action buttons setelah hasil
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if similarity >= 70:  # Threshold untuk lanjut
                            if current_index < total_segments - 1:
                                if st.button("➡️ Lanjut Bagian Berikutnya", type="primary", use_container_width=True):
                                    # Simpan progress
                                    key = f"{selected_topic}_{current_index}" if st.session_state.hafalan_source != "custom" else f"custom_{current_index}"
                                    if key not in st.session_state.memorized_parts:
                                        st.session_state.memorized_parts[key] = []
                                    st.session_state.memorized_parts[key].append(similarity)
                                    
                                    # Pindah ke segment berikutnya
                                    st.session_state.current_segment_index += 1
                                    st.session_state.hafalan_start_time = time.time()
                                    st.session_state.show_hafalan_editor = False
                                    st.session_state.show_hafalan_results = False
                                    st.session_state.hafalan_timer_start = None
                                    st.session_state.auto_editor_shown = False
                                    st.rerun()
                            else:
                                if st.button("✅ Selesai Hafalan", type="primary", use_container_width=True):
                                    # Simpan progress terakhir
                                    key = f"{selected_topic}_{current_index}" if st.session_state.hafalan_source != "custom" else f"custom_{current_index}"
                                    if key not in st.session_state.memorized_parts:
                                        st.session_state.memorized_parts[key] = []
                                    st.session_state.memorized_parts[key].append(similarity)
                                    
                                    st.success("🎉 **SELESAI!** Semua bagian telah dihafal!")
                                    time.sleep(2)
                                    st.session_state.hafalan_mode = False
                                    st.session_state.hafalan_source_selected = False
                                    st.rerun()
                        else:
                            if st.button("🔄 Ulangi Bagian Ini", use_container_width=True):
                                st.session_state.hafalan_start_time = time.time()
                                st.session_state.show_hafalan_editor = False
                                st.session_state.show_hafalan_results = False
                                st.session_state.hafalan_timer_start = None
                                st.session_state.auto_editor_shown = False
                                st.rerun()
                    
                    with col2:
                        if st.button("🔍 Lihat Perbandingan", use_container_width=True):
                            st.session_state.show_comparison = True
                            st.rerun()
                    
                    with col3:
                        if st.button("🚪 Keluar Mode Hafalan", use_container_width=True):
                            st.session_state.hafalan_mode = False
                            st.session_state.hafalan_source_selected = False
                            st.session_state.show_hafalan_editor = False
                            st.session_state.show_hafalan_results = False
                            st.session_state.hafalan_timer_start = None
                            st.rerun()
                    
                    # Tampilkan perbandingan jika diminta
                    if 'show_comparison' in st.session_state and st.session_state.show_comparison:
                        st.markdown("---")
                        st.markdown("### 🔍 Perbandingan Kode")
                        
                        tab_comp1, tab_comp2, tab_comp3 = st.tabs(["Kode Kamu", "Kode Asli", "Side by Side"])
                        
                        with tab_comp1:
                            st.markdown("**Kode yang kamu tulis:**")
                            st.code(st.session_state.last_user_code, language=code_type)
                        
                        with tab_comp2:
                            st.markdown("**Kode asli yang harusnya:**")
                            st.code(current_segment, language=code_type)
                        
                        with tab_comp3:
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.markdown("**Kode Kamu:**")
                                st.code(st.session_state.last_user_code, language=code_type)
                            with col_b:
                                st.markdown("**Kode Asli:**")
                                st.code(current_segment, language=code_type)
            
            # Navigation untuk pindah segment (jika lebih dari 1)
            if total_segments > 1:
                st.markdown("---")
                st.markdown("#### 🔄 Navigasi Antar Bagian:")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    if current_index > 0:
                        if st.button("⬅️ Sebelumnya", use_container_width=True):
                            st.session_state.current_segment_index -= 1
                            st.session_state.hafalan_start_time = time.time()
                            st.session_state.show_hafalan_editor = False
                            st.session_state.show_hafalan_results = False
                            st.session_state.hafalan_timer_start = None
                            st.rerun()
                
                with col2:
                    if st.button("🔁 Acak", use_container_width=True):
                        new_index = random.randint(0, total_segments - 1)
                        st.session_state.current_segment_index = new_index
                        st.session_state.hafalan_start_time = time.time()
                        st.session_state.show_hafalan_editor = False
                        st.session_state.show_hafalan_results = False
                        st.session_state.hafalan_timer_start = None
                        st.rerun()
                
                with col3:
                    if st.button("📊 Lihat Semua", use_container_width=True):
                        st.session_state.show_all_segments = True
                        st.rerun()
                
                with col4:
                    if st.button("🔄 Reset Progress", type="secondary", use_container_width=True):
                        st.session_state.current_segment_index = 0
                        st.session_state.hafalan_start_time = time.time()
                        st.session_state.show_hafalan_editor = False
                        st.session_state.show_hafalan_results = False
                        st.session_state.hafalan_timer_start = None
                        st.session_state.memorized_parts = {}
                        st.rerun()
                
                # Tampilkan semua segment jika diminta
                if 'show_all_segments' in st.session_state and st.session_state.show_all_segments:
                    st.markdown("---")
                    st.markdown("### 📚 Semua Bagian:")
                    
                    for i, segment in enumerate(segments):
                        with st.expander(f"Bagian {i+1} {'✅' if f'{selected_topic}_{i}' in st.session_state.memorized_parts else '⏳'}", 
                                      expanded=i==current_index):
                            st.code(segment, language=code_type)
                            
                            col_btn1, col_btn2 = st.columns(2)
                            with col_btn1:
                                if st.button(f"Pilih Bagian {i+1}", key=f"select_{i}"):
                                    st.session_state.current_segment_index = i
                                    st.session_state.hafalan_start_time = time.time()
                                    st.session_state.show_hafalan_editor = False
                                    st.session_state.show_hafalan_results = False
                                    st.session_state.show_all_segments = False
                                    st.session_state.hafalan_timer_start = None
                                    st.rerun()
                            with col_btn2:
                                # Tampilkan skor hafalan jika ada
                                key = f"{selected_topic}_{i}" if st.session_state.hafalan_source != "custom" else f"custom_{i}"
                                if key in st.session_state.memorized_parts:
                                    scores = st.session_state.memorized_parts[key]
                                    avg_score = sum(scores) / len(scores)
                                    st.metric("Rata-rata", f"{avg_score:.1f}%")

# =========================
# SIMULASI MODE
# =========================
elif selected_mode == "🎯 Simulasi":
    st.title("🎯 Mode Simulasi USK")
    
    # Simulation settings
    col1, col2, col3 = st.columns(3)
    with col1:
        simulation_time = st.slider("⏱️ Waktu (menit):", 30, 180, 120)
    with col2:
        question_count = st.slider("📝 Jumlah Soal:", 3, 10, 5)
    with col3:
        simulation_mode = st.selectbox("🎯 Mode:", ["Full Code", "Fill in the Blank", "Debugging"])
    
    # Start simulation
    if 'simulation_active' not in st.session_state:
        st.session_state.simulation_active = False
    
    if not st.session_state.simulation_active:
        st.markdown("### 📋 Persiapan Simulasi")
        st.warning("""
        ⚠️ **PERATURAN SIMULASI:**
        
        1. Waktu: **2 jam** (120 menit)
        2. Tidak boleh buka catatan/browser lain
        3. Kerjakan dengan sungguh-sungguh
        4. Submit sebelum waktu habis
        5. Target skor minimal: **70%**
        """)
        
        if st.button("🚀 Mulai Simulasi", type="primary", use_container_width=True):
            st.session_state.simulation_active = True
            st.session_state.simulation_start_time = time.time()
            st.session_state.simulation_questions = random.sample(list(materi.keys()), min(question_count, len(materi)))
            st.session_state.current_question = 0
            st.session_state.simulation_answers = {}
            st.rerun()
    else:
        # Timer
        elapsed = time.time() - st.session_state.simulation_start_time
        remaining = max(0, simulation_time * 60 - elapsed)
        
        minutes = int(remaining // 60)
        seconds = int(remaining % 60)
        
        # Timer display dengan auto refresh
        timer_placeholder = st.empty()
        with timer_placeholder.container():
            col_time1, col_time2, col_time3 = st.columns(3)
            with col_time1:
                st.metric("⏱️ Waktu Tersisa", f"{minutes:02d}:{seconds:02d}")
            with col_time2:
                current_q = st.session_state.current_question + 1
                total_q = len(st.session_state.simulation_questions)
                st.metric("📝 Soal", f"{current_q}/{total_q}")
            with col_time3:
                progress = elapsed / (simulation_time * 60)
                st.metric("📊 Progress", f"{int(progress*100)}%")
            
            st.progress(min(1.0, progress))
        
        # Auto refresh timer setiap detik
        if remaining > 0:
            time.sleep(1)
            st.rerun()
        else:
            st.error("⏰ WAKTU HABIS! Simulasi berakhir.")
            st.session_state.simulation_active = False
            st.rerun()
        
        # Current question
        current_q = st.session_state.current_question
        total_q = len(st.session_state.simulation_questions)
        topic = st.session_state.simulation_questions[current_q]
        topic_data = materi[topic]
        
        st.markdown(f"### 📝 Soal {current_q + 1} dari {total_q}")
        st.markdown(f"**{topic}**")
        st.markdown(f"*{topic_data['deskripsi']}*")
        
        # Question based on mode
        if simulation_mode == "Full Code":
            st.markdown("**Tugas:** Tulis kode lengkap untuk implementasi di atas.")
            answer = st.text_area(
                "Tulis kode kamu:",
                height=300,
                placeholder="Tulis kode lengkap di sini...\nTips: Fokus pada bagian kritis seperti session_start(), WHERE clause, dll.",
                key=f"simulation_q_{current_q}"
            )
        
        elif simulation_mode == "Fill in the Blank":
            # Create fill in the blank question
            code_lines = topic_data["kode"].split('\n')
            # Pilih baris yang penting untuk di-blank
            important_lines = []
            for i, line in enumerate(code_lines):
                if any(keyword in line for keyword in ["session_start", "include", "require", "SELECT", "INSERT", "UPDATE", "DELETE", "WHERE", "header", "exit"]):
                    important_lines.append(i)
            
            if len(important_lines) > 5:
                blank_lines = random.sample(important_lines, 5)
            else:
                blank_lines = important_lines
            
            display_code = ""
            line_numbers = []
            line_num = 1
            for i, line in enumerate(code_lines):
                if i in blank_lines:
                    display_code += f"{line_num}. _______\n"
                    line_numbers.append(line_num)
                else:
                    display_code += f"{line_num}. {line}\n"
                line_num += 1
            
            st.code(display_code, language=topic_data["tipe"])
            st.markdown("**Tugas:** Isi bagian yang kosong dengan kode yang tepat.")
            answer = st.text_area(
                "Jawaban (sebutkan nomor baris dan kodenya):",
                height=150,
                placeholder=f"Contoh:\n{line_numbers[0] if line_numbers else 1}. session_start();\n{line_numbers[1] if len(line_numbers) > 1 else 2}. require 'koneksi.php';",
                key=f"simulation_q_{current_q}"
            )
        
        elif simulation_mode == "Debugging":
            # Create buggy code
            original_code = topic_data["kode"]
            buggy_code = original_code
            
            # Introduce common bugs
            bugs_introduced = []
            if "session_start()" in original_code:
                buggy_code = buggy_code.replace("session_start()", "// session_start() // TODO: Uncomment this")
                bugs_introduced.append("session_start() di-comment")
            
            if "WHERE" in original_code:
                lines = buggy_code.split('\n')
                for i, line in enumerate(lines):
                    if "WHERE" in line and ("UPDATE" in line or "DELETE" in line):
                        lines[i] = line.replace("WHERE", "// WHERE")
                        bugs_introduced.append("WHERE clause di-comment")
                buggy_code = '\n'.join(lines)
            
            if "exit" in original_code:
                lines = buggy_code.split('\n')
                for i, line in enumerate(lines):
                    if "header(" in line and "exit" not in line and "die" not in line:
                        lines[i] = line + " // TODO: Add exit() here"
                        bugs_introduced.append("exit() tidak ada setelah header()")
                buggy_code = '\n'.join(lines)
            
            st.code(buggy_code, language=topic_data["tipe"])
            st.markdown("**Tugas:** Temukan dan perbaiki kesalahan dalam kode di atas.")
            answer = st.text_area(
                "Sebutkan kesalahan dan perbaikannya:",
                height=200,
                placeholder="Format:\n1. Baris X: [Kesalahan] → [Perbaikan]\n2. Baris Y: [Kesalahan] → [Perbaikan]\n\nContoh:\n1. Baris 2: session_start() di-comment → Hapus comment\n2. Baris 10: WHERE hilang → Tambahkan WHERE clause",
                key=f"simulation_q_{current_q}"
            )
        
        # Save answer
        st.session_state.simulation_answers[current_q] = answer
        
        # Navigation buttons
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            if current_q > 0:
                if st.button("⬅️ Soal Sebelumnya", use_container_width=True):
                    st.session_state.current_question -= 1
                    st.rerun()
        
        with col2:
            if current_q < total_q - 1:
                if st.button("Soal Berikutnya ➡️", type="primary", use_container_width=True):
                    st.session_state.current_question += 1
                    st.rerun()
            else:
                if st.button("✅ Submit Semua Jawaban", type="primary", use_container_width=True):
                    # Calculate score
                    total_score = 0
                    score_details = []
                    
                    for i in range(total_q):
                        topic = st.session_state.simulation_questions[i]
                        user_answer = st.session_state.simulation_answers.get(i, "")
                        correct_code = materi[topic]["kode"]
                        
                        if simulation_mode == "Full Code":
                            similarity = calculate_similarity(user_answer, correct_code)
                            total_score += similarity
                            score_details.append({
                                "topic": topic,
                                "score": similarity,
                                "type": "full_code"
                            })
                        
                        elif simulation_mode == "Fill in the Blank":
                            # Simple check for fill in the blank
                            critical_found = 0
                            for part in materi[topic]["critical_parts"]:
                                if part.lower() in user_answer.lower():
                                    critical_found += 1
                            
                            if materi[topic]["critical_parts"]:
                                score_percent = (critical_found / len(materi[topic]["critical_parts"])) * 100
                            else:
                                score_percent = 0
                            
                            total_score += score_percent
                            score_details.append({
                                "topic": topic,
                                "score": score_percent,
                                "critical_found": critical_found,
                                "total_critical": len(materi[topic]["critical_parts"]),
                                "type": "fill_blank"
                            })
                        
                        elif simulation_mode == "Debugging":
                            # Count bugs found (simple version)
                            bugs_found = 0
                            common_bugs = ["session_start", "WHERE", "exit()", "header()", "require", "include"]
                            for bug in common_bugs:
                                if bug in user_answer:
                                    bugs_found += 1
                            
                            score_percent = min(100, bugs_found * 25)  # Max 4 bugs = 100%
                            total_score += score_percent
                            score_details.append({
                                "topic": topic,
                                "score": score_percent,
                                "bugs_found": bugs_found,
                                "type": "debugging"
                            })
                    
                    avg_score = total_score / total_q if total_q > 0 else 0
                    
                    # Save simulation result
                    st.session_state.quiz_scores.append({
                        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "mode": simulation_mode,
                        "score": avg_score,
                        "questions": total_q,
                        "details": score_details
                    })
                    
                    st.session_state.simulation_active = False
                    st.session_state.show_simulation_results = True
                    st.session_state.last_simulation_score = avg_score
                    st.session_state.last_simulation_details = score_details
                    st.rerun()
        
        with col3:
            if st.button("⏹️ Akhiri Simulasi", use_container_width=True):
                st.session_state.simulation_active = False
                st.warning("Simulasi diakhiri. Hasil tidak disimpan.")
                st.rerun()
    
    # Show results if available
    if 'show_simulation_results' in st.session_state and st.session_state.show_simulation_results:
        st.markdown("---")
        st.markdown("## 📊 HASIL SIMULASI USK")
        
        score = st.session_state.last_simulation_score
        details = st.session_state.last_simulation_details
        
        # Score card
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Skor Akhir", f"{score:.1f}%")
        with col2:
            if score >= 85:
                grade = "A"
                color = "green"
            elif score >= 70:
                grade = "B"
                color = "blue"
            elif score >= 60:
                grade = "C"
                color = "orange"
            else:
                grade = "D"
                color = "red"
            st.metric("Grade", grade)
        with col3:
            st.metric("Mode", simulation_mode)
        
        # Progress bar dengan warna
        if score >= 85:
            st.success(f"🎉 **LUAR BIASA!** Skor: {score:.1f}%")
            st.progress(score/100)
        elif score >= 70:
            st.info(f"👍 **BAIK!** Skor: {score:.1f}%")
            st.progress(score/100)
        elif score >= 60:
            st.warning(f"⚠️ **CUKUP!** Skor: {score:.1f}%")
            st.progress(score/100)
        else:
            st.error(f"❌ **PERLU BELAJAR LAGI!** Skor: {score:.1f}%")
            st.progress(score/100)
        
        # Detail per soal
        st.markdown("### 📝 Detail Per Soal:")
        for i, detail in enumerate(details):
            with st.expander(f"Soal {i+1}: {detail['topic']} - {detail['score']:.1f}%"):
                if detail['type'] == 'fill_blank':
                    st.write(f"Bagian kritis ditemukan: {detail.get('critical_found', 0)}/{detail.get('total_critical', 0)}")
                elif detail['type'] == 'debugging':
                    st.write(f"Bug ditemukan: {detail.get('bugs_found', 0)}")
        
        # Recommendations
        st.markdown("### 🎯 Rekomendasi:")
        if score >= 85:
            st.success("""
            **Excellent!** Kamu sudah siap menghadapi USK!
            1. Pertahankan konsistensi belajar
            2. Coba simulasi dengan waktu lebih ketat
            3. Review materi yang sudah dikuasai untuk pemahaman lebih dalam
            """)
        elif score >= 70:
            st.info("""
            **Good job!** Hampir siap!
            1. Fokus pada materi dengan skor terendah
            2. Latihan lebih banyak di mode Praktek
            3. Perbaiki detail kecil yang masih kurang
            """)
        elif score >= 60:
            st.warning("""
            **Perlu peningkatan!**
            1. Pelajari lagi materi dasar (Session, CRUD)
            2. Fokus pada bagian kritis yang sering keluar
            3. Perbanyak latihan dengan timer
            """)
        else:
            st.error("""
            **Perlu belajar intensif!**
            1. Kembali ke mode Belajar untuk review fundamental
            2. Fokus pada satu materi sampai paham
            3. Gunakan mode Praktek dengan petunjuk aktif
            4. Jangan terburu-buru, pahami konsep dulu
            """)
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Coba Simulasi Lagi", type="primary", use_container_width=True):
                st.session_state.show_simulation_results = False
                st.session_state.simulation_active = False
                st.rerun()
        with col2:
            if st.button("📊 Lihat Progress", use_container_width=True):
                st.session_state.current_mode = "📊 Progress"
                st.rerun()

# =========================
# PROGRESS MODE
# =========================
elif selected_mode == "📊 Progress":
    st.title("📊 Progress Belajar")
    
    if not st.session_state.practice_scores and not st.session_state.quiz_scores and not st.session_state.memorized_parts and not st.session_state.user_custom_codes:
        st.info("📭 Belum ada data progress. Mulai latihan atau simulasi terlebih dahulu!")
        
        # Quick start buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("✏️ Mulai Latihan", type="primary", use_container_width=True):
                st.session_state.current_mode = "✏️ Praktek"
                st.rerun()
        with col2:
            if st.button("🧠 Buat Hafalan", use_container_width=True):
                st.session_state.current_mode = "✏️ Praktek"
                st.session_state.hafalan_mode = True
                st.rerun()
        with col3:
            if st.button("🎯 Coba Simulasi", use_container_width=True):
                st.session_state.current_mode = "🎯 Simulasi"
                st.rerun()
    else:
        # Overall statistics
        st.markdown("### 📈 Statistik Keseluruhan")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_practices = sum(len(scores) for scores in st.session_state.practice_scores.values())
            st.metric("Total Praktek", total_practices)
        
        with col2:
            total_simulations = len(st.session_state.quiz_scores)
            st.metric("Total Simulasi", total_simulations)
        
        with col3:
            total_memorized = len(st.session_state.memorized_parts)
            st.metric("Bagian Dihafal", total_memorized)
        
        with col4:
            total_custom = sum(len(codes) for codes in st.session_state.user_custom_codes.values())
            st.metric("Kode Custom", total_custom)
        
        # Progress Custom Codes
        if st.session_state.user_custom_codes:
            st.markdown("---")
            st.markdown("### 📝 Kode Custom Kamu")
            
            for category, codes in st.session_state.user_custom_codes.items():
                with st.expander(f"{category} ({len(codes)} kode)", expanded=False):
                    for i, code in enumerate(codes):
                        st.markdown(f"**Kode {i+1}:**")
                        st.code(code[:300] + "..." if len(code) > 300 else code, language="text")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button(f"🧠 Hafalkan {i+1}", key=f"memorize_custom_{category}_{i}"):
                                st.session_state.custom_code_to_memorize = code
                                st.session_state.hafalan_mode = True
                                st.session_state.current_mode = "✏️ Praktek"
                                st.session_state.hafalan_source = "custom"
                                st.session_state.hafalan_source_selected = True
                                st.rerun()
                        with col2:
                            if st.button(f"🗑️ Hapus {i+1}", key=f"delete_custom_{category}_{i}"):
                                st.session_state.user_custom_codes[category].pop(i)
                                if not st.session_state.user_custom_codes[category]:
                                    del st.session_state.user_custom_codes[category]
                                st.rerun()
        
        # Progress hafalan
        if st.session_state.memorized_parts:
            st.markdown("---")
            st.markdown("### 🧠 Progress Hafalan")
            
            # Kelompokkan berdasarkan materi
            material_groups = {}
            for key, scores in st.session_state.memorized_parts.items():
                if "_" in key:
                    material_name = key.split("_")[0]
                    if material_name not in material_groups:
                        material_groups[material_name] = []
                    material_groups[material_name].extend(scores)
                else:
                    if "Custom" not in material_groups:
                        material_groups["Custom"] = []
                    material_groups["Custom"].extend(scores)
            
            for material, scores in material_groups.items():
                with st.expander(f"{material} ({len(scores)} bagian)", expanded=False):
                    if scores:
                        avg_score = sum(scores) / len(scores)
                        best_score = max(scores)
                        last_score = scores[-1]
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Rata-rata", f"{avg_score:.1f}%")
                        with col2:
                            st.metric("Terbaik", f"{best_score:.1f}%")
                        with col3:
                            st.metric("Terakhir", f"{last_score:.1f}%")
                    
                    # Button untuk lanjut hafalan
                    if material != "Custom":
                        if st.button(f"🧠 Lanjut Hafalan {material}", key=f"continue_{material}", use_container_width=True):
                            st.session_state.current_mode = "✏️ Praktek"
                            st.session_state.hafalan_mode = True
                            st.session_state.hafalan_source = "auto_material"
                            st.session_state.hafalan_source_selected = True
                            st.rerun()
        
        # Practice progress per topic
        if st.session_state.practice_scores:
            st.markdown("---")
            st.markdown("### 📊 Progress per Materi")
            
            for topic, scores in st.session_state.practice_scores.items():
                with st.expander(f"{topic} ({len(scores)}x praktek)", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        avg_score = sum(scores) / len(scores)
                        st.metric("Rata-rata", f"{avg_score:.1f}%")
                    with col2:
                        best_score = max(scores)
                        st.metric("Terbaik", f"{best_score:.1f}%")
                    with col3:
                        last_score = scores[-1]
                        st.metric("Terakhir", f"{last_score:.1f}%")
                    
                    # Improvement
                    if len(scores) > 1:
                        improvement = scores[-1] - scores[0]
                        if improvement > 0:
                            st.success(f"📈 Peningkatan: +{improvement:.1f}%")
                        elif improvement < 0:
                            st.warning(f"📉 Penurunan: {improvement:.1f}%")
                        else:
                            st.info("➡️ Stabil")
                    
                    # Quick actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"✏️ Latihan {topic}", key=f"practice_{topic}", use_container_width=True):
                            st.session_state.current_mode = "✏️ Praktek"
                            st.session_state.hafalan_mode = False
                            st.session_state.selected_topic = topic
                            st.rerun()
                    with col2:
                        if st.button(f"🧠 Hafalan {topic}", key=f"memorize_{topic}", use_container_width=True):
                            st.session_state.current_mode = "✏️ Praktek"
                            st.session_state.hafalan_mode = True
                            st.session_state.hafalan_source = "auto_material"
                            st.session_state.hafalan_source_selected = True
                            st.session_state.selected_topic = topic
                            st.rerun()
        
        # Simulation history
        if st.session_state.quiz_scores:
            st.markdown("---")
            st.markdown("### 📝 Riwayat Simulasi")
            
            for i, sim in enumerate(reversed(st.session_state.quiz_scores[-5:])):  # Tampilkan 5 terakhir
                with st.expander(f"Simulasi {len(st.session_state.quiz_scores)-i}: {sim['date']} - {sim['score']:.1f}%", expanded=False):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Skor", f"{sim['score']:.1f}%")
                    with col2:
                        st.metric("Mode", sim['mode'])
                    with col3:
                        st.metric("Soal", sim['questions'])
        
        # Reset button
        st.markdown("---")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Reset Semua Progress", type="secondary", use_container_width=True):
                st.session_state.practice_scores = {}
                st.session_state.quiz_scores = []
                st.session_state.last_viewed = []
                st.session_state.memorized_parts = {}
                st.session_state.user_custom_codes = {}
                st.success("Semua progress telah direset!")
                st.rerun()
        with col2:
            if st.button("💾 Export Progress", use_container_width=True):
                # Create summary
                summary = {
                    "total_practice": sum(len(scores) for scores in st.session_state.practice_scores.values()),
                    "total_simulations": len(st.session_state.quiz_scores),
                    "total_memorized_parts": len(st.session_state.memorized_parts),
                    "total_custom_codes": sum(len(codes) for codes in st.session_state.user_custom_codes.values()),
                    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.json(summary)
                st.success("Progress berhasil diexport!")

# =========================
# QUIZ MODE
# =========================
elif selected_mode == "❓ Quiz":
    st.title("❓ Quick Quiz - Test Pemahaman")
    
    # Quiz questions database (updated with new topics)
    quiz_db = [
        {
            "question": "Di mana session_start() harus diletakkan dalam script PHP?",
            "options": [
                "Di awal script, sebelum output apapun",
                "Di akhir script, sebelum ?>",
                "Di tengah script, setelah include",
                "Di mana saja, tidak masalah"
            ],
            "answer": 0,
            "category": "PHP Session",
            "explanation": "session_start() HARUS dipanggil sebelum output apapun (termasuk spasi atau newline) ke browser."
        },
        {
            "question": "Apa perbedaan antara require dan include di PHP?",
            "options": [
                "require menghasilkan fatal error jika file tidak ditemukan, include hanya warning",
                "include menghasilkan fatal error, require hanya warning",
                "Tidak ada perbedaan",
                "require untuk CSS, include untuk PHP"
            ],
            "answer": 0,
            "category": "PHP Include",
            "explanation": "require akan menghentikan eksekusi script jika file tidak ditemukan, sedangkan include hanya memberikan warning."
        },
        {
            "question": "Apa yang terjadi jika UPDATE query tidak menggunakan WHERE clause?",
            "options": [
                "Hanya data pertama yang terupdate",
                "Semua data dalam tabel akan terupdate",
                "Akan terjadi error",
                "Tidak ada yang terjadi"
            ],
            "answer": 1,
            "category": "SQL",
            "explanation": "UPDATE tanpa WHERE akan mengubah SEMUA baris dalam tabel! Sangat berbahaya."
        },
        {
            "question": "Bagaimana cara membuat filter multiple dengan PHP?",
            "options": [
                "Gunakan $_GET dengan parameter berbeda untuk setiap filter",
                "Hanya bisa satu filter dalam satu waktu",
                "Harus menggunakan JavaScript",
                "Tidak bisa membuat multiple filter"
            ],
            "answer": 0,
            "category": "PHP Filter",
            "explanation": "Gunakan $_GET['category'], $_GET['status'], dll, lalu gabungkan dalam WHERE clause dengan AND."
        },
        {
            "question": "Apa fungsi dari md5() dalam proses pendaftaran?",
            "options": [
                "Mengenkripsi password menjadi hash",
                "Mengkompres data user",
                "Validasi format email",
                "Membersihkan input dari SQL injection"
            ],
            "answer": 0,
            "category": "PHP Security",
            "explanation": "md5() membuat hash dari password untuk disimpan di database (lebih baik gunakan password_hash())."
        },
        {
            "question": "Bagaimana cara membuat sistem favorit tanpa database?",
            "options": [
                "Menggunakan $_SESSION untuk menyimpan status favorit",
                "Tidak bisa tanpa database",
                "Menggunakan cookies",
                "Menggunakan file text"
            ],
            "answer": 0,
            "category": "PHP Session",
            "explanation": "$_SESSION bisa digunakan untuk menyimpan data sementara seperti status favorit."
        },
        {
            "question": "Apa keuntungan menggunakan HTML5 input type='email'?",
            "options": [
                "Validasi format email otomatis di browser",
                "Membuat tampilan lebih menarik",
                "Mempercepat loading halaman",
                "Mencegah SQL injection"
            ],
            "answer": 0,
            "category": "HTML Forms",
            "explanation": "type='email' memberikan validasi client-side otomatis untuk format email."
        },
        {
            "question": "Apa yang harus dilakukan setelah header('location: ...')?",
            "options": [
                "Tidak perlu apa-apa",
                "Panggil exit() atau die()",
                "Tunggu 5 detik",
                "Echo pesan sukses"
            ],
            "answer": 1,
            "category": "PHP Redirect",
            "explanation": "exit() atau die() diperlukan untuk menghentikan eksekusi script setelah redirect."
        },
        {
            "question": "Bagaimana cara membuat responsive grid layout dengan CSS?",
            "options": [
                "display: grid dengan grid-template-columns: repeat(auto-fill, minmax())",
                "display: block dengan width: 100%",
                "table layout dengan colspan",
                "position: absolute dengan media queries"
            ],
            "answer": 0,
            "category": "CSS Layout",
            "explanation": "CSS Grid dengan auto-fill dan minmax() membuat layout yang responsive otomatis."
        },
        {
            "question": "Apa fungsi dari LEFT JOIN dalam SQL?",
            "options": [
                "Mengambil semua data dari tabel kiri meski tidak ada match di tabel kanan",
                "Hanya mengambil data yang ada di kedua tabel",
                "Mengurutkan data dari kiri ke kanan",
                "Menggabungkan tabel secara vertikal"
            ],
            "answer": 0,
            "category": "SQL",
            "explanation": "LEFT JOIN mengambil semua records dari tabel kiri (todo), meski tidak ada matching records di tabel kanan (category)."
        }
    ]
    
    # Quiz settings
    col1, col2 = st.columns(2)
    with col1:
        quiz_count = st.slider("Jumlah soal:", 3, len(quiz_db), 5)
    with col2:
        selected_category = st.selectbox(
            "Kategori:",
            ["Semua"] + list(set([q["category"] for q in quiz_db]))
        )
    
    # Filter questions
    if selected_category == "Semua":
        quiz_questions = random.sample(quiz_db, min(quiz_count, len(quiz_db)))
    else:
        filtered = [q for q in quiz_db if q["category"] == selected_category]
        quiz_questions = random.sample(filtered, min(quiz_count, len(filtered)))
    
    # Initialize quiz state
    if 'quiz_answers' not in st.session_state:
        st.session_state.quiz_answers = {}
    if 'quiz_submitted' not in st.session_state:
        st.session_state.quiz_submitted = False
    
    # Display questions
    for i, q in enumerate(quiz_questions):
        st.markdown(f"**{i+1}. {q['question']}**")
        st.caption(f"Kategori: {q['category']}")
        
        answer_key = f"q_{i}"
        if answer_key not in st.session_state.quiz_answers:
            st.session_state.quiz_answers[answer_key] = None
        
        selected = st.radio(
            "Pilih jawaban:",
            q['options'],
            key=answer_key,
            index=st.session_state.quiz_answers[answer_key] if st.session_state.quiz_answers[answer_key] is not None else 0,
            disabled=st.session_state.quiz_submitted
        )
        
        st.session_state.quiz_answers[answer_key] = q['options'].index(selected)
        
        st.markdown("---")
    
    # Submit button
    if not st.session_state.quiz_submitted:
        if st.button("✅ Submit Jawaban", type="primary", use_container_width=True):
            st.session_state.quiz_submitted = True
            st.rerun()
    else:
        # Calculate score
        correct = 0
        total = len(quiz_questions)
        
        for i, q in enumerate(quiz_questions):
            answer_key = f"q_{i}"
            user_answer = st.session_state.quiz_answers.get(answer_key)
            
            if user_answer == q['answer']:
                correct += 1
        
        score = (correct / total) * 100
        
        # Save quiz result
        st.session_state.quiz_scores.append({
            "date": datetime.now().strftime("%H:%M"),
            "score": score,
            "total": total,
            "correct": correct,
            "type": "quiz"
        })
        
        # Display results
        st.markdown(f"## 📊 Hasil Quiz: {score:.1f}% ({correct}/{total})")
        
        # Progress bar
        if score == 100:
            st.success("🎉 **PERFECT SCORE!** Kamu menguasai semua materi!")
            st.balloons()
            st.progress(score/100)
        elif score >= 80:
            st.success(f"👍 **EXCELLENT!** Pemahaman kamu sangat baik!")
            st.progress(score/100)
        elif score >= 60:
            st.info(f"💪 **GOOD!** Sudah cukup baik, bisa ditingkatkan lagi.")
            st.progress(score/100)
        else:
            st.warning(f"📚 **NEED STUDY!** Pelajari lagi materinya ya.")
            st.progress(score/100)
        
        # Show correct answers
        st.markdown("### 📝 Pembahasan:")
        for i, q in enumerate(quiz_questions):
            answer_key = f"q_{i}"
            user_answer = st.session_state.quiz_answers.get(answer_key)
            
            with st.expander(f"Soal {i+1}: {q['question']}", expanded=False):
                if user_answer == q['answer']:
                    st.success(f"✅ Jawaban kamu benar!")
                else:
                    st.error(f"❌ Jawaban kamu: {q['options'][user_answer] if user_answer is not None else 'Tidak dijawab'}")
                    st.success(f"✅ Jawaban benar: {q['options'][q['answer']]}")
                
                st.info(f"**Penjelasan:** {q['explanation']}")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Coba Quiz Lagi", type="primary", use_container_width=True):
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.rerun()
        with col2:
            if st.button("📚 Kembali Belajar", use_container_width=True):
                st.session_state.current_mode = "📖 Belajar"
                st.rerun()

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>📚 <b>PerpusCode USK - All-in-One Learning Platform</b> | Versi 3.0</p>
    <p>📖 <b>Materi Baru:</b> Index Page Filter & Favorit • Form Daftar • Halaman Profil • CSS Full Project</p>
    <p>🧠 <b>Fitur Enhanced:</b> Timer Otomatis • Auto Refresh • Perbaikan Bug • UI/UX Lebih Baik</p>
    <p>💪 <b>Siap USK:</b> Learn • Practice • Memorize • Simulate • Track • Quiz</p>
</div>
""", unsafe_allow_html=True)