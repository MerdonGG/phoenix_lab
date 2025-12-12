'use client'

import { useState, useEffect } from 'react'
import Image from 'next/image'

export default function Home() {
  const [isDark, setIsDark] = useState(false)
  const [selectedStyle, setSelectedStyle] = useState<string | null>(null)
  const [url, setUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState('')
  const [showResult, setShowResult] = useState(false)
  const [showGif, setShowGif] = useState(false)
  const [gifKey, setGifKey] = useState(0)
  const [showLoadingTest, setShowLoadingTest] = useState(false)
  const [loadingTime, setLoadingTime] = useState(0)

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme') || 'light'
    if (savedTheme === 'dark') {
      setIsDark(true)
      document.body.classList.add('dark-theme')
    }
  }, [])

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

  const handleStyleClick = (style: string) => {
    setSelectedStyle(style)
  }

  const handleSocialClick = (social: string) => {
    alert(`Публикация в ${social}`)
  }

  const getStyleName = (style: string) => {
    const styles: Record<string, string> = {
      'scientific': 'Научно-деловой стиль',
      'meme': 'Мемный стиль',
      'casual': 'Повседневный стиль'
    }
    return styles[style] || style
  }

  const handleSubmit = () => {
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

    // Симуляция обработки
    setTimeout(() => {
      setLoading(false)
      setResult(`Статья успешно обработана!\n\nURL: ${url}\nСтиль: ${getStyleName(selectedStyle)}\n\n[Здесь будет результат рерайта статьи]`)
      setShowResult(true)
    }, 2000)
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
        <button className="theme-toggle" onClick={toggleTheme}>
          {isDark ? '☀️ Светлая' : '🌙 Тёмная'}
        </button>
        <div 
          className="logo-container"
          onClick={handleLogoClick}
          style={{ cursor: showGif ? 'default' : 'pointer' }}
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
              onClick={() => handleStyleClick('scientific')}
            >
              Научно-деловой стиль
            </button>
            <button
              className={`style-btn ${selectedStyle === 'meme' ? 'active' : ''}`}
              onClick={() => handleStyleClick('meme')}
            >
              Мемный стиль
            </button>
            <button
              className={`style-btn ${selectedStyle === 'casual' ? 'active' : ''}`}
              onClick={() => handleStyleClick('casual')}
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
              onClick={() => handleSocialClick('Вконтакте')}
            >
              Вконтакте
            </button>
            <button
              className="social-btn"
              onClick={() => handleSocialClick('Telegram')}
            >
              Telegram
            </button>
            <button
              className="social-btn"
              onClick={() => handleSocialClick('Instagram')}
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
            <div className="result-text">{result}</div>
          </div>
        </div>
      </div>

      {/* Панель теста загрузки */}
      {showLoadingTest && (
        <div className="loading-test-panel">
          <div className="loading-test-content">
            <img 
              src="/assets/1212(1)/1212(1).gif"
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
    </div>
  )
}

