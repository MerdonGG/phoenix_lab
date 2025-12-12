const fs = require('fs');
const path = require('path');

// Создаем папку assets если её нет
const assetsPath = path.join('public', 'assets');
if (!fs.existsSync(assetsPath)) {
  fs.mkdirSync(assetsPath, { recursive: true });
  console.log('✅ Создана папка public/assets');
}

// Файлы для перемещения
const filesToMove = [
  { source: 'public/phoenix-logo.png', dest: 'public/assets/phoenix-logo.png' },
  { source: 'Без имени-1.png', dest: 'public/assets/без-имени-1.png' },
  { source: 'горение/горение.gif', dest: 'public/assets/горение.gif' },
  { source: 'горение/горение.mp4', dest: 'public/assets/горение.mp4' },
  { source: '1212.mp4', dest: 'public/assets/1212.mp4' },
];

let movedCount = 0;

filesToMove.forEach(({ source, dest }) => {
  if (fs.existsSync(source)) {
    try {
      // Создаем директорию для файла назначения если нужно
      const destDir = path.dirname(dest);
      if (!fs.existsSync(destDir)) {
        fs.mkdirSync(destDir, { recursive: true });
      }
      
      // Копируем файл
      fs.copyFileSync(source, dest);
      console.log(`✅ Перемещен: ${source} -> ${dest}`);
      movedCount++;
    } catch (error) {
      console.error(`❌ Ошибка при перемещении ${source}:`, error.message);
    }
  } else {
    console.log(`⚠️  Файл не найден: ${source}`);
  }
});

console.log(`\n✨ Готово! Перемещено файлов: ${movedCount}/${filesToMove.length}`);

