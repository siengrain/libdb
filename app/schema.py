instructions = [
    'DROP TABLE IF EXISTS user;',
    'DROP TABLE IF EXISTS books;',
    'SET FOREIGN_KEY_CHECKS=1;',
    """
        CREATE TABLE user (
            id INT PRIMARY KEY AUTO_INCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL
        ) 
    """,
    """
        CREATE TABLE books (
            id INT PRIMARY KEY AUTO_INCREMENT,
            created_by INT NOT NULL,
            book TEXT NOT NULL,
            author TEXT NOT NULL,
            completed BOOLEAN NOT NULL,
            FOREIGN KEY (created_by) REFERENCES user(id)
        );
    """
]
