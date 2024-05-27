// lib/errorHandler.ts
import { toast } from 'react-hot-toast'

export const handleError = (error: any) => {
  console.error(error)
  toast.error(error.message || 'An unexpected error occurred')
}