from .router import router
from fastapi import Response

@router.get("/", tags=["ws"], response_class=Response)
async def get_html():
    html_content = """
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WebSocket Test</title>
        <style>
            body {
                font-family: Arial, sans-serif;
            }
            #authors {
                margin-top: 20px;
            }
        </style>
    </head>
    <body>
        <h1>Тестирование WebSocket</h1>
        <h2>Список авторов:</h2>
        <div id="authors"></div>

        <h2>Добавить автора:</h2>
        <input type="text" id="authorName" placeholder="Имя автора" />
        <button id="addAuthorButton">Добавить</button>

        <script>
            const authorsDiv = document.getElementById('authors');
            const authorNameInput = document.getElementById('authorName');
            const addAuthorButton = document.getElementById('addAuthorButton');
            
            // Подключение к WebSocket
            const socket = new WebSocket('ws://localhost:8000/ws/authors');

            // Обработка сообщения от сервера
            socket.onmessage = function(event) {
                const authors = JSON.parse(event.data);
                updateAuthorsList(authors);
            };

            // Функция для обновления списка авторов
            function updateAuthorsList(authors) {
                authorsDiv.innerHTML = ''; // Очищаем предыдущий список
                authors.forEach(author => {
                    const authorElement = document.createElement('div');
                    authorElement.textContent = `ID: ${author.id}, Имя: ${author.name}`;
                    authorsDiv.appendChild(authorElement);
                });
            }

                // Обработка нажатия кнопки добавления автора
                addAuthorButton.onclick = function() {
                    const name = authorNameInput.value;
                    if (!name) return;

                    // Отправляем имя автора через WebSocket
                    const authorData = { name: name };
                    socket.send(JSON.stringify(authorData));

                    // Очищаем поле ввода после добавления
                    authorNameInput.value = '';
            };
        </script>
    </body>
    </html>
    """
    return Response(content=html_content, media_type="text/html")