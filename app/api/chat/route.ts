// app/api/chat/route.ts
import { kv } from '@vercel/kv'
import { OpenAIStream, StreamingTextResponse } from 'ai'
import { Configuration, OpenAIApi } from 'openai-edge'
import { auth } from '@/auth'
import { nanoid } from '@/lib/utils'
import { getUserId } from '../../actions'
import { handleError } from '@/lib/errorHandler'

export const runtime = 'edge'

const configuration = new Configuration({
  apiKey: process.env.OPENAI_API_KEY
})

const openai = new OpenAIApi(configuration)

export async function POST(req: Request) {
  try {
    const json = await req.json()
    const { messages, previewToken } = json

    const session = await auth()
    const userId = await getUserId(session) || ''

    if (!userId) {
      return new Response('Unauthorized', {
        status: 401
      })
    }

    if (previewToken) {
      configuration.apiKey = previewToken
    }

    const model = process.env.OPENAI_MODEL || 'gpt-4'

    const res = await openai.createChatCompletion({
      model,
      messages,
      temperature: 0.7,
      stream: true
    })

    const stream = OpenAIStream(res, {
      async onCompletion(completion) {
        const title = json.messages[0].content.substring(0, 100)
        const id = json.id ?? nanoid()
        const createdAt = Date.now()
        const path = `/chat/${id}`
        const payload = {
          id,
          title,
          userId,
          createdAt,
          path,
          messages: [
            ...messages,
            {
              content: completion,
              role: 'assistant'
            }
          ]
        }
        await kv.hmset(`chat:${id}`, payload)
        await kv.zadd(`user:chat:${userId}`, {
          score: createdAt,
          member: `chat:${id}`
        })
      }
    })

    return new StreamingTextResponse(stream)
  } catch (error) {
    handleError(error)
    return new Response('Internal Server Error', {
      status: 500
    })
  }
}