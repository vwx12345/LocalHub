const BASE_URL = '/api/chatbot'

export async function sendChatMessage(message, previousResponseId = null) {
  const response = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      previous_response_id: previousResponseId,
    }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.detail ?? '챗봇 요청 실패')
  }

  return data
}
