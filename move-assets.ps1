# Скрипт для перемещения всех медиа-файлов в папку public/assets

# Создаем папку assets если её нет
$assetsPath = "public\assets"
if (-not (Test-Path $assetsPath)) {
    New-Item -ItemType Directory -Path $assetsPath -Force | Out-Null
    Write-Host "Создана папка $assetsPath" -ForegroundColor Green
}

# Перемещаем файлы из public в assets
$filesToMove = @(
    @{Source = "public\phoenix-logo.png"; Destination = "public\assets\phoenix-logo.png"}
    @{Source = "Без имени-1.png"; Destination = "public\assets\без-имени-1.png"}
    @{Source = "горение\горение.gif"; Destination = "public\assets\горение.gif"}
    @{Source = "горение\горение.mp4"; Destination = "public\assets\горение.mp4"}
    @{Source = "1212.mp4"; Destination = "public\assets\1212.mp4"}
)

foreach ($file in $filesToMove) {
    if (Test-Path $file.Source) {
        Copy-Item -Path $file.Source -Destination $file.Destination -Force
        Write-Host "Перемещен: $($file.Source) -> $($file.Destination)" -ForegroundColor Yellow
    } else {
        Write-Host "Файл не найден: $($file.Source)" -ForegroundColor Red
    }
}

Write-Host "`nВсе файлы успешно перемещены в public/assets" -ForegroundColor Green

