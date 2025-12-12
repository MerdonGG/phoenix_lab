# Инструкция по перемещению медиа-файлов

Папка `public/assets` создана для хранения всех изображений, гифок и видео.

## Файлы для перемещения:

1. `public/phoenix-logo.png` → `public/assets/phoenix-logo.png`
2. `Без имени-1.png` → `public/assets/без-имени-1.png`
3. `горение/горение.gif` → `public/assets/горение.gif`
4. `горение/горение.mp4` → `public/assets/горение.mp4`
5. `1212.mp4` → `public/assets/1212.mp4`

## Автоматическое перемещение:

Запустите PowerShell скрипт:
```powershell
.\move-assets.ps1
```

## Ручное перемещение:

1. Откройте папку проекта в проводнике
2. Переместите все изображения, гифки и видео в папку `public/assets`
3. После перемещения пути в коде уже обновлены на `/assets/имя-файла`

## Использование в коде:

Все пути к медиа-файлам должны начинаться с `/assets/`:

```jsx
<Image src="/assets/phoenix-logo.png" alt="Logo" />
<img src="/assets/горение.gif" alt="Animation" />
<video src="/assets/горение.mp4" />
```

