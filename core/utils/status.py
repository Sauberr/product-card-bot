def get_status_text(status: str) -> str:
    status_texts = {
        "pending": "⏳ На модерации",
        "approved": "✅ Одобрен",
        "rejected": "❌ Отклонен",
    }
    return status_texts.get(status, status)