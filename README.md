requirements:
    - Python 3.8.10
    - mysql :
        user : root
        pass : (empty)
        ip : localhost:3306
        DB : library
    * note : disini pakai WINDOWS

langkah - langkah :
eksekusi query berikut untuk create database terlebih dahulu
"
CREATE DATABASE IF NOT EXISTS library;

USE library;

CREATE TABLE IF NOT EXISTS authors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bio TEXT,
    birth_date DATE
);

CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    publish_date DATE,
    author_id INT,
    FOREIGN KEY (author_id) REFERENCES authors(id) ON DELETE CASCADE
);

-- Mengatur auto_increment untuk authors
ALTER TABLE authors AUTO_INCREMENT = 1;

-- Mengatur auto_increment untuk books
ALTER TABLE books AUTO_INCREMENT = 1;
"

guankan VSCode untuk menjalankan aplikasi:
1. buka aplikasi di VSCoode. dan pastikan python anda sudah berjalan dengan normal
2. jalankan di terminal perintah "pip install -r .\requirements.txt". untuk install library yang dibutuhkan
3. buka file 'service/config.py', sesuaikan user, password dll sesuai dengan database anda
4. klik run -> run without debugging. pastikan saat runniing file yang di buka di app.py, dan juga port 8083 belum terpakai
5. setelah running anda bisa coba di postman dengan URL http://{ip anda}:8083/.... atau http://localhost:8083/....
6. untuk URL API bisa cek di file app.py
7. untuk auto testing pakai 'pytest':
    - pertama install pytest 'pip install pytest'
    - masuk directory project. lalu masuk ke terminal, jalankan file test_app.py dengan perintah 'pytest .\test_app.py'
8. untuk test di postman pakai URL http://{ip anda}:8083/.... atau http://localhost:8083/....
    --------------------------------------- author ------------------------------------------
    - get all authors           -> 'GET' /service/library/authors
    - get spesific authors      -> 'GET' /service/library/authors/<authorsId>
    - post new author           -> 'POST' /service/library/authors
        contoh format payload yg dikirim :
            {"name":"jhonny","bio":"biography2","birth_date":"2022-02-02"}
    - put author                -> 'PUT' /service/library/authors/update
        contoh format payload yg dikirim :
            {"id":20,"name":"jhonny","bio":"biography2","birth_date":"2022-02-02"}
    - delete author             -> 'DELETE' /service/library/authors/delete/<id>

    --------------------------------------- book ------------------------------------------
    - get all books             -> 'GET' /service/library/books
    - get spesific book         -> 'GET' /service/library/books/<bookId>
    - post new book             -> 'POST' /service/library/books
        contoh format payload yg dikirim :
            {"title":"test3","description":"desc","publish_date":"2024-02-05","author_id":19}
    - put book                  -> 'PUT' /service/library/books/update
        contoh format payload yg dikirim :
            {"id":22,"title":"test3","description":"desc","publish_date":"2024-02-05","author_id":19}
    - delete book               -> 'DELETE' /service/library/books/delete/<id>

    -------------------------------------- Utility ----------------------------------------
    - get all author with all reference book -> /service/library/all/data
9. contoh sedikit list data author dan book. eksekusi query berikut :
"
INSERT INTO authors (name, bio, birth_date) VALUES
('J.K. Rowling', 'British author, best known for the Harry Potter series', '1965-07-31'),
('George R.R. Martin', 'American novelist and short story writer in the fantasy, horror, and science fiction genres', '1948-09-20'),
('J.R.R. Tolkien', 'English writer, poet, philologist, and academic, best known for The Lord of the Rings', '1892-01-03'),
('Agatha Christie', 'English writer known for her sixty-six detective novels and fourteen short story collections', '1890-09-15'),
('Stephen King', 'American author of horror, supernatural fiction, suspense, and fantasy novels', '1947-09-21');


INSERT INTO books (title, description, publish_date, author_id) VALUES
('Harry Potter and the Philosopher\'s Stone', 'The first novel in the Harry Potter series and J.K. Rowling\'s debut novel', '1997-06-26', 1),
('Harry Potter and the Chamber of Secrets', 'The second novel in the Harry Potter series written by J.K. Rowling', '1998-07-02', 1),
('A Game of Thrones', 'The first book in A Song of Ice and Fire, a series of fantasy novels by American author George R.R. Martin', '1996-08-06', 2),
('A Clash of Kings', 'The second novel in A Song of Ice and Fire, a series of fantasy novels by George R.R. Martin', '1998-11-16', 2),
('The Hobbit', 'A children\'s fantasy novel by English author J.R.R. Tolkien', '1937-09-21', 3),
('The Fellowship of the Ring', 'The first of three volumes of the epic novel The Lord of the Rings by J.R.R. Tolkien', '1954-07-29', 3),
('Murder on the Orient Express', 'A detective novel by British writer Agatha Christie featuring the Belgian detective Hercule Poirot', '1934-01-01', 4),
('The Murder of Roger Ackroyd', 'A work of detective fiction by Agatha Christie, first published in June 1926', '1926-06-01', 4),
('The Shining', 'A horror novel by American author Stephen King', '1977-01-28', 5),
('It', 'A horror novel by American author Stephen King', '1986-09-15', 5);
"

* jika ada kendala atau permasalahan ataupun penjjelasan yang kurang jelas bisa hubungi developer