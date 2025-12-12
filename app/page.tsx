'use client'

import { useState, useEffect, useRef } from 'react'
import Image from 'next/image'
import AuthMenu from './components/AuthMenu'

// Компонент летящей птицы
function FlyingBirdComponent({ bird }: { 
  bird: { 
    show: boolean
    startX: number
    startY: number
    endX: number
    endY: number
    targetButtonId: string | null
  }
}) {
  const [position, setPosition] = useState({ x: bird.startX, y: bird.startY })
  const [isAnimating, setIsAnimating] = useState(false)
  const [showStaticLogo, setShowStaticLogo] = useState(false)

  useEffect(() => {
    if (bird.show) {
      // Устанавливаем начальную позицию
      setPosition({ x: bird.startX, y: bird.startY })
      setIsAnimating(true)
      setShowStaticLogo(false)
      
      // Запускаем анимацию к конечной позиции через небольшую задержку
      requestAnimationFrame(() => {
        setTimeout(() => {
          setPosition({ x: bird.endX, y: bird.endY })
          // После завершения анимации показываем статический логотип
          setTimeout(() => {
            setIsAnimating(false)
            setShowStaticLogo(true)
          }, 600) // Длительность анимации
        }, 10)
      })
    } else {
      setIsAnimating(false)
      setShowStaticLogo(false)
    }
  }, [bird.show, bird.startX, bird.startY, bird.endX, bird.endY])

  if (!bird.show) return null

  return (
    <div
      className={`flying-bird ${isAnimating ? 'animating' : 'completed'}`}
      style={{
        position: 'fixed',
        left: `${position.x}px`,
        top: `${position.y}px`,
        width: '80px',
        height: '80px',
        pointerEvents: 'none',
        zIndex: 10000,
        transform: 'translate(-50%, -50%)',
        transition: isAnimating 
          ? 'left 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94), top 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94)'
          : 'none',
        opacity: 1
      }}
    >
      {isAnimating ? (
        <img
          src="/assets/fly/fly.gif"
          alt="Flying Phoenix"
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 15px rgba(255, 102, 0, 1))',
            display: 'block'
          }}
        />
      ) : showStaticLogo ? (
        <Image
          src="/assets/phoenix-logo.png"
          alt="Phoenix Logo"
          width={80}
          height={80}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 15px rgba(255, 102, 0, 1))'
          }}
        />
      ) : null}
    </div>
  )
}

export default function Home() {
  const [isDark, setIsDark] = useState(false)
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null)
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState('')
  const [showResult, setShowResult] = useState(false)
  const [images, setImages] = useState<{
    original: string | null
    pexels: string | null
    generated: string | null
  } | null>(null)
  const [selectedImage, setSelectedImage] = useState<string | null>(null)
  const [showGif, setShowGif] = useState(false)
  const [gifKey, setGifKey] = useState(0)
  const [showLoadingTest, setShowLoadingTest] = useState(false)
  const [loadingTime, setLoadingTime] = useState(0)
  const [flyingBird, setFlyingBird] = useState<{
    show: boolean
    startX: number
    startY: number
    endX: number
    endY: number
    targetButtonId: string | null
  }>({
    show: false,
    startX: 0,
    startY: 0,
    endX: 0,
    endY: 0,
    targetButtonId: null
  })
  const [hideLogo, setHideLogo] = useState(false)
  const logoRef = useRef<HTMLDivElement>(null)
  const [showAuthMenu, setShowAuthMenu] = useState(false)
  const [user, setUser] = useState<any>(null)

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    if (savedTheme === 'dark') {
      setIsDark(true)
      document.body.classList.add('dark-theme')
    }

    // Проверяем сохраненного пользователя
    const savedUser = localStorage.getItem('telegram_user')
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser))
      } catch (e) {
        console.error('Ошибка загрузки данных пользователя:', e)
      }
    }
  }, [])

  const handleLogin = (userData: any) => {
    setUser(userData)
    setShowAuthMenu(false)
  }

  // Таймер для панели загрузки
  useEffect(() => {
    let interval: NodeJS.Timeout | null = null
    
    if (showLoadingTest && loadingTime > 0) {
      interval = setInterval(() => {
        setLoadingTime(prev => {
          if (prev <= 0.1) {
            setShowLoadingTest(false)
            return 0
          }
          return prev - 0.1
        })
      }, 100)
    }
    
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [showLoadingTest, loadingTime])

  const handleLoadingTest = () => {
    setLoadingTime(10) // 10 секунд для теста (можно изменить)
    setShowLoadingTest(true)
  }

  const toggleTheme = () => {
    const newTheme = !isDark
    setIsDark(newTheme)
    if (newTheme) {
      document.body.classList.add('dark-theme')
      localStorage.setItem('theme', 'dark')
    } else {
      document.body.classList.remove('dark-theme')
      localStorage.setItem('theme', 'light')
    }
  }

  const handleStyleClick = (style: string, event: React.MouseEvent<HTMLButtonElement>) => {
    setSelectedStyle(style)
    animateBirdToButton(event.currentTarget)
  }

  const handleSocialClick = (social: string, event: React.MouseEvent<HTMLButtonElement>) => {
    animateBirdToButton(event.currentTarget)
    // Можно добавить логику публикации позже
    // alert(`Публикация в ${social}`)
  }

  const animateBirdToButton = (targetButton: HTMLElement) => {
    // Получаем позицию логотипа через ref
    const logoElement = logoRef.current
    if (!logoElement || !targetButton) return

    // Используем requestAnimationFrame для гарантии, что позиция актуальна
    requestAnimationFrame(() => {
      // Получаем позиции ДО скрытия логотипа
      const logoRect = logoElement.getBoundingClientRect()
      const buttonRect = targetButton.getBoundingClientRect()

      // Вычисляем позиции (центры элементов)
      // Используем window.scrollX/Y для учета скролла, хотя для fixed это не обязательно
      const startX = logoRect.left + logoRect.width / 2
      const startY = logoRect.top + logoRect.height / 2
      const endX = buttonRect.left + buttonRect.width / 2
      const endY = buttonRect.top + buttonRect.height / 2

      console.log('Logo position:', { startX, startY, logoRect })
      console.log('Button position:', { endX, endY, buttonRect })

      // Генерируем уникальный ID для кнопки
      const buttonId = targetButton.getAttribute('data-button-id') || `button-${Date.now()}`
      targetButton.setAttribute('data-button-id', buttonId)

      // Запускаем анимацию с правильными координатами
      setFlyingBird({
        show: true,
        startX,
        startY,
        endX,
        endY,
        targetButtonId: buttonId
      })

      // Скрываем логотип после установки позиций
      setHideLogo(true)
    })
  }


  const getStyleName = (style: string) => {
    const styles: Record<string, string> = {
      'scientific': 'Научно-деловой стиль',
      'meme': 'Мемный стиль',
      'casual': 'Повседневный стиль'
    }
    return styles[style] || style
  }

  const handleSubmit = async () => {
    if (!url.trim()) {
      alert('Пожалуйста, введите URL статьи')
      return
    }

    if (!selectedStyle) {
      alert('Пожалуйста, выберите стиль рерайта')
      return
    }

    setLoading(true)
    setShowResult(false)
    setResult('')

    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
      
      const response = await fetch(`${API_URL}/api/rewrite-article`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          url: url.trim(),
          style: selectedStyle
        })
      })

      const data = await response.json()

      if (response.ok && data.success) {
        setResult(data.rewritten_text)
        setImages(data.images || null)
        // По умолчанию выбираем оригинальное изображение, если есть
        if (data.images?.original) {
          setSelectedImage('original')
        } else if (data.images?.pexels) {
          setSelectedImage('pexels')
        } else if (data.images?.generated) {
          setSelectedImage('generated')
        } else {
          setSelectedImage(null)
        }
        setShowResult(true)
        setLoading(false)
      } else {
        alert(`Ошибка: ${data.error || 'Неизвестная ошибка'}`)
        setLoading(false)
      }
    } catch (error) {
      console.error('Ошибка при обработке статьи:', error)
      alert(`Ошибка подключения к серверу: ${error instanceof Error ? error.message : 'Неизвестная ошибка'}`)
      setLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleSubmit()
    }
  }

  const handleLogoClick = () => {
    // Предотвращаем повторный клик во время проигрывания гифки
    if (showGif) {
      console.log('Гифка уже воспроизводится, игнорируем клик')
      return
    }
    
    console.log('Клик по логотипу, запускаем гифку')
    
    // Сначала скрываем, чтобы сбросить состояние
    setShowGif(false)
    setGifKey(prev => prev + 1)
    
    // Затем показываем гифку через небольшую задержку для правильной перезагрузки
    setTimeout(() => {
      setShowGif(true)
      console.log('Показываем гифку')
    }, 50)
    
    // Возвращаем логотип через 11.24 секунды (полная длительность гифки)
    setTimeout(() => {
      setShowGif(false)
      console.log('Гифка завершена, возвращаем логотип')
    }, 11290) // 11240 + 50 (задержка показа)
  }

  const handleGifLoad = () => {
    console.log('Гифка успешно загружена')
  }

  const handleGifError = (e: React.SyntheticEvent<HTMLImageElement, Event>) => {
    console.error('Ошибка загрузки гифки')
    const target = e.target as HTMLImageElement
    // Пробуем загрузить без query параметра
    target.src = '/assets/горение.gif'
  }

  return (
    <div className="container">
      <div className="header">
        <div className="header-controls">
          <button className="auth-btn" onClick={() => setShowAuthMenu(true)}>
            {user ? `👤 ${user.first_name}` : '🔐 Войти'}
          </button>
          <button className="theme-toggle" onClick={toggleTheme}>
            {isDark ? '☀️ Светлая' : '🌙 Тёмная'}
          </button>
        </div>
        <div 
          ref={logoRef}
          className="logo-container"
          onClick={handleLogoClick}
          style={{ 
            cursor: showGif ? 'default' : 'pointer',
            opacity: hideLogo ? 0 : 1,
            transition: 'opacity 0.3s ease',
            pointerEvents: hideLogo ? 'none' : 'auto'
          }}
        >
          {showGif ? (
            <img 
              key={gifKey}
              src="/assets/горение.gif"
              alt="Phoenix Burning Animation" 
              className="logo"
              width={120}
              height={120}
              onLoad={handleGifLoad}
              onError={handleGifError}
              style={{ 
                width: '120px', 
                height: '120px', 
                objectFit: 'contain', 
                pointerEvents: 'none',
                display: 'block'
              }}
            />
          ) : (
            <Image 
              src="/assets/phoenix-logo.png" 
              alt="Phoenix Lab Logo" 
              className="logo"
              width={120}
              height={120}
              priority
            />
          )}
        </div>
        <h1>Phoenix Lab</h1>
        <p className="subtitle">AI Рерайт Статей</p>
      </div>

      <div className="main-content">
        <div className="input-section">
          <label htmlFor="article-url">URL статьи</label>
          <input
            type="url"
            id="article-url"
            className="url-input"
            placeholder="https://example.com/article"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            onKeyPress={handleKeyPress}
          />
        </div>

        <div className="style-section">
          <label>Стиль рерайта</label>
          <div className="style-buttons">
            <button
              className={`style-btn ${selectedStyle === 'scientific' ? 'active' : ''}`}
              onClick={(e) => handleStyleClick('scientific', e)}
            >
              Научно-деловой стиль
            </button>
            <button
              className={`style-btn ${selectedStyle === 'meme' ? 'active' : ''}`}
              onClick={(e) => handleStyleClick('meme', e)}
            >
              Мемный стиль
            </button>
            <button
              className={`style-btn ${selectedStyle === 'casual' ? 'active' : ''}`}
              onClick={(e) => handleStyleClick('casual', e)}
            >
              Повседневный стиль
            </button>
          </div>
        </div>

        <div className="social-section">
          <label>Публикация в соцсетях</label>
          <div className="social-buttons">
            <button
              className="social-btn"
              onClick={(e) => handleSocialClick('Вконтакте', e)}
            >
              Вконтакте
            </button>
            <button
              className="social-btn"
              onClick={(e) => handleSocialClick('Telegram', e)}
            >
              Telegram
            </button>
            <button
              className="social-btn"
              onClick={(e) => handleSocialClick('Instagram', e)}
            >
              Instagram
            </button>
          </div>
        </div>

        <button className="submit-btn" onClick={handleSubmit}>
          Рерайт статьи
        </button>

        <button 
          className="test-loading-btn"
          onClick={handleLoadingTest}
        >
          Тест загрузки
        </button>

        <div className={`loading ${loading ? 'show' : ''}`}>
          <div className="spinner"></div>
          <p>Обработка статьи...</p>
        </div>

        <div className={`result-section ${showResult ? 'show' : ''}`}>
          <div className="result-box">
            <div className="result-title">Результат рерайта:</div>
            
            {/* Выбор изображения */}
            {images && (
              <div className="image-selection">
                <h3 className="image-selection-title">Выберите изображение для статьи:</h3>
                <div className="image-options">
                  {images.original && (
                    <div 
                      className={`image-option ${selectedImage === 'original' ? 'selected' : ''}`}
                      onClick={() => setSelectedImage('original')}
                    >
                      <img src={images.original} alt="Оригинальное изображение" />
                      <div className="image-label">Оригинальное</div>
                    </div>
                  )}
                  {images.pexels && (
                    <div 
                      className={`image-option ${selectedImage === 'pexels' ? 'selected' : ''}`}
                      onClick={() => setSelectedImage('pexels')}
                    >
                      <img src={images.pexels} alt="Изображение из API" />
                      <div className="image-label">Из API</div>
                    </div>
                  )}
                  {images.generated && (
                    <div 
                      className={`image-option ${selectedImage === 'generated' ? 'selected' : ''}`}
                      onClick={() => setSelectedImage('generated')}
                    >
                      <img src={images.generated} alt="Сгенерированное изображение" />
                      <div className="image-label">Сгенерированное</div>
                    </div>
                  )}
                  {!images.original && !images.pexels && !images.generated && (
                    <div className="no-images-message">
                      <p>⚠️ Изображения не найдены. Статья будет отправлена без изображения.</p>
                    </div>
                  )}
                </div>
                {selectedImage && images[selectedImage as keyof typeof images] && (
                  <div className="selected-image-preview">
                    <p>Выбрано: <strong>{selectedImage === 'original' ? 'Оригинальное' : selectedImage === 'pexels' ? 'Из Pexels' : 'Сгенерированное'}</strong></p>
                    <img 
                      src={images[selectedImage as keyof typeof images]!} 
                      alt="Выбранное изображение" 
                      className="preview-image"
                    />
                  </div>
                )}
              </div>
            )}
            
            <div className="result-text">{result}</div>
            {result && (
              <button 
                className="submit-btn" 
                onClick={async () => {
                  try {
                    const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'
                    const response = await fetch(`${API_URL}/api/send-article`, {
                      method: 'POST',
                      headers: {
                        'Content-Type': 'application/json',
                      },
                      body: JSON.stringify({
                        article_text: result,
                        image_url: selectedImage && images && images[selectedImage as keyof typeof images] 
                          ? images[selectedImage as keyof typeof images] 
                          : null
                      })
                    })
                    const data = await response.json()
                    if (response.ok && data.success) {
                      alert(`Статья успешно отправлена в ${data.sent} канал(ов)!`)
                    } else {
                      alert(`Ошибка отправки: ${data.error || 'Неизвестная ошибка'}`)
                    }
                  } catch (error) {
                    console.error('Ошибка отправки статьи:', error)
                    alert(`Ошибка подключения к серверу: ${error instanceof Error ? error.message : 'Неизвестная ошибка'}`)
                  }
                }}
                style={{ marginTop: '20px' }}
              >
                Отправить в Telegram каналы
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Панель теста загрузки */}
      {showLoadingTest && (
        <div className="loading-test-panel">
          <div className="loading-test-content">
            <img 
              src="/assets/death/death.gif"
              alt="Loading Animation"
              className="loading-test-gif"
              style={{
                width: '150px',
                height: '150px',
                objectFit: 'contain',
                marginBottom: '20px',
                display: 'block'
              }}
            />
            <div className="loading-test-time">
              {loadingTime.toFixed(1)} сек
            </div>
          </div>
        </div>
      )}

      {/* Анимированная летящая птица */}
      <FlyingBirdComponent bird={flyingBird} />

      {/* Меню авторизации */}
      {showAuthMenu && (
        <AuthMenu 
          isDark={isDark} 
          onClose={() => setShowAuthMenu(false)}
          onLogin={handleLogin}
        />
      )}
    </div>
  )
}

