@echo off
set /p tema="Introduce el tema del nuevo artículo: "
python generate_post.py "%tema%"
pause
