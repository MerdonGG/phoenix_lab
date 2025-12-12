#!/usr/bin/env python3
"""Скрипт для проверки токенов в файле"""
import json
import os
import time

AUTH_TOKENS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "TelegramBot", "auth_tokens.json")

print(f"Проверка файла: {AUTH_TOKENS_FILE}")
print(f"Файл существует: {os.path.exists(AUTH_TOKENS_FILE)}")

if os.path.exists(AUTH_TOKENS_FILE):
    try:
        with open(AUTH_TOKENS_FILE, 'r', encoding='utf-8') as f:
            tokens = json.load(f)
        print(f"Токенов в файле: {len(tokens)}")
        if tokens:
            print("Токены:")
            for token, data in tokens.items():
                expires_at = data.get('expires_at', 0)
                status = data.get('status', 'unknown')
                expired = expires_at < time.time()
                print(f"  {token[:20]}... - статус: {status}, истек: {expired}, expires_at: {expires_at}")
        else:
            print("Файл пустой!")
    except Exception as e:
        print(f"Ошибка чтения файла: {e}")
else:
    print("Файл не существует!")

