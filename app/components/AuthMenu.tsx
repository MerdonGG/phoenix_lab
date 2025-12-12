'use client'

import { useState, useEffect, useRef } from 'react'

interface TelegramUser {
  id: number
  first_name: string
  last_name?: string
  username?: string
  is_bot?: boolean
  language_code?: string
}

interface AuthMenuProps {
  isDark: boolean
  onClose: () => void
  onLogin: (user: TelegramUser) => void
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000'

// Проверка доступности API при загрузке компонента
if (typeof window !== 'undefined') {
  console.log('API URL:', API_URL)
}

export default function AuthMenu({ isDark, onClose, onLogin }: AuthMenuProps) {
  const [user, setUser] = useState<TelegramUser | null>(null)
  const [authToken, setAuthToken] = useState<string | null>(null)
  const [isChecking, setIsChecking] = useState(false)
  const [botUsername, setBotUsername] = useState('PhoenixLogIN_bot') // Имя бота без @
  const checkIntervalRef = useRef<NodeJS.Timeout | null>(null)

  useEffect(() => {
    // Проверяем, есть ли сохраненный пользователь
    const savedUser = localStorage.getItem('telegram_user')
    if (savedUser) {
      try {
        const parsedUser = JSON.parse(savedUser)
        setUser(parsedUser)
        return // Если пользователь уже авторизован, не генерируем токен
      } catch (e) {
        console.error('Ошибка загрузки данных пользователя:', e)
      }
    }

    // Генерируем токен при открытии меню
    generateToken()

    return () => {
      // Очищаем интервал при размонтировании
      if (checkIntervalRef.current) {
        clearInterval(checkIntervalRef.current)
      }
    }
  }, [])

  const generateToken = async () => {
    console.log('Генерация токена...', API_URL)
    try {
      const response = await fetch(`${API_URL}/api/auth/generate-token`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({}) // Отправляем пустой JSON объект
      })

      console.log('Ответ от сервера:', response.status, response.statusText)

      if (response.ok) {
        const data = await response.json()
        console.log('Данные от сервера:', data)
        if (data.success && data.token) {
          console.log('Токен получен:', data.token.substring(0, 20) + '...')
          setAuthToken(data.token)
          // Начинаем проверку статуса токена
          startTokenCheck(data.token)
        } else {
          console.error('Ошибка генерации токена: неверный формат ответа', data)
        }
      } else {
        const errorText = await response.text()
        console.error(`Ошибка генерации токена: ${response.status} ${response.statusText}`, errorText)
      }
    } catch (error) {
      console.error('Ошибка при генерации токена:', error)
      // Показываем пользователю сообщение об ошибке
      alert('Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен на http://localhost:5000')
    }
  }

  const startTokenCheck = (token: string) => {
    setIsChecking(true)
    
    // Проверяем каждые 2 секунды
    checkIntervalRef.current = setInterval(async () => {
      try {
        const response = await fetch(`${API_URL}/api/auth/verify-token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ token })
        })

        if (response.ok) {
          const data = await response.json()
          if (data.success && data.authorized && data.user) {
            // Пользователь авторизован!
            setUser(data.user)
            onLogin(data.user)
            localStorage.setItem('telegram_user', JSON.stringify(data.user))
            
            // Останавливаем проверку
            if (checkIntervalRef.current) {
              clearInterval(checkIntervalRef.current)
              checkIntervalRef.current = null
            }
            setIsChecking(false)
          }
        }
      } catch (error) {
        console.error('Ошибка проверки токена:', error)
      }
    }, 2000) // Проверяем каждые 2 секунды
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('telegram_user')
    onClose()
  }

  const getBotLink = () => {
    if (!authToken) return '#'
    return `https://t.me/${botUsername}?start=${authToken}`
  }

  return (
    <div className={`auth-menu-overlay ${isDark ? 'dark-theme' : ''}`} onClick={onClose}>
      <div className="auth-menu" onClick={(e) => e.stopPropagation()}>
        <button className="auth-menu-close" onClick={onClose}>
          ×
        </button>
        <h2 className="auth-menu-title">Вход / Регистрация</h2>
        
        {user ? (
          <div className="auth-user-info">
            <div className="auth-user-details">
              <h3>{user.first_name} {user.last_name || ''}</h3>
              {user.username && <p>@{user.username}</p>}
              <p className="auth-user-id">ID: {user.id}</p>
            </div>
            <button className="auth-logout-btn" onClick={handleLogout}>
              Выйти
            </button>
            <button 
              className="auth-logout-btn" 
              onClick={() => {
                localStorage.removeItem('telegram_user')
                setUser(null)
                generateToken()
              }}
              style={{ marginTop: '10px' }}
            >
              Переавторизоваться
            </button>
          </div>
        ) : (
          <div className="auth-telegram-widget">
            <p className="auth-description">
              Войдите через Telegram бота для доступа к дополнительным функциям
            </p>
            
            {authToken ? (
              <>
                <a 
                  href={getBotLink()}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="auth-bot-link"
                  style={{
                    display: 'inline-block',
                    padding: '12px 24px',
                    backgroundColor: '#0088cc',
                    color: 'white',
                    textDecoration: 'none',
                    borderRadius: '8px',
                    fontWeight: 'bold',
                    margin: '20px 0',
                    transition: 'background-color 0.3s'
                  }}
                >
                  🔐 Открыть бота для авторизации
                </a>
                
                {isChecking && (
                  <div style={{
                    marginTop: '20px',
                    padding: '10px',
                    backgroundColor: isDark ? 'rgba(255, 255, 255, 0.1)' : 'rgba(0, 0, 0, 0.05)',
                    borderRadius: '8px',
                    fontSize: '14px',
                    color: isDark ? '#fff' : '#333'
                  }}>
                    ⏳ Ожидание авторизации... Откройте бота и нажмите кнопку "Авторизоваться на сайте"
                  </div>
                )}
              </>
            ) : (
              <div style={{
                padding: '20px',
                textAlign: 'center',
                color: isDark ? '#fff' : '#333'
              }}>
                Генерация токена...
              </div>
            )}
            
            <p className="auth-note" style={{ marginTop: '20px', fontSize: '12px', opacity: 0.7 }}>
              После авторизации вы сможете сохранять свои настройки и историю рерайтов
            </p>
          </div>
        )}
      </div>
    </div>
  )
}
