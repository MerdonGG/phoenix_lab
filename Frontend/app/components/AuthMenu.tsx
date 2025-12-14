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
        body: JSON.stringify({})
      })

      if (response.ok) {
        const data = await response.json()
        if (data.success && data.token) {
          setAuthToken(data.token)
          startTokenCheck(data.token)
        }
      }
    } catch (error) {
      console.error('Ошибка при генерации токена:', error)
      alert('Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен.')
    }
  }

  const startTokenCheck = (token: string) => {
    setIsChecking(true)
    
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
            setUser(data.user)
            onLogin(data.user)
            localStorage.setItem('telegram_user', JSON.stringify(data.user))
            
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
    }, 2000)
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
                >
                  🔐 Открыть бота для авторизации
                </a>
                
                {isChecking && (
                  <div className="auth-checking">
                    ⏳ Ожидание авторизации... Откройте бота и нажмите кнопку "Авторизоваться на сайте"
                  </div>
                )}
              </>
            ) : (
              <div className="auth-generating">
                Генерация токена...
              </div>
            )}
            
            <p className="auth-note">
              После авторизации вы сможете сохранять свои настройки и историю рерайтов
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

