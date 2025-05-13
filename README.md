<div align="center">
  <h1>GlitchMe! 🔀</h1>
  <p>Настольная «хардкорная» социальная игра с REST-API, реактивным фронтендом и Telegram-ботом.</p>
  <!-- Badges -->
  [![Python](https://img.shields.io/badge/python-3.13-blue)](https://www.python.org/)
  [![FastAPI](https://img.shields.io/badge/fastapi-vX.X-success)](https://fastapi.tiangolo.com/)
  [![Flet](https://img.shields.io/badge/flet-0.28-purple)](https://flet.dev/)
  [![Aiogram3](https://img.shields.io/badge/aiogram-3.x-green)](https://docs.aiogram.dev/)
  [![License: MIT](https://img.shields.io/github/license/your-org/glitchme)](LICENSE)
</div>

---

## 📖 Описание

GlitchMe! — это уникальная комбинация **настольной игры** и **компьютерного интерфейса**:
- **FastAPI**-бекенд на Python 3.13 с полностью модульной архитектурой  
- **Flet**-фронтенд (веб-интерфейс) на версии 0.28  
- **Aiogram 3** Telegram-бот для удобного подключения и взаимодействия  
- Поддержка **неограниченного** числа параллельных матчей и игроков

---

## 🚀 Установка и запуск

1. Клонируйте репозиторий  
   ```bash
   git clone https://github.com/your-org/glitchme.git
   cd glitchme
````

2. Создайте и активируйте виртуальное окружение

   ```bash
   python3.13 -m venv venv
   source venv/bin/activate
   ```
3. Установите зависимости

   ```bash
   pip install -r requirements.txt
   ```
4. Запустите бекенд

   ```bash
   uvicorn app.main:app --reload
   ```
5. Запустите фронтенд

   ```bash
   python -m your_frontend.main
   ```
6. Запустите Telegram-бот

   ```bash
   python -m your_bot.main
   ```

---

## 🛠 Killer-фичи

* **Модульная архитектура** — механика в REST-API, клиенты (Flet, бот) только отображают и отправляют данные
* **Мгновенная регистрация** — скан QR + 1 клик в боте или UI
* **Конфигурируемость** — неограниченное число тем/заданий, авто-подбор вопросов в каждом раунде
* **Реактивный интерфейс** — Flet-сайт обновляется в реальном времени без перезагрузки

---

## 🎮 Механика игры

1. **Подготовка:**

   * Администратор создаёт игру (`POST /game/create` → QR + метаданные)
   * Игроки подключаются (`PATCH /game/connect/{id}`)
2. **Раунды:** N раундов, в каждом:

   1. **Начало:** рассылка заданий с учётом роли «Глюка»
   2. **Обсуждение:** опросы игроков (каждый не более 1 раза)
   3. **Голосование:** исключение наиболее подозрительного (секретный алгоритм при «ничье»)
3. **Завершение:** выжившие побеждают или побеждает Глюк после последнего раунда

---

## 📚 Конфигурация

Все темы и задания настраиваются в файле `config.py` в словаре `ROUNDS_QUESTIONS`. Просто добавьте новые ключи и списки строк — и они автоматически появятся в игре!

---

## 🤝 Contributing

1. Форкните репозиторий
2. Создайте ветку feature/YourFeature
3. Сделайте изменения и напишите тесты
4. Откройте Pull Request

---

## ⚖️ Лицензия

MIT © 2025 Your Name

---

## 📞 Контакты

* Email: [your.email@example.com](mailto:your.email@example.com)
* Telegram: [@your\_handle](https://t.me/your_handle)

Enjoy the glitch! 🎲

[1]: https://github.com/jehna/readme-best-practices?utm_source=chatgpt.com "jehna/readme-best-practices - GitHub"
[2]: https://www.reddit.com/r/github/comments/136ks63/10_mustknow_tips_for_crafting_the_perfect/?utm_source=chatgpt.com "10 must-know tips for crafting the perfect README.md for ... - Reddit"
[3]: https://www.freecodecamp.org/news/how-to-write-a-good-readme-file/?utm_source=chatgpt.com "How to Write a Good README File for Your GitHub Project"
[4]: https://www.reddit.com/r/webdev/comments/18sozpf/how_do_you_write_your_readmemd_or_docs_for_your/?utm_source=chatgpt.com "How do you write your README.md or Docs for your Git repo?"
[5]: https://www.hatica.io/blog/best-practices-for-github-readme/?utm_source=chatgpt.com "Best Practices For An Eye Catching GitHub Readme - Hatica"
[6]: https://github.com/jehna/readme-best-practices/blob/master/README-default.md?utm_source=chatgpt.com "readme-best-practices/README-default.md at master - GitHub"
[7]: https://medium.com/%40berastis/creating-a-powerful-readme-best-practices-for-your-project-f974a1e69a51?utm_source=chatgpt.com "Creating a Powerful README: Best Practices for Your Project"
[8]: https://docs.github.com/github/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax?utm_source=chatgpt.com "Basic writing and formatting syntax - GitHub Docs"
[9]: https://docs.github.com/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes?utm_source=chatgpt.com "About READMEs - GitHub Docs"
[10]: https://www.wired.com/2010/08/write-your-readme-before-your-code?utm_source=chatgpt.com "Write Your README Before Your Code"
